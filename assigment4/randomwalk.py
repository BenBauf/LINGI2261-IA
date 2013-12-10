'''NAMES OF THE AUTHOR(S): Baufays Benoit - Colmonts Julien'''

from search import *
from knapsack import *


###################### Launch the search #########################
        
problem=Knapsack(sys.argv[1])
node=random_walk(problem)
print(node.state[0])
print("Step")
print(node.step)
print("Best val")
print(node.state[2][0])

