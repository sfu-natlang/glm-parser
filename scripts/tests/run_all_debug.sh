#!/bin/bash
cd "$( dirname "$0" )"
./run_debug_sequential.sh
./run_debug_standalone.sh
./run_debug_yarn.sh
