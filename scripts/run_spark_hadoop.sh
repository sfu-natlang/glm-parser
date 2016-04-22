#!/bin/bash

source $MODULESHOME/init/bash
module load natlang
module load bigdata
module load spark/1.6.1
module load NL/LANG/PYTHON/Anaconda-2.4.0 

cd ../src

python setup_module.py bdist_egg
mv dist/module-0.1-py2.7.egg module.egg

cd learn
#pre-partion the data and move to hdfs: it's not necessary: the structure to be changed!!!
python partition.py /cs/natlang-user/vivian/penn-wsj-deps/ 'wsj_0[2-9][0-9][0-9].mrg.3.pa.gs.tab|wsj_1[0-9][0-9][0-9].mrg.3.pa.gs.tab|wsj_2[0-1][0-9][0-9].mrg.3.pa.gs.tab' 16

cd ..
#change the data paths of the penn-wsj-deps and config files to user's local dir which the hadoop workers can access
spark-submit --master yarn-cluster --num-executors 8 --driver-memory 10g --executor-memory 10g --py-files module.egg glm_parser.py -i 10 -s 16 -p /cs/natlang-user/vivian/penn-wsj-deps/ --train='wsj_0[2-9][0-9][0-9].mrg.3.pa.gs.tab|wsj_1[0-9][0-9][0-9].mrg.3.pa.gs.tab|wsj_2[0-1][0-9][0-9].mrg.3.pa.gs.tab' --test='wsj_0[0-1][0-9][0-9].mrg.3.pa.gs.tab|wsj_22[0-9][0-9].mrg.3.pa.gs.tab|wsj_24[0-9][0-9].mrg.3.pa.gs.tab' --learner=perceptron --fgen=english_1st_fgen --parser=ceisner --config=/cs/natlang-user/vivian/config/penn2malt.config
