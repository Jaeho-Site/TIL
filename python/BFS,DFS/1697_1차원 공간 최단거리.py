"""

"""
from collections import deque

def solution(numbers, target):
    answer = 0
    # 큐에 (현재까지의 합계, 사용한 숫자의 인덱스)를 담습니다.
    # 시작은 (0, 0) 즉, 합계 0에서 0번째 인덱스 숫자부터 시작하겠다는 뜻입니다.
    queue = deque([(0, 0)])
    
    while queue:
        current_sum, index = queue.popleft()
        
        # 모든 숫자를 다 사용했을 때 (인덱스가 리스트 길이와 같아짐)
        if index == len(numbers):
            # 타겟 넘버와 일치하면 정답 카운트 증가
            if current_sum == target:
                answer += 1
        else:
            # 아직 사용할 숫자가 남았다면 다음 숫자를 가져옵니다.
            number = numbers[index]
            
            # 1. 현재 합계에 다음 숫자를 더하는 경우
            queue.append((current_sum + number, index + 1))
            
            # 2. 현재 합계에서 다음 숫자를 빼는 경우
            queue.append((current_sum - number, index + 1))
            
    return answer