"""
"차이 배열(Difference Array)을 이용해 구간 업데이트를 O(1)으로 처리하고, 
마지막에 누적 합(Prefix Sum)을 구하는 방식으로 시간 복잡도를 최적화했습니다."
"""
# 정석 풀이
def solution(w, h, route):
    if len(route) == 1:
        answer = [0] * (w * h)
        answer[route[0] - 1] = 1
        return answer
        
    # 가로(행), 세로(열) 방향의 누적 합을 위한 차이 배열
    # 끝나는 지점 + 1 에 -1을 기록해야 하므로 길이를 +1 씩 여유 있게 만듭니다.
    row_diff = [[0] * (w + 1) for _ in range(h)]
    col_diff = [[0] * (h + 1) for _ in range(w)]
    
    # 1. 구간별 차이 배열 기록 (O(L))
    for i in range(len(route) - 1):
        prev = route[i]
        target = route[i+1]
        
        # 1-based index를 2D 좌표(0-based)로 변환 (r=행, c=열)
        r1, c1 = divmod(prev - 1, w)
        r2, c2 = divmod(target - 1, w)
        
        if r1 == r2: # 가로 이동 (같은 행)
            c_start, c_end = min(c1, c2), max(c1, c2)
            row_diff[r1][c_start] += 1
            row_diff[r1][c_end + 1] -= 1
        else: # 세로 이동 (같은 열)
            r_start, r_end = min(r1, r2), max(r1, r2)
            col_diff[c1][r_start] += 1
            col_diff[c1][r_end + 1] -= 1
            
    # 2. 누적 합(Prefix Sum) 계산 (O(W * H))
    for r in range(h):
        for c in range(1, w):
            row_diff[r][c] += row_diff[r][c-1]
            
    for c in range(w):
        for r in range(1, h):
            col_diff[c][r] += col_diff[c][r-1]
            
    # 3. 정답 배열 생성
    answer = [0] * (w * h)
    for i in range(w * h):
        r, c = divmod(i, w)
        answer[i] = row_diff[r][c] + col_diff[c][r]
        
    # 4. 중복 방문된 경유지(waypoint) 차감
    # A->B, B->C 구간에서 B가 두 번씩 더해졌으므로, 출발지와 최종 도착지를 제외한 경유지만 1을 빼줍니다.
    for i in range(1, len(route) - 1):
        answer[route[i] - 1] -= 1
        
    return answer