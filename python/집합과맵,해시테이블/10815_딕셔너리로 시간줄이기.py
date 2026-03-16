""" 
5
6 3 2 10 -10 : nums
8
10 9 -5 2 3 4 5 -10 : cards
1. cards가 nums에 있으면 출력 이런식으로 구현하니 시간초과
2. 딕셔너리에 cards와 nums를 모두 저장하고 m의 길이 만큼만 추출력한다.
"""
# 정답 풀이 1 : 집합 (set) 사용
import sys
input = sys.stdin.readline
n = int(input())
nums = set(map(int, input().split())) 
m = int(input())
cards = list(map(int, input().split()))

# 검사해야 할 카드들을 하나씩 확인합니다. set의 탐색 O(1)
for card in cards:
    if card in nums:
        print(1, end=' ')
    else:
        print(0, end=' ')

#################### 내 풀이 ######################
import sys
input=sys.stdin.readline
n = int(input())
nums=list(map(int,input().split()))
m = int(input())
cards=list(map(int,input().split()))
d={}
for card in cards:
    d[card]=0
for num in nums:
    d[num]=1

count=0
for v in d.values():
    count+=1
    if count>m:
        break
    print(v,end=' ')

# d={}

# for card in cards:
#     if card in nums:
#         d[card]=1
#     else:
#         d[card]=0
        
# for v in d.values():
#     print(v,end=' ')