"""
1. 나보다 늦게 도착한 방문이 벽도 많이 부수고 왔다면 그 케이스는 절대
최단거리가 될 수 없다는 논리 적용
2. nx,ny로 다음 방문 정할때 큐에 넣지 말고 조건만족하면 early return
-> 근데 이것도 시간초과
-> 정답 보니까 다 pypy3로 제출한듯.
-> 극한으로 최적화한 코드보니까 70줄 넘어감 -> 솔직히 문제의도 벗어난다고 생각 
"""

from collections import deque
import sys
input=sys.stdin.readline
N,M,K=map(int,input().split())
board=[list(input().strip()) for _ in range(N)]

dx,dy=[-1,1,0,0],[0,0,-1,1]
visited = [[K + 1] * M for _ in range(N)]
q=deque([(0,0,0,1)])
visited[0][0]=0

while q:
    x,y,broken,dist=q.popleft()
    
    if x==N-1 and y==M-1:
        print(dist)
        sys.exit()
    
    for i in range(4):
        nx,ny=x+dx[i],y+dy[i]
        
        if not (0<=nx<N and 0<=ny<M) : continue
        
        if nx==N-1 and ny==M-1:
            print(dist+1)
            sys.exit()
            
        if board[nx][ny]=='0':
            if broken<visited[nx][ny]:
                visited[nx][ny]=broken
                q.append((nx,ny,broken,dist+1))
        
        if board[nx][ny]=='1':
            if broken<K and broken+1<visited[nx][ny]:
                visited[nx][ny]=broken+1
                q.append((nx,ny,broken+1,dist+1))
            
print(-1)   