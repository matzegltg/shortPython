import matplotlib.pyplot as plt
import numpy as np
import math
import random

def getRandom():
    x = random.randint(-1,1)
    if x == 0:
        getRandom()
    else:
        return x
        
def LambdaTschebyscheff(n):
    x = np.linspace(-1,1,1000)
    g = 1
    result = 0
    stuetzstellen = []
    lagrangePolynome = []

    for j in range(0,n+1):

        xj = np.cos(((2*j+1)*math.pi)/(2*(n+1)))
        stuetzstellen.append(xj)
        l = 1
        for i in range(0,n+1): 
            if j is not i:
                xi = np.cos(((2*i+1)*math.pi)/(2*(n+1)))
                l = abs(l* (x-xi)/((xj - xi)))
        
        lagrangePolynome.append(l)

        result = result + l

    print(result)
    f = result
    '''
        for i in range(0,n+1):
            g = g * (x-(2*i/n -1))
    '''
    ystuetz = []
    for i in range(len(stuetzstellen)):
        ystuetz.append(getRandom())
    
    for i in range(0,n+1):
        g = g*(x-np.cos(((2*i+1)*math.pi)/(2*(n+1))))
    
    #print(stuetzstellen)
    plt.grid()
    #plt.plot(stuetzstellen, ystuetz, "bo")
    plt.plot(x,g, label = "Tschebyscheff n = " + str(n))
    plt.plot(x,f, label = "lambda mit n = " + str(n))
    #for i in range(0,n+1):
        #plt.plot(x,lagrangePolynome[i], label ="lagrangepoly für x" + str(i), alpha = 0.5)
    #plt.plot(x,g, label = "äquidistant mit n = " + str(n))
    plt.ylabel('lambda(x)')
    plt.xlabel('x')
    plt.axis( [-1, 1, 0, 2] )
    plt.legend()
    plt.title("Lebesgue")
    plt.show()

def zwanzig():
    x = np.linspace(-1,1,100)
    #print(x)
    n = 20
    f = 1
    g = 1

    for i in range(0,n+1):
        f = f*(x-(2*i/n - 1))
    print(f)
    for i in range(0,n+1):
        g = g*(x-np.cos(((2*i+1)*math.pi)/(2*(n+1))))


    plt.axis( [-1, 1, 0, 0.00006] )
    plt.grid()
    plt.plot(x,f, label = "äquidisant mit n = " + str(n))
    plt.plot(x,g, label = "Tschebyscheff mit n = " + str(n))
    plt.ylabel('Phi(x)')
    plt.xlabel('x')
    plt.legend()
    plt.title("n = 20")
    plt.show()


def LambdaAequidistant(n):
    x = np.linspace(-1,1,1000)
    g = 1
    result = 0
    stuetzstellen = []
    lagrangePolynome = []

    for j in range(0,n+1):

        xj = (2*j/n -1)
        stuetzstellen.append(xj)
        l = 1
        for i in range(0,n+1): 
            if j is not i:
                xi = (2*i/n -1)
                l = abs(l* (x-xi)/((xj - xi)))
        
        lagrangePolynome.append(l)

        result = result + l

    print(result)
    f = result
    '''
        for i in range(0,n+1):
            g = g * (x-(2*i/n -1))
    '''
    ystuetz = []
    for i in range(len(stuetzstellen)):
        ystuetz.append(getRandom())
    
    for i in range(0,n+1):
        g = g*(x-(2*i/n -1))
    
    #print(stuetzstellen)
    print(np.max(result))
    plt.grid()
    #plt.plot(stuetzstellen, ystuetz, "bo")
    plt.plot(x,g, label = "äquidistant n = " + str(n))
    plt.plot(x,f, label = "lambda mit n = " + str(n))
    #for i in range(0,n+1):
        #plt.plot(x,lagrangePolynome[i], label ="lagrangepoly für x" + str(i), alpha = 0.5)
    #plt.plot(x,g, label = "äquidistant mit n = " + str(n))
    plt.ylabel('lambda(x)')
    plt.xlabel('x')
    plt.axis( [-1, 1, 0, 100] )
    plt.legend()
    plt.title("Lebesgue")
    plt.show()


#LambdaTschebyscheff(8)
#LambdaTschebyscheff(20)

LambdaAequidistant(8)
LambdaAequidistant(20)


