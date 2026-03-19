"""
맨 앞의 사람만 이동이 가능하다 -> 현재 줄서있는 스택(배열)
번호표 순서대로만 통과할 수 있는 라인 -> (정답 스택)
대기열이 있는데 한번 들어가면 정답스택으로만 갈수있음 -> 대기 스택
---
* 내 생각이었던것
그냥 모든 프로세스를 
시작 스택 -> 대기 스택 -> 정답 스택으로 가도록 설정 
* 내가 놓친 히든케이스
나는 모든 start에서 pending에 넣고 그 값만 비교했었음.
근데 pending에 3이 들어있고, result에 3이들어갈 차례인데 start에서
뺀건 4라면, pending에서의 3은 충분히 result로 갈수있지만 
"4만 검사하고 있으므로" 3이 4의 밑에 깔리게되어 'Sad'를 출력하게됨.
---
1. result배열에 다시 넣을 필요없이 answer_num이 n+1에 도달했는지만 체크하면됨.
2. 일단 pending에 넣는건 okay근데, 방금 넣은 값과 원래 pending에 있던 값도 다시 체크

"""
# 히든케이스 힌트 받고 다시 푼 풀이
n=int(input())
start=list(map(int,input().split()))
start=start[::-1] # 2 3 1 4 5

pending=[] # 대기열
answer_num=1

for _ in range(n):
   pending.append(start.pop())
   
   # Start에서 뽑으면 answer가 1올라간다. 
   # 그러면 pending에 있던 값도 answer가 될수있다. -> 이걸 다시 while로 처리
   while pending and pending[-1]==answer_num:
       pending.pop()
       answer_num+=1
   
while pending:
    if pending[-1]==answer_num:
        pending.pop()
        answer_num+=1
    else:
        break
      
if answer_num==n+1:
    print('Nice')
else:
    print('Sad')

############# 초기 코드 #############
n=int(input())
start=list(map(int,input().split()))
start=start[::-1] # 2 3 1 4 5

pending=[] # 대기열
result=[] # 정답 스택
answer_num=1

for _ in range(n):
    pending.append(start.pop()) # 우선 start에서 pending으로 사람이동
    if pending[-1]==answer_num: # 기다리는 사람중 정답순서면 기다림에서 pop
        result.append(pending.pop()) 
        answer_num+=1
   
while pending:
    if answer_num==pending.pop():
        result.append(answer_num) 
        answer_num+=1
             
if len(result)==n:
    print('Nice')
else:
    print('Sad')