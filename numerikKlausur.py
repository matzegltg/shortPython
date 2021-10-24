import numpy as np
import math as m

def transpose(Q):
    for i in range(0,4):
        for j in range(0,i):
            copy = Q[i][j]
            Q[i][j] = Q[j][i]
            Q[j][i] = copy
    return Q

A = np.array([[1, 0],
                [1, 1],
                [1, 2],
                [1,3]])

b = np.array([[3], [-1], [1], [2]])

#print(A)
#print(b)
Q = np.identity(4)


for j in range(0,2):
    for i in range(j+1, 4):
        if A[i][j] != 0:
            r = m.sqrt((A[i][j]**2) + (A[j][j]**2))
            
            c = A[j][j]/r
            s = A[i][j]/r
            givens = np.identity(4)
            givens[j][j] = c
            givens[i][i] = c
            givens[i][j] = -s
            givens[j][i] = s
            
            A = np.matmul(givens, A)
           
            Q = np.matmul(givens, Q)

print()
L = Q.transpose()
r = np.matmul(L, b)
K = transpose(Q)
print(L)
print(K)
print(np.matmul(K,L))

##print(A)

#r = np.matmul(K, b)
print(r)

print(np.linalg.solve(A, b))