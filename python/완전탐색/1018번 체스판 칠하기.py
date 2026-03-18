"""
8 <= N,M <= 50
8 8
WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBBBWBW
WBWBWBWB
BWBWBWBW
WBWBWBWB
BWBWBWBW

1. 8x8을 만들어야하므로 그냥 다 돌아야 할듯
2. (0,0)부터 시작해서 
이 문제의 핵심은 일단 모든 좌표를 비교해야한다는것이고, 
함정 케이스로 짝수열과 홀수열 별로 구분해야하는 문자가 다르다는 것이다.
보드위에 8x8크기의 체스판을 이동시켜가며 모든 좌표를 비교하고 가장 작은 값을 출력하자.
"""
def d(x,y):
    case1=['W','B','W','B','W','B','W','B'] # 0 2 4 6 열
    case2=['B','W','B','W','B','W','B','W'] # 1 3 5 7 열
    count1=0
    count2=0
    # 행단위로 case2개를 모두 검사한후 min으로 최소를 찾는다.
    for i in range(8):
        for j in range(8):
            if i%2==0 : # 짝수 열 일때
                if case1[j]!=board[x+i][y+j]:
                    count1+=1
                if case2[j]!=board[x+i][y+j]:
                    count2+=1
            else : # 홀수 열 일때
                if case2[j]!=board[x+i][y+j]:
                    count1+=1
                if case1[j]!=board[x+i][y+j]:
                    count2+=1

    return min(count1,count2)   
        
n,m = map(int,input().split())
board=[list(input().strip()) for _ in range(n)]
answer=[]

# 시작 좌표 설정 
for i in range(n-7):      # 탐색 시작 열 좌표
    for j in range(m-7):  # 탐색 시작 행 좌표
        answer.append(d(i,j))
        
print(min(answer))