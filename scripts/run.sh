#!/bin/bash

qsub -V -e $PWD -o $PWD -l walltime=24:00:00,nodes=1:ppn=1,pmem=8gb -W group_list=colony-users qsub_train.sh

