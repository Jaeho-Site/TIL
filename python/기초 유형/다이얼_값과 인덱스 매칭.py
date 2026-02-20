""" 
A~Z : 
97~123
"""
dial = ['ABC','DEF','GHI','JKL','MNO','PQRS','TUV','WXYZ']
word = input().strip()
time = 0
for ch in word:
    for idx, w in enumerate(dial):
        if ch in w:
            time += idx + 3
            break
print(time)

# 인덱스와 아스키코드 사용
"""
# times[i] = 알파벳 chr(ord('A')+i)의 시간
times = [3,3,3,4,4,4,5,5,5,6,6,6,7,7,7,8,8,8,8,9,9,9,10,10,10,10]

s = input().strip()
ans = 0
for ch in s:
    ans += times[ord(ch)-65]
print(ans)
"""
    