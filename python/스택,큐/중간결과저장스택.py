"""
((A)2B(C2)3)2(D)
-> 48
"""
S=input()

# A ~ Z : 1 ~ 26 -> -64
# 2 ~ 9 : 배수 적용
# ( )   : 안의 모든 질량계산 및 숫자오면 곱
stack=[]
is_digit=['2','3','4','5','6','7','8','9'] # ord(s)-64
for i in range(len(S)):
    s=S[i]
    
    # 여는 괄호면 스택에 넣는다.
    if s=='(':
        stack.append(s)
    
    # 알파벳도 스텍에 넣는다.
    elif s.isalpha():
        stack.append(str(ord(s)-64))
    
    # 숫자가 나오면 가장 상단의 요소를 빼서 곱하고 결과를 다시 넣는다.
    elif s in is_digit:
        ch=stack.pop()
        tmp=int(ch)*int(s)
        # 스트링으로 넣어야함.
        stack.append(str(tmp))
    
    # 닫는 괄호가 나오면 여는 괄호가 나올때까지 pop하고 들어있는 모든 수를 더한다.
    elif s==')':
        tmp=0
        while True:
            ch=stack.pop()
            if ch=='(' : break
            tmp+=int(ch)
        
        stack.append(str(tmp))

answer=0
for i in stack:
    answer+=int(i)
print(answer)