#!/bin/bash
cd "$( dirname "$0" )"
./tagger_debug_sequential.sh
./tagger_debug_standalone.sh
./tagger_debug_yarn.sh
