n=int(input())
rainbow=['ChongChong']

for _ in range(n):
    a,b=input().split()
    if a in rainbow and b not in rainbow:
        rainbow.append(b)
    elif a not in rainbow and b in rainbow:
        rainbow.append(a)

print(len(rainbow))  