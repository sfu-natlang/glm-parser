#!/bin/bash

project_path=/home/sunyans/sfu-natlang/glm-parser/src/

source $MODULESHOME/init/bash
module load LANG/PYTHON/2.7.6-SYSTEM

export PYTHONPATH=$PYTHONPATH:/cs/natlang-projects/glm-parser/Cython-0.20.1

cd $project_path

echo "Compile Cython classes ..."
python setup.py build_ext --inplace


echo "Compile hvector ..."
cd hvector
python setup.py install --install-lib .


cd ..
python glm_parser.py -i 1 -b 2 -e 21 -t 0,1,22,24 -p /cs/natlang-projects/glm-parser/penn-wsj-deps/

