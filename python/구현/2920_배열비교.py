"""
python은 배열 == 베열이 가능하다.
아직 python 언어에 대한 이해가 부족하다
"""
# 내 풀이
nums=list(map(int,input().split()))
start=nums[0]
ascending, descending=True,True


for i in range(1,8):
    if nums[i]-start == 1:
        descending=False
    elif nums[i]-start == -1:
        ascending=False
    start=nums[i]

if ascending:
    print('ascending')
elif descending:
    print('descending')
else:
    print('mixed')   
    
#################################
nums = list(map(int, input().split()))
ascending, descending = True, True

# 1번 인덱스부터 7번 인덱스까지 돌면서 '바로 앞의 숫자'와 비교합니다.
for i in range(1, 8):
    if nums[i] > nums[i-1]:  # 앞 숫자보다 크면 내림차순은 아님
        descending = False
    elif nums[i] < nums[i-1]: # 앞 숫자보다 작으면 오름차순은 아님
        ascending = False

if ascending:
    print('ascending')
elif descending:
    print('descending')
else:
    print('mixed')
    
######################################3
nums = list(map(int, input().split()))

if nums == [1, 2, 3, 4, 5, 6, 7, 8]:
    print('ascending')
elif nums == [8, 7, 6, 5, 4, 3, 2, 1]:
    print('descending')
else:
    print('mixed')