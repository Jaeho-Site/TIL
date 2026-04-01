"""
7
B001111
B000000
B000000
1100000
0000000
0000000
0000EEE
"""
import sys
from collections import deque
input = sys.stdin.readline

N=int(input())

board=[list(input().strip())for _ in range(N)]
visited=[[[False]*2 for _ in range(N)] for _ in range(N)]

# 중심점만 갖고 계산, 지금이 행배치인지 열배치인지 bool
Tree=[]
goal=[]
for i in range(N):
    for j in range(N):
        if board[i][j]=='B':
            Tree.append((i,j))
        elif board[i][j]=='E':
            goal.append((i,j))
            
is_cul = 1 if Tree[0][0]!=Tree[1][0] else 0 # 세로면 1이다.
goal_cul = 1 if goal!=goal else 0
center=Tree[1]

q=deque([(center[0],center[1],is_cul,0)])
visited[center[0]][center[1]][is_cul]=True

dx,dy=[-1,1,0,0],[0,0,-1,1]
rx,ry=[-1,1,0,0,-1,-1,1,1],[0,0,-1,1,-1,1,-1,1]
while q:
    t2_x,t2_y,cul,dist=q.popleft()
    if cul: t1_x,t1_y,t3_x,t3_y=t2_x-1,t2_y,t2_x+1,t2_y      # 세로면
    else: t1_x,t1_y,t3_x,t3_y=t2_x,t2_y-1,t2_x,t2_y+1        # 가로면
    
    if t2_x==goal[1][0] and t2_y==goal[1][1] and cul==goal_cul:
        print(dist)
        sys.exit()
    
    for i in range(4):
        nx_1,ny_1=t1_x+dx[i],t1_y+dy[i]
        nx_2,ny_2=t2_x+dx[i],t2_y+dy[i]
        nx_3,ny_3=t3_x+dx[i],t3_y+dy[i]

        if not(0<=nx_1<N and 0<=ny_1<N) or not(0<=nx_3<N and 0<=ny_3<N): continue    
        if visited[nx_2][ny_2][cul]:continue
        if (board[nx_1][ny_1]=='1' or board[nx_2][ny_2]=='1' 
            or board[nx_3][ny_3]=='1'): continue
        
        q.append((nx_2,ny_2,cul,dist+1))
        visited[nx_2][ny_2][cul]=True
        
    # 회전할 수 있으면 회전하기
    can_rotate=True
    for i in range(8):
        rnx,rny=t2_x+rx[i],t2_y+ry[i]
        if not (0<=rnx<N and 0<=rny<N):can_rotate=False; break
        if board[rnx][rny]=='1':can_rotate=False
    
    if can_rotate and not visited[t2_x][t2_y][abs(cul-1)]:
        q.append((t2_x,t2_y,abs(cul-1),dist+1))
        visited[t2_x][t2_y][abs(cul-1)]=True
        
print(0)