"""
S의 서로 다른 부분 문자열의 개수

모든 부분문자열을구하고 set해버리자
"""
s=input()
n=len(s)
count=0

for i in range(1,n+1):
    substring=set([s[j:j+i] for j in range(n-i+1)])
    count+=len(substring)
print(count)
