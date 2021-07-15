import math as m

h = m.pi/2
m = 3
a = 0
b = 1
T = []
x = []

def g(x):
    return m.cos(x)


def arrangeStuetz(a,N):
    h = (b-a)/N
    for i in range(0,N):
        x.append(a+i*h)

    x.append(a+N*h)
    return x

def trapezsumme(x, N, a, b) -> float:
    x = arrangeStuetz(a, N)
    result = 0
    # print(f'Stuetzstellen: {N}, {x} ')
    for i in range(1,N):
        result += g(x[i])

    result += g(x[0])*1/2 
    result += g(x[N]) * 1/2 

    return result*(b-a)/N
