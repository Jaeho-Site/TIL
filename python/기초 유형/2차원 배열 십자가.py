import sys
input = sys.stdin.readline

# 2차원 리스트 입력 -> 처음엔 배열 선언, 초기화 복잡하게 했었음. -> 리스트 컴프리헨션
board = [list(map(int, input().split())) for _ in range(19)]
n=int(input())

for i in range(n):
    x, y = map(int,input().split())
    x-=1
    y-=1
    for j in range(19):
        # board[x][j] = int(not board[x][j])    # bool 성질 이용
        # board[x][j] = 1 - board[x][j]         # 1에서 빼서 수를 뒤집기 
        
        if board[x][j]==0:
            board[x][j]=1
        else :
            board[x][j]=0
    
        if board[j][y]==0:
            board[j][y]=1
        else :
            board[j][y]=0

for i in range(19):
    for j in range(19):
        print(board[i][j],end=' ')
    print()     