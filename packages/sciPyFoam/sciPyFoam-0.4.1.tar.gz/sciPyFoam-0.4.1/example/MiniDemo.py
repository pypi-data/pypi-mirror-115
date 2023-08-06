import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import sciPyFoam.polyMesh2d as mesh2d
# Read data
caseDir='cases/blockMesh'  # case dir
fieldNames=['T','U']       # field name list
times,times_value=mesh2d.getTimes(caseDir)      # get all times name and value
MeshData=mesh2d.getMesh(caseDir, 'frontAndBack')
# read field data, return a dict contains point data and cell data 
fieldData=mesh2d.readCellData_to_pointData(caseDir, times[-1], fieldNames,MeshData) 
field_boundary=mesh2d.readField(caseDir,times[-1],'p','top')
print(len(field_boundary))

# read cellZones
owners=mesh2d.readOwner(caseDir)
cellZones=mesh2d.readCellZones(caseDir)
for cellZone in cellZones:
    print(cellZone)
# read boundaries
boundaries=mesh2d.readBoundary(caseDir)
print(boundaries.keys())
# Plot 
fig=plt.figure(figsize=(14,6))
ax=plt.gca()
ax.tricontourf(MeshData['x'],MeshData['y'],MeshData['triangles'],fieldData['pointData']['T'],levels=50,cmap='rainbow')
# ax.invert_yaxis()
plt.tight_layout()
# plt.savefig('test.pdf')
plt.show()