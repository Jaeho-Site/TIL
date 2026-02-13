n = int(input())
x = list(map(int, input().split()))

# 크기 역순으로 정렬하고, 가장 작은 값만큼 그룹 생성
array = sorted(x)
print(array)
count = 0

for i in range(len(array)):
    array[i]
    
"아이디어는 정답과 동일, 하지만 구현을 못했음 -> 경험 부족"

import sys

input = sys.stdin.readline
n = int(input())
data = list(map(int, input().split()))

# 2. 공포도를 오름차순으로 정렬 (그리디의 핵심)
data.sort()

result = 0  # 총 그룹의 수
count = 0   # 현재 그룹에 포함된 모험가의 수

# 3. 공포도가 낮은 모험가부터 확인하며 그룹 결성
for i in data:
    count += 1          # 현재 모험가를 그룹에 포함
    if count >= i:      # 현재 그룹 인원수가 현재 확인 중인 모험가의 공포도 이상이라면
        result += 1     # 그룹 결성 완료 (총 그룹 수 증가)
        count = 0       # 새로운 그룹을 위해 현재 그룹 인원수 초기화

print(result)