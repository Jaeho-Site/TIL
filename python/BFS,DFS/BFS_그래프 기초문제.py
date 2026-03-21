"""
연결된 컴포넌트 개수 세기
 N명의 학생이 있다. 학생들 사이의 친구 관계가 M개 주어진다.
 친구의 친구도 친구라고 할 때,
 이 학교에는 총 몇 개의 '친구 무리'가 있는지 구하는 문제
"""
from collections import deque
def bfs(start):
    q=deque([start])
    visited[start]=True
    
    while q:
        v=q.popleft()   
        for i in graph[v]:
            if not visited[i]:
                q.append(i)
                visited[i]=True
            
n,m=map(int,input().split())
graph=[[] for _ in range(n+1)]
visited=[False]*(n+1)
count=0

for _ in range(m):
    u,v=map(int,input().split())
    graph[u].append(v)
    graph[v].append(u)

for i in range(1,n+1):
    if not visited[i]:
        bfs(i)
        count+=1
        
print(count)