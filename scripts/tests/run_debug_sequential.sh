#!/bin/bash
cd "$( dirname "$0" )"
./debug_sequential.sh
./debug_sequential_perceptron.sh
./debug_sequential_tagger.sh
