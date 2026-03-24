"""
7
0110100
0110101
1110101
0000111
0100000
0111110
0111000
3 7 8 9

1인 곳이 집이다.
"""
from collections import deque
n=int(input())
graph=[list(map(int,list(input().strip()))) for _ in range(n)]
visited=[[False]*n for _ in range(n)]

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
            
            if not(0<=nx<n and 0<=ny<n):
                continue
            if not visited[nx][ny] and graph[nx][ny]==1:
                visited[nx][ny]=True
                q.append((nx,ny))
    return size

area=[]
for i in range(n):
    for j in range(n):
        if not visited[i][j] and graph[i][j]==1:
            area.append(bfs(i,j))

print(len(area))
area.sort()
for size in area:
    print(size)