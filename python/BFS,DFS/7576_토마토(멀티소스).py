"""
정수 1은 익은 토마토, 
정수 0은 익지 않은 토마토,
정수 -1은 토마토가 들어있지 않은 칸
6 4
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 1
저장된게 다 익어있으면 0, 다 못익으면 -1, 최소 날짜
멀티소스 문제임 -> 마지막에 검사할때 애초에 토마토가 있을수없었던
graph상 좌표가 -1인부분은 검사하면 안됨. 이거빼고 bfs로직은 맞았다.
"""
from collections import deque
m,n=map(int,input().split())
graph=[list(map(int,input().split())) for _ in range(n)]
dist = [[-1] * m for _ in range(n)]

dx,dy=[-1,1,0,0],[0,0,-1,1]
def bfs():
    q=deque()
    max_time=0
    for i in range(n):
        for j in range(m):
            if graph[i][j]==1:
                q.append((i,j))
                dist[i][j]=0
    while q:
        x,y=q.popleft()
        
        for i in range(4):
            nx,ny=x+dx[i],y+dy[i]
            
            if not(0<=nx<n and 0<=ny<m):
                continue
            if dist[nx][ny]==-1 and graph[nx][ny]!=-1:
                dist[nx][ny]=dist[x][y]+1
                max_time=max(max_time,dist[nx][ny])
                q.append((nx,ny))
    return max_time

# answer=bfs()

# is_end=True
# for i in range(n):
#     for j in range(m):
#         if dist[i][j]==-1:
#             is_end=False
# if is_end:
#     print(answer)
# else:
#     print(-1)
                
answer=bfs()

# BFS 이후 검사
for i in range(n):
    for j in range(m):
        if graph[i][j]==0 and dist[i][j]==-1:
            print(-1)
            exit()

print(answer)               