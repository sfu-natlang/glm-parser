#!/bin/bash

project_path=$(python get_path.py)

source $MODULESHOME/init/bash
module load LANG/PYTHON/2.7.6-SYSTEM

export PYTHONPATH=$PYTHONPATH:/cs/natlang-projects/glm-parser/Cython-0.20.1

cd $project_path

echo "Compile Cython classes ..."
python setup.py build_ext --inplace


echo "Compile hvector ..."
cd hvector
python setup.py install --install-lib .


