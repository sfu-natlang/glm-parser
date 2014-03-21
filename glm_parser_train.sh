#!/bin/bash
#!/usr/bin/env python2.7
export PYTHONPATH=$PYTHONPATH:/cs/natlang-projects/glm-parser/Cython-0.20.1

train_sec_begin="2"
train_sec_end="6"
acc_test_sec_list="2"
iter="0"
test_data_path="/cs/natlang-projects/glm-parser/penn-wsj-deps/"
output_path="/cs/natlang-projects/glm-parser/results/"

# this bash accept 3 valuables
# 1.  begin train section
# 2.  end train section
# 3.  iteration number (i -- indicate ith iteration)

HELP_MSG=" 
This is the script for training glm parser:

options:
	-tb:	set the begin section of training data
	-te:	set the end section of training data
	-op:	set the output path
	-i:		set the iteration number (for the name of the output db)
	-tp:	set the test data path
	--help:	help message for the script
"

opt=""
for value in $@;
do
	if [ "$value" == "--help" ]
	then
	   echo "$HELP_MSG"
	   exit 0
	fi
	
	if [ "$opt" == "-tb" ]
	then
	   train_sec_begin=$value 
	elif [ "$opt" == "-te" ]
	then
	   train_sec_end=$value
	elif [ "$opt" == "-op" ]
	then
	   output_path=$value
	elif [ "$opt" == "-i" ]
	then
	   iter=$value
	elif [ "$opt" == "-tp" ]
	then
	   test_data_path=$value
	fi
	
	opt=$value

done

output_file_name=$output_path"sec_"$train_sec_begin"_"$train_sec_end"_iter_"$iter


cd /home/yulanh/glm-parser
python setup.py build_ext --inplace

#train: python glm_parser.py -b 2 -e 2 -o sec_02 
#accuracy test: python glm_parser.py -d weight_iter_1.db -o sec_02 -a 2

python glm_parser.py -b $train_sec_begin -e $train_sec_end -o $output_file_name -t $test_data_path
#-a $acc_test_sec_list
