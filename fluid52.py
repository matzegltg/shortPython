import matplotlib.pyplot as plt
import math
import numpy as np

#parameter
H0 = 3.5
q = 10.72
g = 9.81
yalt = 2/3 * 3.5
c1 = q**2/(2*g)

eps = 1


x = [0]
y = [yalt]
eps = [0.1]
itcounter = 1

while eps[itcounter-1] > 0.0001:
    yneu = math.sqrt(c1/(H0-yalt))
    eps.append((abs(yneu-yalt)/yneu))
    x.append(itcounter)
    y.append(yneu)
    itcounter+=1
    yalt = yneu

#damit der plot schöner wird
eps[0] = eps[1]
plt.plot(x,y, label='Wassertiefe')
plt.plot(x,eps, label='epsilon')
plt.xlabel('Iterationen')
plt.grid(True)
plt.legend(loc='lower right')
plt.show()