# 3. 여러 지점 동시 탐색 (멀티 소스 BFS)
# 백준 7576번: 토마토 (기초), 백준 4179번: 불! (응용), 17142번
"""
[핵심 아이디어]
큐를 비운 상태에서 시작하지 않고, 
모든 시작점들을 미리 큐에 다 넣은 상태에서 while문을 시작한다.
"""
from collections import deque

def multi_source_bfs():
    # 0: 빈칸, 1: 바이러스 시작점
    grid = [
        [1, 0, 0],
        [0, 0, 0],
        [0, 0, 1]
    ]
    n = 3
    queue = deque()
    dist = [[-1] * n for _ in range(n)]

    # [핵심] 모든 시작점을 미리 큐에 넣고 시작!
    for x in range(n):
        for y in range(n):
            if grid[x][y] == 1:
                queue.append((x, y))
                dist[x][y] = 0  # 시작점의 시간은 0

    max_time = 0
    dx, dy = [0, 0, 1, -1], [1, -1, 0, 0]

    while queue:
        x, y = queue.popleft()
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]

            if 0 <= nx < n and 0 <= ny < n and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1
                max_time = max(max_time, dist[nx][ny])
                queue.append((nx, ny))
    
    return max_time


print(f"모두 퍼지는 시간: {multi_source_bfs()}초")  # 결과: 2초