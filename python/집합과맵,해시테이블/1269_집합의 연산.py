"""
3 5
1 2 4
2 3 4 5 6

두 집합의 대칭 차집합의 원소의 개수를 출력
합집합에서 교집합을 뺀 결과의 집합 길이를 출력 
"""
# 정석 풀이
import sys
input = sys.stdin.readline
an, bn = map(int, input().split())
a = set(map(int, input().split()))
b = set(map(int, input().split()))

# 대칭 차집합 연산 (A-B) ∪ (B-A)
# ^ 기호 하나로 끝납니다.
result = a ^ b
# a | b (합집합), a & b (교집합), a - b (차집합)

print(len(result))

# 내 풀이
an,bn=map(int,input().split())
a=set(map(int,input().split()))
b=set(map(int,input().split()))

sum_ab=b.copy() # 합집합 
for i in a:
    sum_ab.add(i)
    
and_ab=set() # 교집합 
for i in a:
    if i in b:
        and_ab.add(i)

print(len(sum_ab)-len(and_ab))