"""
참가자의 수 N, 김지민의 번호, 임한수의 번호

인접할때 싸움
N은 부전승
다음 라운드 -> 처음 번호의 순서를 유지하면서 1번부터 매긴다
16 8 9
4

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
->
2 4 6 8 10 12 14 16
-> 4,5

둘이 만난다 = 1차이 나면서, 작은 수가 홀수일 경우
다음 라운드에서 짝수는 절반이 되고, 홀수는 절반 +1이 된다.

"""
n, kim, lim = map(int,input().split()) 
round=1

while True:
    if abs(kim-lim)==1 and min(kim,lim)%2 != 0:
        print(round)
        break
    round+=1
    
    if kim%2==0:
        kim//=2
    else :
        kim=kim//2+1
        
    if lim%2==0:
        lim//=2
    else :
        lim=lim//2+1
        
# 정답 코드
n, kim, lim = map(int, input().split())
round = 0

while kim != lim:
    kim = (kim + 1) // 2
    lim = (lim + 1) // 2
    round += 1

print(round)