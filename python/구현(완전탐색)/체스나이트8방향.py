""" 
총 8개 방향으로 이동할 수 있는데, 보드를 나가면 안됨.
방향벡터 정의하고 보드아웃체크
"""
dx = [-2,-2,2,2,1,-1,1,-1]
dy = [1,-1,1,-1,-2,-2,2,2]

y1,x1=input()
y=ord(y1)-96
x=int(x1)
count=0
for i in range(8):
    nx = x+dx[i]
    ny = y+dy[i]
    
    if nx<1 or ny<1 or nx>8 or ny>8:
        continue
    
    count+=1
print(count)  

