n=int(input())
enter=input()
target='ENTER'
answer=0
human=[]

for _ in range(n-1):
    cur=input()
    if cur==target:
        answer+=len(list(set(human)))
        human=[]
    else :
        human.append(cur)
    
answer+=len(list(set(human)))
print(answer)