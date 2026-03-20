"""
등급이 P인 과목은 계산에서 제외
전공평점은 전공과목별 (학점 * 과목평점)의 합을 학점의 총합으로 나눈 값
A+,A0,B+,B0,C+,C0,D+,D0,F,P
"""
# 정석 풀이 : 이 문제는 비트마스킹을 쓰는게 권장되는 문제이다.
import sys
input = sys.stdin.readline
M = int(input().strip())
S = 0 # 세트 대신 정수 0 (이진수 0000...0000)을 사용합니다.

for _ in range(M):
    cmd = input().split()
    
    if len(cmd) == 1:
        if cmd == 'all':
            S = (1 << 21) - 1 # 1~20번째 비트를 모두 1로 만듦
        else:
            S = 0 # 모두 0으로 만듦
    else:
        op, num = cmd, int(cmd)
        
        if op == 'add':
            S |= (1 << num)
        elif op == 'remove':
            S &= ~(1 << num)
        elif op == 'check':
            print(1 if S & (1 << num) else 0)
        elif op == 'toggle':
            S ^= (1 << num)

# 내 풀이 ######################################################################
import sys
input=sys.stdin.readline
M=int(input().strip())
S=set()
for _ in range(M):
    cmd=input().split()
    if cmd[0]=='add':
        S.add(int(cmd[1]))
    elif cmd[0]=='remove':
        if int(cmd[1]) in S: S.remove(int(cmd[1]))
    elif cmd[0]=='check':
        if int(cmd[1]) in S: print(1)
        else: print(0)
    elif cmd[0]=='toggle':
        if int(cmd[1]) in S: S.remove(int(cmd[1]))
        else: S.add(int(cmd[1]))
    elif cmd[0]=='all':
        S={i for i in range(1,21)}
    else:
        S=set()
        
        