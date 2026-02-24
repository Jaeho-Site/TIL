# 풀이에 대한 해석
"""
'미리 쳐다보고 이동(Look-ahead)' 하는 방식이라 if-elif 구조가 복잡하다
-> 일단 현재 위치를 칠하고 -> 그 다음 어디로 갈지 정하는(Current & Next)" 패턴으로 바꾸면 깔끔하다.

정답코드는 개미_2차원배열_정답.py
"""

import sys
input = sys.stdin.readline

board=[list(map(int,input().split())) for _ in range(10)]
x = 1
y = 1
board[1][1]=9
while True:
    if x==8 and y==8 : 
        break 
    if board[x][y+1] == 0:
        y+=1
        board[x][y]=9
    elif board[x][y+1]==2:
        y+=1
        board[x][y]=9
        break
    else :
        if board[x+1][y] == 0:
            x+=1
            board[x][y]=9
        elif board[x+1][y]==2:
            x+=1
            board[x][y]=9
            break
        else :
            break

for i in range(10):
    for j in range(10):
        print(board[i][j],end=' ')
    print()