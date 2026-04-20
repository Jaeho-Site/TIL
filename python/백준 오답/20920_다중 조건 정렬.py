"""
1. 처음엔 조건문으로 접근해서 풀다가 너무 길어져서 아이디어확인
2. 아이디어가 다중 조건 정렬이어서 정답 확인
"""
# 정답 풀이
import sys
from collections import Counter

input = sys.stdin.readline

n, m = map(int, input().split())
words = []

for _ in range(n):
    word = input().rstrip()
    if len(word) >= m:
        words.append(word)

# 1. 빈도수 계산
recent = Counter(words)

# 2. 중복 제거된 단어 리스트 생성
# set(words)보다 recent.keys()가 더 깔끔합니다.
unique_words = list(recent.keys())

# 3. 다중 조건 정렬 (핵심!)
unique_words.sort(key=lambda x: (-recent[x], -len(x), x))

# 4. 출력
print('\n'.join(unique_words))

"""
자주 나오는 단어일수록 앞에 배치한다.
해당 단어의 길이가 길수록 앞에 배치한다.
알파벳 사전 순으로 앞에 있는 단어일수록 앞에 배치한다
m이상인 것들만 배치한다.

1. 최빈값 순서로 한번 정렬하고 Counter
중복삭제
2. 최빈값으로 해결이 안되는 문제다 -> 단어의 길이가 가장 긴것 순으로도 정렬하고(반복문)
3. 그래도 안된다 -> 사전순으로 정렬하고(sort)
"""
import sys
from collections import Counter
input=sys.stdin.readline

n,m=map(int,input().split())
words=[]

for _ in range(n):
    cur = input().rstrip()
    if len(cur)>=m:
        words.append(cur)
#########################################
new_words=list(set(words))
recent=Counter(words)
# if len(recent)==len(new_words): # 최빈값만으로 해결되는 문제라면 