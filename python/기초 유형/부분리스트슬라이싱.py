n,m=map(int,input().split())
bucket=[i for i in range(1,n+1)]

for _ in range(m):
    i,j=map(int,input().split())
    bucket[i-1:j] = bucket[i-1:j][::-1]

print(*bucket)  

# 리스트 슬라이싱으로 해결가능하지만, '투포인터' 알고리즘이다.
""" 
arr = [0, 1, 2, 3, 4, 5, 6]

i = 2
j = 5

while i < j:
    arr[i], arr[j] = arr[j], arr[i]
    i += 1
    j -= 1

print(arr)

"""