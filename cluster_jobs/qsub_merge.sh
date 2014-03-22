#!/bin/bash

HELP_MSG="
This script is for submit merge jobs in cluster

Options:
	-tb:	set the begin section of training data
	-te:	set the end section of training data
	-op:	set the output path
	-i:	set the iteration number
	-tp:	set the test data path
	-cp:	set the code path
	-cop:	set the cluster output path
	--help:	help message for the script
"

begin_sec=2
end_sec=21
iter=0
test_data_path="/cs/natlang-projects/glm-parser/penn-wsj-deps/"
output_path="/cs/natlang-projects/glm-parser/results/"
code_path="/home/yulanh/glm-parser/trunk/"
cluster_output_path="/home/yulanh/cluster_out/"


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
	   begin_sec=$value
	elif [ "$opt" == "-te" ]
	then
	   end_sec=$value
	elif [ "$opt" == "-op" ]
	then
	   output_path=$value
	elif [ "$opt" == "-i" ]
	then
	   iter=$value
	elif [ "$opt" == "-tp" ]
	then
	   test_data_path=$value
	elif [ "$opt" == "-cp" ]
	then
	   code_path=$value
	elif [ "$opt" == "-cop" ]
	then
	   cluster_output_path=$value
	fi
	
	opt=$value

done

cd $cluster_output_path
cat <<EOS | qsub -
#PBS -W group_list=cs-natlang
#PBS -l pmem=16gb
#PBS -l walltime=10:00:00
#PBS -N glm_parser_merge_iter_$iter
#PBS -S /bin/csh

cd $code_path
./merge_db.sh -op $output_path -tb $begin_sec -te $end_sec -i $iter 
EOS


#cd $code_path
#./merge_db.sh -op $output_path -tb $begin_sec -te $end_sec -i $iter
echo "./merge_db.sh -op "$output_path" -tb "$begin_sec" -te "$end_sec" -i "$iter
