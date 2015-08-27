#!/bin/bash

project_path='/cs/natlang-projects/glm-parser'
result_path=$project_path/new_results

# lossless
python conll_tree_generator.py -t $project_path/wsj_trees/ -d $result_path/wsj_conll_tree/lossless/ -c $project_path/penn-wsj-deps/

# lossy
python conll_tree_generator.py -t $project_path/wsj_trees/ -d $result_path/wsj_conll_tree/lossy/ -c $project_path/penn-wsj-deps/ -l
