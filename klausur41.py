import matplotlib.pyplot as plt
import numpy as np
import math
import random

x = np.linspace(-1,1, 1000000)

def stuetzstellenpolÄQ(n, x):
    out = 1
    for i in range(0,n+1):
        out = out * (x-(((2*i)/n)-1))
    return out


def stuetzstellenpolTschebyscheff(n, x):
    out = 1
    for i in range(0,n+1):
        out = out * (x-np.cos(((2*i+1)*np.pi)/(2*(n+1))))
    return out


fig, axs = plt.subplots(1,2, sharex=True, sharey=True)
axs[0].set_title("n = 8")
axs[0].set_xlabel("x")
axs[0].set_ylabel("y")
axs[0].plot(x, stuetzstellenpolÄQ(8, x), color="green", label="äquidistant")
axs[0].plot(x, stuetzstellenpolTschebyscheff(8,x), color="red", label="tschebyscheff")
axs[0].grid()

axs[1].set_title("n = 20")
axs[1].set_xlabel("a")
axs[1].set_ylabel("y")
axs[1].plot(x, stuetzstellenpolÄQ(20, x), color="green", label="äquidistant")
axs[1].plot(x, stuetzstellenpolTschebyscheff(20,x), color="red", label="tschebyscheff")
axs[1].grid()


plt.tight_layout()
plt.show()