"""
처음에 한 생각은 
1. 키와 몸무게와 인덱스(순서)와 랭크를 하나의 배열로 묶고
2. 키를 1번키로, 몸무게를 2번키로 해서 정렬해서 랭크 갱신
이런 로직으로 했을때 테스트 케이스는 맞았음 -> 하지만 안되는케이스가 많음
##
결국 이문제의 핵심은 나보다 덩치큰 사람이 몇명이냐? -> 다 하나씩 찾아보는 브루트포스 문제임

"""
N=int(input())
man=[[i,*map(int,input().split()),0] for i in range(N)]

man.sort(key=lambda m:(m[1],m[2]),reverse=True)
man[0][3]=1
rank=1
man_count=1
for i in range(1,N):
    man_count+=1
    if man[i-1][1]>man[i][1] and man[i-1][2]>man[i][2]: # 전사람이 크면
        rank=man_count
        man[i][3]=rank
    else:
        man[i][3]=rank

man.sort(key=lambda m:m[0])
for m in man:
    print(m[3],end=' ')
    
##########################################아이디어 받고 해결
import sys
input=sys.stdin.readline
N=int(input().strip())
man=[[*map(int,input().split()),1] for _ in range(N)]

for i in range(N):
    for j in range(N):
        if man[i][0]<man[j][0] and man[i][1]<man[j][1]:
            man[i][2]+=1
for m in man:
    print(m[2],end=' ')  
    
########################################### 정답 풀이
import sys
input = sys.stdin.readline

N = int(input().strip())
man = [list(map(int, input().split())) for _ in range(N)]

for i in range(N):
    rank = 1
    for j in range(N):
        # 나(i)보다 상대방(j)의 몸무게와 키가 모두 크면 내 등수가 1씩 밀려남
        if man[i][0] < man[j][0] and man[i][1] < man[j][1]:
            rank += 1
    print(rank, end=' ')