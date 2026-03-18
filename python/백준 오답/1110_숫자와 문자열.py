""" 
1. 10보다 작다면 앞에 0을 붙여 두 자리 수로 만들고
2. 각 자리의 숫자를 더한다.
3. 주어진 수의 가장 오른쪽 자리 수와 앞에서 구한 합의 
가장 오른쪽 자리 수를 이어 붙이면 새로운 수를 만들 수 있다. 
"""
# 내 풀이 기반 
N = int(input())
target = N
count = 0
current = str(N)

while True:
    # 1. 10보다 작으면 앞에 0을 붙임
    if len(current) < 2:
        current = '0' + current
    
    # 2. 각 자리 숫자를 더함
    temp_sum = int(current[0]) + int(current[1])
    
    # 3. 새로운 수 만들기 (원래 수의 가장 오른쪽 + 합의 가장 오른쪽)
    # temp_sum도 문자열로 바꾸어 [-1] 인덱스로 가장 오른쪽 문자를 가져옵니다.
    current = current[-1] + str(temp_sum)[-1]
    
    # 4. 사이클 1 증가
    count += 1
    
    # 5. 새로운 수가 target과 같은지 정수로 변환하여 비교
    if int(current) == target:
        print(count)
        break

# 내풀이는 코드의 설명을 따라가지 못했다. 이해부족
N=int(input())
target=N
count=0
current=str(N)

while True:
    #길이<2 일때 0을 앞에 붙이기  
    if len(current)<2:
        current='0'+current
    
    temp=int(current[0])+int(current[1])   
    
    if temp==target:
        print(count)
        break
    
    count+=1
    if len(str(temp))<2:
        current=current[1]+str(temp)[0]
    else:
        current=current[1]+str(temp)[1]


## 수를 활용한 방법
N = int(input())
target = N
count = 0

while True:
    # 십의 자리(a)와 일의 자리(b) 구하기
    a = N // 10
    b = N % 10
    
    # 각 자리의 합(c) 구하기
    c = a + b
    
    # 새로운 수 만들기 (원래 수의 일의 자리 b * 10 + 합의 일의 자리 c % 10)
    N = (b * 10) + (c % 10)
    
    count += 1
    
    if N == target:
        print(count)
        break