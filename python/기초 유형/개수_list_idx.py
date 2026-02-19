n=int(input())

num=list(map(int,input().split()))
answer=[0 for i in range(24)]

for i in num:
    answer[i]+=1

for i in range(1,24):
    print(answer[i],end=' ')