import matplotlib.pyplot as plt
import math
import numpy as np
import sys

ig = 0.8359258237575212
errorTrapez = []
errorSimpson = []
kvalues = []

def g(x):
    return math.cos(x)+1/10  * math.cos(10*x) + 1/50 * math.cos(50*x)

def trapezsumme(x, N, h) -> float:
    result = 0
    for i in range(1,N):
        result += g(x[i])

    result += g(x[0])*1/2 
    result += g(x[N]) * 1/2 

    return result*h

def simpson(x, N, h) -> float:
    result = 0


    for i in range(1,N):

        result += 2* g(x[i])
        result += 4* g((x[i]+x[i+1])/2)
    
    result += 4 * g(x[0]+x[1]/2)
    result += g(x[0])
    result += g(x[N])

    return result*h/6

for k in range(1,20):
    N = 2**k
    a = 0
    b = 1
    h = (b-a)/N
    x = []

    for i in range(0,N):
        x.append(a+i*h)

    x.append(a+N*h)

    trapezfehler = abs(ig - trapezsumme(x,N,h))
    simpsonfehler = abs(ig - simpson(x,N,h))
    if (simpsonfehler >= sys.float_info.epsilon):
        errorSimpson.append(simpsonfehler)
    else:
        errorSimpson.append(sys.float_info.epsilon)
   
    errorTrapez.append(trapezfehler)

    kvalues.append(k)

eps = []
for i in range(len(kvalues)):
    eps.append(sys.float_info.epsilon)

plt.plot(kvalues, errorTrapez, "o-", label = "error Trapez")
plt.plot(kvalues, errorSimpson, "o-", label="error Simpson")
plt.plot(kvalues, eps, "--", color="grey", label = "epsilon")
plt.title(f"Fehlervergleichsanalyse")
plt.xlabel('k')
plt.ylabel('Fehler')
plt.legend(loc="lower right")
plt.yscale("log")
plt.grid(True)

plt.show()