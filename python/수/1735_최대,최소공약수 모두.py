"""
분수의 합인데 기약분수까지 써야함.
"""
import sys
import math
input=sys.stdin.readline
a,b=map(int,input().split())
c,d=map(int,input().split())

parent=math.lcm(b,d)
child=parent//b*a + parent//d*c

_gcd=math.gcd(parent,child)
print(child//_gcd,parent//_gcd)