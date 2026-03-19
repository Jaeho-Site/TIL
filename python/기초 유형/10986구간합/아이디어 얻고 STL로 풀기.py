######################세번째 풀었을때####################
import sys
from collections import Counter
import math
input=sys.stdin.readline
n,m=map(int,input().split())
nums=list(map(int,input().split()))

d=[] 
temp=0
for num in nums:
    temp=temp+num
    d.append(temp%m)

answer=0
for key, count in Counter(d).items():
    if key==0:
        answer+=count
        if count>1:
            answer+=math.comb(count,2)
    else:
        if count<2:
            continue
        else:
            answer+=math.comb(count,2)
print(answer)