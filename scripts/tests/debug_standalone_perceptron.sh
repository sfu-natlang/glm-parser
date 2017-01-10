#!/bin/bash
cd "$( dirname "$0" )"
cd ../
./cleanup.sh
./setup_env.sh

cd ../src/
rm glm_parser.log
rm glm_parser.log.bak

spark-submit --driver-memory 4g   \
			 --executor-memory 4g \
			 --master 'local[*]'  \
             glm_parser.py -s 4 --learner=perceptron config/debug.config

../scripts/proc_log.sh glm_parser.log

mv glm_parser.log ../scripts/tests/debug_standalone_perceptron.log
