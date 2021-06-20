from kmc_withPeriodicity import doVisualizations
import numpy
from numpy import copy
import matplotlib.pyplot as plt
import math 
def solve(aa, bb, cc, dd):
    """ Thomas Algorithmus zum Loesen eines tridiagonalen Gleichungssystems
   
    aa -- N-1 Eintraege der unteren Nebendiagonale: (2,1) ... (N, N-1)
    bb -- N Eintraege der Hauptdiagonale: (1,1) ... (N,N)
    cc -- N-1 Eintraege der oberen Nebendiagonale: (1,2) ... (N-1,N)
    dd -- dd N Eintraege der rechten Seite: 1 ... N

    return xx = (diag(aa,-1)+diag(bb)+diag(cc,1))^{-1} dd
    """
    cnew = copy(cc); dnew = copy(dd); NN = len(dd)
    cnew[0] /= bb[0]
    for ii in range(1, NN-1):
        cnew[ii] /= bb[ii] - cnew[ii-1]*aa[ii-1]
    dnew[0] /= bb[0]
    for ii in range(1, NN):
        dnew[ii] -= dnew[ii-1]*aa[ii-1]
        dnew[ii] /= bb[ii] - cnew[ii-1]*aa[ii-1]
    for ii in range(NN-2, -1, -1):
        dnew[ii] -= cnew[ii]*dnew[ii+1]
    return dnew

def test():
    """ Ein Beispiel/Test
    """
    # Diagonalen
    aa = [1.0, 1.0, 1.0];
    bb = [3.0]*4
    cc = [2.0]*3
    # rechte Seite
    dd = [7., 13., 19., 15.]
    # Loesen
    xx = solve(aa, bb, cc, dd)
    print(aa, bb, cc, dd)
    a2=numpy.array(aa); b2=numpy.array(bb); c2=numpy.array(cc); d2=numpy.array(dd)
    x2 = solve(a2, b2, c2, d2)
    print(a2, b2, c2, d2)
    # ganze Matrix aufstellen
    AA = numpy.diag(aa, -1)+numpy.diag(bb)+numpy.diag(cc, 1) 
    # Ausgaben
    print("A:\n", AA)
    print("d: ", dd)
    print("x: ", xx)
    # Proben
    print("Ax:  ", numpy.dot(AA, xx))
    print("Ax-d ", numpy.dot(AA, xx)-dd)
    print("Ax2: ", numpy.dot(AA, x2))
    print("ax2-d", numpy.dot(AA, x2)-d2)

#if _name_ == '__main__':
    #test()
    
def stueckweise_hermite(xx, x_list, f_list, abl_list, abl = 0):
    """ Stueckweise Hermite-Interpolation
   
    Sei x in dem Intervall [xl,xr] := [x_list[i-1],x_list[i]] und p das kubische Polynom mit
    p(xl) = f_list[i-1], p(xr) = f_list[i],
    p'(xl) = abl_list[i-1], p'(xr) = abl_list[i]
    Die Funktion wertet p (oder dessen 1. oder 2. Ableitung) in x aus
    (falls x<x_list[0], das Polynom fuer das erste Intervall,
    falls x>x_list[-1], das Polynom fuer das letzte Intervall)
   
    xx -- Auswertestelle
    x_list -- Liste von Stuetzstellen, aufsteigend geordnet
    f_list -- Liste mit zugehoerigen Stuetzwerten
    abl_list -- Liste mit zugehoerigen Ableitungen
    x_list, f_list und abl_list muessen gleich lang sein
    abl -- 0, um Funktionswert auszuwerten, 1 fuer erste Ableitung, 2 fuer zweite Ableitung

    Ergebnis: p(x) bzw. p'(x) bzw. p''(x)
    """
    NN = len(x_list) - 1
    # Teilintervall bestimmen, in dem x liegt
    ii = 1;
    while xx>x_list[ii] and ii<NN:
        ii = ii + 1
    # Parameter fuer Hermite-Interpolation
    f_links = f_list[ii-1]
    f_rechts = f_list[ii]
    abl_links = abl_list[ii-1]
    abl_rechts = abl_list[ii]
    hh = x_list[ii] - x_list[ii-1]
    # Koordinatentransformation
    tt = (xx - x_list[ii-1]) / hh
    # Koeffizienten aus p(t(x)) = c0 + c1*t + c2*t**2 + c3**3
    c0 = f_links
    c1 = hh*abl_links
    c2 = -3.*f_links + 3.*f_rechts - 2.*hh*abl_links - hh*abl_rechts
    c3 = 2.*f_links - 2.*f_rechts + hh*abl_links + hh*abl_rechts
    # Auswerten im Horner Schema
    if abl == 0:
        return ((c3*tt + c2)*tt + c1)*tt + c0
    elif abl == 1:
        return ((3.*c3*tt + 2.*c2)*tt + c1) / hh
    elif abl == 2:
        return (6.*c3*tt + 2.*c2) / hh**2
    
def getaacc(tau):
    aa = []
    for i in range(0,26):
        aa.append(1/(tau[i+1] - tau[i]))
    return aa


def getbb(tau):
    bb = []
    for i in range(0,27):
        if i == 0:
            bb.append(2/(tau[1]-tau[0]))
        elif i == 26:
            bb.append(2/(tau[i]-tau[i-1]))
        else:
            y = 2/(tau[i]-tau[i-1]) + 2/(tau[i+1]-tau[i])
            bb.append(y)
    
    return bb

