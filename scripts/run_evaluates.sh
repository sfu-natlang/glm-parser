#!/bin/bash

project_path='/home/sunyans/sfu-natlang/glm-parser'

source $MODULESHOME/init/bash
module load LANG/PYTHON/2.7.6-SYSTEM
export PYTHONPATH=$PYTHONPATH:/cs/natlang-projects/glm-parser/Cython-0.20.1

cd $project_path'/src'
python setup.py build_ext --inplace

cd hvector
python setup.py install --install-lib .

cd $project_path'/src'
python glm_parser.py -i 1 -b 2 -e 21 -t 0,1,22,24 -p /cs/natlang-projects/glm-parser/penn-wsj-deps/ -d "/cs/natlang-projects/glm-parser/new_results/weight/OneIter0"

for i in {1..10}
do
    echo "===============================================" >> ./glm_parser.log
    echo "Iter $i :" >> ./glm_parser.log
    j=$(($i-1))
    python glm_parser.py -i 1 -b 2 -e 21 -t 0,1,22,24 -p /cs/natlang-projects/glm-parser/penn-wsj-deps/ -d "/cs/natlang-projects/glm-parser/new_results/weight/OneIter$i" -l "/cs/natlang-projects/glm-parser/new_results/weight/11-18-2014/Weight_Iter_$j.db"
done
 
