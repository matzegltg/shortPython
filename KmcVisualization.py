import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib.widgets import Slider


def visualizeAnimation(results):
    size = len(results[1][0])
    fig, ax = plt.subplots()

    #dont know why results[1][0] doesnt work...
    matrice = ax.matshow(results[1][-1])
    #Update function for visualization
    def update(i):
        surfaceX = results[1][i]
        print(surfaceX)
        matrice.set_array(surfaceX)
        
    
    ani = anim.FuncAnimation(fig, update, frames=len(results[0]), interval =10)
    
    plt.title(f'KMC on a {size} x {size} lattice')
    plt.show()
    
    
def visualizeOccupancy(results):
    size = len(results[1][0])
    plt.plot(results[0], results[2], 'o--', linewidth=0.5, alpha=0.9)
    plt.axis([0, results[0][len(results[0])-1], 0, 1])
    plt.xlabel('time t')
    plt.ylabel('share of occupied places')
    plt.title(f'Occupancy of a quadratic lattice with size {size} x {size}')
    plt.grid(True)
    plt.show()


def plotInfo(results):
    size = len(results[1][0])
    plt.subplots_adjust(wspace=0.0,hspace=0.5)
    plt.subplot(211)
    plt.title('number of depositions, diffusions and desorptions over time')
    yDepos = []
    yDiffus = []
    yDesorb = []
    yDepos.append(0)
    yDiffus.append(0)
    yDesorb.append(0)

    for i in range(len(results[0])):
        if results[3][i] == 1:
            yDepos.append(yDepos[i-1]+1)
            yDiffus.append(yDiffus[i-1])
            yDesorb.append(yDesorb[i-1])
        elif results[3][i] == 2:
            yDepos.append(yDepos[i-1])
            yDiffus.append(yDiffus[i-1]+1)
            yDesorb.append(yDesorb[i-1])
        elif results[3][i] == 3:
            yDepos.append(yDepos[i-1])
            yDiffus.append(yDiffus[i-1])
            yDesorb.append(yDesorb[i-1]-1)
    

    plt.plot(results[0], yDepos, 'o--', linewidth=0.5, alpha=0.9, label='depositions', markersize = 2)        
    plt.plot(results[0], yDiffus, 'o--', linewidth=0.5, alpha=0.9, label='diffusions', markersize = 2)
    plt.plot(results[0], yDesorb, 'o--', linewidth=0.5, alpha=0.9, label = 'desorptions', markersize = 2)

    plt.legend(loc='lower left')
    plt.axis([0, results[0][len(results[0])-1], -max(yDesorb), max(yDepos)])
    plt.grid()
    plt.subplot(212)
    grainCount = []
    grainCount.append(0)
    for i in range(len(results[0])):
        if results[3][i] == 1:
            grainCount.append(grainCount[i-1] +1)
        elif results[3][i] == 2:
            grainCount.append(grainCount[i-1])
        elif results[3][i] == 3: 
            grainCount.append(grainCount[i-1]-1)
    plt.plot(results[0], grainCount, 'o--', linewidth=0.5, alpha=0.9)
    plt.title('number of species on grain')
    plt.grid(True)
    plt.axis([0, results[0][len(results[0])-1], 0, size*size])
    plt.show()
