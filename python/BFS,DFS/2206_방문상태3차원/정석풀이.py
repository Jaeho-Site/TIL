from collections import deque
import sys
input = sys.stdin.readline

def solve():
    N, M = map(int, input().split())
    graph = [list(map(int, input().strip())) for _ in range(N)]

    # visited[r][c][broken]: 벽을 부순 적 있는지 여부
    visited = [[[False] * 2 for _ in range(M)] for _ in range(N)]

    # (행, 열, 벽부순여부, 거리)
    queue = deque([(0, 0, 0, 1)])
    visited[0][0][0] = True

    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    while queue:
        r, c, broken, dist = queue.popleft()

        if r == N - 1 and c == M - 1:
            print(dist)
            return

        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]

            if 0 <= nr < N and 0 <= nc < M:
                # 빈 칸으로 이동
                if graph[nr][nc] == 0 and not visited[nr][nc][broken]:
                    visited[nr][nc][broken] = True
                    queue.append((nr, nc, broken, dist + 1))
                # 벽을 부수고 이동 (아직 벽을 안 부쉈을 때)
                elif graph[nr][nc] == 1 and broken == 0 and not visited[nr][nc][1]:
                    visited[nr][nc][1] = True
                    queue.append((nr, nc, 1, dist + 1))

    print(-1)

solve()