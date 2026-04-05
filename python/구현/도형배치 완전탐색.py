"""
6<=N,M<=10 이므로 완전탐색
도형1을 배치하고, 그 경우마다 도형2도 배치: 4중 for문
"""
def solution(board):
    N, M = len(board), len(board)
    answer = []
    
    for i in range(N - 3 + 1):
        for j in range(M - 4 + 1):
            # [(0,0),(1,0),(1,1),(1,2),(1,3),(2,0)] 레고는 뒤집을 수도 회전할 수도 없다. 고정 모양 
            lego1 = set([(i, j), (i + 1, j), (i + 1, j + 1), (i + 1, j + 2), (i + 1, j + 3), (i + 2, j)]) # O(1) 처리를 위해 set 사용
            
            # 레고 1의 점수 계산
            score = 0
            for r, c in lego1:
                score += board[r][c]
            
            lego2_score = []
            
            # 레고 1을 고정해두고 레고2 조사
            for n in range(N - 4 + 1):
                for m in range(M - 3 + 1):
                    # [(0,1),(1,1),(2,1),(3,0),(3,1),(3,2)]
                    lego2 = [(n, m + 1), (n + 1, m + 1), (n + 2, m + 1), (n + 3, m), (n + 3, m + 1), (n + 3, m + 2)]
                    
                    cur_score = 0
                    is_overlapped = False
                    
                    # lego2가 차지한 영역 점수 계산하는데 좌표가 lego1에 포함되어 있으면 break
                    for r, c in lego2:
                        if (r, c) in lego1:
                            is_overlapped = True
                            break
                        cur_score += board[r][c]
                    
                    # 안 겹쳤다면 lego2_score.append(cur_score)
                    if not is_overlapped:
                        lego2_score.append(cur_score)
            
            # 레고2 계산 중 최대값을 계산 (최소가 6이므로 겹치지 않는 경우는 무조건 있지만, 혹시 모를 빈 배열 예외처리 추가)
            if lego2_score:
                answer.append(score + max(lego2_score))
    
    return max(answer)