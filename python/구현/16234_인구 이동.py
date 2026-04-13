import sys
from collections import deque
input=sys.stdin.readline

N,L,R=map(int,input().split())
board=[list(map(int,input().split())) for _ in range(N)]
dx,dy=[-1,1,0,0],[0,0,-1,1]
day=0

while True:
    q=deque()
    visited=[[False]*N for _ in range(N)]
    is_move=False
    
    for i in range(N):
        for j in range(N):
            if not visited[i][j]:
                # bfs 돌아서 찾은 영역 좌표구하기
                q.append((i,j,board[i][j]))
                visited[i][j]=True
                union=[(i,j)]
                cur_sum=board[i][j]
                
                while q:
                    x,y,target=q.popleft()
                    
                    for k in range(4):
                        nx,ny=x+dx[k],y+dy[k]
                        
                        if not(0<=nx<N and 0<=ny<N) or visited[nx][ny]:continue
                        
                        if L<=abs(target-board[nx][ny])<=R:
                            union.append((nx,ny))
                            visited[nx][ny]=True
                            q.append((nx,ny,board[nx][ny]))
                            cur_sum+=board[nx][ny]
                
                # 구한 좌표들 계산, 업데이트
                if len(union)>1:
                    is_move=True
                    cur=cur_sum//len(union)
                    for u in union:
                        board[u[0]][u[1]]=cur
                
    # 이동이 없다면 출력
    if not is_move:
        print(day)
        break

    day+=1