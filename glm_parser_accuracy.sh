#!/bin/bash

test_secs=0,1,22,24
iter=0
db_name=""
output_file="accuracy.out"

HELP_MSG="
This is the script for test the accuracy of the glm parser with specified db data

Options:
	-s:	set the sections for accuracy testing
	-db:	set the db file name that needs loading
	-i:	set the iteration number
	-of:	set the output file name
	--help:	help message for the script
"

opt=""
for value in $@;
do
	echo $value
	if [ "$value" == "--help" ]
	then
	   echo $HELP_MSG
	   exit 0
	fi
	
	if [ "$opt" == "-s" ]
	then
	   test_secs=$value 
	elif [ "$opt" == "-db" ]
	then
	   db_name=$value
	elif [ "$opt" == "-i" ]
	then
	   iter=$value
	elif [ "$opt" == "-of" ]
	then
	   output_file=$value
	fi

	opt=$value

done

echo $test_secs $db_name $iter

echo $db_name" accuracy on sections: "$test_secs >> $output_file
python glm_parser.py -a $test_secs -d $db_name >> $output_file 
