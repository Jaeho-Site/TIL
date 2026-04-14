"""
위치가 X일 때 
걷는다면 1초 후에 X-1 또는 X+1로 이동
순간이동을 하는 경우에는 0초 후에 2*X의 위치로 이동
---
수학적으론 *2, -1, +1 순서로 배치하면 정답은 맞다. 
하지만 visited배열을 True/False로 둔다는것은 논리가 맞지는않다. 
visited배열을 False대신 -1로 초기화시키고, 시간이 적게 걸린것만 저장하게
하는것이 맞다.
"""
### 정석 풀이
import sys
from collections import deque
input = sys.stdin.readline

N, K = map(int, input().split())
# True/False 대신 도달하는 데 걸린 최소 시간을 저장 (-1은 미방문)
dist = [-1] * 100001 

if N == K:
    print(0)
    sys.exit()

q = deque([(N, 0)])
dist[N] = 0

while q:
    cur, time = q.popleft()
    if cur == K: 
        print(time)
        break
    
    # 1. 순간이동 (*2)
    # 미방문이거나, 기존에 기록된 시간보다 현재 경로가 더 빠를 경우 갱신
    if cur * 2 <= 100000 and (dist[cur * 2] == -1 or dist[cur * 2] > time):
        dist[cur * 2] = time
        q.appendleft((cur * 2, time))
        
    # 2. 걷기 (+1)
    if cur + 1 <= 100000 and (dist[cur + 1] == -1 or dist[cur + 1] > time + 1):
        dist[cur + 1] = time + 1
        q.append((cur + 1, time + 1))
    
    # 3. 걷기 (-1)
    if cur - 1 >= 0 and (dist[cur - 1] == -1 or dist[cur - 1] > time + 1):
        dist[cur - 1] = time + 1
        q.append((cur - 1, time + 1))
        
        
        
        
### 내 풀이
import sys
from collections import deque
input = sys.stdin.readline

N,K=map(int,input().split())
visited=[False]*100001
if N==K:print(0); sys.exit()

q=deque([(N,0)])
visited[N]=True

while q:
    cur,time=q.popleft()
    if cur==K: print(time); break
    
    if cur*2<=100000 and not visited[cur*2]:
        q.appendleft((cur*2,time))
        visited[cur*2]=True
    
    if cur-1>=0 and not visited[cur-1]:
        q.append((cur-1,time+1))
        visited[cur-1]=True
         
    if cur+1<=100000 and not visited[cur+1]:
        q.append((cur+1,time+1))
        visited[cur+1]=True