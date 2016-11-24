#!/bin/bash
cd "$( dirname "$0" )"
cd ../
./cleanup.sh
./setup_env.sh

cd ../src/
rm ner_tagger.log
rm ner_tagger.log.bak

python ner_tagger.py config/ner_debug.config

../scripts/proc_log.sh ner_tagger.log

mv pos_tagger.log ../scripts/tests/ner_debug_sequential.log
