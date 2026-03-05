"""
문자열 슬라이싱을 어디까지 잘 알고있나를 검증하는 문제이다.

구현 과정 : 집합을 생각했지만, 문자열 슬라이싱과 타겟 문자열을 비교하면 되겠다고 생각하고 작성하다가 막힘

"""

# 정답 코드
import sys
input = sys.stdin.readline

n = int(input())
nums = [input().strip() for _ in range(n)]
length = len(nums[0])

# k를 1부터 전체 길이까지 늘려가며 확인
for k in range(1, length + 1):
    # 뒤에서 k자리만큼 자른 번호들을 저장할 집합
    sliced_numbers = set()
    
    for i in range(n):
        # 뒤에서 k번째부터 끝까지 슬라이싱
        suffix = nums[i][-k:]
        sliced_numbers.add(suffix)
    
    # 집합의 크기가 n과 같다면 모두 중복되지 않는다는 의미
    if len(sliced_numbers) == n:
        print(k)
        break

############ 내 코드 ############
import sys

n=int(input())
nums=[input() for _ in range(n)]
last=nums.pop()
l=len(last)
#print(l)
for i in range(l,0,-1):
    target=last[:i]
    #print(target)
    for idx in range(len(nums)):
        if target==nums[idx]:
            print(l-i)
            sys.exit()
        else:
            nums[idx] = nums[idx][1:] 