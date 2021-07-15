import matplotlib.pyplot as plt
import numpy as np
import math as mth

def explizitEuler(a, b, p0, h, n):
    t = [0]
    y = [p0]
    for i in range(0, n):
        t.append(t[i]+h)
        y.append(y[i]+h*(a*y[i]-b*y[i]**2))
    
    return t,y

def heun(a,b,p0,h,n):
    t = [0]
    y = [p0]
    
    for i in range(0,n):
        t.append(t[i]+h)
        ytilde = y[i] + h*(a*y[i]-b*y[i]**2)
        y.append(y[i] + h/2 * ((a*y[i]-b*y[i]**2) + (a*ytilde - b*ytilde**2)))
    
    return t, y

def aufgabeA():
    t1, y1 = explizitEuler(a=2, b=0.01, p0=1, h=0.01, n=1000)
    t20, y20 = explizitEuler(a=2, b=0.01, p0=20, h=0.01, n=1000)
    t100, y100 = explizitEuler(a=2, b=0.01, p0=100, h=0.01, n=1000)
    t200, y200 = explizitEuler(a=2, b=0.01, p0=200, h=0.01, n=1000)
    t400, y400 = explizitEuler(a=2, b=0.01, p0=400, h=0.01, n=1000)


    # Lösung mit p0 = 1
    #t = np.linspace(0,10, 1000)
    #y = 2/(0.01+(2-0.01)*np.exp(-2*t))

    #plt.plot(t, y, "--", color = "grey", label = "solution for p0 = 1")
    plt.plot(t1, y1, label = "p0 = 1")
    plt.plot(t20, y20, label = "p0 = 20")
    plt.plot(t100, y100, label = "p0 = 100")
    plt.plot(t200, y200, label = "p0 = 200")
    plt.plot(t400, y400, label = "p0 = 400")
    plt.title("Aufgabe 6a")
    plt.xlabel('t')
    plt.ylabel('y(t)')
    plt.legend(loc="lower right")
    plt.grid(True)

    plt.show()

def aufgabeAHeun():
    t1, y1 = heun(a=2, b=0.01, p0=1, h=0.01, n=1000)
    t20, y20 = heun(a=2, b=0.01, p0=20, h=0.01, n=1000)
    t100, y100 = heun(a=2, b=0.01, p0=100, h=0.01, n=1000)
    t200, y200 = heun(a=2, b=0.01, p0=200, h=0.01, n=1000)
    t400, y400 = heun(a=2, b=0.01, p0=400, h=0.01, n=1000)


    # Lösung mit p0 = 1
    #t = np.linspace(0,10, 1000)
    #y = 2/(0.01+(2-0.01)*np.exp(-2*t))

    #plt.plot(t, y, "--", color = "grey", label = "solution for p0 = 1")
    plt.plot(t1, y1, label = "p0 = 1")
    plt.plot(t20, y20, label = "p0 = 20")
    plt.plot(t100, y100, label = "p0 = 100")
    plt.plot(t200, y200, label = "p0 = 200")
    plt.plot(t400, y400, label = "p0 = 400")
    plt.title("Aufgabe 6a - Verfahren von Heun")
    plt.xlabel('t')
    plt.ylabel('p(t)')
    plt.legend(loc="lower right")
    plt.grid(True)

    plt.show()
    

def aufgabeB():
    t1, y1 = explizitEuler(a=2, b=0.01, p0=1, h=0.01, n=2000)
    t20, y20 = explizitEuler(a=2, b=0.01, p0=1, h=0.1, n=200)
    t100, y100 = explizitEuler(a=2, b=0.01, p0=1, h=0.5, n=40)
    t200, y200 = explizitEuler(a=2, b=0.01, p0=1, h=1, n=20)



    # Lösung mit p0 = 1
    t = np.linspace(0,10, 1000)
    y = 2/(0.01+(2-0.01)*np.exp(-2*t))

    plt.plot(t, y, "--", color = "grey", label = "solution for p0 = 1")
    plt.plot(t1, y1, label = "h = 0.01")
    plt.plot(t20, y20, label = "h = 0.1")
    plt.plot(t100, y100, label = "h = 0.5")
    plt.plot(t200, y200, label = "h = 1")

    plt.title("Aufgabe 6b")
    plt.xlabel('t')
    plt.ylabel('p(t)')
    plt.legend(loc="lower right")
    plt.grid(True)

    plt.show()

