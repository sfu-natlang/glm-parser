#!/bin/bash

project_path=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )'/..'

source $MODULESHOME/init/bash
module load LANG/PYTHON/2.7.6-SYSTEM
export PYTHONPATH=$PYTHONPATH:/cs/natlang-projects/glm-parser/Cython-0.20.1

cd $project_path'/src'
python setup.py build_ext --inplace

cd hvector
python setup.py install --install-lib .

cd ..
python glm_parser.py -i 30 -b 2 -e 21 -t 0,1,22,24 -p /cs/natlang-projects/glm-parser/penn-wsj-deps/ -d '/cs/natlang-projects/glm-parser/new_results/Weight' --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner
