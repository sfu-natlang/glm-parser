#!/bin/bash
cd "$( dirname "$0" )"
cd ../
./cleanup.sh
./setup_env.sh

cd ../src/
rm pos_tagger.log
rm pos_tagger.log.bak

python pos_tagger.py -d penn2malt_tagger config/pos_penn-wsj-deps.config

../scripts/proc_log.sh pos_tagger.log

mv pos_tagger.log ../scripts/tests/penn2malt_tagger.log
mv penn2malt_tagger*.db ../scripts/tests/
