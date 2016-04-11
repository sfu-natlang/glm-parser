#!/bin/bash

# run spark locally

project_path=$(python get_path.py)

source $MODULESHOME/init/bash
module load natlang
module load NL/LANG/PYTHON/Anaconda-2.4.0
module load bigdata
module load spark/1.5.1

cd $project_path

echo "Compile Cython classes ..."
python setup.py build_ext --inplace


echo "Compile hvector ..."
cd hvector
python setup.py install --install-lib .
cd ..

spark-submit --driver-memory 10g --executor-memory 10g --master local[4] glm_parser.py -i 10 -s 4 -p /cs/natlang-projects/glm-parser/penn-wsj-deps/ --train='wsj_0[2-9][0-9][0-9].mrg.3.pa.gs.tab|wsj_1[0-9][0-9][0-9].mrg.3.pa.gs.tab|wsj_2[0-1][0-9][0-9].mrg.3.pa.gs.tab' --test='wsj_0[0-1][0-9][0-9].mrg.3.pa.gs.tab|wsj_22[0-9][0-9].mrg.3.pa.gs.tab|wsj_24[0-9][0-9].mrg.3.pa.gs.tab' --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/penn2malt.config
