from collections import deque

def solution(bridge_length, weight, truck_weights):
    bridge = deque([0] * bridge_length)
    current_weight = 0
    time = 0
    truck_idx = 0
    
    while truck_idx < len(truck_weights) or current_weight > 0:
        time += 1
        # 다리 앞에서 트럭 하나 제거
        current_weight -= bridge.popleft()
        
        # 다음 트럭이 올라갈 수 있으면 올리기
        if truck_idx < len(truck_weights):
            next_truck = truck_weights[truck_idx]
            
            if current_weight + next_truck <= weight:
                bridge.append(next_truck)
                current_weight += next_truck
                truck_idx += 1
            else:
                bridge.append(0)
    
    return time