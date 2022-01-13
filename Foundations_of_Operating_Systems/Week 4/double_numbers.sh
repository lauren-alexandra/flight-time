#!/bin/bash
SECONDS=0
filename='file1.txt'

while read line
do
    # trim
    newline=$(echo "$line" | tr -d $'\r')

    doubled=$(( newline * 2 ))
    echo $doubled >> newfile1.txt
done < $filename

duration=$SECONDS
echo $duration