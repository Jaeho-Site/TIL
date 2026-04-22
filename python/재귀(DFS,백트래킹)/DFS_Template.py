import sys
sys.setrecursionlimit(10**6)

############### 인접 기반 리스트(그래프) #################

def dfs(v):
    # 1. 현재 노드 방문 처리
    visited[v] = True
    # (필요하다면 여기서 v에 대한 로직 처리. 예: print(v))  
    # 2. 현재 노드와 연결된 다른 노드를 재귀적으로 방문
    for next in graph[v]:
        if not visited[next]:
            dfs(next)
            
            
############### 2차원 배열 Grid #################

dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

def dfs(x, y):
    visited[x][y] = True

    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]
				
        if not (0 <= nx < n and 0 <= ny < m): # 조건 1: 맵 범위를 벗어나면 패스
            continue
        if visited[nx][ny]:    # 조건 2: 이미 방문했으면 패스
            continue
        if graph[nx][ny] == 0: # 조건 3: 갈 수 없는 곳
            continue
				# 3. 모든 조건을 통과했다면 다음 위치로 재귀 깊이 진입!
        dfs(nx, ny)
        
############### 백트래킹 #################

def dfs():
    if len(path) == M:
        print(*path)
        return

    for i in range(1, N+1):
        if not visited[i]:
            visited[i] = True
            path.append(i)        # append

            dfs()                 # dfs

            path.pop()            # pop
            visited[i] = False