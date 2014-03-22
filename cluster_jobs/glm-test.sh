#!/bin/bash

begin_sec=2
end_sec=21
test_data_path="/cs/natlang-projects/glm-parser/penn-wsj-deps/"
output_path="/cs/natlang-projects/glm-parser/results/"
code_path="/home/yulanh/glm-parser/trunk/"
cluster_output_path="/home/yulanh/cluster_out/"
iter=0

#./qsub_train.sh -tb $begin_sec -te $end_sec -i $iter -op $output_path -tp $test_data_path -cp $code_path -cop $cluster_output_path

./qsub_merge.sh -tb $begin_sec -te $end_sec -i $iter -op $output_path -tp $test_data_path -cp $code_path -cop $cluster_output_path

#cd $code_path
#./merge_db.sh $output_path $begin_sec $end_sec $iter

#acc_output="acc.out"
#echo "iteration: "$iter >> $acc_output
#python glm_parser.py -a 0,1,22,24 -d $merge_output >> $acc_output

echo "iteration: "$iter" done!!"


