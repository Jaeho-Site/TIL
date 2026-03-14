"""
1번 카드가 젤 위에, n번이 가장 아래에 순서대로 있다.
1. 제일 위에 있는 카드를 바닥에 버린다.
2.  제일 위에 있는 카드를 제일 아래에 있는 카드 밑으로 옮긴다.

제일 마지막에 남게 되는 카드를 구하자.
"""
from collections import deque

n=int(input())
q=deque([i for i in range(1,n+1)])

while True: 
    if len(q)==1:
        print(q.popleft())
        break
    # 1번 연산은 가장 popleft로 카드를 버리는 행위
    q.popleft()
    # 2번 연산은 popleft한 카드를 다시 append하는 행위
    q.append(q.popleft())