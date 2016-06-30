#!/bin/bash

cd "$( dirname "$0" )"

project_path=$(python get_path.py)

source $MODULESHOME/init/bash
module load natlang
module load NL/LANG/PYTHON/Anaconda-2.4.0
module load bigdata
module load spark/1.5.1

cd $project_path

echo "Compile Cython classes ..."
python setup.py build_ext --inplace


echo "Compile hvector ..."
cd hvector
python setup.py install --install-lib .
cd ..

