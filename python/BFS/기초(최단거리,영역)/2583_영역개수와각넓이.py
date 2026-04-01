"""
5 7 3
0 2 4 4
1 1 2 5
4 0 6 2

DFS특성상 Grid일 경우 보통 그래프를 0과1로 초기화한다.
하지만 그래프를 세팅할때 문제에선 격자(수학처럼)로 주어지고
행렬 리스트는 0,0이 좌측 상단이다. 
-> 프로그래머스 환경에선 보통 입력세팅을 신경쓰지 않아도 되므로
입력방식에 대한 정답은 보았지만 알고리즘은 풀었으므로, 오답처리 안함.
-> 수학 좌표 형식으로 주어진다? -> x,y->y,x 행과 열을 바꾸는 아이디어 가져가자.
"""
import sys
sys.setrecursionlimit(10**6)
input=sys.stdin.readline

dx=[-1,1,0,0]
dy=[0,0,-1,1]

def dfs(x,y):
    global extent
    visited[x][y]=True
    extent+=1
    
    for i in range(4):
        nx=x+dx[i]
        ny=y+dy[i]
        
        if not(0<=nx<m and 0<=ny<n):
            continue
        if visited[nx][ny] or graph[nx][ny]==1:
            continue

        dfs(nx,ny)
        
m,n,k=map(int,input().split())
graph=[[0]*n for _ in range(m)]
visited=[[False]*n for _ in range(m)]
count=0
extent=0
extents=[]

for i in range(k):
    x1,y1,x2,y2=map(int,input().split())
    for y in range(y1,y2):
        for x in range(x1,x2):
            graph[y][x]=1
      
for i in range(m):
    for j in range(n):
        if visited[i][j] or graph[i][j]:
            continue
        dfs(i,j)
        count+=1
        extents.append(extent)
        extent=0
               
print(count)
extents.sort()
for i in extents:
    print(i,end=' ')
