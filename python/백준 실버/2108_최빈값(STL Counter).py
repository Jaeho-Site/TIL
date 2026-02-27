"""
N은 홀수이다. 
산술평균 : N개의 수들의 합을 N으로 나눈 값                            -> 소수점 이하 첫째 자리에서 반올림
중앙값 : N개의 수들을 증가하는 순서로 나열했을 경우 그 중앙에 위치하는 값
최빈값 : N개의 수들 중 가장 많이 나타나는 값                          -> 여러 개 있을 때에는 최빈값 중 두 번째로 작은 값을 출력
범위 : N개의 수들 중 최댓값과 최솟값의 차이

5           2
1           2
3           1
8           10
-2
2
"""
import sys
from collections import Counter
input=sys.stdin.readline

n=int(input())
num=[]

for _ in range(n):
    num.append(int(input().rstrip()))
    
num.sort()
print(round(sum(num)/n))
print(num[n//2])
counts=Counter(num).most_common()
if len(counts) > 1 and counts[0][1] == counts[1][1]:
    print(counts[1][0])
else:
    print(counts[0][0])
print(max(num)-min(num))
   