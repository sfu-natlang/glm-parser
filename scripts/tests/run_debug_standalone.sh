#!/bin/bash
cd "$( dirname "$0" )"
./debug_standalone.sh
./debug_standalone_perceptron.sh
./debug_standalone_tagger.sh
