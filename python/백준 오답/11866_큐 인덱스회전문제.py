"""(1 ≤ K ≤ N ≤ 1,000)
1 2 3 4 5 6 7

1. 순환 인덱스 연산을 통해 다음 정답 배열에 넣을 것을 찾는다
2. 타겟을 찾아서 정답 배열에 넣고 배열에서 삭제한다.
----
* 놓친 부분 : 배열에서 pop연산을 하면 다른 인덱스들도 한개씩 당겨진다는 사실

"""
# deque를 사용한 정석 풀이
from collections import deque

n = 7
k = 3

q = deque([1, 2, 3, 4, 5, 6, 7])
result = []

while q:
    # k-1칸만큼 왼쪽으로 회전시킵니다. (앞의 2명이 맨 뒤로 감)
    q.rotate(-(k - 1)) 
    
    # 이제 맨 앞에 있는 사람이 k번째 사람이므로 빼서 정답에 넣습니다.
    result.append(q.popleft())

print(result) # [3, 6, 2, 7, 5, 1, 4]


########### 내 풀이 처럼 %길이 연산으로 풀때의 정답 코드 #############
n, k = map(int, input().split())

num = [i for i in range(1, n + 1)]
answer = []
# 시작 인덱스는 0부터 출발합니다.
idx = 0 

while num:
    # 1. 이동할 인덱스 계산: 현재 위치에서 (k - 1)만큼 이동합니다.
    # 2. 리스트의 범위를 넘어가면 원형으로 돌아오도록 len(num)으로 나눈 나머지를 구합니다.
    idx = (idx + (k - 1)) % len(num)
    
    # 해당 위치의 사람을 빼서 정답 리스트에 넣습니다.
    # pop()이 실행되는 순간 num의 길이는 1 줄어들고, 다음 턴의 len(num)에 자동으로 반영됩니다.
    answer.append(num.pop(idx))
print("<" + ", ".join(map(str, answer)) + ">")


# 틀린 내 풀이
n,k=map(int,input().split())

num=[i for i in range(1,n+1)]
answer=[]
cur_idx=k-1
nxt_idx=k-1
count=0
while num:
    answer.append(num[idx])
    idx=(idx+k) % (n-count)
    num.pop(idx)
      
print(answer)