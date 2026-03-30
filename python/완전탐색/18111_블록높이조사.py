"""
최소 시간과 그 경우 땅의 높이를 출력 (시간이 같다면 더 높이가 높은 경우)
"""
# 정석 풀이 높이가 같은 블럭들을 묶어서 함께 계산
import sys
from collections import Counter
input=sys.stdin.readline
N,M,B=map(int,input().split())
board=[]
for _ in range(N):
    board.extend(map(int,input().split()))
    
counts=Counter(board)

answer=[]
count=(sum(board)+B)//(N*M)

for height in range(count+1): # 전체 높이별 걸리는 시간을 계산 
    time=0
    for target, count in counts.items():
        if target>height: # 조사 층보다 높으면 빼기
            time+=(target-height)*2*count
        else:
            time+=(height-target)*count
    answer.append((time,height))

answer.sort(key=lambda a:(a[0],-a[1]))
print(*answer[0])


# 처음 풀이
import sys
input=sys.stdin.readline
N,M,B=map(int,input().split())
board=[list(map(int,input().split())) for _ in range(N)]

answer=[]
count=min(256,int((sum((sum(row) for row in board))+B)/(N*M)))

for height in range(count+1): # 전체 높이별 걸리는 시간을 계산 
    time=0
    for row in board:
        for target in row:
            if target>height: # 조사 층보다 높으면 빼기
                time+=(target-height)*2
            else:
                time+=(height-target)
    answer.append((time,height))

answer.sort(key=lambda a:(a[0],-a[1]))
print(*answer[0])
