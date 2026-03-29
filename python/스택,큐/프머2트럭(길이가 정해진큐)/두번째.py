"""
두번째 풀었을 때 테스트 케이스 하나를 통과하지 못했는데, 
이유가 트럭을 싣는 행동을 트럭시간(있던 트럭이 나갈시간)전에 해버려서 다리건너는 정답시간이 초과됨.

"""

from collections import deque

def solution(bridge_length, weight, truck_weights):
    time=0; bridge=deque(); truck=deque()
    for t in truck_weights: truck.append((t,0)) # 트럭 무게와 다리진입 시간
    cur_weight=0

    while True:
        time+=1
        print(time,bridge)
        # 대기 트럭을 다리에더 올라갈수있으면 올라가기
        if (truck and bridge_length > len(bridge)
            and (truck[0][0]+cur_weight)<=weight):
            cur_weight+=truck[0][0]
            x,y=truck.popleft()
            bridge.append((x,y))        

        # 다리의 모든 트럭 시간 1씩 늘려주기
        for i in range(len(bridge)):
            bridge[i]=(bridge[i][0],bridge[i][1]+1)
        
        if bridge[0][1]>bridge_length:
            cur_weight-=bridge[0][0]
            bridge.popleft()
   
        # 다리에도 없고 트럭도 없다면 끝
        if not bridge and not truck:
            return time