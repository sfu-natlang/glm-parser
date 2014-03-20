#!/bin/bash
#!/usr/bin/env python2.7
export PYTHONPATH=$PYTHONPATH:/cs/natlang-projects/glm-parser/Cython-0.20.1

train_sec_begin="2"
train_sec_end="6"
acc_test_sec_list="2"
test_data_path="/cs/natlang-projects/glm-parser/penn-wsj-deps/"
output_path="/cs/natlang-projects/glm-parser/results/"

# this bash accept 3 valuables
# 1.  begin train section
# 2.  end train section
# 3.  iteration number (i -- indicate ith iteration)

if [ "" != "$1" ]
then
   train_sec_begin=$1 
fi

if [ "" != "$2" ]
then
   train_sec_end=$2
fi

output_file_name=$output_path"sec_"$train_sec_begin"_"$train_sec_end

if [ "" != "$3" ]
then
   output_file_name=$output_file_name"_iter_"$3
fi
echo $output_file_name
cd /home/yulanh/glm-parser
python setup.py build_ext --inplace

#train: python glm_parser_train.py -b 2 -e 2 -o sec_02 
#accuracy test: python glm_parser_train.py -d weight_iter_1.db -o sec_02 -a 2

python glm_parser_train.py -b $train_sec_begin -e $train_sec_end -o $output_file_name -t $test_data_path
#-a $acc_test_sec_list
