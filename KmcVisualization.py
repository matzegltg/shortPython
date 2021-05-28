import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib.offsetbox import AnchoredText
import time as tim
def calculateCumOccupancy(results):
    occupancySum = [0]
    for i in range(1,len(results[2])):
        occupancySum.append((occupancySum[i-1]*results[0][i-1] + ((results[2][i]+results[2][i-1])/2)*(results[0][i]-results[0][i-1]))/results[0][i])
    print(f"approached limit of occupancy: {occupancySum[len(results[0])-1]}")
    return occupancySum

def calculateProbabilitys(results):
    
    probDep = []
    probDiff = []
    probDes = []

    for i in range(0,len(results[0])):
        kTot = results[4][i][0]+ results[4][i][1] + results[4][i][2]
        probDep.append((results[4][i][0]/kTot))
        probDiff.append((results[4][i][1]/kTot))
        probDes.append((results[4][i][2]/kTot))

    return probDep, probDiff, probDes

def visualizeAnimation(results, kDep, kHop, kDesorb):
    size = len(results[1][0])
    fig, ax = plt.subplots()

    #dont know why results[1][0] doesnt work...
    matrice = ax.matshow(results[1][-1], cmap="inferno")
    #Update function for visualization
    def update(i):
        surfaceX = results[1][i]
        print(surfaceX)
        matrice.set_array(surfaceX)
        
    description = f"yellow: occupied by species \nblack: empty  \n \nused rate constants: \nkDeposition = {kDep} [1/s], \nkHopping = {kHop} [1/s], \nkDesorption = {kDesorb} [1/s]"
    ani = anim.FuncAnimation(fig, update, frames=len(results[0]), interval =10, repeat = False)
    fig.set_size_inches(9,5)
    plt.title(f'KMC on a {size} x {size} lattice')
    plt.text(10, 5.5, description)
    plt.show()
    
def visualizeOccupancy(results, avgOccup):
    size = len(results[1][0])
    plt.plot(results[0], results[2], 'o--', linewidth=0.5, alpha=0.9)
    plt.plot(results[0], avgOccup, '--', linewidth=0.75)
    plt.axis([0, results[0][len(results[0])-1], 0, 1])
    plt.xlabel('time t [s]?')
    plt.ylabel('share of occupied places [-]')
    plt.title(f'Occupancy of a quadratic lattice with size {size} x {size}')
    plt.grid(True)
    
    plt.show()

def plotInfo(probDep, probDiff, probDes, results, kDep, kHop, kDesorb):
    size = len(results[1][0])
    
    plt.title(f"kDeposition = {kDep} [1/s], \nkHopping = {kHop} [1/s], \nkDesorption = {kDesorb} [1/s]")
    plt.plot(results[0], probDep, '--', linewidth=0.5, alpha=0.9, label='depositions', markersize = 2)        
    plt.plot(results[0], probDiff, '--', linewidth=0.5, alpha=0.9, label='diffusions', markersize = 2)
    plt.plot(results[0], probDes, '--', linewidth=0.5, alpha=0.9, label = 'desorptions', markersize = 2)
    plt.legend(loc='lower left')
    plt.axis([0, results[0][len(results[0])-1], 0, 1])
    plt.xlabel('time t [s]')
    plt.ylabel('probability of respective event [-]')
    plt.grid(True)
    plt.suptitle(f'probability of depositions, diffusions and desorptions over time on a {size} x {size} lattice')
    plt.show()