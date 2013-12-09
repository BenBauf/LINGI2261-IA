'''NAMES OF THE AUTHOR(S): Baufays Benoit - Colmonts Julien'''

from search import *


######################  Implement the search #######################

class Knapsack(Problem):
    max_size=0
    number=0
    step=0
    allObjects=()
    sumUtility=0
    
    def __init__(self,path):
        self.createMap(path)
        self.initial=('init',((),self.allObjects,(0,0)))

    
    def goal_test(self, state):
        return self.step > 100

        
    def successor(self, state):
        self.step=self.step+1
        if(state[0]=='init'):
            state=state[1]
        available=state[1]
        utility , weight=state[2]
        #add
        for object in available:
            sleigh=list(state[0])
            notinSleigh=list(available)
            notinSleigh.remove(object)
            sleigh.append(object)
            if weight+object[1]<= self.max_size:
                yield('add',(tuple(sleigh),tuple(notinSleigh),(utility+object[2],weight+object[1])))
        
        #remove
        sleigh=list(state[0])
        for object in sleigh:
            sleigh=list(state[0])
            notinSleigh=list(available)
            sleigh.remove(object)
            notinSleigh.append(object)
            yield('remove',(tuple(sleigh),tuple(notinSleigh),(utility-object[2],weight-object[1])))

        #replace
        sleigh=list(state[0])
        notin=list(available)
        for object in sleigh:
                        
            for gift in notin:
                sleigh=list(state[0])
                notinSleigh=list(available)
                if weight-object[1]+gift[1]<= self.max_size:
                    sleigh.remove(object)
                    notinSleigh.append(object)
                    sleigh.append(gift)
                    notinSleigh.remove(gift)
                    yield('replace',(tuple(sleigh),tuple(notinSleigh),(utility-object[2]+gift[2],weight-object[1]+gift[1])))


    def value(self,state):
        if(state[0]=='init'):
            state=state[1]
        if(len(state[0]) is 0):
            return 0
        return state[2][0]
        


    #read the file, create the list and code it for the state schema
    def createMap(self,path):
        allObjects=[]
        sum=0
        
        f = open(path,'r')
        ligne=-1
        for line in f:
            ligne+=1
            object=[]
            if(ligne is 0):
                self.number=int(line)
            elif(ligne > self.number):
                self.max_size=int(line)
            else:
                for char in line.split(' '):
                    if len(char)>0:
                        object.append(int(char))
                allObjects.append(tuple(object))
                sum+=object[2]
                
        self.sumUtility=sum
        self.allObjects=tuple(allObjects)
         

#____________________________________________________________________________
# Local Search Algorithms

class LSNode:
    """A node in a local search. You will not need to subclass this class 
        for local search."""

    def __init__(self, problem, state, step):
        """Create a local search Node."""
        self.problem = problem
        self.state = state
        self.step = step
        self._value = None

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def value(self):
        """Returns the value of the state contained in this node."""
        if self._value is None:
            self._value = self.problem.value(self.state)
        return self._value

    def expand(self):
        """Yields nodes reachable from this node. [Fig. 3.8]"""
        for (act, next) in self.problem.successor(self.state):
            yield LSNode(self.problem, next, self.step + 1)




def randomized_max_value(problem, limit=100, callback=None):
    def getBest(current):
        bestMax=[]        
        bestMinValue=0
        elemMin=0
        for elem in list(current.expand()):
            if elem.value() > bestMinValue:
                if elemMin is 0:
                    bestMax.append(elem)
                    elemMin=elem
                    bestMinValue=elem.value()
                elif len(bestMax)>5:
                    bestMax.remove(elemMin)
                    bestMax.append(elem)
                    bestMinValue=elem.value()
                    elemMin=elem
                    for min in bestMax:
                        if min.value()< bestMinValue:
                            bestMinValue=min.value()
                            elemMin=min
                else:
                    bestMax.append(elem)
                    for min in bestMax:
                        if min.value()< bestMinValue:
                            bestMinValue=min.value()
                            elemMin=min
        
        return random.choice(bestMax)
        
    """Perform a random walk in the search space and return the best solution
    found. The returned value is a Node.
    If callback is not None, it must be a one-argument function that will be
    called at each step with the current node.
    """
    current = LSNode(problem, problem.initial, 0)
    best = current
    for step in range(limit):
        if callback is not None:
            callback(current)
        current = getBest(current)
        if current.value() > best.value():
            best = current
    return best




###################### Launch the search #########################
        
problem=Knapsack("knapsack_instances/knapsack_instances/knapsack0.txt")
node=randomized_max_value(problem,70)
print(node.state[0])

