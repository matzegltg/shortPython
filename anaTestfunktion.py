import matplotlib.pyplot as plt
import math
import numpy as np

x = np.linspace(-1, 1, 5000)
y = np.exp(1/(x**2 - 1))

plt.plot(x,y)
plt.show()
