"""
A<=B<=50
A의 앞에 아무 알파벳이나 추가한다.
A의 뒤에 아무 알파벳이나 추가한다.
이때, A와 B의 길이가 같으면서, A와 B의 차이를 최소로 하는 프로그램을 작성하시오
-> 부분문자열? 이라기엔 인덱스까지 같아야함.

[첫번째 생각] a를 b처럼 직접 만들어보기
0. a가 b의 부분 문자열이면 0을 출력한다.
1. 길이가 다르면 b랑 같은 문자로 a에 앞 뒤 두번 다 붙여보자.
2. 이제 인덱스 돌면서 하나하나 계산한다.
---
[두번째 생각] a의 서브스트링을 b와 비교
1. a의 서브 스트링의 배열을 구하고 
2. b의 길이에서 a의 길이를 뺀값을 더한다.
 ---
 [정답] 슬라이딩으로 처리(a를 b위에서 슬라이딩)
1. A 를 B의 부분 문자열 중 하나라고 가정한다.
2. A와 길이가 같은 B의 모든 구간을 다 뒤져본다.
3. 그중 글자가 가장 많이 겹치는 곳을 고른다.
4. 나머지 빈칸은 B와 똑같이 채운다고 가정하면 차이는 0이 되므로 무시한다. 
"""
a,b=input().split()
max_len=0

for i in range(len(a)):
    print(a[0:i+1])
    if a[0:i+1] in b:
        max_len=i+1
print(max_len)

###################################3
a,b=input().split()

if a in b:
    print(0)
else :
    fa=''
    ba=''
    fa_count=0
    ba_count=0
    b_len=len(b)
    a_len=len(a)

    for i in range(b_len-a_len):
        fa+=b[i]
        ba+=b[a_len+i]

    a=fa+a
    for a_ch,b_ch in zip(a,b):
        if a_ch==b_ch:
            fa_count+=1
    a=a+ba
    for a_ch,b_ch in zip(a,b):
        if a_ch==b_ch:
            ba_count+=1       
    print(b_len-max(ba_count,fa_count))

##################################################
import sys

# A와 B 입력 받기
a, b = sys.stdin.readline().split()

# 결과(최소 차이)를 저장할 변수. 최대값인 B의 길이로 초기화
min_diff = len(b)

# B 안에서 A가 시작할 수 있는 모든 위치를 탐색
# 예: len(b)=8, len(a)=3 이면 i는 0부터 5까지 (8-3=5)
for i in range(len(b) - len(a) + 1):
    count = 0
    # 현재 위치(i)에서 A와 B의 글자를 하나씩 비교
    for j in range(len(a)):
        if a[j] != b[i + j]:
            count += 1
    
    # 전체 위치 중 가장 작은 차이값을 갱신
    if count < min_diff:
        min_diff = count

print(min_diff)