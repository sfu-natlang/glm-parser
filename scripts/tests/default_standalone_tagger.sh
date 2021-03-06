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
			 glm_parser.py -s 4 --tagger-w-vector=$NATLANG_DATA/penn2malt_tagger_Iter_1.db config/default.config

../scripts/proc_log.sh glm_parser.log

mv glm_parser.log ../scripts/tests/default_standalone_tagger.log
