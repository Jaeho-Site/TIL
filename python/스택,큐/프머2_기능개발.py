"""
[95, 90, 99, 99, 80, 99] [1, 1, 1, 1, 1, 1]	-> [1, 3, 2]
"""
# 정석 풀이
import math

def solution(progresses, speeds):
    answer = []  
    # 1. 각 작업별 배포까지 남은 일수 계산
    days_left = [math.ceil((100 - p) / s) for p, s in zip(progresses, speeds)]
    
    # 2. 배포 그룹 묶기
    front = 0 # 현재 배포 그룹의 기준이 되는 작업 인덱스
    
    for i in range(len(days_left)):
        # 뒤에 있는 작업이 현재 기준 작업보다 오래 걸린다면
        if days_left[i] > days_left[front]:
            # 지금까지 묶인 작업들을 배포하고, 기준(front)을 갱신
            answer.append(i - front)
            front = i
            
    # 3. 마지막으로 남은 그룹 배포
    answer.append(len(days_left) - front)
    
    return answer


# 내 풀이
from collections import deque
def solution(progresses, speeds):
    p=deque(progresses)
    s=deque(speeds)
    count=0
    answer=[]
    for day in range(1,101):
        if not p: break
        
        # 첫 작업이 100이 되면
        first=p[0]+s[0]*day
        if first>=100:
            p.popleft()
            s.popleft()
            count+=1
            while p:
                next=p[0]+s[0]*day
                if next>=100:
                    p.popleft()
                    s.popleft()
                    count+=1
                else:
                    answer.append(count)
                    count=0
                    break
            if count!=0:
                answer.append(count)
                count=0
    return answer