#!python
# -*-coding:utf-8-*-
# Plot 2D results
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 'Zhikui Guo, 2021/02/12, GEOMAR
# ===============================================================

import sys
import argparse
import sys
import os
from colored import fg, bg, attr
C_GREEN = fg('green')
C_RED = fg('red')
C_BLUE = fg('blue')
C_DEFAULT = attr('reset')
#===============================================================
import linecache
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from matplotlib.ticker import MultipleLocator
import os,linecache
import sciPyFoam.polyMesh2d as mesh2d
import vtk
from vtk.util import numpy_support as VN

# import proplot as pplot # there are some nice colormaps in the proplot package
mpl.rcParams['font.family'] = 'Helvetica'  #default font family
mpl.rcParams['mathtext.fontset'] = 'cm' #font for math
def usage(argv):
    basename = argv[0].split('/')
    basename = basename[len(basename)-1]
    description='Plot 2D results'
    num_symbol=int((len(description)+20 - len(basename))/2)
    head='='*num_symbol+basename+'='*num_symbol
    print(head)
    print(description)
    print('Zhikui Guo, 2021/02/12, GEOMAR')
    print('[Example]: '+C_RED + basename+C_BLUE + ' caseDir timeName["all"/number(e.g. 0)/start:(e.g. 2324.423:)/start:end] fieldName[T|p|U]'+C_DEFAULT)
    print('='*len(head))
def getCaseName(caseDir):
    abspath_case=os.path.abspath(caseDir)
    caseName=abspath_case.split('/')[-1]
    return caseName
def timeStr(time_second):
    Scale,name_time=1,'seconds'
    if(time_second>(86400*365)):
        Scale = 3.17e-08
        name_time='years'
    elif(time_second>86400):
        Scale = 1.1574074074074073e-05
        name_time='days'
    elif(time_second>3600):
        Scale = 0.0002777777777777778
        name_time='hours'
    elif(time_second>60):
        Scale = 0.016666666666666666
        name_time='minutes'
    str_time=str('%d %s'%(time_second*Scale,name_time))
    return str_time
def plotMesh(caseDir,x,y,polygons,fmts=['jpg'],dpi=600,figpath='.'):
    figwidth=8
    figheight=figwidth/(x.max()-x.min())*(y.max()-y.min())
    fig=plt.figure(figsize=(figwidth,figheight))
    ax=plt.gca()
    ax.axis('scaled')
    ax.set_xlim(x.min(),x.max())
    ax.set_ylim(y.min(),y.max())
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    for polygon in polygons:
        ax.plot(np.append(x[polygon],x[polygon[0]]),np.append(y[polygon],y[polygon[0]]),lw=0.1,color='k')
    plt.tight_layout()
    for fmt in fmts:
        plt.savefig('%s/Mesh_%s.%s'%(figpath,getCaseName(caseDir),fmt),dpi=dpi)
        print('Figure is saved: %s/Mesh_%s.%s'%(figpath,getCaseName(caseDir),fmt))
def plot_contourf(caseDir,timeName,x,y,triangles, data,figname,cmap,levels, label, ticks=[],fmts=['jpg'],dpi=600,figpath='.'):
    figwidth=8
    figheight=figwidth/(x.max()-x.min())*(y.max()-y.min())
    fig=plt.figure(figsize=(figwidth,figheight))
    ax=plt.gca()
    ax.axis('scaled')
    ax.set_xlim(x.min(),x.max())
    ax.set_ylim(y.min(),y.max())
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    CS=ax.tricontourf(x,y,triangles,data,levels=levels,cmap=cmap,extend='both')
    ax_cb = ax.inset_axes([1.04, 0, 0.02,1])
    if(ticks==[]):
        plt.colorbar(CS,cax=ax_cb,label=label)
    else:
        plt.colorbar(CS,cax=ax_cb,format='%.0f',ticks=ticks,label=label)
    ax.text(0.02,0.96,'%s'%(timeStr(float(timeName))),bbox={'fc':'w','ec':'None','alpha':0.5},fontsize=13,fontweight='bold',transform=ax.transAxes,ha='left',va='top')
    # ax.triplot(x,y,triangles,lw=0.1,color='k',alpha=0.5)
    plt.tight_layout()
    for fmt in fmts:
        plt.savefig('%s/%s.%s'%(figpath,figname,fmt),dpi=dpi)
        print('Figure is saved: %s/%s.%s'%(figpath,figname,fmt))
