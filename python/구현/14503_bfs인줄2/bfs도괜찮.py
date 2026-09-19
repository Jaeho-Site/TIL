""" 0은 빈칸이고 1은 벽이다.
bfs문제이긴 한데, 방향을 기억해야하는 bfs이다.
---
우선 내 코드는 2줄때문에 실패했고, 디버깅에 실패했다.
1. 주석처럼 회전과 후진의 로직을 미리정해두고 하다보니, 
후진시엔 방향을 바꾸지말고 후진만 했어햐했는데, 방향도 바꿔버렸다.
2. 3번 조건에서 보통 bfs처럼 nx,ny가 1(벽)을 만나면 continue했는데,
사실 후진했어햐 했다.
---
3. 애초에 이문제는 bfs로도 풀수있지만 시뮬레이션 문제이다. 
4. 하지만 이제 어느정도 비문학 지문같은 문제를 코드로 차례로 옮기는 능력은 향상되었다. 
"""
import sys
from collections import deque
input=sys.stdin.readline

N,M=map(int,input().split())
r,c,d=map(int,input().split()) 
room=[list(map(int,input().split())) for _ in range(N)]

is_finished=False
q=deque([(r,c)])
room[r][c]=2 # 현재 칸이 아직 청소되지 않은 경우, 현재 칸을 청소한다. (시작점) 
dx,dy=[-1,0,1,0],[0,1,0,-1] # 바라보는 방향 북동남서 // 회전:(n+3)%4, 후진:(n+2)%4
while q:
    x,y=q.popleft()
    # 이동 가능한 4칸중 0이 있는지 체크하기
    is_dirty=False
    for i in range(4):
        nx,ny=x+dx[i],y+dy[i]
        if not(0<=nx<N and 0<=ny<M) or room[nx][ny]==1:
            continue
        if room[nx][ny]==0:
            is_dirty=True
            
    # 2,3번 중에 뭐임? -> 각각 진행
    if is_dirty: # 3번 조건
        d=(d+3)%4 # 반시계 회전한다.
        nx,ny=x+dx[d],y+dy[d]
        if not(0<=nx<N and 0<=ny<M):
            continue
        if room[nx][ny]==0:
            q.append((nx,ny)) # 큐에 넣어서 1번으로 돌아간다. (전진)
            room[nx][ny]=2
        else:
            q.append((x,y)) # 방향만 바꾼다.
    else:
        nx,ny=x+dx[(d+2)%4],y+dy[(d+2)%4]
        if not(0<=nx<N and 0<=ny<M):
            continue
        if room[nx][ny]==1:
            is_finished=True
        q.append((nx,ny)) # 큐에 넣어서 1번으로 돌아간다. (후진)
    
    if is_finished:
        break
print(sum(row.count(2) for row in room))
