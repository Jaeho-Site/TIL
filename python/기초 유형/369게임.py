n = int(input())

arr=[3,6,9]

for i in range(1,n+1):
    if i%10 in arr:
        print('X', end=' ')
    else:
        print(i, end=' ')