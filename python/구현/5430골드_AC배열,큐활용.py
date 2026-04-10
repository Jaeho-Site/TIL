"""
R은 배열에 있는 수의 순서를 뒤집는 함수 
D는 첫 번째 수를 버리는 함수

1. 배열을 뒤집을 필요가 있을까?
popleft가 정상일때
pop은 뒤집었을때
"""
import sys
from collections import deque
input=sys.stdin.readline

T=int(input().strip())
for _ in range(T):
    # 전처리
    p=input().strip()
    n=int(input())
    string=(input().strip())#[1:2*n] 1차 디버깅으로 해결
    l=len(string)
    string=string[1:l-1] # string[1:-1] 파이썬틱한 코드
    
    # print(string) -> 전처리도 하나의 핵심이었다. 디버깅 중단점 1
    
    arr=deque(string.split(',')) # 여기도 n==0인거랑 조건문처리하면 좋을듯
    if n==0: arr=deque()   
    
    is_reverse=False
    flag=False
    #print(arr) -> 이번엔 배열도 잘만들어졌는지 확인 디버깅 중단점 2

    # 함수 작업 수행
    for cmd in p: # RDD
        if cmd=='R':
            is_reverse=not is_reverse
        else: # 'D' 인 경우
            if not arr: # 배열이 비었으면 에러
                print('error')
                flag=True
                break
            else:
                if is_reverse: # 뒤집힌 상태면 pop
                    arr.pop()
                else:          # 정상이면 popleft
                    arr.popleft()
    
    if flag:
        continue
    
    if is_reverse:
        arr=list(arr) # arr.reverse() 데큐에서 지원하는 뒤집기 함수
        arr=arr[::-1]
        print(f'[{",".join(arr)}]')   
    else:
        print(f'[{",".join(arr)}]')
    # break #한번씩 테스트 케이스를 넣어가며 확인 디버깅 중단점 3