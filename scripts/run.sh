#!/bin/bash

qsub -V -l walltime=08:00:00,nodes=1pn=1,pmem=8gb -W group_list=colony-users qsub_train.sh

