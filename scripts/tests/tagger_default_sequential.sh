#!/bin/bash
cd "$( dirname "$0" )"
cd ../
./cleanup.sh
./setup_env.sh

cd ../src/
rm pos_tagger.log
rm pos_tagger.log.bak

python pos_tagger.py config/pos_default.config

../scripts/proc_log.sh pos_tagger.log

mv pos_tagger.log ../scripts/tests/tagger_default_sequential.log