def plot_field(caseDir, fieldName, timeName, ind_time, MeshData):
    figname='%s_%s_%d'%(fieldName,getCaseName(caseDir),ind_time)
    field=mesh2d.readCellData_to_pointData(caseDir, timeName, fieldName, MeshData)
    if(fieldName=='T'):
        # plot temperature
        T=field['pointData']['T']-273.15 # K->deg.C
        plot_contourf(caseDir,timeName,MeshData['x'],MeshData['y'],MeshData['triangles'], T,figname=figname, cmap='rainbow', levels=50,label='Temperature ($^{\circ}$C)',ticks=MultipleLocator(50))
    elif(fieldName=='p'):
        # plot pressure
        p=field['pointData']['p']
        plot_contourf(caseDir,timeName,MeshData['x'],MeshData['y'],MeshData['triangles'], p,figname=figname, cmap='cubehelix', levels=50,label='Pressure (Pa)')
    elif(fieldName=='U'):
        # plot pressure
        U=np.sqrt(field['pointData']['U_0']**2 + field['pointData']['U_1']**2 + field['pointData']['U_2']**2)
        plot_contourf(caseDir,timeName,MeshData['x'],MeshData['y'],MeshData['triangles'], U,figname=figname, cmap='RdYlBu_r', levels=50,label='Velocity magnitude (m/s)')
    else:
        print("Please modify plot_field function and add field support",fieldName)
        exit()
def main(argv):
    argc=len(argv)
    if(argc!=4):
        usage(argv)
        exit(0)
    caseDir=argv[1]
    timeName=argv[2]
    fieldName=argv[3]
    patchName='frontAndBack'

    print('Reading mesh data ...')
    MeshData=mesh2d.getMesh(caseDir, patchName)
    print('Ploting mesh, it could take a while')
    # plotMesh(caseDir,MeshData['x'],MeshData['y'],MeshData['polygons'])
    print('Getting all time name ...')
    times,times_value=mesh2d.getTimes(caseDir)
    indices_times=np.arange(0,len(times))
    time_start=0
    time_end=times_value.max()
    
    if(timeName=='all'):
        print('Plot all results of all time')
        ind=((times_value>time_start) & (times_value<=time_end))
        for timeName, index_time in zip(times[ind],indices_times[ind]):
            print('Plot result at time %s (%d th)'%(timeName,index_time))
            plot_field(caseDir,fieldName,timeName,index_time, MeshData)
    elif(':' in timeName):
        start_end=timeName.split(':')
        print(start_end)
        if(start_end[1]==''):
            time_start=float(start_end[0])
            print('Plot results from %s to %s'%(start_end[0],times[-1]))
        else:
            time_start=float(start_end[0])
            time_end=float(start_end[1])
            print('Plot results from %s to %s'%(start_end[0],start_end[1]))

        ind=((times_value>time_start) & (times_value<=time_end))
        for timeName, index_time in zip(times[ind],indices_times[ind]):
            print('Plot result at time %s (%d th)'%(timeName,index_time))
            plot_field(caseDir,fieldName,timeName,index_time, MeshData)
    else:
        if(timeName=='latestTime'):
            timeName=times[-1]
        print('Single time name')
        ind_time,=np.where(times==timeName)
        if(len(ind_time)==0):
            print('The input timeName: %s can not be identified'%(timeName))
            exit()
        print('Plot result at time %s (%d th)'%(timeName,ind_time))
        plot_field(caseDir,fieldName,timeName,ind_time, MeshData)

if __name__ == '__main__':
    sys.exit(main(sys.argv))