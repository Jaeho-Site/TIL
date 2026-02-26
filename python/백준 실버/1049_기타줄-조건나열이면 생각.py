"""
6개 패키지만을 구매하는 경우
낱개 패키지만을 구매하는 경우
6개 패키지와 낱개를 함께 사야하는 경우
---
6단위로 생각해야할듯
1. n을 6으로 나누고 몫은 가장싼 브랜드 가격이랑 곱하고, 
나머지는 낱개가 가장싼 브랜드에서 구매.

-> 히든케이스 : 낱개가 6개 패키지보다 쌀때가 있음
-> n이 6보다 작은 경우

"""
import sys
n,m = map(int,input().split())
package=[]
one=[]

for i in range(m):
    for _ in range(m):
        p, o = map(int, sys.stdin.readline().split())
        min_package = min(min_package, p)
        min_one = min(min_one, o)
    case1 = ((n // 6) + 1) * min_package
    case2 = n * min_one
    case3 = (n // 6) * min_package + (n % 6) * min_one
    
    # 3가지 경우가 있는데, 이걸 조건문으로 나누지 않고 다 계산하고 가장 작은걸 출력
    print(min(case1, case2, case3))