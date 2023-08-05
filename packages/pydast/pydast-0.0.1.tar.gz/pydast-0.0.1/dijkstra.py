import sys,os
import time
from xml.dom import minidom
if not os.environ.get('ONLINE_JUDGE'):
    sys.stdin=open('in.txt','r')
    sys.stdout=open('out.txt','w')
start_time=time.time()

from heapq import *

n=int(input())
vertices=set(i for i in range(1,n+1))
m=int(input())
edges=[list(map(int,input().split())) for i in range(m)]
src=int(input())

def vertex(n): return n-1

# Building Graph
graph={}
for i in range(1,n+1):
    graph[i]={}
for u,v,w in edges:
    if v in graph[u]: graph[u][v]=graph[v][u]=min(graph[u][v],w)
    else: graph[u][v]=graph[v][u]=w

def dijsktra(src):
    if src not in vertices:
        raise ValueError("Source Node not present in Graph")

    mindist={i:float('inf') for i in range(1,n+1)}
    mindist[src]=0

    heap=[[0,src]]
    while len(heap):
        dist,u=heappop(heap)
        for v in graph[u]:
            w=graph[v][u]
            if dist+w<mindist[v]: 
                mindist[v]=dist+w
                heappush(heap,[mindist[v],v])

    return mindist

print("Result : ")
mindist=dijsktra(src)
res=[]
for i in range(1,n+1):
    if i==src: continue
    if i in mindist:
        res.append(mindist[i])
    else: res.append(-1)

print(*res)


print(f'\n\n--------------- took {time.time()-start_time} ms to run --------------')


# def shortestReach(n, edges, s):
#     graph={}
#     for i in range(1,n+1): graph[i]={}
#     for u,v,w in edges:
#         graph[u][v]=graph[v][u]=w
    
#     mindist={}
#     heap=[[0,s]]
#     while len(heap):
#         dist,curr=hq.heappop(heap)
#         if curr not in mindist or dist<mindist[curr]:
#             mindist[curr]=dist
#             for v in graph[curr]:
#                 hq.heappush(heap,[dist+graph[curr][v],v])
    
#     res=[]
#     for i in range(1,n+1):
#         if i==s: continue
#         if i in mindist:
#             res.append(mindist[i])
#         else: 
#             res.append(-1)
#     return res