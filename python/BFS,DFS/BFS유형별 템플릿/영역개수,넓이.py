# 2. 연결된 영역 개수와 넓이 구하기
# 백준 : 2583번: 영역 구하기, 2667번: 단지번호붙이기
"""
[핵심 아이디어]
1. 전체 맵을 돌며 방문하지 않은 '땅'을 찾으면 BFS를 시작
2. BFS가 한 번 실행될 때마다 영역 개수 + 1
3. BFS 내부에서 queue.popleft()가 일어나는 횟수를 세면 해당 영역의 넓이
"""
from collections import deque
grid = [
    [1, 1, 0, 0],
    [1, 0, 0, 0],
    [0, 0, 1, 1],
    [0, 0, 1, 0]
]
n = 4
visited = [[False] * n for _ in range(n)]

def bfs(x, y):
    queue = deque([(x, y)])
    visited[x][y] = True
    area_size = 0  # 영역의 넓이 측정
    
    dx, dy = [0, 0, 1, -1], [1, -1, 0, 0]
    
    while queue:
        x, y = queue.popleft()
        area_size += 1  # 큐에서 뺄 때마다 넓이 증가
        
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if not(0 <= nx < n and 0 <= ny < n):
                continue
            if grid[nx][ny] == 1 and not visited[nx][ny]:
                visited[nx][ny] = True
                queue.append((nx, ny))
                
    return area_size

areas = []
for i in range(n):
    for j in range(n):
        # 방문하지 않은 땅(1)을 발견하면 새로운 BFS 시작
        if grid[i][j] == 1 and not visited[i][j]:
            areas.append(bfs(i, j))

print(f"영역 개수: {len(areas)}")  # 결과: 2
print(f"각 영역의 넓이: {sorted(areas)}")  # 결과: [3, 3]