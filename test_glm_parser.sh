#!/bin/bash
#!/usr/bin/env python2.7
export PYTHONPATH=$PYTHONPATH:/cs/natlang-projects/glm-parser/Cython-0.20.1

train_sec_begin="2"
train_sec_end="6"
acc_test_sec_list="2"


if [ "" != "$1" ]
then
   train_sec_begin=$1 
fi

if [ "" != "$2" ]
then
   train_sec_end=$2
fi

output_file_name="sec_"$train_sec_begin"_"$train_sec_end

cd /home/yulanh/glm-parser
python setup.py build_ext --inplace

#train: python test_glm_parser.py -b 2 -e 2 -o sec_02 
#accuracy test: python test_glm_parser.py -d weight_iter_1.db -o sec_02 -a 2

python test_glm_parser.py -b $train_sec_begin -e $train_sec_end -o $output_file_name 
#-a $acc_test_sec_listl
