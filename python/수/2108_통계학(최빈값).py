"""
최빈값 : Counter사용
빈도수가 같다면 가장 처음 마주친것을 앞에두기때문에
nums를 미리 정렬한게 포인트
"""
import sys
from collections import Counter
input=sys.stdin.readline
N=int(input())

nums=[int(input())for _ in range(N)]
nums.sort()
# 평균
print(round(sum(nums)/N))
# 중앙값
print(nums[N//2])
# 최빈값
if N==1:
    print(nums[0])
else:
    my_dict=Counter(nums).most_common(2)
    if my_dict[0][1]==my_dict[1][1]:
        print(my_dict[1][0])
    else:
        print(my_dict[0][0])
# 범위
print(nums[-1]-nums[0])