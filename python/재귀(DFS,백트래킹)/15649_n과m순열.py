"""
이 문제는 DFS를 연습하라고 만든문제지만 가장 쉬운 방법은 itertools를 사용하는것이다.
두가지 방식으로 모두 풀어보자
전형적인 dfs백트래킹 문제이다.
"""
# 1. dfs로 해결하기
def dfs(depth):
    if depth==m:
        print(*path)
        return
    
    for i in range(1,n+1):
        if not visited[i]:
            visited[i]=True
            path.append(i)
            
            dfs(depth+1)
            
            path.pop()
            visited[i]=False
         
n,m=map(int,input().split())

visited=[False]*(n+1)
path=[]

dfs(0)

# 2. 순열 딸깍하기
from itertools import permutations

n,m=map(int,input().split())
nums=[i for i in range(1,n+1)]

for i in permutations(nums,m):
    print(*i)