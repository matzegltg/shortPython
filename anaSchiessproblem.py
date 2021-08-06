import math as mth
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
# Faltungsintegral

eps = .0001
def w(x):
    if x > -1 and x < 1:     
        return 1/eps * mth.exp(1/((x/eps)**2-1))
    else:
       return x-x
    #return mth.exp(x)

def j(x):
    return abs(x)

x = np.linspace(-3, 3, 1000)

wvect = np.vectorize(w)
fig, axs = plt.subplots()
axs.set_title("Tesfunktion w")
axs.set_xlabel("x")
axs.set_ylabel("y")
axs.axis([-2,2,0,2])

print("Hallo")
axs.plot(x,wvect(x), color="green")
axs.plot(x,j(x), color="blue")
axs.plot(x, j(x)*wvect(x), color="orange")

axs.grid()

def integrand(x):
    return j(x) * wvect(x)
I = quad(integrand, -1,1)

print(I)
plt.tight_layout()
plt.show()