import random
import matplotlib.pyplot as plt
import numpy as np

sum = []
xA = []
sum.append(0)
xA.append(0)
for i in range(0,1000000):
    xA.append(i)
    x = random.randint(0,1)

    if x == 0:

        sum.append(sum[i]-1)
    else:
        sum.append(sum[i]+1)

#print(sum)

plt.plot(xA, sum, '--', linewidth=1, alpha=0.9)

plt.show()