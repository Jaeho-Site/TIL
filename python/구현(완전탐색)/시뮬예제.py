n = int(input())
data = input().split()

dx = [0,-1,0,1] # x축(행) 이동량
dy = [1,0,-1,0] # y축(열) 이동량

x,y=1,1 # 현재 위치 (중심)
#5
#R R R U D D
# x가 1일때는 U불가
# x가 5일때는 D불가
# y가 1일때는 L불가
# y가 5일때는 R불가 

for i in range(len(data)):
    if data[i] == 'R' and y>=n:
        y += dy[0]
    elif data[i] == 'U' and x<=1:
        x += dx[1]
    elif data[i] == 'D' and x>=n:
        x += dx[3]
    elif data[i] == 'L' and y<=1:
        y += dy[2]    
 
print(x, y)       

"처음 공부해보는 시뮬 유형... 구현이 엉망이다."
# 정답 코드 #

import sys

input = sys.stdin.readline
n = int(input())
plans = input().split()

# 2. 방향 벡터 공식 (상, 하, 좌, 우 순서)
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
move_types = ['U', 'D', 'L', 'R']

x, y = 1, 1 # 시작 좌표

# 3. 이동 계획을 하나씩 확인
for plan in plans:
    # 이동 후 좌표 구하기
    for i in range(len(move_types)):
        if plan == move_types[i]:
            nx = x + dx[i]
            ny = y + dy[i]
    
    # 4. 공간을 벗어나는 경우 무시 (공식: 0 <= nx < n 형식이지만 여기선 1부터 시작)
    if nx < 1 or ny < 1 or nx > n or ny > n:
        continue
    
    # 이동 수행
    x, y = nx, ny

print(x, y)
