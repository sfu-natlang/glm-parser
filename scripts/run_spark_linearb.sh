#!/bin/bash

project_path=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )'/..'

source $MODULESHOME/init/bash
module load natlang
module load bigdata
module load spark/1.6.1
module load NL/LANG/PYTHON/Anaconda-2.4.0 

cd $project_path'/src'
python setup.py build_ext --inplace

cd hvector
python setup.py install --install-lib .

cd ..
spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 10 -p /cs/natlang-projects/glm-parser/penn-wsj-deps/ --train='wsj_0[2-9][0-9][0-9].mrg.3.pa.gs.tab|wsj_1[0-9][0-9][0-9].mrg.3.pa.gs.tab|wsj_2[0-1][0-9][0-9].mrg.3.pa.gs.tab' --test='wsj_0[0-1][0-9][0-9].mrg.3.pa.gs.tab|wsj_22[0-9][0-9].mrg.3.pa.gs.tab|wsj_24[0-9][0-9].mrg.3.pa.gs.tab' --learner=perceptron --fgen=english_1st_fgen --parser=ceisner

