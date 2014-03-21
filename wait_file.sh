#!/bin/bash

#script wait for the specified file to be created

HELP_MSG="
This is the script, which waits the specified file to be created.

Options:
	-f:	set the name of the file (mandatory)
	-t:	set the waiting time: NUMBER[SUFFIX] (default 5m)
		SUFFIX: s -- seconds (the default); m -- minutes; h -- hours; d -- days
	--help:	help message
"

file_name=""
wait_time="5m"

for value in $@;
do
    if [ "$value" == "--help" ]
    then
        echo "$HELP_MSG"
        exit 0
    fi

    if [ "$opt" == "-f" ]
    then
        file_name=$value
    elif [ "$opt" == "-t" ]
    then
        wait_time=$value
    fi
    opt=$value
done

if [ "$file_name" == "" ]
then
    echo "please enter the file name, see --help for help"
    exit 1
fi

while ! [ -e "$file_name" ]
do
    echo "wait for "$file_name
    sleep $wait_time
done
