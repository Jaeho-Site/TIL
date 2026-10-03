import sys
from collections import deque
input = sys.stdin.readline

N, M = map(int, input().split())
start_r, start_c, start_d = map(int, input().split()) 
room = [list(map(int, input().split())) for _ in range(N)]

dx = [-1, 0, 1, 0] # 북, 동, 남, 서
dy = [0, 1, 0, -1]

# 큐에 시작 좌표와 방향을 함께 넣음 (r, c, d)
q = deque([(start_r, start_c, start_d)])
cleaned_count = 0

while q:
    r, c, d = q.popleft()
    
    # 1. 현재 칸이 아직 청소되지 않은 경우, 청소한다.
    if room[r][c] == 0:
        room[r][c] = 2 
        cleaned_count += 1
        
    # 이동 가능한 4칸 중 빈 칸(0)이 있는지 체크
    is_dirty = False
    for i in range(4):
        nx, ny = r + dx[i], c + dy[i]
        if 0 <= nx < N and 0 <= ny < M and room[nx][ny] == 0:
            is_dirty = True
            break
            
    # 조건에 따른 큐 삽입 (다음 상태 예약)
    if is_dirty: 
        # 3. 청소되지 않은 빈 칸이 있는 경우
        nd = (d + 3) % 4 # 반시계 회전 (새로운 방향)
        nx, ny = r + dx[nd], c + dy[nd]
        
        # 앞쪽 칸이 청소되지 않은 빈 칸이면 전진 (큐에 새로운 좌표와 방향 삽입)
        if 0 <= nx < N and 0 <= ny < M and room[nx][ny] == 0:
            q.append((nx, ny, nd))
        else:
            # 전진할 수 없다면 제자리에서 방향만 바꾼 상태를 큐에 삽입
            q.append((r, c, nd))
            
    else: 
        # 2. 주변에 청소되지 않은 빈 칸이 없는 경우
        back_d = (d + 2) % 4 # 뒤쪽 방향 계산
        nx, ny = r + dx[back_d], c + dy[back_d]
        
        # 후진할 수 있다면 후진 (주의: 방향은 원래 방향인 'd'를 유지해서 큐에 삽입!)
        if 0 <= nx < N and 0 <= ny < M and room[nx][ny] != 1:
            q.append((nx, ny, d)) 
        else:
            # 후진할 수 없다면 큐에 아무것도 넣지 않음 -> 자연스럽게 while문 종료 (작동 멈춤)
            break

print(cleaned_count)