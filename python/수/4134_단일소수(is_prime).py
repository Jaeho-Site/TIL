"""
3
6
20
100
-> n보다 큰 가장작은 소수 찾기 문제 
"""
import sys
input=sys.stdin.readline
n=int(input().strip())

def is_prime(t):
    if t<2:
        return False

    for i in range(2,int(t**0.5)+1):
        if t%i==0:
            return False
    return True

for _ in range(n):
    target=int(input().strip())
    
    while not is_prime(target):
        target+=1
    print(target)