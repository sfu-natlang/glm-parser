#!/bin/bash

# run spark locally

project_path=$(python get_path.py)

source $MODULESHOME/init/bash
module load natlang
module load NL/LANG/PYTHON/Anaconda-2.3.0
#load spark 1.2.1, no need on the hadoop cluster
module load NL/HADOOP/SPARK/1.2.1

cd $project_path

echo "Compile Cython classes ..."
python setup.py build_ext --inplace


echo "Compile hvector ..."
cd hvector
python setup.py install --install-lib .
cd ..

spark-submit glm_parser.py -i 10 -s 4 -p /cs/natlang-projects/glm-parser/penn-wsj-deps/ 
--train='wsj_02[0-9][0-9].mrg.3.pa.gs.tab' 
--test='wsj_00[0-9][0-9].mrg.3.pa.gs.tab' 
--learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/penn2malt.config