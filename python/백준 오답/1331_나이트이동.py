"""
1. 나이트 투어가 성립하려면 일단 입력에 중복이 있으면 안된다.
2. 나이트는 다음 인덱스 증가량이 |x+y|=3이 돼야함.(하나는 1증가, 하나는 2증가)
-> 내 코드는 순환을 생각안했음
"""
# 내풀이
route=[]
prev_x,prev_y=input()
check_prev_x=int(prev_x,16)
check_prev_y=int(prev_y,16)
Valid=True
route.append(prev_x+prev_y)

for i in range(35):
    x,y=input()
    check_x=int(x,16)
    check_y=int(y,16)
    
    if (abs(check_prev_x-check_x)==2 and abs(check_prev_y-check_y)==1) or (abs(check_prev_y-check_y)==2 and abs(check_prev_x-check_x)==1):      
        prev_x=x
        check_prev_x=check_x
        prev_y=y
        check_prev_y=check_y
        route.append(x+y)
    else:
        Valid=False
        break

if len(set(route))==36 and Valid:
    print('Valid')
else:
    print('Invalid')

#######################정답코드########################
import sys
route = []
for _ in range(36):
    route.append(sys.stdin.readline().strip())

valid = True
if len(set(route)) != 36:
    valid = False

if valid:
    for i in range(36):
        curr = route[i]
        nxt = route[(i + 1) % 36]
 
        curr_x, curr_y = ord(curr[0]), ord(curr[1])
        nxt_x, nxt_y = ord(nxt[0]), ord(nxt[1])
        
        dx = abs(curr_x - nxt_x)
        dy = abs(curr_y - nxt_y)

        if not ((dx == 1 and dy == 2) or (dx == 2 and dy == 1)):
            valid = False
            break

if valid:
    print("Valid")
else:
    print("Invalid")