#!/bin/bash

: <<'END'
Usage:
NAME
    ./autolog.sh - re-organize and submit log files

SYNOPSIS
    ./autolog.sh SOURCE DEST MACHINE

DESCRIPTION
    Extract useful info from SOURCE and re-organize it in DEST, then submit the
    log file to wiki. The third argument is to specify on which machine did the
    training happened.

END

while read line; do
    if [[ $line == *"Using learner"* ]]
    then
        learnerLine=$line
    elif [[ $line == *"Using parser"* ]]
    then
        parserLine=$line
    elif [[ $line == *"Using feature generator"* ]]
    then
        fgenLine=$line
    elif [[ $line == *"PARSER"*"Using data from"* ]]
    then
        datapathLine=$line
    elif [[ $line == *"Training data sections"* ]]
    then
        trainLine=$line
    elif [[ $line == *"Testing data sections"* ]]
    then
        testLine=$line
    elif [[ $line == *"Total training iterations"* ]]
    then
        iterLine=$line
    elif [[ $line == *"Total Training Time"* ]]
    then
        trainTimeLine=$line
    elif [[ $line == *"Feature count"* ]]
    then
        fcountLine=$line
    elif [[ $line == *"Unlabeled accuracy"* ]]
    then
        uaLine=$line
    elif [[ $line == *"Unlabeled accuracy"* ]]
    then
        uaaLine=$line
    fi

done < $1

echo "Environment" >> $2
echo "-------------------" >> $2
echo -e "Machine: $3\n" >> $2
python --version >> $2 2>&1
echo -e "" >> $2
cython --version >> $2 2>&1
echo -e "\n" >> $2

echo -e "Configuration" >> $2
echo -e "-------------------" >> $2
echo -e "$learnerLine\n" >> $2
echo -e "$parserLine\n" >> $2
echo -e "$fgenLine\n" >> $2
echo -e "$datapathLine\n" >> $2
echo -e "$trainLine\n" >> $2
echo -e "$iterLine\n" >> $2
echo -e "$testLine\n\n" >> $2

echo "Configuration" >> $2
echo "-------------------" >> $2
echo -e "$trainTimeLine\n" >> $2
echo -e "$fcountLine\n" >> $2
echo -e "$uaLine\n" >> $2
echo -e "$uaaLine\n" >> $2

git clone git@github.com:sfu-natlang/glm-parser.wiki.git
echo "Submiting log file..."
cd glm-parser.wiki/logs
mkdir -p ${learnerLine:0:10}
mv ../../$2 ${learnerLine:0:10}
git add -A
git commit -m"new log added"
git pull --rebase
git push
cd ../../
echo "Removing wiki repo..."
rm -rf glm-parser.wiki
