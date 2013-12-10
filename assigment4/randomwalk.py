'''NAMES OF THE AUTHOR(S): Baufays Benoit - Colmonts Julien'''

from search import *
from knapsack import *


###################### Launch the search #########################
        
problem=Knapsack("knapsack_instances/knapsack_instances/knapsack0.txt")
node=random_walk(problem)
print(node.state[0])

