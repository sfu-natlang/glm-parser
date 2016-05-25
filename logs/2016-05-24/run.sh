#!/bin/bash
#noti Start_CoNLL_U-1
cd "$( dirname "$0" )"
cd src
echo "Compile Cython classes ..."
python setup.py build_ext --inplace
echo "Compile hvector ..."
cd hvector
python setup.py install --install-lib .
cd ..

#spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' \
#glm_parser.py -i 5 -p /Users/jetic/Daten/glm-parser-data/universal-dependencies-1.2 --train="grc-ud-train.conllu" --test="grc-ud-test.conllu" -d 24-05-2016_Ancient_Greek -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

cd ../../
cd glm-parser-3
./run.sh
