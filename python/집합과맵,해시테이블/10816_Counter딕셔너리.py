"""
10
6 3 2 10 10 10 -10 -10 7 3
8
10 9 -5 2 3 4 5 -10
---
Counter를 사용해서 내 카드의 수를 센다.
cards를 key로 사용해서 값을 조회한다.
"""
# collections의 Counter를 활용한 풀이
import sys
from collections import Counter
input=sys.stdin.readline

n=int(input())
my_cards=list(map(int,input().split()))

my_dict=Counter(my_cards)

m=int(input())
cards=list(map(int,input().split()))
    
for card in cards:
    print(my_dict[card],end=' ')