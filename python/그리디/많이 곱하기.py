# S 0~9

s = list(map(int, input()))

## 0,1이있다면 더한다. 02984
result = s[0]

for i in range(1,len(s)):
    if s[i] in [0, 1] or result in [0,1]:
        result += s[i]
    else : 
        result =  result * s[i]
        
print(result)

    

