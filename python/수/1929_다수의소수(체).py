def seive(m,n):
    prime=[True]*(n+1)
    prime[0] = prime[1] = False
    
    for i in range(2,int(n**0.5)+1):
        if prime[i]:
            for j in range(i*i,n+1,i):
                prime[j]=False
    return [i for i,is_prime in enumerate(prime) if is_prime and i>=m]

m,n=map(int,input().split())

answer=seive(m,n)
for a in answer:
    print(a)