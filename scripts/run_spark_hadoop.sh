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

python setup_module.py bdist_egg
mv dist/module-0.1-py2.7.egg module.egg

spark-submit --master yarn-cluster --driver-memory 10g --executor-memory 10g --py-files module.egg glm_parser.py -i 2 -s 8 -p /cs/natlang-user/vivian/penn-wsj-deps/ --train='wsj_02[0-9][0-9].mrg.3.pa.gs.tab' --test='wsj_00[0-9][0-9].mrg.3.pa.gs.tab' --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=/cs/natlang-user/vivian/config/penn2malt.config
