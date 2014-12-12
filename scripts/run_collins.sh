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
python glm_parser.py -i 20 -b 2 -e 21 -t 23 -p /cs/natlang-projects/glm-parser/wsj_conll_tree_lossy/ -d "/cs/natlang-projects/glm-parser/new_results/weight/Spinal_Weight"
