'''NAMES OF THE AUTHOR(S): Baufays Benoit - Colmonts Julien'''

from search import *


######################  Implement the search #######################

class Knapsack(Problem):
    max_size=0
    number=0
    
    def __init__(self,path):
        objects=self.createMap(path)
        self.createSleigh(objects)
        
    def successor(self, state):
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
        if(len(state[0]) is 0):
            return 0
        return state[2][0]


    #read the file, create the list and code it for the state schema
    def createMap(self,path):
        allObjects=[]
        
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
        allObjects=sorted(allObjects, key=lambda obj: obj[1])
        return allObjects

    def createSleigh(self,allObjects):
        sleigh=[]
        available=allObjects
        weight=0
        utility=0
        while weight <= self.max_size and len(available)>0:
            elem=available.pop(0)
            if (weight+elem[1]<=self.max_size):
                sleigh.append(elem)
                weight=weight+elem[1]
                utility=utility+elem[2]
            else:
                available.append(elem)
                break              

        
        self.initial=(sleigh,available,(utility,weight))
         
