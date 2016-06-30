#!/bin/bash

cd "$( dirname "$0" )"

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
spark-submit --driver-memory 4g --executor-memory 4g --master 'local[*]' glm_parser.py -s 4 config/debug.config
