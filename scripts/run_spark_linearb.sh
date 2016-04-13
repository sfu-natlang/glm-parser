#!/bin/bash

project_path=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )'/..'

source $MODULESHOME/init/bash
module load natlang
module load bigdata
module load spark/1.5.1
module load NL/LANG/PYTHON/Anaconda-2.4.0 

cd $project_path'/src'
python setup.py build_ext --inplace

cd hvector
python setup.py install --install-lib .

cd ..
spark-submit --master local[4] glm_parser.py -s 4 -i 1 -p /cs/natlang-projects/glm-parser/penn-wsj-deps/ --train='wsj_02[0-9][0-9].mrg.3.pa.gs.tab' --test='wsj_00[0-9][0-9].mrg.3.pa.gs.tab' --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner
