
#### import the simple module from the paraview
from paraview.simple import *
import paraview as pv
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active source.
resultfoam = GetActiveSource()
# resultfoam.SkipZeroTime = 0

# check whether T exist
convert_T=False
alldata = pv.servermanager.Fetch(resultfoam)
if(alldata.GetBlock(0).GetPointData().GetArray("T")==None):
    convert_T=False
else:
    convert_T=True

renderView1 = GetActiveViewOrCreate('RenderView')
if(convert_T):
    # create a new 'Calculator'
    calculator1 = Calculator(Input=resultfoam)
    calculator1.Function = 'T-273.15'
    calculator1.ResultArrayName = 'T_degC'
    RenameSource('K2degC', calculator1)
    # SetActiveSource(calculator1)

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')
    # show data in view
    resultfoamDisplay = Show(GetActiveSource(), renderView1)
    

    # get color transfer function/color map for 'p'
    pLUT = GetColorTransferFunction('T_degC')

    # get opacity transfer function/opacity map for 'p'
    pPWF = GetOpacityTransferFunction('T_degC')

    # trace defaults for the display properties.
    resultfoamDisplay.Representation = 'Surface'

    # reset view to fit data
    renderView1.ResetCamera()
    # show color bar/color legend
    resultfoamDisplay.SetScalarBarVisibility(renderView1, True)

    # update the view to ensure updated data information
    renderView1.Update()

    # set scalar coloring
    ColorBy(resultfoamDisplay, ('POINTS', 'T_degC'))

    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(pLUT, renderView1)

    # rescale color and/or opacity maps used to include current data range
    resultfoamDisplay.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    resultfoamDisplay.SetScalarBarVisibility(renderView1, True)


tsteps = resultfoam.TimestepValues
name_time='Time_second'
if(len(tsteps)>1):
    # create a new 'Annotate Time Filter'
    annotateTimeFilter1 = AnnotateTimeFilter(Input=resultfoam)
    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')
    # show data in view
    annotateTimeFilter1Display = Show(annotateTimeFilter1, renderView1)
    # update the view to ensure updated data information
    renderView1.Update()
    # Properties modified on annotateTimeFilter1
    dt=(tsteps[-1]-tsteps[0])/(len(tsteps)-1)
    if(dt>(86400*365)):
        annotateTimeFilter1.Format = 'Time: %.0f years'
        annotateTimeFilter1.Scale = 3.17e-08
        name_time='Time_year'
    elif(dt>86400):
        annotateTimeFilter1.Format = 'Time: %.0f days'
        annotateTimeFilter1.Scale = 1.1574074074074073e-05
        name_time='Time_day'
    elif(dt>3600):
        annotateTimeFilter1.Format = 'Time: %.0f hours'
        annotateTimeFilter1.Scale = 0.0002777777777777778
        name_time='Time_hour'
    elif(dt>60):
        annotateTimeFilter1.Format = 'Time: %.0f minutes'
        annotateTimeFilter1.Scale = 0.016666666666666666
        name_time='Time_minute'
    else:
        annotateTimeFilter1.Format = 'Time: %.2f seconds'
        annotateTimeFilter1.Scale = 1
        name_time='Time_second'
    # Properties modified on annotateTimeFilter1Display
    annotateTimeFilter1Display.Bold = 1
    annotateTimeFilter1Display.FontSize = 5

    # update the view to ensure updated data information
    renderView1.Update()

    # rename source object
    RenameSource(name_time, annotateTimeFilter1)

    # set active source
    if(convert_T):
        SetActiveSource(calculator1)

renderView1.ResetCamera()

# current camera placement for renderView1
renderView1.CameraPosition = [2000.0, -3000.0, 7965.728650875111]
renderView1.CameraFocalPoint = [2000.0, -3000.0, 0.5]
renderView1.CameraParallelScale = 2061.5528734427357

# #### uncomment the following to render all views
# # RenderAllViews()
# # alternatively, if you want to write images, you can use SaveScreenshot(...).
renderView1.Update()
Hide(resultfoam, renderView1)