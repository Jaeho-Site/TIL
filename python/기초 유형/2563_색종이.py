""" 
하나의 크기는 10x10이다.

1. 100*100 배열을 0으로 초기화
2. 새로 입력받는 색종이가 차지하는 좌표를 1로 설정
3. 값이 1인 좌표수세기

점 -> 9
점 -> 16
0,10
...
0,3
0,2
0,1
0,0 1,0 2,0 3,0... 10,0

"""
import sys
input = sys.stdin.readline
board=[[0]*100 for _ in range(100)]

n=int(input())
for _ in range(n):
    x,y=map(int,input().split())
    for i in range(x,x+10):
        for j in range(y,y+10):
            board[j][i]=1

answer=0
for i in range(100):
    for j in range(100):
        if board[j][i]==1:
            answer+=1

print(answer)    
