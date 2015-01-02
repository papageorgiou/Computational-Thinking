
# coding: utf-8

## Provided Code

##### Node

# In[ ]:


class Node(object):
    '''Node'''
    def __init__(self, name):
        self.name = str(name)
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self): 
        return self.name.__hash__()


##### Edge

# In[ ]:

class Edge(object):
    '''Edge'''
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return '{0}->{1}'.format(self.src, self.dest)


##### Digraph

# In[125]:

class Digraph(object):
    """A directed graph"""    
    def __init__(self):
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node in self.nodes:
            # Even though self.nodes is a Set, we want to do this to make sure we
            # don't add a duplicate entry for the same node in the self.edges list.
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[str(k)]:
                res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]


## Problem 1 

##### WeightedEdge

# In[126]:

class WeightedEdge(Edge):   #  This code has been tested - OK
    def __init__(self, src, dest, totDist, outDist):
        Edge.__init__(self, src, dest)
        self.totDist=totDist
        self.outDist=outDist
    def getTotalDistance(self):
        return self.totDist
    def getOutdoorDistance(self):
        return self.outDist
    def __str__(self): 
        return Edge.__str__(self) + " ("   + str(self.totDist) +  ", "  +  str(self.outDist)  +  ")"  



##### WeightedDigraph

# In[158]:

class WeightedDigraph(Digraph):
    
    def __init__(self):
        self.nodes = set([])
        self.edges = {}

        
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        totDist=float(edge.getTotalDistance())
        outDist=float(edge.getOutdoorDistance()) 
        if not self.edges[src]:
            self.edges[src]=[]
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        
        self.edges[src].append([dest,(totDist, outDist)])

#     def addEdge(self, edge):
#         src = edge.getSource()
#         dest = edge.getDestination()
#         if not(src in self.nodes and dest in self.nodes):
#             raise ValueError('Node not in graph')
#         self.edges[src].append(edge)        
        
    def childrenOf(self,node):
        return [child[0] for child in self.edges[node]]
    

    def __str__(self):
        res = '' 
        for k in self.edges:
            for d in self.edges[k]:
                res = '{0}{1}->{2} ({3}, {4})\n'.format(res, k, d[0], float(d[1][0]),float(d[1][1]) ) 
        return res[:-1]        
    
        



##### Problem 2

# In[131]:

def load_map(mapFilename):
    """ Parses the map file and constructs a directed graph"""

    print "Loading map from file..."
    
    MapMIT=WeightedDigraph()
    dataFile=open(mapFilename, "r")

    for line in dataFile:
        s,d,t,o =line.split()
        
        s=Node(s)
        d=Node(d)
        sd=WeightedEdge(s,d,t,o)
        
        try:
            MapMIT.addNode(s)
        except ValueError:
            pass
        
        try:
            MapMIT.addNode(d)
        except ValueError:
            pass        
        
        try:
            MapMIT.addEdge(sd)
        except ValueError:
            pass
            
    dataFile.close()    
    return MapMIT


# In[162]:

#mitMap = load_map("mit_map.txt")


# In[157]:

#type(mitMap.childrenOf(Node(16))[1])


## Problem 3

##### bruteForceSearch

# In[168]:

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.
    """
    return DFS1(digraph, start, end, [], maxTotalDist, maxDistOutdoors)
    
    
    


##### whichShortest

# In[1]:

def whichShortest(digraph, list_of_paths, maxTotalDistance):
    '''Returns the shortest path found under the constraint of maximum total distance'''
#     pathDistDic={}
#     for path in list_of_paths:
#         counter=0
#         for i in range(len(path)-1):
#             counter+=findDist(digraph, list_of_paths[path][i], list_of_paths[path][i+1])
#         pathDistDic[path]=counter
#     best=min(pathDistDic.values())
#     if best<maxTotalDistance and best!=None:
#         return pathDistDic[best]
#     else: 
#         raise ValueError

    benchmark=1000
    for path in list_of_paths:
        counter=0
        for i in range(len(path)-1):
            counter+=findDist(digraph, path[i], path[i+1])
        if counter<benchmark and counter<maxTotalDistance:
            benchmark=counter
            best=path
    return best


##### outDisAdd

# In[136]:

def outDisAdd(digraph, path):
    '''return total outdoor distance of a specific path'''
    count=0
    for i in range(len(path)-1):
        count+=findDist(digraph, path[i], path[i+1])
    return count

def totDistAdd(digraph, path):
    '''return total distance of a specific path'''
    count=0
    for i in range(len(path)-1):
        count+=findDist(digraph, path[i], path[i+1])
    return count    
    
    
    


##### DFS1

# In[137]:

def DFS1(digraph, start, end, path, maxTotalDist, maxDistOutdoors):
    """Depth First Search simple algorithm"""
    listP=[]
    path = path + [start]
    #print 'Current dfs path:', printPath(path)
    if start == end:
        listP.append(path)
    for node in digraph.childrenOf(start):
        if node not in path: #avoid cycles
            newPath = DFS1(digraph,node,end,path, maxTotalDist, maxDistOutdoors)
            if newPath != None:
                if outDisAdd(digraph, newPath) <maxDistOutdoors:
                    listP.append(newPath)
    if listP==[]:
        raise ValueError
    else:
        return whichShortest(digraph, listP, maxTotalDist )        
    


##### findDist

# In[138]:

def findDist(digraph, src, dest):
    """finds the total distance between two nodes of an edge"""
    for i in digraph.edges[src]:
        if i[0]==str(dest):
            result=i[1][0]
            return  result
    


# In[139]:

#findDist(mitMap, 16, 8)


### Problem 4

##### directedDFS

# In[140]:

def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors
    """
    return DFShort(digraph, start, end, [], None, maxTotalDist, maxDistOutdoors)
    


##### DFShort

# In[141]:

def DFShort (digraph, start, end, path, shortest, maxTotalDist, maxDistOutdoors):
    path=path + [start]
    if start==end:
        return path
    for node in digraph.childrenOf(start):
        if node not in path: #avoid cycles
            if shortest==None or totDistAdd(digraph, path)<shortest:
                
                newPath = DFShort(digraph,node,end,path, shortest, maxTotalDist, maxDistOutdoors)
                if newPath != None: 
                    if outDisAdd(digraph, newPath)<maxDistOutdoors:
                        if TotDistAdd(digraph, newPath)<maxTotalDist:
                            shortest=totDistAdd(digraph, newPath)
                            
                            bestPath=newPath
    return bestPath
    


##### outDisAdd

# In[142]:

def outDisAdd(digraph, path):
    '''returns total outdoor distance of a specific path'''
    count=0
    for i in range(len(path)-1):
        count+=findDist(digraph, path[i], path[i+1])
    return count

def totDistAdd(digraph, path):
    '''returns total distance of a specific path'''
    count=0
    for i in range(len(path)-1):
        count+=findDist(digraph, path[i], path[i+1])
    return count    
        


# In[79]:

#mitMap.childrenOf(Node(32))


# In[ ]:

#     expectedPath1 = ['32', '56']
#     brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
#     dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)

