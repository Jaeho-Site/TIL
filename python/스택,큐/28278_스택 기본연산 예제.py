""" 
1 X: 정수 X를 스택에 넣는다. (1 ≤ X ≤ 100,000)
2: 스택에 정수가 있다면 맨 위의 정수를 빼고 출력한다. 없다면 -1을 대신 출력한다.
3: 스택에 들어있는 정수의 개수를 출력한다.
4: 스택이 비어있으면 1, 아니면 0을 출력한다.
5: 스택에 정수가 있다면 맨 위의 정수를 출력한다. 없다면 -1을 대신 출력한다.
"""
import sys
input=sys.stdin.readline
n=int(input().strip())
stack=[]
target=0

for _ in range(n):
    # 그냥 한번에 order=input().split()으로 받아도 됨.
    order=input().strip()
    if len(order)>1:
        order,target=map(int,order.split())
    else:
        order=int(order)    

    _len=len(stack)
      
    if order==1:
        stack.append(target)
    elif order==2:
        if _len>0:
            print(stack.pop())
        else:
            print(-1)
    elif order==3:
        print(len(stack))
    elif order==4:
        if _len>0:
            print(0)
        else:
            print(1)
    else:
        if _len>0:
            print(stack[_len-1]) # 마지막 요소 접근은 -1로 : stack[-1]
        else:
            print(-1)