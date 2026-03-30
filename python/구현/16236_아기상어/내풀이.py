"""
- 아기 상어의 크기는 2이고, 아기 상어는 1초에 상하좌우로 인접한 한 칸씩 이동
- 자신보다 큰 물고기 칸은 지나갈수없다. (같으면 지나갈수있다)
- 자신보다 작은 물고기만 먹을 수 있다.
- 물고기를 먹으면 크기가 1증가한다.

1. 더이상 물고기를 못먹는(이동못하면) 상황이면 종료
2. 먹을수있는 물고기가 1마리면 먹으러 이동
3. 먹을수있는 물고기가 1마리 이상이면 -> 가장 가까운 물고기
---

이 문제는 시작위치(9)를 0으로 초기화해주지않은 한줄때문에 상어의 크기가
9가 넘어가는 경우엔 틀렸다.
"""
from collections import deque
N=int(input())
board=[list(map(int,input().split())) for _ in range(N)]
for i in range(N):
    for j in range(N):
        if board[i][j]==9:
            start=(i,j)
            board[i][j] = 0 # 이걸 안해줘서...

dx,dy=[-1,1,0,0],[0,0,-1,1]
size=2
count=0
answer=0

# 계속 먹이를 찾는 과정의 반복 
while True:
    # 먹을수있는 가까운 먹이 찾기 (하나의 bfs사이클)
    dist = [[-1]*N for _ in range(N)]
    q=deque([start])
    dist[start[0]][start[1]]=0
    fish=[]
    
    # 그냥 다 찾아야할듯
    while q:
        x,y=q.popleft()
        
        for i in range(4):
            nx,ny=x+dx[i],y+dy[i]

            if not (0<=nx<N and 0<=ny<N): continue
            if board[nx][ny]>size or dist[nx][ny]!=-1: continue
            
            if board[nx][ny]<size and board[nx][ny]!=0: 
                # 먹이 위치 저장
                fish.append((nx,ny,dist[x][y]+1))
             
            dist[nx][ny]=dist[x][y]+1
            q.append((nx,ny))
    
    # bfs하나 돌았으니 이제 먹을수있는 먹이들 정보가 들어있을거다.
    
    # 1. 먹이가 비었으면 끝
    if not fish:
        print(answer)
        break
    else: # 먹이가 있으면 먹고, 
        fish.sort(key=lambda a:(a[2],a[0],a[1]))
        start=(fish[0][0],fish[0][1])
        answer+=fish[0][2]
        board[fish[0][0]][fish[0][1]]=0
        count+=1
        
        # 크기 계산
        if size==count:
            size+=1
            count=0

