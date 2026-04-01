# 1. 최단 거리 구하기
# 백준 : 2178번: 미로 탐색, 1697번: 숨바꼭질
"""
[핵심 아이디어] 
1. visited 배열 대신 distance 배열(혹은 grid 자체)에 숫자를 넣는다.
2. 다음 칸의 숫자 = 현재 칸의 숫자 + 1 공식 사용
3. 도착점에 도달하는 순간 그 숫자가 바로 최단 거리
"""
from collections import deque

# 1은 길, 0은 벽
maze = [
    [1, 0, 1, 1],
    [1, 1, 1, 0],
    [0, 0, 1, 1]
]

n, m = 3, 4

# dist 배열을 -1로 초기화 (방문 여부와 거리를 동시에 체크)
dist = [[-1] * m for _ in range(n)]

def bfs(start_x, start_y):
    queue = deque([(start_x, start_y)])
    dist[start_x][start_y] = 1  # 시작 칸 포함 거리 1
    
    dx, dy = [0, 0, 1, -1], [1, -1, 0, 0]
    
    while queue:
        x, y = queue.popleft()
        
        # 목표 지점 도착 시 즉시 종료
        if x == n-1 and y == m-1:
            return dist[x][y]
            
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            
            if not (0 <= nx < n and 0 <= ny < m):
                continue
                
            # 길(1)이고 아직 방문 안 했다면(-1)
            if maze[nx][ny] == 1 and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1
                queue.append((nx, ny))
                
    return -1

print(f"최단 경로 거리: {bfs(0, 0)}")  # 결과: 6