import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x + x**2

def aufgabeA(b):
    a = np.linspace(-1,0)
    x = (a * f(b)-b*f(a))/(f(b)-f(a))

    fig, axs = plt.subplots(1,2, sharex=True, sharey=True)
    axs[0].set_title("a and x0")
    axs[0].set_xlabel("a")
    axs[0].set_ylabel("x0")
    axs[0].axis([-1,0,-1,0])
    axs[0].plot(a,x, color="green")
    axs[0].grid()

    
    xaxis = np.linspace(-1,2)
    func = xaxis + xaxis*xaxis

    axs[1].set_title("function")
    axs[1].set_xlabel("x")
    axs[1].set_ylabel("f")
    axs[1].grid()
    axs[1].plot(xaxis, func, label="f")
    axs[1].legend(loc="upper right")

    plt.tight_layout()
    plt.show()



aufgabeA(b=2)

'''
    axs[0,0]


    ax[0].grid(True)

    ax[1].plot(xaxis, func)

    plt.tight_layout()
    plt.show()
'''