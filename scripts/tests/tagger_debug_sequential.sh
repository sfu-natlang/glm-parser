#!/bin/bash
cd "$( dirname "$0" )"
cd ../
./cleanup.sh
./setup_env.sh

cd ../src/
rm universal_tagger.log
rm universal_tagger.log.bak

python universal_tagger.py config/pos_debug.config

../scripts/proc_log.sh universal_tagger.log

mv universal_tagger.log ../scripts/tests/tagger_debug_sequential.log
