from collections import deque

############### 인접 기반 리스트(그래프) #################

def bfs(start):
    queue = deque([start])
    visited[start] = True # visited 배열은 밖에 전역으로 있다고 가정

    while queue:
        v = queue.popleft()
        
        for i in graph[v]:
            if not visited[i]:
                queue.append(i)
                visited[i] = True
                
############### 2차원 배열(Grid) #################

from collections import deque

dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

def bfs(x, y):
    queue = deque([(x, y)])
    visited[x][y] = True
    
    while queue:
        x, y = queue.popleft() 
        
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            
            # 1. 범위 이탈 시 패스
            if not (0 <= nx < n and 0 <= ny < m):
                continue
            
            # 2. 갈 수 없는 곳이거나, 이미 방문했으면 패스
            if visited[nx][ny] or graph[nx][ny] != 1:
                continue
                
            # 3. 큐에 넣고 방문 처리
            visited[nx][ny] = True
            queue.append((nx, ny))