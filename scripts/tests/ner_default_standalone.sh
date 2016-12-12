#!/bin/bash
cd "$( dirname "$0" )"
cd ../
./cleanup.sh
./setup_env.sh

cd ../src/
rm universal_tagger.log
rm universal_tagger.log.bak

spark-submit --driver-memory 4g   \
			 --executor-memory 4g \
			 --master 'local[*]'  \
			 universal_tagger.py -s 4 config/ner_default.config

../scripts/proc_log.sh universal_tagger.log

mv universal_tagger.log ../scripts/tests/ner_default_standalone.log
