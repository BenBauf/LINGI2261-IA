#!/bin/bash  
for i in Benchs_Large/*; do  echo; echo "$i\n"; echo; time python3 mazeCollect.py $i; done > log_mazeLarge.txt 2>&1;
for i in Benchs_Large/*; do  echo; echo "$i\n"; echo; time python3 mazeCollect2.py $i; done > log_maze2Large.txt 2>&1;  
