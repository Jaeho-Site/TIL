"""
5 7 3
0 2 4 4
1 1 2 5
4 0 6 2
영역 개수, (각 넓이)
"""
from collections import deque
m,n,k=map(int,input().split())
visited=[[False]*n for _ in range(m)]
graph=[[0]*n for _ in range(m)]

for i in range(k):
    x1,y1,x2,y2=map(int,input().split())   
    for y in range(y1,y2):
        for x in range(x1,x2):
            graph[y][x]=1
            
dx,dy=[-1,1,0,0],[0,0,-1,1]

def bfs(x,y):
    q=deque([(x,y)])
    visited[x][y]=True
    size=0
    while q:
        x,y=q.popleft()
        size+=1
        
        for i in range(4):
            nx,ny=x+dx[i],y+dy[i]
            
            if not(0<=nx<m and 0<=ny<n):
                continue
            if not visited[nx][ny] and graph[nx][ny]!=1:
                q.append((nx,ny))
                visited[nx][ny]=True
    return size

area=[]
for i in range(m):
    for j in range(n):
        if not visited[i][j] and graph[i][j]!=1:
            area.append(bfs(i,j))
            
print(len(area))
area.sort()
print(*area)