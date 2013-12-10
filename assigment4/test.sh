for i in knapsack_instances/knapsack_instances/*;  
	do echo; echo " randomwalk $i"; echo; time python3 randomwalk.py $i; 
	   echo; echo " maxvalue $i"; echo; time python3 maxvalue.py $i; 
	   echo; echo " randomized_maxvalue $i"; echo;  time python3 randomized_maxvalue.py $i; 
done > knapsack.log 2>&1; 