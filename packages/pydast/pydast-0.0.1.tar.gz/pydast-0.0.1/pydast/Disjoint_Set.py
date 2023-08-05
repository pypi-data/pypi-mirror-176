class Disjoint_Set:
    
    def __init__(self,arr=[]) -> None:
        self.__parent={}
        self.__rank={}
        self.__totcomponents=len(arr)
        for i in arr:
            self.__parent[i]=i
            self.__rank[i]=0

    def __len__(self):
        return self.__totcomponents

    def push(self,val):
        self.__parent[val]=val
        self.__rank[val]=0
        self.__totcomponents+=1

    def union(self,valA,valB):
        valA=self.find(valA)
        valB=self.find(valB)
        if valA==valB:
            return 
        if self.__rank[valA]<self.__rank[valB]:
            self.__parent[valA]=valB
        elif self.__rank[valB]<self.__rank[valA]:
            self.__parent[valB]=valA
        else:
            self.__parent[valB]=valA
            self.__rank[valA]+=1
        self.__totcomponents-=1

    def find(self,val):
        if self.__parent[val]==val:
            return val
        self.__parent[val]=self.find(self.__parent[val])
        return self.__parent[val]

    def areConnected(self,val1,val2):
        return self.find(val1)==self.find(val2)
