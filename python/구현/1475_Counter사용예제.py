""" 
6은 9를 뒤집어서 이용할 수 있고, 9는 6을 뒤집어서 이용할 수 있다.
필요한 세트의 개수의 최솟값
0 1 2 3 4 5 6 7 8 9 -> 이게 한세트임
"""
# 내 아이디어를 파이썬틱하게 변경
from collections import Counter

N = input().strip().replace('6', '9')
counts = Counter(N)
counts['9'] = (counts['9'] + 1) // 2
print(max(counts.values()))

# 내 풀이
import math
from collections import Counter
N=input()
N=N.replace('6','9')
nums=Counter(N).most_common(2)
if nums[0][0]=='9':
    target1=int(math.ceil(nums[0][1]/2))
    if len(nums)>1:
        target2=nums[1][1]
        print(max(target1,target2))
    else:
        print(target1)
else:
    print(nums[0][1])
    