import sys
from collections import deque
input=sys.stdin.readline

M,N,H=map(int,input().split())
board=[[list(map(int,input().split())) for _ in range(N)]for _ in range(H)]
"""
한가지만 보강하자면 시간배열을 만들필요없이 board값을 1->2->3으로 하면 될듯
원래 꼬일까봐 패스했는데 생각해보니 겹칠일이 없다.
35분안에 골드문제 해결..
"""

# 1인 곳의 좌표를 뽑기(토마토 있는곳)
tomato=deque()
for h in range(H):
    for i in range(N):
        for j in range(M):
            if board[h][i][j]==1:
                tomato.append((h,i,j))

dh,dx,dy=[1,-1,0,0,0,0],[0,0,1,-1,0,0],[0,0,0,0,-1,1]  # 위,아래,상,하,좌,우
time=[[[-1]*M for _ in range(N)] for _ in range(H)]

for t in tomato:
    time[t[0]][t[1]][t[2]]=0

# 방문처리는 토마토로 바꾸면서 1을 체크하면 된다.
while tomato:
    h,x,y=tomato.popleft()
    
    for i in range(6):
        nh,nx,ny=h+dh[i],x+dx[i],y+dy[i]
        
        if not(0<=nh<H and 0<=nx<N and 0<=ny<M):continue
        if board[nh][nx][ny]==1 or board[nh][nx][ny]==-1: continue
        
        if board[nh][nx][ny]==0:
            board[nh][nx][ny]=1
        
        tomato.append((nh,nx,ny))
        time[nh][nx][ny]=time[h][x][y]+1

for hh in range(H):
    for ii in range(N):
        for jj in range(M):
            if board[hh][ii][jj]==0:
                print(-1)
                sys.exit()
                
print(time[h][x][y])