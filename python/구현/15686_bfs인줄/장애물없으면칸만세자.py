"""

"""
import sys
from collections import deque
from itertools import combinations as cb
input=sys.stdin.readline
N,M=map(int,input().split())
city=[list(map(int,input().split())) for _ in range(N)]

# 치킨집을 선택하는 모든 경우에서
chicken,house=[],[]
for i in range(N):
    for j in range(N):
        if city[i][j]==2:
            chicken.append((i,j))
        if city[i][j]==1:
            house.append((i,j))

answer=N**3
for open in cb(chicken,M):
    board=[row[:] for row in city]
    for c in chicken:
        if c not in open:
            board[c[0]][c[1]]=0
    # bfs돌면서 가장 가까운 치킨거리 구하기
    distance=0
    dx,dy=[-1,1,0,0],[0,0,-1,1]
    for h in house: 
        q=deque([h])
        visited=[[False]*N for _ in range(N)]
        visited[h[0]][h[1]]=True
        board[h[0]][h[1]]=3
        while q:
            x,y=q.popleft() 
            for i in range(4):
                nx,ny=x+dx[i],y+dy[i]           
                if not(0<=nx<N and 0<=ny<N) : continue 
                if visited[nx][ny] : continue 
                
                visited[nx][ny]=True
                q.append((nx,ny))
                
                if board[nx][ny]==2:
                    q=deque()
                    distance+=board[x][y]-2
                    break
                board[nx][ny]=board[x][y]+1    
                
    answer=min(answer,distance) 
print(answer)    
        