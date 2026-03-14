""" 
정수가 "0" 일 경우에는 가장 최근에 쓴 수를 지우고, 아닐 경우 해당 수를 쓴다.
괄호 문자열인지를 판단하는 스택의 대표적인 문제

1. 나는 append와 pop상황을 나눠서 처리하고, 마지막에 스택길이로 판단하게함
---
* 정답 풀이는 더 pythontic하게 처리하는 방식을 설명함. 
- for - else 구문을 사용해서 bool변수 사용을 없앴다.
- if stack, if not stack 으로 스택에 값이 들어있는지 판별했다. 
"""
# 정답 풀이
import sys
input = sys.stdin.readline
n = int(input().strip())

for _ in range(n):
    stack = []
    string = input().strip()
    
    for s in string:
        if s == '(':
            stack.append(s)
        else: # s == ')'
            if stack: # len(stack) > 0 과 동일
                stack.pop()
            else:
                print('NO')
                break
    else:
        # break에 걸리지 않고 for문이 정상 종료되었을 때 실행됨
        if not stack: # 스택이 비어있으면 (len(stack) == 0)
            print('YES')
        else:         # 스택에 '('가 남아있으면
            print('NO')

######## 내 풀이 ########
import sys
input=sys.stdin.readline
n=int(input().strip())

for _ in range(n):
    stack=[]
    string=input().strip() # )()
    is_end=False
    
    for s in string:
        if s=='(':
            stack.append(s)
        else:
            if len(stack)>0:
                stack.pop()
            else:
                is_end=True
                print('NO')
                break
                
    if not is_end:
        if len(stack)==0:
            print('YES')
        else:
            print('NO')