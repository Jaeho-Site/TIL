"""
문제가 알파벳으로만 들어오면 포켓몬 번호를 말해야 하고, 
숫자로만 들어오면, 포켓몬 번호에 해당하는 문자를 출력
---
출력 형식을 보면 key,values로 각각 조회해야한다. values를 조회하려면
for문을 돌아야하므로 차라리 key,values가 상반된 딕셔너리 하나를 더 생성해서 조회.
"""
import sys
input=sys.stdin.readline
n,m=map(int,input().split())
d={}
for i in range(1,n+1):
    name=input().strip()
    d[i]=name
    
reversed_d={v:k for k,v in d.items()}
for _ in range(m):
    problem=input().strip()
    if ord(problem[0])>=65: # 이름으로 주어질 경우
        print(reversed_d[problem])
    else: # 숫자가 주어질 경우 
        print(d[int(problem)])
        
################# 풀이 key point ################### 
# 굳이 뒤집지말고 숫자도 저장해버리자
for i in range(1, n + 1):
    name = input().strip()
    # 딕셔너리에 양방향으로 모두 저장해버립니다.
    d[name] = str(i) # 'Pikachu': '25'
    d[str(i)] = name # '25': 'Pikachu'