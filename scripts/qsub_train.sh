#!/bin/bash

code_path="/home/yulanh/glm-parser/trunk/src"

cat <<EOS | qsub -

#PBS -W group_list=cs-natlang
#PBS -l pmem=16gb
#PBS -l walltime=240:00:00
#PBS -N glm-train
#PBS -S /bin/csh

cd $code_path

./train.sh


EOS


