#!/bin/bash
cd "$( dirname "$0" )"
cd ../
./cleanup.sh
./setup_env.sh

cd ../src/
rm glm_parser.log
rm glm_parser.log.bak

python glm_parser.py -d penn2malt_sequential_perceptron --learner=perceptron config/penn-wsj-deps.config

../scripts/proc_log.sh glm_parser.log

mv glm_parser.log ../scripts/tests/penn2malt_sequential_perceptron.log
mv penn2malt_sequential_perceptron*.db ../scripts/tests/
