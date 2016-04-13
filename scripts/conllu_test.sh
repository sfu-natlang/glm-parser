#!/bin/bash

echo -n "Enter the language you would like to test > "
read lang

python ../src/glm_parser.py -i 1 -p ~/Code/natlang/data/CoNLL/universal-dependencies-1.2 --train="$lang-ud-train*.conllu" --test="$lang-ud-dev.connlu" -d conll -a --learner=average_perceptron --fgen=english_1st_fgen --parser=ceisner --config=../src/config/conllu.config

rm conll_Iter_0.db 
rm glm_parser.log
