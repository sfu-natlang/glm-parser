#!/bin/bash
cd "$( dirname "$0" )"
cd ../
./cleanup.sh
./setup_env.sh

cd ../src/
rm pos_tagger.log
rm pos_tagger.log.bak

spark-submit --driver-memory 4g   \
			 --executor-memory 4g \
			 --master 'local[*]'  \
			 pos_tagger.py -s 4 --learner=perceptron config/pos_default.config

../scripts/proc_log.sh pos_tagger.log

mv pos_tagger.log ../scripts/tests/tagger_default_standalone_perceptron.log
