""" 
5
3 4
1 1
1 -1
2 2
3 3
튜플로 묶어서 정렬조건을 2개 쓰는 문제 
"""
import sys
input=sys.stdin.readline
n=int(input())
answer=[]
for _ in range(n):
    a,b=map(int,input().split())
    answer.append((a,b))
answer.sort(key=lambda dt: (dt[0],dt[1]))

for x,y in answer:
    print(x,y)