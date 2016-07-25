#!/bin/bash
cd "$( dirname "$0" )"
cd ../
./cleanup.sh
./setup_env.sh

cd ../src/

python setup_module.py bdist_egg
mv dist/module-0.1-py2.7.egg module.egg

spark-submit --master yarn-cluster \
             --num-executors 9     \
			 --driver-memory 7g    \
			 --executor-memory 7g  \
			 --executor-cores 3    \
			 --py-files module.egg \
			 pos_tagger.py -s 8 --hadoop config/pos_debug.config
