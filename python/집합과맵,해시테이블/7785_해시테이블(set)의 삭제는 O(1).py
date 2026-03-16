"""
회사에는 동명이인이 없으며, 대소문자가 다른 경우에는 다른 이름이다. 
현재 회사에 있는사람 : enter이고 leave를 안한사람 
-> 다르게 말하면 이름이 두번이상 적히지 않은 사람

"""
import sys
input=sys.stdin.readline
n=int(input())

answer=set([])

for _ in range(n):
    name, case=input().split()
    if case == 'enter':
        answer.add(name)
    else:
        answer.remove(name) # 삭제도 O(1)이다.

answer=sorted(answer,reverse=True)
for a in answer:
    print(a)