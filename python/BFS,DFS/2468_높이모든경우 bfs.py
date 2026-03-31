import sys
from collections import deque
input=sys.stdin.readline

N=int(input())
Board=[list(map(int,input().split())) for _ in range(N)]
area=[]
_max=max([max(row) for row in Board])
_min=min([min(row) for row in Board])
dx,dy=[-1,1,0,0],[0,0,-1,1]

for height in range(_min-1,_max):
    visited=[[False]*N for _ in range(N)]
    
    # 높이에 따른 새로운 보드 설정
    board=[row[:] for row in Board]
    for i in range(N):
        for j in range(N):
            if board[i][j]<=height:
                board[i][j]=-1
    
    count=0
    for i in range(N):
        for j in range(N):
            if board[i][j]!=-1 and not visited[i][j]:
                # bfs
                q=deque([(i,j)])
                visited[i][j]=True     
                while q:
                    x,y=q.popleft()
                    for k in range(4):
                        nx,ny=x+dx[k],y+dy[k]
                        
                        if not (0<=nx<N and 0<=ny<N) or visited[nx][ny]:continue
                        
                        if board[nx][ny]!=-1:
                            visited[nx][ny]=True
                            q.append((nx,ny))
                count+=1
                
    area.append(count)
print(max(area))   