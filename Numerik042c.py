import numpy
from numpy import copy
import matplotlib.pyplot as plt
import scipy.integrate as integrate
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
        if i == 26:
            bb.append(2/tau[i]-tau[i-1])
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


values = numpy.genfromtxt('dino.csv', delimiter = ';')
x = values[:,0]
y = values[:,1]
tau = []
for i in range(0,27):
    tau.append(i)

aa = getaacc(tau)
cc = getaacc(tau)
bb = getbb(tau)
dd = getVec(tau,x)

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