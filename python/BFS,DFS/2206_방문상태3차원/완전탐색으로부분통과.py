import sys
from collections import deque
input=sys.stdin.readline

N,M=map(int,input().split())
Board=[list(map(int,list(input().strip()))) for _ in range(N)]
walls=deque()
dx,dy=[-1,1,0,0],[0,0,-1,1]

for i in range(N):
    for j in range(M):
        if Board[i][j]==1:
            walls.append((i,j))

if (N*M-len(walls))<N+M-1:
    print(-1)
    sys.exit()

answer=[]
while walls:
    wall_x,wall_y=walls.popleft()
    board=[row[:] for row in Board]
    board[wall_x][wall_y]=0
    board[0][0]=2
    
    # 벽 하나를 부쉈다. 이제 bfs
    q=deque([(0,0)])
    
    while q:
        x,y=q.popleft()
        
        for k in range(4):
            nx,ny=x+dx[k],y+dy[k]
            
            if not(0<=nx<N and 0<=ny<M) or board[nx][ny]!=0 : continue
            
            board[nx][ny]=board[x][y]+1
            q.append((nx,ny))
        
    if board[N-1][M-1]!=0:
        answer.append(board[N-1][M-1]-1)

if answer:
    print(min(answer))
else:
    print(-1)