""" 
1. 처음엔 head와 tail을 기억하면서 만들었는데 머리와 꼬리의 방향과 상태를 기억해야했음
2. 그래서 그냥 뱀 몸통 자체를 deque에 넣고, [-1]이 haed, [0]은 tail로 두고
조건 보면서 popleft,append를 통해 뱀을 전진시킴
-----
***항상 보면 아이디어를 코드로 옮기기 까진 잘하는데 계속 디테일을 놓친다.
1. 문제를 잘 안읽는것 같다. -> 방향전환은 끝에 하라고 친절하게 했었다.
2. 코드가 길어지면 조건을 검사할때 어디서 해야할지를 감 못잡음
3. 디버깅을 잘 못함 (보드가 이상이 있는지 체크해봐야함)
------
다 풀고 코드 위치만 바꿔서 맞췄다.
- 변수명은 절대 사용했던것 다시 쓰지 말자.
- 지금처럼 주석으로 로직을 써두고 구현하면 잘 되는듯 -> 함정만 계속 생각

"""
import sys
from collections import deque
input=sys.stdin.readline

N=int(input().strip())
K=int(input().strip())
board=[[0]*(N+2) for _ in range(N+2)]
for i in range(N+2): board[i][0]=1; board[i][-1]=1; board[0][i]=1; board[-1][i]=1
direction=deque()
for _ in range(K):
    x,y=map(int,input().split())
    board[x][y]=2
L=int(input().strip())
for _ in range(L):
    X,C=input().split()
    direction.append((X,C))
"""
1. 한칸을 전진한다.
2. 벽이나 자기자신(지난곳은 벽으로만들기)을 만나면 게임오버
3. 이동칸에 사과가 있으면 꼬리안움직임(즉 꼬리가 1이됨)
4. 사과가 없으면 꼬리를 비워준다.(전칸)
---
뱀의 몸통과 방향을 넣을 deque를 하나 둔다. (몸통은 좌표 튜플이다.)
1. 뱀의 머리를 한칸 전진은 q에 append한다.
2. 사과를 만나면 뱀의 꼬리를 appendleft한다.
3. 사과가 없으면 popleft한다.

"""
dx,dy=[0,-1,0,1],[1,0,-1,0]# 우 상 좌 하
snake=deque([(1,1,0)])
board[1][1]=1
sec=0
while True:
    x,y,d=snake[-1][0],snake[-1][1],snake[-1][2]
    sec+=1
    
    nx,ny=x+dx[d],y+dy[d]
    if board[nx][ny]==1 : print(sec); break
    
    # 사과가 없으면 꼬리를 빼고, 0처리
    if board[nx][ny]!=2 :      
        tx,ty,td=snake.popleft()
        board[tx][ty]=0

    # 벽이 아니었으니 뱀머리로 한칸 전진
    snake.append((nx,ny,d))
    board[nx][ny]=1
    
    # 시간에 따른 방향 처리
    if direction and sec==int(direction[0][0]):
        if direction[0][1]=='L':
            d=(d+1)%4
        else:
            d=(d+3)%4
        snake[-1]=(nx,ny,d)
        direction.popleft()