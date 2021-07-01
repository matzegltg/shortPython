import matplotlib.pyplot as plt
import math
import numpy as np

x = np.linspace(-20, 20, 50)

y = (x**3) * 78.48-149.112*(x**2) + 48.67

print(np(y))

fig, ax = plt.subplots()
ax.plot(x,y)

ax.axis([-20,20,-20,20])
plt.grid()
plt.show()
