"""
4 2
fire 3
water 4
fire water water fire
2 2 2 1
-> 2
"""
# 사실 내 풀이의 알고리즘 자체는 맞다. 하지만 간과한점은
"""
*@* 문제에서 앞에서부터 읽는다고 했는데 나는 pop을 했기때문에 뒤에서 부터 읽게됨.
-> 여기서 생각나는 해결방법은 2가지가 있음.
1. for name, num in zip(NAME, E): 이렇게 magic배열은 선언하지 않고,앞에서부터
차례대로 검사하면 될것임.
2. magic을 선언하고 while을 사용하려면 magic을 deque로 바꾸고 popleft하면 된다. 
"""
# 내 풀이
import sys
input=sys.stdin.readline
N,M=map(int,input().split())
case={}
for _ in range(M):
    이름, 수치=input().split()
    case[이름]=int(수치)
    
NAME=list(input().split())
E=list(map(int,input().split()))

magic=[]
for n,e in zip(NAME,E):
    magic.append((n,e))
#---------------------------------------입력세팅
# 원소를 융합할 스택을 하나 선언
stack=[]
answer=0

while magic:
    name,num=magic.pop() # ('fire', 1)
    
    # 뺐는데 수치보다 크면 마법 발동 
    if case[name]<=num: answer+=1
    
    # 수치보다 작으면 
    else:
        # 스택에 뭐가 들어있으면 마지막 거랑 비교, name같으면 합치기
        if stack and stack[-1][0]==name:
            is_over=stack[-1][1]+num
            stack.pop()   
            if is_over>=case[name]:
                answer+=1
            else:
                stack.append((name,is_over))
        # 스택이 비었으면 그냥 추가        
        else:
            stack.append((name,num))        
print(answer)