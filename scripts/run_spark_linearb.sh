#!/bin/bash

project_path=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )'/..'

source $MODULESHOME/init/bash
module load natlang
module load NL/HADOOP/SPARK/1.2.1
module load LANG/PYTHON/2.7.6-SYSTEM
export PYTHONPATH=$PYTHONPATH:/cs/natlang-projects/glm-parser/Cython-0.20.1

cd $project_path'/src'
python setup.py build_ext --inplace

cd hvector
python setup.py install --install-lib .

cd ..
pyspark glm_parser.py -i 10 -b 2 -e 21 -t 0,1,22,24 -p /cs/natlang-projects/glm-parser/penn-wsj-deps/ -d '/cs/natlang-projects/glm-parser/new_results/Weight' --learner=spark_perceptron --fgen=english_1st_fgen --parser=ceisner
