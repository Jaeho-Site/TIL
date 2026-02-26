"""
b배열을 정렬하지 않고, a배열을 b값에 맞게 인덱스에 대응시켜야함.
-> 문제가 아쉬운게 a배열을 함께 출력하라고 했으면 좋았을듯 
왜냐면 a.sort(), b.sort(reverse=False) 두개 곱하면 정답임.

핵심 : a의 가장 최대값으로 b의 최소값으로 매칭해야함
새로운 a배열을 선언, b의 max를 찾고 인덱스를 찾는다. -> 그 인덱스에 a를 넣는다.

"""
n=int(input())
a=list(map(int,input().split()))
b=list(map(int,input().split()))
c=[]
for i in b:
    c.append(i)
sorted_a=[0]*n

for i in range(n):
    cur_num=max(b)
    min_a=min(a)
    cur_idx=b.index(cur_num)
    sorted_a[cur_idx]=min_a
    b[cur_idx]=-1
    a.remove(min_a)

count=0
for i,j in zip(sorted_a,c):
    count+=i*j    
print(count)