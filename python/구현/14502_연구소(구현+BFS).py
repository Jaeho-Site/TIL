""" (3 ≤ N, M ≤ 8)
0은 빈 칸, 1은 벽, 2는 바이러스
바이러스는 모든 빈 칸으로 퍼져나갈 수 있다.
---
벽을 3개 세운 뒤, 바이러스가 퍼질 수 없는 곳을 안전 영역 크기의 최댓값
벽을 3개 세우는 모든 경우 41664
---
우선 모든 '0'중에 3개를 뽑아야 한다는건 인지했음. 근데 어떻게 뽑지?
를 생각못함. 
1. 즉 좌표 튜플을 뽑는다는 생각을 하지 못해서 아이디어 확인했고,
2. BFS 디버깅 못해서 다시 확인했음 -> visited체크를 안함
---
정석풀이 체크포인트 
1. 바이러스가 있는 위치인 '2'도 같이 넣고 돌리기
2. visited를 사용하지 않았다.
3. counts배열 대신 변수 하나로 최대값 갱신

"""
import sys
from itertools import combinations as cb
from collections import deque
input=sys.stdin.readline

N,M=map(int,input().split())
_board=[list(input().split()) for _ in range(N)]

# 일단 벽을 세우는 모든 경우를 조사
empty=[]
for i in range(N):
    for j in range(M):
        if _board[i][j]=='0':
            empty.append((i,j))

# 그 모든 경우에서 bfs돌리고 count
dx=[-1,1,0,0]
dy=[0,0,-1,1]       
def bfs(x,y):
    q=deque([(x,y)])
    visited[x][y]=True
    while q:
        x,y=q.popleft()
        
        for i in range(4):
            nx,ny=x+dx[i],y+dy[i]
            
            if not(0<=nx<N and 0<=ny<M) or board[nx][ny]=='1' or visited[nx][ny]:
                continue   
                     
            visited[nx][ny]=True
            q.append((nx,ny))
            board[nx][ny]='2'
            
counts=[]           
for walls in cb(empty,3): # ((2,1),(1,2),(4,6))
    board=[row[:] for row in _board]
    (r1, c1), (r2, c2), (r3, c3) = walls
    board[r1][c1],board[r2][c2],board[r3][c3] = '1','1','1'
    visited=[[False]*M for _ in range(N)]
    
    for i in range(N):
        for j in range(M):
            if board[i][j]=='2' and not visited[i][j]:
                bfs(i,j)                        
    counts.append(sum(row.count('0') for row in board))
print(max(counts))


############################### 정석 풀이 #####################3########33
import sys
from itertools import combinations as cb
from collections import deque
input = sys.stdin.readline

N, M = map(int, input().split())
_board = [list(input().split()) for _ in range(N)]

# 1. 빈 칸과 바이러스 위치를 처음에 모두 모아둡니다.
empty = []
viruses = []
for i in range(N):
    for j in range(M):
        if _board[i][j] == '0':
            empty.append((i, j))
        elif _board[i][j] == '2':
            viruses.append((i, j))

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

answer = 0 # 최댓값을 저장할 변수

for walls in cb(empty, 3):
    # 맵 복사 및 벽 3개 세우기
    board = [row[:] for row in _board]
    for r, c in walls:
        board[r][c] = '1'
    
    # 2. 바이러스 위치를 한꺼번에 큐에 넣고 다중 출발원 BFS 실행
    q = deque(viruses)
    
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            # 범위 안이고 빈 칸이면 바이러스 전염
            if 0 <= nx < N and 0 <= ny < M and board[nx][ny] == '0':
                board[nx][ny] = '2'
                q.append((nx, ny))
                
    # 안전 영역 계산 및 최댓값 갱신
    safe_zone = sum(row.count('0') for row in board)
    if safe_zone > answer:
        answer = safe_zone

print(answer)