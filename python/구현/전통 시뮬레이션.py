"""
item_type = 1
grid = [
 [0,2,0],
 [1,0,3],
 [0,1,0]
]
빈칸은 0, 십자가는 1. X는 2, 별은 3 일 때 
새 아이템 하나 빈칸에 둘때 최대 값구하기
"""
# + : 상하좌우에 있으면   +1점 (최대 4점)
# X : 대각선 4방향       -1점 (최소 -4점)
# * : 8방향 중복없는 개수 +2점 (최대 6점)

# 내 풀이 -> 모든 0에 넣어보고 점수를 계산 (사실 N<=50이라 N^4해도 6백만이라 안전)
# 최적화 -> 사실 base_score를 구하고 새로운 아이템을 넣었을때
# 영향을 받는 칸만 다시 계산하면 된다.

def solution(item_type, grid):
    N,M=len(grid),len(grid[0])
    spots=[]
    for i in range(N):
        for j in range(M):
            if grid[i][j]==0: spots.append((i,j))
    
    answer=[]
    P_dx,P_dy=[-1,1,0,0],[0,0,-1,1]
    X_dx,X_dy=[-1,-1,1,1],[-1,1,-1,1]
    S_dx,S_dy=[-1,1,0,0,-1,-1,1,1],[0,0,-1,1,-1,1,-1,1]
    for spot in spots:
        grid[spot[0]][spot[1]]=item_type
        score=0
        
        for i in range(N):
            for j in range(M):
                if grid[i][j]==1:
                    for k in range(4):
                        nx,ny=i+P_dx[k],j+P_dy[k]
                        if not(0<=nx<N and 0<=ny<M):continue
                        if grid[nx][ny]!=0:
                            score+=1
                elif grid[i][j]==2:
                    for k in range(4):
                        nx,ny=i+X_dx[k],j+X_dy[k]
                        if not(0<=nx<N and 0<=ny<M):continue
                        if grid[nx][ny]!=0:
                            score-=1
                elif grid[i][j]==3:
                    cur_items=set()
                    for k in range(8):
                        nx,ny=i+S_dx[k],j+S_dy[k]
                        if not(0<=nx<N and 0<=ny<M):continue
                        if grid[nx][ny]!=0:
                            cur_items.add(grid[nx][ny])
                    score+=len(cur_items)*2
        answer.append(score)  
        grid[spot[0]][spot[1]]=0
    return max(answer)

item_type = 3
grid = [[1,2,0],[0,0,0],[3,1,2]]
print(solution(item_type,grid))
