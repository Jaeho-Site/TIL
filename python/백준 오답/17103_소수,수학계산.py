"""
2보다 큰 짝수는 두 소수의 합으로 나타낼 수 있다.
T (1 ≤ T ≤ 100)
N (2 < N ≤ 1,000,000)

1. 일단 N 이하의 소수를 구하는것 까진 맞음
2. 소수들을 2개 선택해서 그 합이 N이 되는지 체크, 카운트증가
-> 내 코드의 문제는
1. 매 n마다 에라토스테네스 체를 새롭게 만들었음
2. 중복조합 방식으로, 순서를 무시해도 좋은데 범위를 모두 체크함.
3. 소수+소수에 집착해서 i + (n-i) 라는 식을 찾지 못함
"""
# 정답 풀이
import sys
input = sys.stdin.readline
# 1. 에라토스테네스의 체: 1,000,000까지의 소수 판별 배열을 '한 번만' 생성
MAX = 1000000
is_prime = [True] * (MAX + 1)
is_prime[0] = is_prime[1] = False

for i in range(2, int(MAX**0.5) + 1):
    if is_prime[i]:
        for j in range(i * i, MAX + 1, i):
            is_prime[j] = False

t = int(input().strip())

for _ in range(t):
    n = int(input().strip())
    count = 0
    
    # n의 절반까지만 확인 (a <= b 조건을 만족하여 중복 방지)
    # 2는 유일한 짝수 소수이므로 따로 체크하거나 루프에 포함
    for i in range(2, n // 2 + 1):
        # i가 소수이고, (n - i)도 소수라면 하나의 파티션 성립!
        if is_prime[i] and is_prime[n - i]:
            count += 1
            
    print(count)


# 내 풀이
import sys
from itertools import combinations_with_replacement as cwr
input=sys.stdin.readline

def seive(n):
    prime=[True]*(n+1)
    prime[0]=prime[1]=False
    
    for i in range(2,int(n**0.5)+1):
        if prime[i]:
            for j in range(i*i,n+1,i):
                prime[j]=False
    primes=[i for i,is_prime in enumerate(prime) if is_prime] 
    count=0
    for a,b in cwr(primes,2):
        if a+b==n:
            count+=1
    return count
    
    
t=int(input().strip())
for _ in range(t):
    print(seive(int(input().strip())))
