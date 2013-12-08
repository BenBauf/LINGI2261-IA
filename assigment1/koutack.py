'''NAMES OF THE AUTHOR(S): Baufays Benoit - Colmonts Julien'''

from search import *


######################  Implement the search #######################

class Koutack(Problem):
    action=('init','gagne','merge','rien')
    def __init__(self,init):
        self.createMap(init)
        self.nodeExplored=0
        pass

    
    def goal_test(self, state):
        #if we have a size of 1 for state, we have only one case occuped so we have reached the goal
        if len(state)==1:
            return True
        else:
            return False

        
    def successor(self, state):
        if state[0]==self.action[0]:
            return self.successorInit(state)
        else:
            return self.getSuccessor(state)

    def getSuccessor(self, mapJeu):
        states=[]
        
        for choice in mapJeu:
            states.extend(self.ia(choice,mapJeu))
        self.nodeExplored+=1
        return tuple(states)

    
    #the state's format is different when you init the model (it's because, after one run, we save in the node the action)
    def successorInit(self, state):
        mapJeu=state[1]
        mapJeu=mapJeu[0:len(mapJeu)-1]

        return self.getSuccessor(mapJeu)
        

    #read the file, create the map and code it for the state schema
    def createMap(self,path):
        sizeY=0
        x=0
        y=-1
        mapInfo=[]
        f = open(path,'r')
        for line in f:
            y=y+1            
            sizeY=sizeY+1
            x=-1
            for elem in line.split(' '):
                x=x+1
                if(elem!= '.' and elem != '.\n'):
                    mapInfo.append((x,y,elem.replace('\n', '')))
        mapInfo.append((x+1,sizeY))
        self.initial=('init',tuple(mapInfo))

    #ia method
    def ia(self,choice,mapJeu):
        states=[]
        #a position can  merge with is vertical friend
        for a in [-1,1]:
            for b in [-1,1]:
                possibilite=(choice[0]+a,choice[1]+b)
                #the new position is occuped by something ?
                value=self.isOccuped(mapJeu, possibilite)
                if value!='none' and value!='outofbound':
                    possibilite=(possibilite[0],possibilite[1],value)
                    #where can you merge ?
                    if(self.isOccuped(mapJeu, (choice[0]+a,choice[1]))=='none'):
                        newMap=list(mapJeu)                        
                        newMap.remove(possibilite)
                        newMap.remove(choice)
                        #is just one choice
                        newCase=(choice[0]+a,choice[1],self.putall(value,choice))
                        states.append(('move',tuple(self.getFriends(newCase,newMap,newCase[2]) )))
                    if(self.isOccuped(mapJeu, (choice[0],choice[1]+b))=='none'):
                        newMap=list(mapJeu)
                        newMap.remove(possibilite)
                        newMap.remove(choice)

                        newCase=(choice[0],choice[1]+b,self.putall(value,choice))
                        states.append(('move',tuple(self.getFriends(newCase,newMap,newCase[2]) )))
        #a position can also merge with a  friend 2 ligne
        for a in [(-2,0),(0,-2),(2,0),(0,-2)]:            
            possibiliteA=(choice[0]+a[0],choice[1]+a[1])
            valueA=self.isOccuped(mapJeu, possibiliteA)
            if valueA!='none' and valueA!='outofbound':
               #where can you merge ?
               if(self.isOccuped(mapJeu, (choice[0]+(a[0]/2),choice[1]+(a[1]/2)))=='none'):
                   newMap=list(mapJeu)
                   possibiliteA=(possibiliteA[0],possibiliteA[1],valueA)
                   newMap.remove(possibiliteA)
                   newMap.remove(choice)
                   newCordoX=round(choice[0]+(a[0]/2))
                   newCordoY=round(choice[1]+(a[1]/2))
                   newCase=(newCordoX,newCordoY,self.putall(valueA,choice))
                   states.append(('move',tuple(self.getFriends(newCase,newMap,newCase[2]) )))     
        if len(states)==0:
            #('nothing to do',mapJeu)
            return []
        return states

    #quand o na trouve un nouveau mouvement, o nregardes si d'autres cases adjacentes contiennent des elements afin de les empiler.
    def getFriends(self, position, mapJeu,values):
        valueL=list()
        for value in values:
            valueL.extend(list(value))
        for a in [(-1,0),(0,1),(1,0),(0,-1)]:
                possibilite=(position[0]+a[0],position[1]+a[1])
                value=self.isOccuped(mapJeu, possibilite)
                if value!='none' and value!='outofbound':
                    possibilite=(possibilite[0],possibilite[1],value)
                    mapJeu.remove(possibilite)
                    valueL.extend(value)
        valueL.sort()
        newCase=(position[0],position[1],tuple(valueL))
        mapJeu.append(newCase)
        return mapJeu
                    
                    
    def putall(self,value,choice):
        newV=list()
        for val in value:
            newV.extend(list(val))
        for val in choice[2]:
            newV.extend(list(val))  
        
        valueL=newV

        valueL.sort()
        return tuple(valueL)
    
    #test if possibilite is occuped in mapJeu.  Si c'est le cas, il renvoit la valeur presente dans la case
    def isOccuped(self,mapJeu, possibilite):
        #pas chercher si pas dans le cadre
        if possibilite[0]<0 or possibilite[1]<0:
            return 'outofbound'
        for position in mapJeu:
            if possibilite[0]==position[0]and possibilite[1]==position[1]:
                return position[2]
        return 'none'

    
                
        





###################### Launch the search #########################
        
problem=Koutack(sys.argv[1])
#example of bfs search
if len(sys.argv)>2:
	searchType = int (sys.argv[2])
else:
	searchType = 1
if searchType == 1:
	node=breadth_first_graph_search(problem)
elif searchType == 2:
	node=depth_first_graph_search(problem)
if searchType == 3:
	node=breadth_first_tree_search(problem)
elif searchType == 4:
	node=depth_first_tree_search(problem)

#example of print
path=node.path()
path.reverse()
sizeElements=len(path[0].state[1])
size=path[0].state[1][sizeElements-1]
for n in path:
    a=[' . ' ] * size[1]
    for i in range(0,size[1]):
        a[i]=['.'] * size[0]
    state=n.state
    if(state[0]=="init"):
        state=state[1]
    for elem in state:
        if len(elem)==3:
            a[elem[1]][elem[0]]=elem[2]
    for ligne in a:
        ligneP=""
        #print(ligne)
        for elem in ligne:
            if elem!='.':
                if len(elem)>1:
                    listE=list(elem)
                    elemStr=str(listE)[1:-1]
                    elemStr=elemStr.replace('\'','')
                    elemStr=elemStr.replace(' ','')
                    ligneP=ligneP+"["+elemStr+"] "
                else:
                    ligneP=ligneP+elem+" "
            else:
                
                ligneP=ligneP+'. '
        print(ligneP)
    print('')
#print('nodes to solution :' + str (len(path)-1) + ' nodes explored :'+ str (problem.nodeExplored))
