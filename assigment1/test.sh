#!/bin/bash  
for i in Instances/Instances/*; do for j in `seq 1 4`; do echo; echo "$i - $j"; echo; time python3 koutack.py $i $j;  done; done > log_koutack_hard.txt 2>&1; 
