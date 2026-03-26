import sys
input = sys.stdin.readline

S = input().strip()

stack = []
answer = 0
tmp = 1 # 분배법칙을 위한 임시 곱셈기

for i in range(len(S)):
    s = S[i]
    
    # 1. 여는 괄호: 배수를 곱하고 스택에 넣는다 (깊어짐)
    if s == '(':
        tmp *= 2
        stack.append(s)
    elif s == '[':
        tmp *= 3
        stack.append(s)
    elif s == '<':
        tmp *= 5
        stack.append(s)
        
    # 2. 닫는 괄호: 
    elif s == ')':
        # 짝이 안 맞거나 스택이 비었으면 비정상 종료
        if not stack or stack[-1] != '(':
            answer = 0
            break
        # ★ 핵심: "바로 직전" 문자가 여는 괄호일 때만 정답에 더함 (가장 안쪽 괄호라는 뜻)
        if S[i-1] == '(':
            answer += tmp
        # 괄호를 닫고 나오므로 깊이가 얕아짐 (배수를 다시 나눔)
        stack.pop()
        tmp //= 2

    elif s == ']':
        if not stack or stack[-1] != '[':
            answer = 0
            break
        if S[i-1] == '[':
            answer += tmp
        stack.pop()
        tmp //= 3

    elif s == '>':
        if not stack or stack[-1] != '<':
            answer = 0
            break
        if S[i-1] == '<':
            answer += tmp
        stack.pop()
        tmp //= 5

# 최종 검증: 모든 과정이 끝났는데 스택에 여는 괄호가 남아있다면 비정상
if stack:
    print(0)
else:
    print(answer)