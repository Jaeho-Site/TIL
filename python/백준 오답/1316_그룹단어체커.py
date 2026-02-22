""" 
1. a가 나오네? 처음 보는 글자군. (기억: a)
2. 또 a네? 방금 본 거랑 똑같으니 괜찮아.
3. b가 나오네? 처음 보는 글자군. (기억: a, b)
4. c가 나오네? 처음 보네. (기억: a, b, c)
5. 어? b가 또 나왔네? 근데 방금 본 건 c였는데? 이전에 나왔던 게 다시 나오면 탈락!

조건 A: 지금 문자가 방금 전 문자와 같다면? → 계속 진행 (연속된 상태).
조건 B: 지금 문자가 방금 전 문자와 다른데, 이미 나왔던 적이 있다면? → 그룹 단어 아님!
"""
############ 내 풀이 ############
n=int(input())
count = n
temp=0

for _ in range(n):
    word=input()
    visited=[]
    prev_idx = 0
    for idx,ch in enumerate(word):
        if idx==0:
            visited.append(ch)
            continue
        
        if ch not in visited:       # 방문 배열에 없는 경우
            visited.append(ch)
        else:                       # 방문 배열에 있는 경우
            if ch!=word[prev_idx]:  # 이전 문자와 다른 문자
                count-=1
                break
        prev_idx+=1   
print(count)

############ 내 코드를 다듬은 정답 풀이 ############
n = int(input())
count = n

for _ in range(n):
    word = input()
    for i in range(1, len(word)):
        # 지금 문자가 바로 전 문자와 다른데, 이미 앞에서 나온 적이 있다면?
        if word[i] != word[i-1] and word[i] in word[:i]:
            count -= 1
            break

print(count)

############ find를 활용한 방법 ############
n = int(input())
count = 0

for _ in range(n):
    word = input()
    # 핵심: key=word.find를 사용하면 문자가 처음 등장한 순서대로 정렬됩니다.
    if list(word) == sorted(word, key=word.find):
        count += 1

print(count)