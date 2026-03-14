""" 
[]와 () 모두가 짝을 맞춰야 YES이고 아니면 NO
[( ]) 이렇게 쌍이 맞아도 순서가 틀려서 안됨.

1. stack을 하나 선언하고, 4가지 케이스에 대해 모두 탐색한다.
2. stack[-1]을 검사해서 pair가 맞는지확인도 해야함.
3. 나머지는 일반 괄호문제랑 똑같이 하면될듯
---
정답은 맞는데 가독성이 안좋음.
* 정석 풀이
- 딕셔너리를 사용해서 페어를 맞춘다.
- 또 단축 평가로 
if stack이 참이면 뒤의 if stack or stack[-1]... 이걸 검사할거고
거짓이면 뒤는 보지도 않으므로 stack[-1]에서 에러날 일이 없음

"""
# 정석 풀이
import sys
input = sys.stdin.readline

# 닫는 괄호와 여는 괄호의 짝을 딕셔너리로 미리 정의합니다.
matching = {')': '(', ']': '['}

while True:
    # rstrip('\n')을 써서 오른쪽 줄바꿈만 깔끔하게 지워줍니다.
    string = input().rstrip('\n')
    
    if string == '.':
        break
        
    stack = []
    
    for s in string:
        # 1. 여는 괄호일 때
        if s in "([": 
            stack.append(s)
            
        # 2. 닫는 괄호일 때 (딕셔너리의 키에 존재하는지 확인)
        elif s in matching: 
            # 스택이 비어있거나, 스택의 맨 위 괄호가 짝이 안 맞으면 아웃!
            if not stack or stack[-1] != matching[s]: 
                print('no')
                break
            # 짝이 맞으면 스택에서 제거
            stack.pop()
            
    # 3. for문이 무사히 다 돌았을 때 (break에 안 걸렸을 때)
    else:
        if not stack:
            print('yes')
        else:
            print('no')



# 내 풀이
import sys
input=sys.stdin.readline
while True:
    string=input().rstrip()
    if string=='.':
        break
    
    stack=[]
    
    for s in string:
        if s=='(' or s=='[': # 여는 괄호는 그냥 스택에 넣으면 된다.
            stack.append(s)
        elif s==')': 
            if stack: # 닫는 괄호는 1. 스택이 비어있지 않고
                if stack[-1]=='(': # 스택의 마지막이 짝이 맞으면 
                    stack.pop()
                else:
                    print('no')
                    break
            else:
                print('no')
                break
        elif s==']': 
            if stack: # 닫는 대괄호는 1. 스택이 비어있지 않고
                if stack[-1]=='[': # 스택의 마지막이 짝이 맞으면 
                    stack.pop()
                else:
                    print('no')
                    break
            else:
                print('no')
                break
    else:
        if not stack:
            print('yes')
        else:
            print('no')