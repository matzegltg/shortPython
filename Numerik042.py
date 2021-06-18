import numpy
from numpy import copy
import matplotlib.pyplot as plt

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
    
tau = [0,2,4,6,8,10,12,14,16]   
y = [0,0,0,0,1,0,0,0,0]
aa = [0.5]*8
cc = [0.5]*8
bb = [1, 2, 2, 2, 2, 2, 2, 2, 1]
dd = [0, 0, 0, 0.75, 0, -0.75, 0, 0, 0]
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

x = [-0.01546392,  0.03092784, -0.10824742,  0.40206186,  0., -0.40206186,
  0.10824742, -0.03092784,  0.01546392]


x = numpy.linspace(0,16,50000)
yvalues = []
yablvalues = []
yablablvalues = []
for elem in x:
    yvalues.append(stueckweise_hermite(elem, tau, y, x, 0))

for elem in x:
    yablvalues.append(stueckweise_hermite(elem, tau, y, x, 1))

for  elem in x:
    yablablvalues.append(stueckweise_hermite(elem, tau, y, x, 2))

plt.grid()
plt.plot(x,yvalues, label = "Spline")
plt.plot(x, yablvalues, label = "erste Ableitung vom Spline")
plt.plot(x, yablablvalues, label = "zweite Ableitung vom Spline")
plt.ylabel('f(x)')
plt.xlabel('x')
plt.axis( [0,16, -2, 2] )
plt.legend()
plt.title("Zeichnung von Spline")
plt.show()