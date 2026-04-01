import sys
from collections import deque
input=sys.stdin.readline

K=int(input())
W,H=map(int,input().split())
board=[input().split() for _ in range(H)]
visited=[[[False]*(K+1) for _ in range(W)] for _ in range(H)]

if W == 1 and H == 1:
    print(0)
    sys.exit()
    
q=deque([(0,0,0,0)]) # (0,0)시작, 0번 나이트 이동, 거리0
visited[0][0][0]=0

dx,dy=[-1,1,0,0,-2,-2,-1,-1,1,1,2,2],[0,0,-1,1,-1,1,-2,2,-2,2,-1,1]

while q:
    x,y,horse,dist=q.popleft()
    
    if horse>=K: count=4
    else: count=12
    
    for i in range(count):
        nx,ny=x+dx[i],y+dy[i]
        
        if not(0<=nx<H and 0<=ny<W) or board[nx][ny]=='1':continue
        
        # 종료 조건
        if nx==H-1 and ny==W-1: print(dist+1); sys.exit()
        
        # 큐에 넣고, visited의 horse값을 업데이트하기
        next_horse= horse if i<4 else horse+1
        
        if not visited[nx][ny][next_horse]:
            q.append((nx,ny,next_horse,dist+1))
            visited[nx][ny][next_horse]=True
        
print(-1)