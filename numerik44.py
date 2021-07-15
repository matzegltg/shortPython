import numpy as np
import math as m
'''
p = 3

# result = 

a = 0
b = m.pi/2
x = []
rhSide = []

def arrangeStuetz(a,N):
    h = (b-a)/N
    for i in range(0,N):
        x.append(a+i*h)

    x.append(a+N*h)
    return x

def g(x):
    return m.cos(x)

def trapezsumme(x, N, a, b) -> float:
    x = arrangeStuetz(a, N)
    result = 0
    # print(f'Stuetzstellen: {N}, {x} ')
    for i in range(1,N):
        result += g(x[i])

    result += g(x[0])*1/2 
    result += g(x[N]) * 1/2 

    return result*(b-a)/N

rhSide.append(trapezsumme(x, 1, a, b))
x = []
rhSide.append(trapezsumme(x, 2, a, b))
x = []
rhSide.append(trapezsumme(x, 4, a, b))
x = []
rhSide.append(trapezsumme(x, 8, a, b))
print(rhSide)
result = rhSide
h = m.pi/2
coeffMatrix = [[1, h**2, h**4, h**6], [1, (h/2)**2, (h/2)**4, (h/2)**6],[1, (h/4)**2, (h/4)**4, (h/4)**6],[1, (h/8)**2, (h/8)**4, (h/8)**6]]

for i in range(0,len(rhSide)):
    rhSide[i] = 1- rhSide[i]

print(rhSide)
coeffMatrix = np.asmatrix(coeffMatrix)
print('\n ')
print(coeffMatrix)
print('\n')
cj = np.linalg.solve(coeffMatrix, rhSide)
print(cj)
'''

result = [0.7853981633974483, 0.9480594489685199, 0.9871158009727755, 0.9967851718861696]

n = 3
T = [[], []]


for k in range(0,n+1):
    T[].append(result[k])

print(T)
for j in range(1,n):
    for l in range(n,j,-1):
        T[k].append((4**l * T[k] - T[k-1])/(4**l -1))

print(T)
