#!/bin/bash
cd "$( dirname "$0" )"
cd ../
./cleanup.sh
./setup_env.sh

cd ../src/
rm glm_parser.log
rm glm_parser.log.bak

python glm_parser.py -i 1 --tagger-w-vector=$NATLANG_DATA/fv_Iter_5.db config/default.config

../scripts/proc_log.sh glm_parser.log

mv glm_parser.log ../scripts/tests/default_sequential_tagger.log
