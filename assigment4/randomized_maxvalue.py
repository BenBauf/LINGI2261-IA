'''NAMES OF THE AUTHOR(S): Baufays Benoit - Colmonts Julien'''

from search import *
from knapsack import *

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

