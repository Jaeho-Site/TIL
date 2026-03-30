"""
나는 먹이를 모든 맵을 돌면서 모두 찾았지만, 최단거리의 먹이들만 찾으면
되는게 최적화한것.
"""

from collections import deque

# 1. 입력 및 초기화
N = int(input())
board = [list(map(int, input().split())) for _ in range(N)]

shark_x, shark_y = 0, 0
shark_size = 2
eat_count = 0
total_time = 0

# 상어 초기 위치 찾기 및 맵에서 지우기 (핵심!)
for i in range(N):
    for j in range(N):
        if board[i][j] == 9:
            shark_x, shark_y = i, j
            board[i][j] = 0

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

# 2. 먹이를 찾는 BFS 함수 (독립적으로 분리)
def find_fish(sx, sy, size):
    dist = [[-1] * N for _ in range(N)]
    q = deque([(sx, sy)])
    dist[sx][sy] = 0
    
    candidates = [] # 먹을 수 있는 물고기 리스트
    min_dist = float('inf') # 가장 가까운 물고기의 거리
    
    while q:
        x, y = q.popleft()
        
        # 현재 거리가 이미 찾은 최단 거리보다 크다면 더 이상 탐색할 필요 없음 (효율성 핵심)
        if dist[x][y] > min_dist:
            break
            
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            
            if 0 <= nx < N and 0 <= ny < N and dist[nx][ny] == -1:
                # 지나갈 수 있는 경우 (빈칸이거나 크기가 작거나 같은 물고기)
                if board[nx][ny] <= size:
                    dist[nx][ny] = dist[x][y] + 1
                    q.append((nx, ny))
                    
                    # 먹을 수 있는 물고기인 경우
                    if 0 < board[nx][ny] < size:
                        candidates.append((nx, ny, dist[nx][ny]))
                        min_dist = dist[nx][ny] # 최단 거리 갱신
                        
    # 조건에 맞는 물고기가 여러 마리일 경우 정렬 (1순위: 거리, 2순위: 가장 위, 3순위: 가장 왼쪽)
    if candidates:
        candidates.sort(key=lambda x: (x, x, x))
        return candidates # 가장 우선순위가 높은 물고기 1마리 반환
    else:
        return None

# 3. 메인 시뮬레이션 루프
while True:
    fish = find_fish(shark_x, shark_y, shark_size)
    
    if fish is None: # 더 이상 먹을 수 있는 물고기가 없으면 종료
        print(total_time)
        break
        
    fx, fy, dist = fish
    
    # 상어 이동 및 먹기 로직
    shark_x, shark_y = fx, fy
    total_time += dist
    board[fx][fy] = 0 # 먹은 물고기 자리 지우기
    eat_count += 1
    
    # 크기 증가 로직
    if eat_count == shark_size:
        shark_size += 1
        eat_count = 0