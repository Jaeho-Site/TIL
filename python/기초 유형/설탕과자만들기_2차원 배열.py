# -> 방향 벡터로도 생각해볼 수 있다.
"""
dr = [0, 1] # Row(행) 변화량
dc = [1, 0] # Col(열) 변화량

for i in range(l):
    nx = x + dr[d] * i
    ny = y + dc[d] * i
    
    if 0 <= nx < h and 0 <= ny < w: # 범위 체크
        board[nx][ny] = 1        
"""
import sys
input=sys.stdin.readline

h,w=map(int,input().split())
n=int(input())

board=[[0]*w for _ in range(h)]

for i in range(n):
    l, d, x, y = map(int,input().split())
    x-=1
    y-=1
    if d==0:
        for j in range(l):
            if y+j>=w:
                break
            board[x][y+j]=1
    else :
        for j in range(l):
            if x+j>=h:
                break
            board[x+j][y]=1
            
for i in range(h):
    for j in range(w):
        print(board[i][j],end=' ')
    print()
    
