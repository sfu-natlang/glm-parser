#!/bin/bash

project_path='/home/sunyans/sfu-natlang/glm-parser'

source $MODULESHOME/init/bash
module load LANG/PYTHON/2.7.6-SYSTEM
export PYTHONPATH=$PYTHONPATH:/cs/natlang-projects/glm-parser/Cython-0.20.1

cd $project_path'/src'
python setup.py build_ext --inplace

cd hvector
python setup.py install --install-lib .
