import sys
from collections import deque
input=sys.stdin.readline

N=int(input().strip())
board=[list(input().strip()) for _ in range(N)]

""" 일반 사람과 적록색약일 경우를 출력
적록색약은 R과 G를 구분할 수없다.

"""
dx,dy=[-1,1,0,0],[0,0,-1,1]
def bfs(board):
    count=0
    visited=[[False]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if not visited[i][j]:
                target=board[i][j]
                q=deque([(i,j)])
                visited[i][j]=True
                
                while q:
                    x,y=q.popleft()
                    
                    for k in range(4):
                        nx,ny=x+dx[k],y+dy[k]
                        
                        if not(0<=nx<N and 0<=ny<N) or board[nx][ny]!=target:continue
                        if visited[nx][ny]: continue
                        
                        visited[nx][ny]=True
                        q.append((nx,ny))
                count+=1
    return count

# 일반 사람의 경우 
normal=bfs(board)
         
# 적록 색약인 사람의 경우 
same={'R','G'}
for i in range(N):
    for j in range(N):
        if board[i][j] in same:
            board[i][j]='K'
color=bfs(board)

print(normal,color)