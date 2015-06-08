#!/bin/bash

script_path=$(python get_path.py)

cat <<EOS | qsub -

#PBS -W group_list=cs-natlang
#PBS -l pmem=200gb
#PBS -l walltime=120:00:00
#PBS -N glm-train
#PBS -S /bin/csh

cd $script_path

./train.sh


EOS


