"""
처음 풀었을땐 다음과 같이 풀었음
1. 입력받은 배열의 구간합 배열을 구함
2. 구한 구간합 배열로 다시 범위 구간합을 구함
이랬더니 메모리 초과가 생김
---
두번째 풀이는 다음과 같이 해결함
1. 위처럼 d1,d2를 구하지 않고 바로 d2를 구해버림
근데도 메모리 초과 생김
---
세번째 풀이 핵심
범위값을 전부 구해버리면 사용 메모리가 너무 커짐. 
그럼 d1을 안구하는게 아니라 d2를 구하면 안됨.
그럼 방법이 있지 않을까? 를 생각하다가 그걸 못 생각함.
"정답은 %연산에 있었어."
1. 구간 합을 구한다.
2. 구간합값에 나머지 연산을 한다.
3. 나머지가 같은 것 2개를 뽑아 개수를 더한다.
---
*정석 풀이
나는 3가지 STL을 떡칠해서 풀었다. 근데 이게 의도가 맞는걸까?

"""
import sys
input=sys.stdin.readline

n,m=map(int,input().split())
nums=list(map(int,input().split()))
d=[0] # 구간합
temp=0

for num in nums:
    temp=temp+num
    d.append(temp)

d2=[]
for i in range(1,n+1):
    for j in range(i,n+1): 
        d2.append(d[j]-d[i-1])

count=0
for d in d2:
    if d%m==0:
        count+=1
print(count)

####################두번째 풀었을때####################
import sys
input=sys.stdin.readline

n,m=map(int,input().split())
nums=list(map(int,input().split()))

d=[]
for i in range(n):
    temp=0
    for j in range(i,n):
        temp=temp+nums[j]
        d.append(temp)
        
count=0
for i in d:
    if i%m==0:
        count+=1
print(count)