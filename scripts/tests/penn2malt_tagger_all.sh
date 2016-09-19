#!/bin/bash
cd "$( dirname "$0" )"
./penn2malt_tagger.sh
./penn2malt_tagger_standalone.sh
./penn2malt_tagger_yarn.sh
