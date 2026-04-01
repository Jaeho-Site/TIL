"""
6 4 2
0100
1110
1000
0000
0111
0000
시간이 4400만정도 나와서 시간아웃
"""
from collections import deque
import sys
input=sys.stdin.readline
N,M,K=map(int,input().split())
board=[list(input().strip()) for _ in range(N)]

dx,dy=[-1,1,0,0],[0,0,-1,1]
visited=[[[False]*(K+1) for _ in range(M)] for _ in range(N)]
q=deque([(0,0,0,1)])
visited[0][0][0]=True

while q:
    x,y,broken,dist=q.popleft()
    
    for i in range(4):
        nx,ny=x+dx[i],y+dy[i]
        
        if not (0<=nx<N and 0<=ny<M) : continue
        
        if nx==N-1 and ny==M-1:
            print(dist+1)
            sys.exit()
        
        # 빈칸이면 전진한다.
        if board[nx][ny]=='0' and not visited[nx][ny][broken]:
            # 만약 같은칸인데 벽을 더 많이 부순상태면 큐에 넣지 않는다.
            q.append((nx,ny,broken,dist+1))
            visited[nx][ny][broken]=True

        # 벽인데 회수 안넘으면 뚫고 지나간다.
        elif board[nx][ny]=='1' and broken<K and not visited[nx][ny][broken+1]:
            q.append((nx,ny,broken+1,dist+1))
            visited[nx][ny][broken+1]=True
            
print(-1)   