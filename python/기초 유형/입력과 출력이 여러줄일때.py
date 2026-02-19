""" 
입력                    출력
3                       
ACDKJFOWIEGHE           AE
O                       OO
AB                      AB
"""
# 아래처럼 간단하게 작성가능
"""
for _ in range(int(input())):
    a=input();print(a[0]+a[-1])
"""

n=int(input())
answer=[]
for i in range(n):
    s=input()
    first=s[0]
    last=s[len(s)-1]
    answer.append(first+last)
    
for i in answer:
    print(i)
    
