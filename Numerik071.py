import numpy as np


a = [1,2,3,4,5,6,7,8,9,10]

s = a[0]
c = 0

print(len(a))
for i in range(1,len(a)):
    print(i)
    t1 = a[i]-c
    t2 = s + t1
    t3 = t2 -s
    s = t2
    c = t3-t1

print(s)

untereDreiecks = np.array([[1, 0, 0, 0, 0],
                             [3, 1, 0, 0, 0],
                             [-2, 1, 1, 0, 0],
                             [-1, -1, -2, 1, 0],
                             [1,2,3,4,1]
                             ])

print(untereDreiecks)
inverseMatrix = np.ones((5,5))
def berechneInverseUD(matrix):
    for i in range(0, len(matrix)):
        for j in range(0, i):
            matrix[i][j] = -matrix[i][j]

    
    return matrix

print(berechneInverseUD(untereDreiecks))