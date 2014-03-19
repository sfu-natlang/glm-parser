#!/bin/bash
#export PYTHONPATH=$PYTHONPATH:/cs/ugrad/yulanh/sfuhome/Cython-0.20.1

train_sec_begin="3"
train_sec_end="4"
output_file_name="sec_03_04"
acc_test_sec_list="2"


#python setup.py build_ext --inplace

#train: python test_glm_parser.py -b 2 -e 2 -o sec_02 
#accuracy test: python test_glm_parser.py -d weight_iter_1.db -o sec_02 -a 2

python test_glm_parser.py -b $train_sec_begin -e $train_sec_end -o $output_file_name 
#-a $acc_test_sec_listl
