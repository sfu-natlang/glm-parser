#!/bin/bash

cd "$( dirname "$0" )"

source $MODULESHOME/init/bash
module load natlang
module load bigdata
module load spark/1.6.1
module load NL/LANG/PYTHON/Anaconda-2.4.0

cd ../src

python setup_module.py bdist_egg
mv dist/module-0.1-py2.7.egg module.egg

#change the data paths of the penn-wsj-deps and format files to user's local dir which the hadoop workers can access
# It is very important to use the option --hadoop here, otherwise the clusters will only use the data from local hard drives instead of hdfs
spark-submit --master yarn-cluster --num-executors 9 --driver-memory 7g --executor-memory 7g --executor-cores 3 --py-files module.egg glm_parser.py -s 8 -i 1 --hadoop config/default.config
