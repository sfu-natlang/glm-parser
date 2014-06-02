#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/cs/natlang-projects/glm-parser/Cython-0.20.1

cd ..
cd src

echo "Compile Cython classes ..."
python setup.py build_ext --inplace
