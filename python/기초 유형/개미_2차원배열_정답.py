"""
조건이 많은 구현 문제는 "동작을 말로 순서대로 적어보고" 코드를 짜자.
1. 현재 칸 색칠하기
2. 여기가 먹이였나? -> 맞으면 종료
3. 오른쪽 뚫렸나? -> 이동 (y+=1) & continue
4. 아래 뚫렸나? -> 이동 (x+=1) & continue
5. 갈 곳 없나? -> 종료
"""

import sys
input = sys.stdin.readline
board = [list(map(int, input().split())) for _ in range(10)]
x, y = 1, 1

while True:
    # 1. 현재 위치의 상태 확인 (먹이라면 종료 플래그)
    #    (주의: 문제 조건상 먹이를 먹어도 9로 바꾸고 끝내야 함)
    is_food = (board[x][y] == 2)
    
    # 2. 현재 위치 방문 표시
    board[x][y] = 9
    
    # 3. 종료 조건: 먹이를 찾았으면 멈춤
    if is_food:
        break

    # 4. 이동 로직: 오른쪽 우선, 안되면 아래, 둘 다 안되면 종료
    #    (굳이 0인지 2인지 따지지 않고 '벽(1)이 아니면' 간다고 생각하면 됨)
    if board[x][y+1] != 1:  # 오른쪽이 벽이 아니면
        y += 1
    elif board[x+1][y] != 1: # (오른쪽은 막혔고) 아래쪽이 벽이 아니면
        x += 1
    else: # 더 이상 움직일 수 없으면
        break

for row in board:
    print(*row) # 리스트의 요소를 공백으로 구분해 출력하는 파이썬 꿀팁 (*언패킹)