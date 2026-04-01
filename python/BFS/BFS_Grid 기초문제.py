"""
4 4
1011
1110
0101
1111
"""
from collections import deque
dx=[-1,1,0,0]
dy=[0,0,-1,1]

def bfs(x,y):
    q=deque([(x,y)])
    visited[x][y]=True
    dist[x][y]=1
    
    while q:
        x,y=q.popleft()
        
        if x==n-1 and y==m-1:
            return dist[x][y]
        
        for i in range(4):
            nx=x+dx[i]
            ny=y+dy[i]
            
            if not(0<=nx<n and 0<=ny<m):
                continue
            if visited[nx][ny] or graph[nx][ny]==0:
                continue
            
            visited[nx][ny]=True
            dist[nx][ny]=dist[x][y]+1
            q.append((nx,ny))
                   
n,m=map(int,input().split())
graph=[list(map(int,input().strip())) for _ in range(n)]
visited=[[False]*(m) for _ in range(n)]
dist=[[0]*m for _ in range(n)]

print(bfs(0,0))
