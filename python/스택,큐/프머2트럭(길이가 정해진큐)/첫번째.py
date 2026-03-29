""" 
계속 deque index error가 생겨서 디버깅하는데 시간이 오래걸림.
1. 프머 환경(def)으로 푸는 습관이 아직 잘 안되어있음.
2. 프머 환경에서의 디버깅과정이 익숙치 않음

"""

from collections import deque

def solution(bridge_length, weight, truck_weights):
    time=0; bridge=deque(); truck=deque()
    for t in truck_weights: truck.append((t,0)) # 트럭 무게와 다리진입 시간
    cur_weight=0

    while True:
        time+=1
        # 대기 트럭을 다리에더 올라갈수있으면 올라가기
        if truck and (truck[0][0]+cur_weight)<=weight:
            cur_weight+=truck[0][0]
            x,y=truck.popleft()
            bridge.append((x,y))
        
        # 다리의 모든 트럭 시간 1씩 늘려주기
        for i in range(len(bridge)):
            bridge[i][1]+=1
            # 트럭이 다리를 넘어갈 시간이면 pop해버리기
            if bridge[i][1]>bridge_length:
                cur_weight-=truck[i][0]
                bridge.popleft()
        # 다리에도 없고 트럭도 없다면 끝
        if not bridge and not truck:
            return time