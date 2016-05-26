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
spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 5 -p /cs/natlang-data/CoNLL/universal-dependencies-1.2 --train='grc_proiel-ud-train.conllu' --test='grc_proiel-ud-test.conllu' --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

mv ../src/glm_parser.log ../logs/2016-05-24/UD_Ancient_Greek-PROIEL.log



spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 5 -p /cs/natlang-data/CoNLL/universal-dependencies-1.2 --train='en-ud-train.conllu' --test='en-ud-test.conllu' --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

mv ../src/glm_parser.log ../logs/2016-05-24/UD_English.log



spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 5 -p /cs/natlang-data/CoNLL/universal-dependencies-1.2 --train='et-ud-train.conllu' --test='et-ud-test.conllu' --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

mv ../src/glm_parser.log ../logs/2016-05-24/UD_Estonian.log



spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 5 -p /cs/natlang-data/CoNLL/universal-dependencies-1.2 --train='fi-ud-train.conllu' --test='fi-ud-test.conllu' --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

mv ../src/glm_parser.log ../logs/2016-05-24/UD_Finnish.log



spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 5 -p /cs/natlang-data/CoNLL/universal-dependencies-1.2 --train='fi_ftb-ud-train.conllu' --test='fi_ftb-ud-test.conllu' --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

mv ../src/glm_parser.log ../logs/2016-05-24/UD_Finnish-FTB.log



spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 5 -p /cs/natlang-data/CoNLL/universal-dependencies-1.2 --train='fr-ud-train.conllu' --test='fr-ud-test.conllu' --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

mv ../src/glm_parser.log ../logs/2016-05-24/UD_French.log



spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 5 -p /cs/natlang-data/CoNLL/universal-dependencies-1.2 --train='de-ud-train.conllu' --test='de-ud-test.conllu' --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

mv ../src/glm_parser.log ../logs/2016-05-24/UD_German.log



spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 5 -p /cs/natlang-data/CoNLL/universal-dependencies-1.2 --train='got-ud-train.conllu' --test='got-ud-test.conllu' --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

mv ../src/glm_parser.log ../logs/2016-05-24/UD_Gothic.log



spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 5 -p /cs/natlang-data/CoNLL/universal-dependencies-1.2 --train='el-ud-train.conllu' --test='el-ud-test.conllu' --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

mv ../src/glm_parser.log ../logs/2016-05-24/UD_Greek.log



spark-submit --driver-memory 20g --executor-memory 20g --master 'local[*]' glm_parser.py -s 8 -i 5 -p /cs/natlang-data/CoNLL/universal-dependencies-1.2 --train='he-ud-train.conllu' --test='he-ud-test.conllu' --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=config/conllu.config

mv ../src/glm_parser.log ../logs/2016-05-24/UD_Hebrew.log

