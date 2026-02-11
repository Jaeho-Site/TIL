
"처음 내 풀이 : 문제는 없지만 log(N)으로 해결가능한 문제를 N으로 해결함."
# N, k = list(map(int,input().split()))
# count=0

# while(N!=1):
#     if(N%k==0):
#         N//=k
#     else:
#         N-=1
#     count+=1

# print(count)    

import sys
input = sys.stdin.readline

n, k = map(int, input().split())
count = 0

while True:
    "이 부분을 반복문 안에 넣는걸 놓침 -> 예외도 있음 25 3 등"
    # 1. n이 k의 배수가 되도록 한 번에 빼기
    target = (n // k) * k
    count += (n - target) # 1씩 빼야 하는 횟수를 한 번에 더함
    n = target
    
    # 2. n이 k보다 작아서 더 이상 나눌 수 없을 때 반복문 탈출
    if n < k:
        break
    
    # 3. k로 나누기
    n //= k
    count += 1

# 4. 마지막으로 남은 수에서 1이 될 때까지 빼기
count += (n - 1)
print(count)
 