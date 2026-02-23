""" 
1. 배열을 '*'문자로 초기화 해두고(반복문 돌기위해)
나중에 '*'문자를 제거한다.
"""
# 내 풀이
import sys
input = sys.stdin.readline

words = [['*']*15 for _ in range(5)]
answer=''
max_len=0

for i in range(5):
    word = input().strip()
    for j in range(len(word)):
        words[i][j]=word[j]

for i in range(15):
    for j in range(5):
        answer+=words[j][i]

answer=answer.replace('*','')
print(answer)

# 정답 풀이(아이디어) -> 미리 초기화하지않고 조건문으로 길이체크 
arr=[]
for i in range(5):
    arr.append(list(input()))

for i in range(15):
    for j in range(5):
        if i<len(arr[j]):
            print(arr[j][i],end='')