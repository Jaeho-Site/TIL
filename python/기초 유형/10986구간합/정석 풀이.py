#####################정석풀이#######################
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
nums = list(map(int, input().split()))

# 나머지의 개수를 저장할 배열 (0부터 m-1까지)
remainder_count = [0] * m
prefix_sum = 0
answer = 0

for i in range(n):
    prefix_sum += nums[i]
    remainder = prefix_sum % m
    
    # 1. 누적 합 자체가 m으로 나누어떨어지는 경우
    if remainder == 0:
        answer += 1
    
    # 2. 나머지가 같은 지점들의 개수를 카운트
    remainder_count[remainder] += 1

# 3. 나머지가 같은 두 지점을 선택하는 경우 (nC2)
for count in remainder_count:
    if count >= 2:
        answer += (count * (count - 1)) // 2

print(answer)