#!/bin/bash

## Run as:

##qsub -V -l walltime=08:00:00,nodes=1pn=1,pmem=8gb -W
##group_list=colony-users <this-file>.sh

project_path=$PWD'/src'

source $MODULESHOME/init/bash

module load LANG/PYTHON/2.7.6-SYSTEM

export PYTHONPATH=$PYTHONPATH:/cs/natlang-projects/glm-parser/Cython-0.20.1

cd $project_path

python glm_parser.py -i 2 -b 2 -e 21 -t 0,1,22,24 -p
/cs/natlang-projects/glm-parser/penn-wsj-deps/ -d
$PWD'/scripts/Weight'
