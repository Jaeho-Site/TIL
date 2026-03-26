"""
중간합 계산에 대한 문제는 해결했지만 히든케이스를 다 처리하지 못함.
1. 입력이 닫는괄호로 시작하면? 런타임 에러임
2. 여는 괄호만 남고 끝나면? 0을 출력해야함.
3. 망가진 깊이 계산 : 다른 괄호그룹이 병렬로 존재할 때
테스트 케이스: (()(()))
올바른 계산식: 2 * (2+2*2)
"""
# 스택이 빌 때 전체 스코어를 계산하고, 스택이 차있으면 중간합으로 집계한다.
# 닫는 흐름이 연속되면 곱하고, 단절되면 더한다.
import sys
S = input()
stack=[]
score=0
open_type=('(','[','<')
close_count=0
middle_score=0

for s in S: # ()<[<>()]>
    
    # 여는 타입이면 그냥 스택에 넣기
    if s in open_type:
        stack.append(s)
        close_count=0
        continue
    
    # 닫는 타입이면 스택에서 하나 빼서 잘못되었는지 체크, 현 스코어 계산
    close_count+=1
    ch=stack.pop()
    if ch=='(' and s==')': cur_score=2
    elif ch=='[' and s==']': cur_score=3
    elif ch=='<' and s=='>': cur_score=5
    else : print(0); sys.exit()
    
    # 연속적인 닫기라면
    if close_count>1:
        middle_score*=cur_score
    else:
        middle_score+=cur_score
    
    # 스택이 비었으면 최종 계산
    if not stack:
        score+=middle_score
        middle_score=0

print(score)