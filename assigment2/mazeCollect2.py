'''NAMES OF THE AUTHOR(S): Baufays Benoit - Colmonts Julien'''

from search import *
import math

#we use a minimal mazeCollect to get the cost for a minimal path between two point
###############  class to find the small cost for one path  ########
class MazeCollectMinimal(Problem):
    def __init__(self,mapInfo):
        #a dictionnary of all vide points of the map
        self.vide=mapInfo[3]
        #the goal
        self.goal=mapInfo[0]
        self.initial=('init',(mapInfo[1],mapInfo[2]))

    #get a String representation of a point (utility for the key of the vide dictionnary)
    def getString(self,point):
        final="{0}#{1}".format(point[0],point[1])
        return final
        
    def goal_test(self, state):
        if(state[0]=="init"):
            mapInfo=state[1]
        else:
            mapInfo=state
            
        return self.goal==mapInfo[0]

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
        for a in [(-1,0),(0,-1),(1,0),(0,1)]:
            newPosition=(position[0]+a[0],position[1]+a[1])
            if self.getString(newPosition) in self.vide:
                yield(('move',(newPosition,mapInfo[1])))

    #a basic heuristique that get the manhattan distance between the current position and the goal
    def Heuristique(self,node):
        state=node.state
        if(state[0]=="init"):
            mapInfo=state[1]
        else:
            mapInfo=state
        return self.manhattan(mapInfo[0],self.goal)

    #the manhattan distance between two points
    def manhattan(self, toPoint,fromPoint):
        #print(toPoint)
        return (math.fabs(toPoint[0] - fromPoint[0]) + math.fabs(toPoint[1] - fromPoint[1]))


######################  Implement the search #######################
class MazeCollect2(Problem):
    money_Index=1
    def __init__(self,init):
        #a dictionnary of all vide points of the map
        self.vide=None
        #the goal position
        self.goal=None
        self.createMap(init)
       
    
    def goal_test(self, state):
        if(state[0]=="init"):
            mapInfo=state[1]
        else:
            mapInfo=state
            
        return (len(mapInfo[1])==0) and mapInfo[0]==self.goal

        
    def successor(self, state):
        if(state[0]=="init"):
            mapInfo=state[1]
        else:
            mapInfo=state
        retour=(tuple(self.IA(mapInfo)))
        return retour
    

    def IA(self,mapInfo):
        pos=[]
        moneyStack=list(mapInfo[1])
        if len(moneyStack)>0:
            #each money is a successor
            for money in moneyStack:
                newMoneyStack=list(mapInfo[1])
                newMoneyStack.remove(money)
                yield (('move',((money,tuple(newMoneyStack)))))
        else:
            #we have not enough money to find, go to the goal
            yield (('move',((self.goal,tuple(moneyStack)))))

    
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
    
    def Heuristique(self,node):
        state=node.state
        if(state[0]=="init"):
            mapInfo=state[1]
        else:
            mapInfo=state
        allNodes=list(mapInfo[self.money_Index])
        if len(allNodes) is 0:
            return self.manhattan(self.goal,mapInfo[0])
        else:
            closest=self.closestDollar(allNodes,mapInfo[0])
            dist=self.dist(allNodes)
            return self.manhattan(mapInfo[0], closest) +dist
        
    #the manhattan distance between two points
    def manhattan(self, toPoint,fromPoint):
        return (math.fabs(toPoint[0] - fromPoint[0]) + math.fabs(toPoint[1] - fromPoint[1]))

    
    def path_cost(self, c, state1, action, state2):
        if(state1[0]=="init"):
            mapInfo=state1[1]
        else:
            mapInfo=state1

        problem=MazeCollectMinimal((mapInfo[0],state2[0],mapInfo[1],self.vide))
        node=astar_graph_search(problem, problem.Heuristique)
        path=node.path()
        return c + len(path)
    
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

        mapInfo=('init',(debut,tuple(moneyStack),(x,sizeY)))
        self.vide=vide
        self.initial=mapInfo

    def printOneState(self,n):
        a=['#' ] * size[1]
        for i in range(0,size[1]):
            a[i]=['#'] * size[0]
        state=n.state
        if(state[0]=="init"):
            state=state[1]

        freeSpaces=problem.vide
        for spaceS in freeSpaces:
            space=spaceS.split('#')
            a[int(space[1])][int(space[0])]=' '
        

        #money
        moneyStack=state[1]
        for money in moneyStack:
            a[money[1]][money[0]]='$'

        #coffre
        elem=self.goal
        a[elem[1]][elem[0]]='+'

        #current position
        elem=state[0]
        a[elem[1]][elem[0]]='@'


        for ligne in a:
            ligneP=""
            for elem in ligne:
                ligneP=ligneP+elem
            print(ligneP)
        print('')


###################### Launch the search #########################


if(len(sys.argv)>1):
    problem=MazeCollect2(sys.argv[1])
else:
    problem=MazeCollect2("Benchs_Small/mazeCollect0")
node=astar_graph_search(problem, problem.Heuristique)
path=node.path()
path.reverse()
sizeElements=len(path[0].state[1])
size=path[0].state[1][sizeElements-1]
tmp=None
number=0
for n in path:
    if tmp is not None:
        subProblem=MazeCollectMinimal((tmp[0],n.state[0],tmp[1],problem.vide))
        subNode=astar_graph_search(subProblem, problem.Heuristique)
        subNode=breadth_first_graph_search(subProblem)
        subPath=subNode.path()
        l=0
        subPath.reverse()
        for sub in subPath:
            if l>0:
                problem.printOneState(sub)
            l+=1
        number+=l-1
    if n.state[0] is "init":
        tmp=n.state[1]
        problem.printOneState(n)
    else:
        tmp=n.state
