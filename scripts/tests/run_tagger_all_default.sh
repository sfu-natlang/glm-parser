#!/bin/bash
cd "$( dirname "$0" )"
./tagger_default_sequential.sh
./tagger_default_standalone.sh
./tagger_default_yarn.sh
