"""
n의 가장 작은 생성자
2(1+1)         9 -> 9
11(10+1+0)     9 9 -> 18
99(90+9+0)
100(86+8+6)    9 9 9 -> 27
216(198+1+9+8) 9 9 9 -> 27

시간복잡도 : n ~ nlogn시간 안에 해결
1. 일단 다 돌고,각 자리수이므로 n에 따라 9 9 9 ~ 컷
2. 
9*3
"""
# 아이디어는 얼추 맞는데 코드로 옮기는것 실패. max활용못함
# 정답코드
import sys

n_str = sys.stdin.readline().strip()
n = int(n_str)
k = len(n_str) # 자릿수 (예: 216이면 3)

answer = 0
start = max(1, n - 9 * k)

for i in range(start, n):
    # i의 각 자릿수를 분리하여 리스트로 만들고 합산
    digit_sum = sum(map(int, str(i)))
    total = i + digit_sum

    if total == n:
        answer = i
        break 
print(answer)