def getVec(tau, values):
    vec = []
    for i in range(0,27):
        if i == 0:
            vec.append(3 * (values[1]-values[0])/((tau[1]-tau[0])*(tau[1]-tau[0])))
            
        elif i == 1:
            vec.append(3 * (values[1]-values[0])/((2/tau[1]-tau[0])**2) + 3 * (values[2]-values[1])/((tau[2]-tau[1])**2))
            
        elif i == 26:
            vec.append(3 * (values[26]-values[25])/((2/tau[i]-tau[i-1])**2))
            
        else:
            y =  (3 * (values[i-1]-values[i-2])/((tau[i-1]-tau[i-2])**2) + 3 * (values[i]-values[i-1])/((tau[i]-tau[i-1])**2))
            vec.append(y)
    return vec

def interPolEqual(tau):
    xAbl = [-2.08661798, -0.32676405, -2.23132583,  0.25206735, -0.27694358, -2.14429301, -6.14588436, -0.27216955,  7.23456255, 2.83391934,  2.42976008,  0.94704032,
    -0.21792137,  2.92464515,  0.51934075, -2.00200817, -0.01130807, -0.95275954,
    -0.67765378,  0.66337464, -0.4758448,  -0.25999544,  0.01582657, -1.30331083,
    -0.80258326, -1.48635612,  0.74800773]

    yAbl =  [-0.78671845, 1.57343691,  0.49297082,  2.45467981,  1.68830993,  1.29208047,
    -0.8566318,   0.63444674,  1.31884484,  0.09017392, -0.1795405,  0.6279881,
    2.16758811, -0.29834054, -0.97422597, -0.3047556,  -0.80675164, -0.96823785,
    -1.32029698, -1.25057424, -1.17740608, -0.03980145,  1.33661187,  0.69335398,
    -1.11002778, -2.25324285,  1.12299917]

    t = numpy.linspace(0,26,15000)
    xvalues = []
    yvalues = []
    for elem in t:
        xvalues.append(stueckweise_hermite(elem, tau, x, xAbl, 0))

    for elem in t:
        yvalues.append(stueckweise_hermite(elem, tau, y, yAbl, 0))
    return xvalues, yvalues

def interPolSqrt(tauN): 
    print(tauN)
    #print(len(tauN))
    
    xAbl = [-1.03774564, -0.92450872, -1.46783577,  0.30621681,  0.04393505, -1.66219477,
 -1.87251703,  0.1367708,   0.69996019,  0.57640794,  1.10209875,  0.22944072,
  0.43387568,  1.42226904, -0.03407562, -0.75817964, -0.96469079, -0.61078945,
 -0.50953192,  0.55683377, -0.18078909, -0.1281951,   0.38511907, -1.52423113,
 -1.05842722, -0.67148966,  0.33810646] 
    yAbl = [-0.24635167,  0.49270334,  0.18283497,  1.01320293,  0.9035878,   0.60113786,
 -0.04801981,  0.08366525,  0.05791358,  0.15357533, -0.12660139,  0.10551172,
  1.3514673,   0.5040215,  -0.07239215, -0.44013218, -1.36215564, -0.90970243,
 -0.65604063, -0.94501791, -1.1119436,   0.3687941,   1.00873031,  0.1952025,
 -0.16486468, -1.28224466,  0.63935111]

    t = numpy.linspace(0,tauN[26],1000)
    xvaluesN = []
    yvaluesN = []

    for elem in t:
        xvaluesN.append(stueckweise_hermite(elem, tauN, x, xAbl, 0))

    for elem in t:
        yvaluesN.append(stueckweise_hermite(elem, tauN, y, yAbl, 0))
    
    stützpunkteX = []
    stützpunkteY = []
    
    print(t)
    resultpoints = []
    for elem in tauN:
        dist = 1000
        storedindex = 0
        for i in range(0,len(t)):
            if abs(t[i] - elem) < dist:
                dist = abs(t[i] - elem)
                storedindex = i
        
        resultpoints.append(storedindex)

    print(resultpoints)

    for elem in resultpoints:
        stützpunkteX.append(xvaluesN[elem])
        stützpunkteY.append(yvaluesN[elem])
    return xvaluesN, yvaluesN, stützpunkteX, stützpunkteY

def doVizualization(xtaui, ytaui, xtauN, ytauN, x,y, px, py):
    plt.grid()
    plt.plot(xtaui,ytaui, label = "Spline mit taui = i")
    plt.plot(xtauN, ytauN, label = "Spline mit anderen taui")
    plt.plot(x,y, "bo")
    plt.plot(px,py, "ro")
    #plt.plot(t, yvalues, label = "Spline für y")
    plt.ylabel('y')
    plt.xlabel('x')
    plt.axis( [-2.5,20, -1, 11] )
    plt.legend()
    plt.title("Zeichnung von Spline")
    plt.show()


values = numpy.genfromtxt('dino.csv', delimiter = ';')
x = values[:,0]
y = values[:,1]

tauN = [0]
for i in range(1,27):
    newTau = math.sqrt((x[i] - x[i-1])**2 + (y[i]-y[i-1])**2) + tauN[i-1]
    #print(newTau)
    tauN.append(newTau)

taui = []
for i in range(0,27):
    taui.append(i)

aa = getaacc(taui)
cc = getaacc(taui)
bb = getbb(taui)
dd = getVec(taui,y)


xx = solve(aa, bb, cc, dd)

a2=numpy.array(aa); b2=numpy.array(bb); c2=numpy.array(cc); d2=numpy.array(dd)
x2 = solve(a2, b2, c2, d2)
#print(a2, b2, c2, d2)
# ganze Matrix aufstellen
AA = numpy.diag(aa, -1)+numpy.diag(bb)+numpy.diag(cc, 1) 
# Ausgaben
#print("A:\n", AA)
#print("d: ", dd)
#print("x: ", xx)


xtaui, ytaui = interPolEqual(taui)
xtauN, ytauN, px, py = interPolSqrt(tauN)

doVizualization(xtaui, ytaui, xtauN, ytauN, x,y, px, py)