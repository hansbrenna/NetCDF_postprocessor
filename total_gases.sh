#!/bin/bash

for file in files/BRCLO3_list*.dat
do

    for var in CLO BRO HCL HBR
    do
	echo $file	
	echo $var
	python total_gases.py $file $var
    done
done