"""
중요도는 1 이상 9 이하의 정수이고, 
중요도가 같은 문서가 여러 개 있을 수도 있다.
"""
import sys
from collections import deque
input=sys.stdin.readline

T=int(input())
for _ in range(T):
    N,M=map(int,input().split())
    score=list(map(int,input().split()))
    docs = deque(enumerate(score))

    score.sort() # 지금의 최고 우선순위 확인
    count=1
    while docs: # 1 1 9 1 1 1
        target=score[-1]
        
        if docs[0][1]==target:
            if docs[0][0]==M:
                print(count)
                break
            docs.popleft()
            score.pop()
            count+=1
        else:
            docs.append(docs.popleft())