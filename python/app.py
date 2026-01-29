# import sys

# data = sys.stdin.readline().rstrip()
# data2 = list(map(int,input().split()))
# print(data)

array = [('gildong',50),('chulsu', 32),('minjae',74)]

def my_key(x):
    return x[1]

print(sorted(array,key=my_key))
print(sorted(array,key=lambda x:x[1]))