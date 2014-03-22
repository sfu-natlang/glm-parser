#!/bin/bash
#TODO user friendly parameter input
output_path="./"
begin_sec=2
end_sec=21
iter=0

HELP_MSG="
This is the script for training glm parser:

options:
	-tb:	set the begin section of training data
	-te:	set the end section of training data
	-op:	set the output path
	-i:	set the iteration number
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
	fi

	opt=$value
done
output_file_name="$output_path"merged_iter_"$iter"_sec_"$begin_sec"_"$end_sec
echo "python feature_set_merge.py -b "$begin_sec" -e "$end_sec" -i "$iter" -p "$output_path" -o "$output_file_name"".db"

python feature_set_merge.py -b $begin_sec -e $end_sec -i $iter -p $output_path -o $output_file_name".db"
echo "" > $output_file_name".done"

<<SINGLE_JOB
merge_output_pre=$output_path"merged_iter_"$iter"_sec_"
#rm $merge_output_pre"*.done"

merge_file_pre=$output_path"train_iter_"$iter"_sec_"

merge_file_1=$merge_file_pre$begin_sec
./wait_file.sh -f $merge_file_1".done"

let "begin_sec_1=$begin_sec+1"
for i in `seq $begin_sec_1 $end_sec`
do
    merge_output_file=$merge_output_pre$i
    
    if [ -e "$merge_output_file.done" ]
    then
        echo $merge_output_file".done exist, pass merge"
        continue
    fi

    merge_file_2=$merge_file_pre$i
    ./wait_file.sh -f $merge_file_2".done"

    python feature_set_merge.py -x $merge_file_1".db" -y $merge_file_2".db" -o $merge_output_file".db"
    echo "" > $merge_output_file".done"
    merge_file_1=$merge_output_file

    echo $merge_file_2" is merged!!" 
done

SINGLE_JOB
