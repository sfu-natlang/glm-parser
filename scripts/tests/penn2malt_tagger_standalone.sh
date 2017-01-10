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
			 pos_tagger.py -s 4 -d penn2malt_tagger_standalone config/pos_penn-wsj-deps.config

../scripts/proc_log.sh pos_tagger.log

mv pos_tagger.log ../scripts/tests/penn2malt_tagger_standalone.log
mv penn2malt_tagger_standalone*.db ../scripts/tests/
