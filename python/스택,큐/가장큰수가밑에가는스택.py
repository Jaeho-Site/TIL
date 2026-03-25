"""
6
10
3
7
4
12
2
->5
이문제는 이중for문으로 풀린다면 백준 브론즈3도 아까울 문제이다.
하지만 시간복잡도가 제한되므로, 스택을 활용한 아이디어가 필요하다.
송전탑은 오른쪽으로만 전파를 쏘고, 쏘는 개수를 역으로 생각해서,
그 탑에 전파를 쏘고 있는 송전탑을 스택에 넣어두고 길이를 계산한다.
"""
import sys
input=sys.stdin.readline
N=int(input())
TOP=[int(input()) for _ in range(N)] # 10 3 7 4 12 2
answer=0
stack=[]

for target in TOP:
    while stack:
        cur=stack[-1]
        
        # 송전탑이 기존 탑들보다 작은 경우
        if cur>target:
            stack.append(target)
            break
        else:
            stack.pop()
        
    if not stack:
        stack.append(target)
    
    answer+=len(stack)-1
print(answer)

############## while문을 조금더 파이썬틱하게 #############

for target in TOP:
    # 내 높이보다 작거나 같은 탑들은 가려지므로 스택에서 전부 제거
    while stack and stack[-1] <= target:
        stack.pop()
    
    # 나는 무조건 스택에 추가
    stack.append(target)
    
    # 내 왼쪽에 남아있는 탑들(나보다 큰 탑들)은 모두 나를 볼 수 있음
    answer += len(stack) - 1 

print(answer) 