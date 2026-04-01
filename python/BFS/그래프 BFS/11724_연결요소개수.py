"""
6 5
1 2
2 5
5 1
3 4
4 6

1-2-5-1

    6   
  3 4
무방향 그래프 이므로 양방향 그래프임. 각 노드별 연결 노드를 리스트로 그래프를 만들고,
방문하지 않은 노드에 한해서 dfs를 다시 돌리면, 몇개의 연결이 생기는지 풀수있다.
DFS문제이다. 
Dfs로 돌리면 재귀에러 처리 해야함 setrecursionlimit(10**6)
"""
import sys
sys.setrecursionlimit(10**6)
input=sys.stdin.readline

def dfs(v):
    visited[v]=True
    
    for next in graph[v]:
        if not visited[next]:
            dfs(next)

n,m=map(int,input().split())
graph = [[] for _ in range(n+1)]
visited=[False]*(n+1)
count=0

for _ in range(m): 
    u,v=map(int,input().split())
    graph[u].append(v)
    graph[v].append(u)

for i in range(1,n+1):
    if visited[i]:
        continue
    dfs(i)
    count+=1
    
print(count)   