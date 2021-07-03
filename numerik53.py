import matplotlib.pyplot as plt
import math
import numpy as np

a = 0
b = math.pi/2
N = 10
h = (b-a)/N
x = []

def arrangeStuetz(a,N):
    for i in range(0,N):
        x.append(a+i*h)

    x.append(a+N*h)
    return x

def trapezsumme(x, N, h) -> float:
    result = 0
    for i in range(1,N):
        result += math.cos(x[i])

    result += math.cos(x[0])*1/2 
    result += math.cos(x[N]) * 1/2 

    return result*h

def simpson(x, N, h) -> float:
    result = 0


    for i in range(1,N):

        result += 2* math.cos(x[i])
        result += 4* math.cos((x[i]+x[i+1])/2)
    
    result += 4 * math.cos(x[0]+x[1]/2)
    result += math.cos(x[0])
    result += math.cos(x[N])

    return result*h/6



print(f'Trapezsumme: {trapezsumme(arrangeStuetz(a,N), N, h)}\n')
print(f'Simpsonsumme: {simpson(arrangeStuetz(a,N), N, h)}\n')

