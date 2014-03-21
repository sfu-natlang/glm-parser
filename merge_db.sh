#!/bin/bash
#TODO user friendly parameter input
output_path=$1
begin_set=$2
end_set=$3
iter=$4

merge_output=$output_path"merged_weight_iter_"$iter".db"

merge_file_1=$output_path"sec_"$begin_set"_iter_"$iter".db"
./wait_file.sh -f $merge_file_1

let "begin_set_1=$begin_set+1"
for i in `seq $begin_set_1 $end_set`
do
    echo $i
    merge_file_2=$output_path"sec_"$i"_iter_"$iter".db"
    ./wait_file.sh -f $merge_file_2

    python feature_set_merge.py $merge_file_1 $merge_file_2 $merge_output
    merge_file_1=$merge_output

    echo $merge_file_2" is merged!!" 
done

