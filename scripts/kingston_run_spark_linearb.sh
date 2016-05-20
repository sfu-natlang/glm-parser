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
#spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 1 -p /ugrad/2/jca303/data/CoNLL-X/Bulgarian/data --train="bulgarian_bultreebank_train.conll" --test="bulgarian_bultreebank_test.conll" --learner=perceptron --fgen=english_1st_fgen --parser=ceisner --config=/ugrad/2/jca303/glm-parser/src/config/conllx.config

#spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 1 -p /ugrad/2/jca303/data/CoNLL-X/Danish/data --train="danish_ddt_train.conll" --test="danish_ddt_test.conll" --learner=perceptron --fgen=english_1st_fgen --parser=ceisner --config=/ugrad/2/jca303/glm-parser/src/config/conllx.config

#spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 1 -p /ugrad/2/jca303/data/CoNLL-X/Dutch/data --train="dutch_alpino_train.conll" --test="dutch_alpino_test.conll" --learner=perceptron --fgen=english_1st_fgen --parser=ceisner --config=/ugrad/2/jca303/glm-parser/src/config/conllx.config

spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 1 -p /ugrad/2/jca303/data/CoNLL-X/English/data --train="conll08st_train.conll" --test="conll08st_test.conll" --learner=perceptron --fgen=english_1st_fgen --parser=ceisner --config=/ugrad/2/jca303/glm-parser/src/config/conllx.config

#spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 1 -p /ugrad/2/jca303/data/CoNLL-X/German/data --train="german_tiger_train.conll" --test="german_tiger_test.conll" --learner=perceptron --fgen=english_1st_fgen --parser=ceisner --config=/ugrad/2/jca303/glm-parser/src/config/conllx.config

#spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 1 -p /ugrad/2/jca303/data/CoNLL-X/Japanese/data --train="japanese_verbmobil_train.conll" --test="japanese_verbmobil_test.conll" --learner=perceptron --fgen=english_1st_fgen --parser=ceisner --config=/ugrad/2/jca303/glm-parser/src/config/conllx.config

#spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 1 -p /ugrad/2/jca303/data/CoNLL-X/Portuguese/data --train="portuguese_bosque_train.conll" --test="portuguese_bosque_test.conll" --learner=perceptron --fgen=english_1st_fgen --parser=ceisner --config=/ugrad/2/jca303/glm-parser/src/config/conllx.config

#spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 1 -p /ugrad/2/jca303/data/CoNLL-X/Slovene/data --train="slovene_sdt_train.conll" --test="slovene_sdt_test.conll" --learner=perceptron --fgen=english_1st_fgen --parser=ceisner --config=/ugrad/2/jca303/glm-parser/src/config/conllx.config

#spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 1 -p /ugrad/2/jca303/data/CoNLL-X/Spanish/data --train="spanish_cast3lb_train.conll" --test="spanish_cast3lb_test.conll" --learner=perceptron --fgen=english_1st_fgen --parser=ceisner --config=/ugrad/2/jca303/glm-parser/src/config/conllx.config

#spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 1 -p /ugrad/2/jca303/data/CoNLL-X/Swedish/data --train="swedish_talbanken05_train.conll" --test="swedish_talbanken05_test.conll" --learner=perceptron --fgen=english_1st_fgen --parser=ceisner --config=/ugrad/2/jca303/glm-parser/src/config/conllx.config

#spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 1 -p /ugrad/2/jca303/data/CoNLL-X/Turkish/data --train="turkish_metu_sabanci_train.conll" --test="turkish_metu_sabanci_test.conll" --learner=perceptron --fgen=english_1st_fgen --parser=ceisner --config=/ugrad/2/jca303/glm-parser/src/config/conllx.config

