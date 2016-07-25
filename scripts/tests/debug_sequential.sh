#!/bin/bash
cd "$( dirname "$0" )"
cd ../
./cleanup.sh
./setup_env.sh

cd ../src/
rm glm_parser.log
rm glm_parser.log.bak

python glm_parser.py config/debug.config

../scripts/proc_log.sh glm_parser.log

mv glm_parser.log ../scripts/tests/debug_sequential.log
