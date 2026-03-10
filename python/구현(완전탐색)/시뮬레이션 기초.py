for i in range(5):
    for j in range(5):
        print('(', i,',',j, ')', end=' ')
    print()

dx = [0,-1,0,1] # x축(행) 이동량
dy = [1,0,-1,0] # y축(열) 이동량

x,y=2,2 # 현재 위치 (중심)

for i in range(4):
    nx=x+dx[i] # 다음 이동할 x좌표
    ny=y+dy[i] # 다음 이동할 y좌표
    print(nx,ny)

"""
i=0: (dx[0], dy[0]) = (0, 1)  → 우(Right) 이동
i=1: (dx[1], dy[1]) = (-1, 0) → 상(Up)    이동
i=2: (dx[2], dy[2]) = (0, -1) → 좌(Left)  이동
i=3: (dx[3], dy[3]) = (1, 0)  → 하(Down)  이동
"""