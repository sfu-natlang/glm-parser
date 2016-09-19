#!/bin/bash
cd "$( dirname "$0" )"
./run_default_sequential.sh
./run_default_standalone.sh
./run_default_yarn.sh
