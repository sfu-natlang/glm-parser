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
spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 5 -p /cs/natlang-data/CoNLL/universal-dependencies-1.2 --train='grc_proiel-ud-train.conllu' --test='grc_proiel-ud-test.conllu' --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --format=format/conllu.format
