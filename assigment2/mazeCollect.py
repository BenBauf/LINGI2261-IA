'''NAMES OF THE AUTHOR(S): Baufays Benoit - Colmonts Julien'''

from search import *
import math


######################  Implement the search #######################

class MazeCollect(Problem):
    #index for the money tuple in the state
    money_Index=1
    
    def __init__(self,init):
        #dictionnary of vide position
        self.vide=None
        #position of the goal
        self.goal=None
        self.createMap(init)
       
    
    def goal_test(self, state):
        if(state[0]=="init"):
            mapInfo=state[1]
        else:
            mapInfo=state
            
        return (len(mapInfo[self.money_Index])==0) and mapInfo[0]==self.goal

        
    def successor(self, state):
        if(state[0]=="init"):
            mapInfo=state[1]
        else:
            mapInfo=state
        retour=(tuple(self.IA(mapInfo)))
        return retour

    def IA(self,mapInfo):
        pos=[]
        position=mapInfo[0]
        #the four possibilities
        for a in [(-1,0),(0,-1),(1,0),(0,1)]:
            #take the money list
            moneyStack=list(mapInfo[self.money_Index])
            newPosition=(position[0]+a[0],position[1]+a[1])
            #if the new position is a entry of the vide dictionnary
            if self.getString(newPosition) in self.vide:
                if(newPosition in moneyStack):
                    #if it is a dollar case, we must recompute the minimal distance between all the dollars \{newPosition}
                    moneyStack.remove(newPosition)
                    saveMoney=list(mapInfo[self.money_Index])
                    saveMoney.remove(newPosition)                  
                    distance=self.dist(saveMoney)
                else:
                    distance=mapInfo[2]
                #we use the yield to return a iteraor.  With this, we use less memory
                yield (('move',((newPosition,tuple(moneyStack),distance))))

    #find the closest dollar of a position
    def closestDollar(self, dollars,position):    
        closestDollar = None
        dst = 0
        
        if len(dollars) is not 0 :
            dst = self.manhattan(position, dollars[0])
            for elem in dollars :
                temp=self.manhattan(position, elem)
                if temp <= dst: 
                    dst = temp
                    closestDollar = elem
        return closestDollar

    #see the rapport for a explication of this heuristique
    def Heuristique(self,node):
        state=node.state
        if(state[0]=="init"):
            mapInfo=state[1]
        else:
            mapInfo=state
        infoDollar=mapInfo[2]
        allNodes=list(mapInfo[self.money_Index])
        #if we have reach all dollar, we must now find the best past to the goal
        if len(allNodes) is 0:
            return self.manhattan(self.goal,mapInfo[0])
        else:
            closest=self.closestDollar(allNodes,mapInfo[0])                
            return self.manhattan(mapInfo[0], closest) +mapInfo[2]


    #the manhattan distance between two points
    def manhattan(self, toPoint,fromPoint):
        return (math.fabs(toPoint[0] - fromPoint[0]) + math.fabs(toPoint[1] - fromPoint[1]))

    #get a String representation of a point (utility for the key of the vide dictionnary)
    def getString(self,point):
        final="{0}#{1}".format(point[0],point[1])
        return final

    #method to find the small path between all non reached dollars
    def dist(self,moneyT):
        dist=1000000000000
        money=list(moneyT)
        for node in money:
            nodeMin=None
            distance=0
            moneyStack=money
            moneyStack.remove(node)
            while len(moneyStack)>0:
                distMin=dist=self.manhattan(moneyStack[0],node)
                nodeMin=(moneyStack[0])
                for dollar in moneyStack:
                    dist=self.manhattan(dollar,node)
                    if(dist<distMin):
                        distMin=dist
                        nodeMin=dollar
                distance+=distMin
                moneyStack.remove(nodeMin)
            #we add the path between the last node and the goal
            if nodeMin is not None:
                distance+=self.manhattan(self.goal,nodeMin)
            if dist>distance:
                dist=distance

        return dist

    
    #read the file, create the map and code it for the state schema
    def createMap(self,path):
        sizeY=0
        x=0
        y=-1
        moneyStack=[]
        debut=[]
        vide={}
        
        f = open(path,'r')
        for line in f:
            y=y+1            
            sizeY=sizeY+1
            x=-1
            for elem in line:
                x=x+1
                if(elem!='#'and elem!="\n"):
                    if(elem=='$'):
                        moneyStack.append((x,y))
                    elif(elem=='@'):
                        debut=(x,y)
                    elif(elem=='+'):
                        self.goal=(x,y)
                    vide[self.getString((x,y))]=(x,y)

        
        saveMoneyStack=list(moneyStack)
        distance=self.dist(saveMoneyStack)
        mapInfo=('init',(debut,tuple(moneyStack),distance,(x,sizeY)))
        self.vide=vide
        self.initial=mapInfo


###################### Launch the search #########################

if(len(sys.argv)>1):
    problem=MazeCollect(sys.argv[1])
else:
    problem=MazeCollect("Benchs_Small/mazeCollect0")
node=astar_graph_search(problem, problem.Heuristique)
path=node.path()
path.reverse()
sizeElements=len(path[0].state[1])
size=path[0].state[1][sizeElements-1]
for n in path:
    a=['#' ] * size[1]
    for i in range(0,size[1]):
        a[i]=['#'] * size[0]
    state=n.state
    if(state[0]=="init"):
        state=state[1]

    #place libre
    freeSpaces=problem.vide
    for spaceS in freeSpaces:
        space=spaceS.split('#')
        a[int(space[1])][int(space[0])]=' '
    
    #coffre
    elem=problem.goal
    a[elem[1]][elem[0]]='+'

    #current position
    elem=state[0]
    a[elem[1]][elem[0]]='@'

    #money
    moneyStack=state[problem.money_Index]
    for money in moneyStack:
        a[money[1]][money[0]]='$'


    for ligne in a:
        ligneP=""
        for elem in ligne:
            ligneP=ligneP+elem
        print(ligneP)
    print('')
