# 5. 가중치(이동 비용이 0인 경로와 1인 경로가 섞여 있을 때)
# 백준 13549번: 숨바꼭질 3
"""
[핵심 아이디어]
비용이 0이면 appendleft(가장 먼저 처리), 
비용이 1이면 append(나중에 처리)를 한다.
if cost == 0:
    queue.appendleft((nx, ny)) # 0원이면 우선순위 부여
else:
    queue.append((nx, ny))    # 1원이면 일반적인 순서
"""
from collections import deque

def zero_one_bfs():
    start, target = 1, 10
    max_val = 20
    dist = [-1] * (max_val + 1)
    
    queue = deque([start])
    dist[start] = 0

    while queue:
        x = queue.popleft()
        if x == target:
            return dist[x]

        # 1. 순간이동 (비용 0)
        for nx in [x * 2]:
            if 0 <= nx <= max_val and dist[nx] == -1:
                dist[nx] = dist[x]
                queue.appendleft(nx)

        # 2. 걷기 (비용 1)
        for nx in [x - 1, x + 1]:
            if 0 <= nx <= max_val and dist[nx] == -1:
                dist[nx] = dist[x] + 1
                queue.append(nx)

    return -1


print(f"최단 시간: {zero_one_bfs()}초")