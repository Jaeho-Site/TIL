input_data = input() # 예: a1

# 1. 현재 나이트의 위치 파악
# row: 행 (숫자 1 -> 1)
row = int(input_data[1])
# col: 열 (문자 a -> 1, b -> 2 ...)
col = int(ord(input_data[0])) - int(ord('a')) + 1

# 2. 나이트가 이동할 수 있는 8가지 방향 정의 (행 변화량, 열 변화량)
steps = [
    (-2, -1), (-1, -2), (1, -2), (2, -1),
    (2, 1), (1, 2), (-1, 2), (-2, 1)
]

count = 0

# 3. 8가지 방향에 대하여 이동 가능한지 확인
for step in steps:
    # step[0]: 행 변화량(dx), step[1]: 열 변화량(dy)
    next_row = row + step[0]
    next_col = col + step[1]
    
    # 4. 해당 위치로 이동이 가능하다면 카운트 증가
    if 1 <= next_row <= 8 and 1 <= next_col <= 8:
        count += 1

print(count)