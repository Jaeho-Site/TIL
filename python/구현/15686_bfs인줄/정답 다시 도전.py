import sys
from itertools import combinations as cb

input = sys.stdin.readline

N, M = map(int, input().split())
city = [list(map(int, input().split())) for _ in range(N)]

chicken, house = [], []
for i in range(N):
    for j in range(N):
        if city[i][j] == 2:
            chicken.append((i, j))
        if city[i][j] == 1:
            house.append((i, j))

answer = float('inf')

for open_chicken in cb(chicken, M):
    distance = 0
    
    for h in house: 
        min_dist = float('inf')
        for c in open_chicken:
            dist = abs(h - c) + abs(h - c)
            if dist < min_dist:
                min_dist = dist
        
        distance += min_dist
            
    answer = min(answer, distance) 

print(answer)