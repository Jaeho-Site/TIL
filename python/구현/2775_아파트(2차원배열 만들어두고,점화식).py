"""
0층

1 2 3 4 5 6 7 ...
1 2 3 4 5 6 7

1 ≤ k, n ≤ 14
4층의 3호는
3층의 3호
"""
### 사실 이문제는 조합 딸깍으로 풀린다.
# math.comb(k+n,n-1)

###
import sys
input=sys.stdin.readline
T=int(input().strip())
apart=[[0]*14 for _ in range(15)]

apart[0]=[i for i in range(1,15)]
for i in range(1,15):
    apart[i][0]=1

for i in range(1,15): # 1층부터
    for j in range(1,14): # 14호까지
        apart[i][j]=apart[i-1][j]+apart[i][j-1]

for _ in range(T):
    k=int(input().strip()) # k층 
    n=int(input().strip()) # n호 
    print(apart[k][n-1])