def aufgabeBHeun():
    t1, y1 = heun(a=2, b=0.01, p0=1, h=0.01, n=2000)
    t20, y20 = heun(a=2, b=0.01, p0=1, h=0.1, n=200)
    t100, y100 = heun(a=2, b=0.01, p0=1, h=0.5, n=40)
    t200, y200 = heun(a=2, b=0.01, p0=1, h=1, n=20)



    # Lösung mit p0 = 1
    t = np.linspace(0,10, 1000)
    y = 2/(0.01+(2-0.01)*np.exp(-2*t))

    plt.plot(t, y, "--", color = "grey", label = "solution for p0 = 1")
    plt.plot(t1, y1, label = "h = 0.01")
    plt.plot(t20, y20, label = "h = 0.1")
    plt.plot(t100, y100, label = "h = 0.5")
    plt.plot(t200, y200, label = "h = 1")

    plt.title("Aufgabe 6b - Verfahren von Heun")
    plt.xlabel('t')
    plt.ylabel('p(t)')
    plt.legend(loc="lower right")
    plt.grid(True)

    plt.show()

def aufgabeC():
    nachse = []
    fehler = []
    fehlerHeun = []
    p3 = 2/(0.01+(2-0.01)*mth.exp(-2*3))

    for i in range(5,21):
        n = 2**i
        h = 3/n
        nachse.append(n)
        p0 = 1
        b = 0.01
        a = 2
        t1, y1 = explizitEuler(a, b, p0, h, n)
        err = abs(y1[2**i] - p3)
        fehler.append(err)
    
    nachse = []
    for i in range(5,21):
        n = 2**i
        h = 3/n
        nachse.append(n)
        p0 = 1
        b = 0.01
        a = 2
        t1, y1 = heun(a, b, p0, h, n)
        err = abs(y1[2**i] - p3)
        fehlerHeun.append(err)
    
    plt.plot(nachse, fehler, "o-", label = "expliziter Euler Fehler")
    plt.plot(nachse, fehlerHeun, "o-", label = "Heun Fehler")

    # Lösung mit p0 = 1
    #t = np.linspace(0,10, 1000)
    # y = 2/(0.01+(2-0.01)*np.exp(-2*t))

    plt.title("Aufgabe 6c - Fehlervergleich")
    plt.xlabel('n')
    plt.xscale('log')

    plt.ylabel('fehler')
    plt.yscale('log')
    plt.legend(loc="lower right")
    plt.grid(True)

    plt.show()


def aufgabeCgraphs():
    
    nachse = []
    fehler = []
    p3 = 2/(0.01+(2-0.01)*mth.exp(-2*3))

    for i in range(5,21):
        
        n = 2**i
        h = 3/n
        nachse.append(n)
        p0 = 1
        b = 0.01
        a = 2
        t1, y1 = explizitEuler(a, b, p0, h, n)
        err = abs(y1[2**i] - p3)
        fehler.append(err)
    
        plt.plot(t1, y1, label = f"n = {n}")

    # Lösung mit p0 = 1
    #t = np.linspace(0,10, 1000)
    # y = 2/(0.01+(2-0.01)*np.exp(-2*t))

    plt.title("Aufgabe 6c")
    plt.xlabel('n')
    #plt.xscale('log')

    plt.ylabel('fehler')
    #plt.yscale('log')
    plt.legend(loc="lower right")
    plt.grid(True)

    plt.show()

aufgabeC()