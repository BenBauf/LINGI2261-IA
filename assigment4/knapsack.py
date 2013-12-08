'''NAMES OF THE AUTHOR(S): Baufays Benoit - Colmonts Julien'''

from search import *


######################  Implement the search #######################

class Knapsack(Problem):
    max_size=0
    step=0
    allObjects=((1,1,1),(2,2,2),(3,3,3),(4,4,4),(5,5,5),(6,6,6),(7,7,7))
    
    def __init__(self,path):
        self.max_size=40
        self.initial=('init',((),self.allObjects,(0,0)))

    
    def goal_test(self, state):
        return self.step > 2

        
    def successor(self, state):
        self.step=self.step+1
        if(state[0]=='init'):
            state=state[1]
        available=state[1]
        #add
        for object in available:
            sleigh=list(state[0])
            notinSleigh=list(available)
            notinSleigh.remove(object)
            sleigh.append(object)
  
            yield('add',(tuple(sleigh),tuple(notinSleigh),(self.step,0)))

    #def path_cost(self, c, state1, action, state2):
    #    newObject=list(state2[0]).pop()
    #    return c+newObject[0]

    def Heuristique(self,node):
        state=node.state
        if(state[0]=='init'):
            state=state[1]
        if(len(state[0]) is 0):
            return 0
        newObject=list(state[0]).pop()
        return newObject[0]
         
        
    




###################### Launch the search #########################
        
problem=Knapsack("test")
#node=depth_first_tree_search(problem)
node=astar_graph_search(problem, problem.Heuristique)
#example of print
path=node.path()
path.reverse()
for n in path:
    print(n)
