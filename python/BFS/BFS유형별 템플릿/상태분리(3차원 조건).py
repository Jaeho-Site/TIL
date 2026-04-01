# 4. 상태 분리(특정 조건 : 능력,벽 깨기)
# 백준 2206번: 벽 부수고 이동하기 (필수), 백준 1600번: 말이 되고픈 원숭이 (심화)
"""
[핵심 아이디어]
visited[x][y]로는 부족하다.
visited[상태][x][y] 방문 배열에 차원(상태)을 하나 더 추가한다.
"""
from collections import deque

def state_bfs():
    # 0: 길, 1: 벽
    grid = [
        [0, 1, 1],
        [0, 1, 0],
        [0, 0, 0]
    ]
    n, m = 3, 3

    # visited[벽부순상태][x][y] -> 상태 0: 아직 안부숨, 1: 이미 부숨
    visited = [[[False] * m for _ in range(n)] for _ in range(2)]
    
    # 큐에 (x, y, 거리, 벽부쉈는지여부) 담기
    queue = deque([(0, 0, 1, 0)])
    visited[0][0][0] = True

    dx, dy = [0, 0, 1, -1], [1, -1, 0, 0]

    while queue:
        x, y, d, broken = queue.popleft()
        if x == n-1 and y == m-1:
            return d

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]

            if 0 <= nx < n and 0 <= ny < m:
                # 1. 벽이 아니고, 현재 상태(broken)에서 방문한 적 없을 때
                if grid[nx][ny] == 0 and not visited[broken][nx][ny]:
                    visited[broken][nx][ny] = True
                    queue.append((nx, ny, d + 1, broken))

                # 2. 벽인데, 아직 벽을 부순 적이 없을 때
                elif grid[nx][ny] == 1 and broken == 0:
                    visited[1][nx][ny] = True
                    queue.append((nx, ny, d + 1, 1))

    return -1


print(f"최단 거리: {state_bfs()}")  # 결과: 5