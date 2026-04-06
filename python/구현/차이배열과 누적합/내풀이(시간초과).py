"""
경비원이 순찰을 도는데 지정된 라우트에 명시된 번호를 거쳐서 간다.
w,h,route가 주어지고 w는 가로, h는 세로길이이다. 
번호는 왼쪽부터 순서대로 번호가 쓰여진다. 예를들어 w가 4이고 h가 3이라면 아래같은 보드가 된다.
1 2 3 4
5 6 7 8
9 10 11 12
만약 route가 [2,10,12,8,5]라면 경비원은 2->6->10->11->12->8->7->6->5 순으로 방문하고,
경비원이 방문한 각 번호의 개수를 출력하면된다. [0,1,0,0,1,2,1,1,0,1,1,1]
인접한 라우트는 무조건 같은열이나 같은 행에 위치한다.
"""

# 내풀이
def solution(w, h, route):
    if not route:
        return []
        
    answer = [0] * (w * h)
    
    # 첫 번째 방문지 처리
    prev = route
    answer[prev - 1] += 1 
    
    # 두 번째 라우트부터 순회
    for i in range(1, len(route)):
        target = route[i]
        
        # 열(column) 이동인 경우: 두 값의 차이가 w로 나누어 떨어짐
        if abs(target - prev) % w == 0:
            answer[target - 1] += 1
            
            # 작은 값과 큰 값을 구분
            start = min(prev, target)
            end = max(prev, target)
            
            # 사이 값들(start + w 부터 end - w 까지) 방문 처리
            cur = start + w
            while cur < end:
                answer[cur - 1] += 1
                cur += w
                
        # 행(row) 이동인 경우
        else:
            answer[target - 1] += 1
            
            # 작은 값과 큰 값을 구분
            start = min(prev, target)
            end = max(prev, target)
            
            # 사이 값들(start + 1 부터 end - 1 까지) 방문 처리
            for j in range(start + 1, end):
                answer[j - 1] += 1
                
        # 다음 이동을 위해 prev 업데이트
        prev = target
        
    return answer