from collections import deque

def solution(bridge_length, weight, truck_weights):
    time=0; bridge=deque(); truck=deque()
    for t in truck_weights: truck.append((t,0)) # 트럭 무게와 다리진입 시간
    cur_weight=0

    while True:
        time+=1
        # Debug 3.1 -> 시간별로 어디서 에러생기나 확인해보니 6초에 4,5가 있던 시점, 6이 들어오는 찰나에 에러생김 -> why? 종이에 시나리오 그려보기
        """
        if time==6:
            print(bridge)
        """

        if truck and (truck[0][0]+cur_weight)<=weight:
            cur_weight+=truck[0][0]
            x,y=truck.popleft()
            bridge.append((x,y))
        
        # Debug 2 -> 배열 인덱스 에러가 생겨서 테스트케이스의 첫트럭이 잘가는지 확인했을때 잘 지나가더라
        # Tip : return으로 bridge를 찍으면 에러남. -> print하기
        """
        print(bridge) # deque([(7,0)]) deque([(7,1)]) deque([(7,2])])
        return
        """
        
        
        for i in range(len(bridge)):
            # Debug 1 -> 에러 메세지로 튜플엔 정수를 할당할수없다고 함. -> 따라서 튜플연산한곳을 찾으면됨. 
            bridge[i][1]+=1 # -> bridge[i]=(bridge[i][0],bridge[i][1]+1)

            # Debug 3.2 -> 만약 4번차가 시간 차서 bridge에서 빼버리면, bridge길이가 줄어서 인덱스 에러가 생기겠지? -> 검거
            if bridge[i][1]>bridge_length:
                cur_weight-=truck[i][0] # Debug 2.1 -> 그럼 위는 딱히 문제없는거임(애초에 넣는것밖에없음)-> truck이 아니라 bridge이어야함.
                bridge.popleft()
        
        
        # Debug 3 -> 4,5가 같이 잘 올라가는 확인하고 싶었음.(어디까지 성공하나) -> 여기까진 정상인데 다음에 에러남
        """
        if len(bridge)==2: # # deque([(4,2),(5,1)]) 
            print(bridge)
            return
        """

        if not bridge and not truck:
            return time