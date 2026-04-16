"""
기존 가로수에 다른 가로수를 최소로 추가해서 동일 간격으로 만드려고함
1. 우선 간격들을 모두 구해서
2. 간격들의 최대 공약수의 간격 만큼씩 나무를 심으면됨.
3. 일단 일정 간격대로 나무를 다 심어버리고, cur(기존)이 나무가있다면 count를 빼면됨. 
"""
# 답은 맞았다. 근데 -> 저 마지막에 set으로 바꿔서 확인한다고 쳐도 오래걸림
# 그래서 저 for문을 안돌 방법이 필요 -> 처음 생각한대로 전체 가로등수-현재가로등수해야함.
import sys
import math
input=sys.stdin.readline
n=int(input().strip())

cur=[int(input().strip()) for _ in range(n)]
distance=[]
for i in range(n-1):
    distance.append(cur[i+1]-cur[i])
_gcd=math.gcd(*distance)

"""  
count=0
cur_set=set(cur)
for i in range(cur[0],cur[n-1],_gcd):
    if i in cur_set:
        continue
    count+=1   
print(count)
"""
total_lamps = ((cur[-1] - cur[0]) // _gcd) + 1
# 새로 심어야 하는 가로등 = 전체 가로등 수 - 현재 가로등 수
print(total_lamps - n)