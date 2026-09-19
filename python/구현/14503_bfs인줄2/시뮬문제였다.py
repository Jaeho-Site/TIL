import sys
input = sys.stdin.readline

N, M = map(int, input().split())
r, c, d = map(int, input().split()) 
room = [list(map(int, input().split())) for _ in range(N)]

dx = [-1, 0, 1, 0] # 북, 동, 남, 서
dy = [0, 1, 0, -1]

while True:
    # 1. 현재 칸이 아직 청소되지 않은 경우, 현재 칸을 청소한다.
    if room[r][c] == 0:
        room[r][c] = 2
        
    # 4방향 탐색해서 청소할 곳이 있는지 확인 (is_dirty 체크)
    is_dirty = False
    for i in range(4):
        nx, ny = r + dx[i], c + dy[i]
        if 0 <= nx < N and 0 <= ny < M and room[nx][ny] == 0:
            is_dirty = True
            break
        
    if is_dirty:
        # 3. 청소되지 않은 빈 칸이 있는 경우
        d = (d + 3) % 4 # 반시계 회전
        nx, ny = r + dx[d], c + dy[d]
        
        # 앞쪽 칸이 청소되지 않은 빈 칸이면 "한 칸 전진 (좌표 갱신)"
        if 0 <= nx < N and 0 <= ny < M and room[nx][ny] == 0:
            r, c = nx, ny
            
        # (전진하지 못하더라도 방향은 돌렸으니 그냥 다음 while 루프로 넘어가면 됨)
        
    else:
        # 2. 청소되지 않은 빈 칸이 없는 경우
        back_d = (d + 2) % 4 # 방향 d는 유지!
        nx, ny = r + dx[back_d], c + dy[back_d]
        
        # 후진할 수 있다면 후진 (좌표 갱신)
        if 0 <= nx < N and 0 <= ny < M and room[nx][ny] != 1:
            r, c = nx, ny
        # 뒤쪽이 벽이라 후진할 수 없다면 작동 멈춤
        else:
            break