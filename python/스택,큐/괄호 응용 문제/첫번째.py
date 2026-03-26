"""
()는 2, []는 3, <>는 5의 마력
어떤 올바른 괄호열 $X$가 괄호로 둘러싸여 있다면 마력이 곱해집니다.
((<[]>))
[] = 3
<[]> = 5 * 3
(<[]>) = 2 * 15
((<[]>)) = 2 * 30

그러니까 일단 괄호 짝이 안맞으면 0임
()[<>()]     23
()<[<>()]>   107
((<[]>))     60
()[<>]       17
중간합을 어떻게 처리할지에 따라 연속적인것과 불연속인것의 정답을
반반만 맞추는 문제가 있었음.

"""


import sys
S=input() # ((<[]>))

stack=[]
open=('(','[','<')
score=0
temp_score=1
is_first=0
for s in S:
    if s in open:
        stack.append(s)
    else:
        if not stack : print(0); sys.exit()
        
        # 스택을 뽑아서 현재 점수를 계산한다.
        ch = stack.pop()
        is_first+=1
        
        if ch=='(' and s==')':
            cur_score=2
        elif ch=='[' and s==']':
            cur_score=3
        elif ch=='<' and s=='>':
            cur_score=5
        else: print(0); sys.exit()
            
        print(f'현타켓 : {s}, ts:{temp_score}, score : {score}')
        
        # 스택이 비었으면 중간합 정산은 끝난것이므로 다시 1로 비운다.
        if not stack:      
            score+=temp_score*cur_score
            temp_score=1

        # 스택이 안비었으면 중간합을 계속 계산해야함 
        else:
            if is_first>1:
                temp_score*=cur_score
                is_first=0
            else:
                if temp_score==1: 
                    temp_score+=cur_score-1
                else:
                    temp_score+=cur_score
        
print(score)