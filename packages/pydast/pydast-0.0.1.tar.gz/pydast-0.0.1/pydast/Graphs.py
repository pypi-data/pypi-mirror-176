
# & ------------------------------------------------------------------------------------------------------------
# & ---------------------------------------- Undirected Graph --------------------------------------------------
# & ------------------------------------------------------------------------------------------------------------

# Unweighted Graph
# Attributes :     graph    
# Object Methods : path_exists      components
# Dunder Methods :
class unweighted_graph:

    # >-------------------------------------- Dunder Methods ---------------------------------------------------

    # constructor
    def __init__(self,Vertices=[],edges=[],undirected=False) -> None :

        self.graph={}
        self.undirected=undirected

        if isinstance(Vertices,int):
            for i in range(1,Vertices+1):
                self.graph[i]=[]
        elif isinstance(Vertices,list) or isinstance(Vertices,tuple):
            for i in Vertices:
                self.graph[i]=[]

        for i,j in edges:
            if i not in self.graph:
                self.graph[i]=[]
            self.graph[i].append(j)
        if undirected:
            if j not in self.graph:
                self.graph[j]=[]

    # Representation Method
    def __repr__(self) -> str:
        return self

    # String Method
    def __str__(self) -> str:
        s=""
        for i in self.graph:
            s+=str(i)+" : "+", ".join(self.graph[i])+"\n"
        s=s.rstrip("\n")
        return s
    
    # Operator Overloading
    def __iadd__(self,val) :
        if isinstance(val,int) or isinstance(val,str):
            self.graph[val]=[]
        elif isinstance(val,list) or isinstance(val,tuple):
            try:
                self.graph[val[0]].append(val[1])
                self.graph[val[1]].append(val[0])
            except:
                raise ValueError("Either or both of the Nodes doesn't exist")
        return self

    # >---------------------------------------- Object Methods -------------------------------------------------

    # check if a path exists from  source to destination
    def path_exists(self,source,destination) -> bool :
        s=[source]
        visited={}
        for i in self.graph:
            visited[i]=False
        visited[source]=True
        while len(s):
            curr=s.pop()
            if curr==destination:
                return True
            for j in self.graph[curr]:
                if not visited[j]:
                    visited[j]=True
                    s.append(j)
        return False

    def components(self) -> int :
        visited={}
        for i in self.graph:
            visited[i]=False
        islands=0
        for i in self.graph:
            if not visited[i]:
                s=[i]
                visited[i]=True
                while len(s):
                    curr=s.pop()
                    for j in self.graph[curr]:
                        if not visited[j]:
                            visited[j]=True
                            s.append(j)
                islands+=1
        return islands

    def shortestpath(self,source,destination) -> int :
        visited={}
        for i in self.graph:
            visited[i]=False
        q=[(source,0)]
        visited[source]=True
        while len(q):
            curr,dist=q.pop()
            if curr==destination:
                return dist
            for j in self.graph[curr]:
                if not visited[j]:
                    q.insert(0,(j,dist+1))
        return -1

    def mothernodes(self):
        if self.components>1:
            return []
        if self.undirected:
            return [i for i in self.graph]
        visited={}
        for i in self.graph:
            visited[i]=False
        
        for i in self.graph:
            if not visited[i]:
                v=i
                s=[i]
                visited[i]=True
                while len(s):
                    curr=s.pop()
                    for j in self.graph[curr]:
                        if not visited[j]:
                            s.append(j)
                    

    # >------------------------------------------- Utilites ----------------------------------------------------


# & ------------------------------------------------------------------------------------------------------------
# & ---------------------------------------- Undirected Graph --------------------------------------------------
# & ------------------------------------------------------------------------------------------------------------

# Weighted Graph
# Attributes :     vertices         adjacencylist     
# Object Methods : path_exists      count_islands
# Dunder Methods :

class weigted_graph:

    # >-------------------------------------- Dunder Methods ---------------------------------------------------

    def __init__(self,vertices=[],edges=[],undirected=False) -> None:
        self.undirected=undirected
        self.graph={}

    def addEdge(self,u,v,w):
        self.graph[u][v]=w

    def dijkstra(self,src):
        vertices=self.vertices

    def bellmanFord(self,src):
        mindist={i:-1 for i in self.vertices}
        mindist[src]=0

        for _ in range(len(self.vertices)-1):
            for u in self.graph:
                for v in self.graph[u]:
                    if mindist[u]+self.graph[u][v]<mindist[v]:
                        mindist[v]=mindist[u]+self.graph[u][v]
        
        for u in self.graph:
            for v in self.graph[u]:
                if mindist[u]+self.graph[u][v]<mindist[v]:
                    return None
        
        return mindist
                