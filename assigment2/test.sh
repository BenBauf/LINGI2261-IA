#!/bin/bash  
for i in Benchs_Small/*; do  echo; echo "$i\n"; echo; time python3 mazeCollect.py $i; done > log_maze.txt 2>&1; 
