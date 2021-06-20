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

def getaaccN(x, y):
    aa = []
    for i in range(0,26):
        if i == 0:
            #tau1 - tau0
            h0 = math.sqrt((x[1]-x[0])**2 + (y[1]-y[0])**2)
            aa.append(1/h0)
        else:
            h = math.sqrt((x[i+1]-x[i])**2 + (y[i+1] - y[i])**2)
            aa.append(1/h)
    
    return aa

def getbbN(x, y):
    bb = []
    for i in range(0,27):
        if i == 0:
            h0 = math.sqrt((x[1]-x[0])**2 + (y[1]-y[0])**2)
            bb.append(2/h0)
        elif i == 26:
            h = math.sqrt((x[i]-x[i-1])**2 + (y[i] - y[i-1])**2)
            bb.append(2/h)
        
        else:
            h0 = (x[i]-x[i-1])**2 + (y[i]-y[i-1])**2
            h1 = math.sqrt((x[i+1]-x[i])**2 + (y[i+1]-y[i])**2)
            val = 2/h0 + 2/h1
            bb.append(val)
    
    return bb


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

def getVecN(x, y, values):
    vec = []
    for i in range(0,27):
        if i == 0:
            vec.append(3 * (values[1]-values[0])/((x[1]-x[0])**2 + (y[1]-y[0])**2))
            
        elif i == 1:
            vec.append(3 * (values[1]-values[0])/((x[1]-x[0])**2 + (y[1]-y[0])**2) + 3 * (values[2]-values[1])/(((x[2]-x[1])**2 + (y[2]-y[1])**2)))
            
        elif i == 26:
            vec.append(3 * (values[26]-values[25])/(x[i]-x[i-1])**2 + (y[i] - y[i-1])**2)
            
        else:
            val = 3 * (values[i-1]-values[i-2])/((x[i-1]-x[i-2])**2 + (y[i-1]+y[i-2])**2) + 3 * (values[i]-values[i-1])/((x[i]-x[i-1])**2 + (y[i]+y[i-1])**2)
            vec.append(val)
    return vec

values = numpy.genfromtxt('dino.csv', delimiter = ';')
x = values[:,0]
y = values[:,1]

tau = []
for i in range(0,27):
    tau.append(i)


aa = getaaccN(x,y)
cc = getaaccN(x,y)
bb = getbbN(x,y)
dd = getVecN(x, y,x)


xx = solve(aa, bb, cc, dd)

a2=numpy.array(aa); b2=numpy.array(bb); c2=numpy.array(cc); d2=numpy.array(dd)
x2 = solve(a2, b2, c2, d2)
print(a2, b2, c2, d2)
# ganze Matrix aufstellen
AA = numpy.diag(aa, -1)+numpy.diag(bb)+numpy.diag(cc, 1) 
# Ausgaben
print("A:\n", AA)
print("d: ", dd)
print("x: ", xx)

def interPolEqual():
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

def interPolSqrt():
    tauN = [0]
    for i in range(1,27):
        newTau = math.sqrt((x[i] - x[i-1])**2 + (y[i]-y[i-1])**2) + tauN[i-1]
        print(newTau)
        tauN.append(newTau)
    
    print(tauN)
    print(len(tauN))
    yAbl = [-3.19892513e-01,  6.39785027e-01,  2.31839631e-01,  9.44813935e-01,
    -2.88240988e-01,  3.46003253e-01, -2.15565821e-01,  9.13816586e-02,
    1.40663190e-02,  1.53608874e-03, -1.13741110e-03,  1.70958099e-03,
    1.94207380e-02, -3.75537788e-03, -3.23223576e-03, -3.23923832e-04,
    -4.35270560e-03, -7.65572007e-03, -1.50366290e-02, -1.46410351e-02,
    -4.23253713e-02,  6.91374654e-04, 5.29630781e-02, -3.04656432e-02,
    1.81951879e-01, -6.17268747e-01,  1.71488437e+00]
    xAbl = [-1.18109676e+00, -6.37806485e-01, -2.13854469e+00,  2.95673959e-01,
    -9.33535259e-02, -2.91575743e-02, -4.91435811e-01,  5.31055608e-02,
    1.65579270e-01,  1.11717890e-02,  3.67957168e-02,  6.23247578e-03,
    -3.28589782e-03,  2.92331983e-02, -1.14683878e-03, -3.82662399e-03,
    -1.19650397e-03, -7.26156179e-03, -9.77493909e-03,  1.49467278e-02,
    -1.83329521e-02, -1.92031017e-02,  4.89006338e-02, -1.37897794e-01,
    5.98137625e-01, -1.58401110e+00, 5.47950555e+00]

    t = numpy.linspace(0,57,15000)
    xvaluesN = []
    yvaluesN = []

    for elem in t:
        xvaluesN.append(stueckweise_hermite(elem, tauN, x, xAbl, 0))

    for elem in t:
        yvaluesN.append(stueckweise_hermite(elem, tauN, y, yAbl, 0))
    return xvaluesN, yvaluesN


f, g = interPolEqual()
xN, yN = interPolSqrt()
plt.grid()
plt.plot(f,g, label = "Spline mit taui = i")
plt.plot(xN, yN, label = "Spline mit anderen taui")
plt.plot(x,y, "bo")
#plt.plot(t, yvalues, label = "Spline für y")
plt.ylabel('f(x)')
plt.xlabel('x')
plt.axis( [0,20, 0, 10] )
plt.legend()
plt.title("Zeichnung von Spline")
plt.show()