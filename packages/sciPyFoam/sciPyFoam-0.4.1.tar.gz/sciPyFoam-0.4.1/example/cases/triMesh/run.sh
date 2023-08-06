#!/bin/sh
cd ${0%/*} || exit 1    # Run from this directory

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions

application=`getApplication`

./clean.sh
gmsh gmsh/box.geo -3 -o gmsh/box.msh -format msh22
gmshToFoam gmsh/box.msh
changeDictionary

runApplication $application
