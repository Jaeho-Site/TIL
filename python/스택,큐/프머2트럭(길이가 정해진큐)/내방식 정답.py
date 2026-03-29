"""
컨베이어 벨트(정해진 길이의) 큐 문제의 핵심은 나갈때까지 걸리는 시간임.
시간이 지남에 따라 저장된 값을 1씩 올리지말고, 애초에 저장할때부터 탈출할 시간을 명시하고 검사하면 끝
"""

from collections import deque

def solution(bridge_length, weight, truck_weights):
    time = 0
    bridge = deque()
    truck = deque(truck_weights)
    cur_weight = 0

    while True:
        time += 1

        # 1. 다리를 완전히 건넌 트럭 제거
        if bridge and bridge[0][1] == time:
            cur_weight -= bridge[0][0]
            bridge.popleft()

        # 2. 대기 트럭을 다리에 올릴 수 있으면 올리기
        if (truck
                and len(bridge) < bridge_length
                and truck[0] + cur_weight <= weight):
            cur_weight += truck[0]
            t = truck.popleft()
            bridge.append((t, time + bridge_length))  # 탈출 예정 시간

        # 3. 다리에도 없고 대기 트럭도 없다면 종료
        if not bridge and not truck:
            return time