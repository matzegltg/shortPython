import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib.offsetbox import AnchoredText
import time as tim
import numpy as np
import math as mth
'''
def calculateCumOccupancy(results):
    occupancySum = [0]
    for i in range(1,len(results[2])):
        occupancySum.append((occupancySum[i-1]*results[0][i-1] + ((results[2][i]+results[2][i-1])/2)*(results[0][i]-results[0][i-1]))/results[0][i])
    print(f"approached limit of occupancy: {occupancySum[len(results[0])-1]}")
    return occupancySum
'''

def calculateMovingAverage(results, lastpoints):
    #moving average of last lastpoints elements
    occupancyMovingAverage = []
    for i in range(0,lastpoints-1):
        occupancyMovingAverage.append(0)
    
    #print(occupancyMovingAverage)
    for i in range(lastpoints-1,len(results[0])):
        sum = 0
        for j in range(0,lastpoints):
            sum = sum + results[2][i-j]
        x = sum/lastpoints
        occupancyMovingAverage.append(x)
    
    #print(len(occupancyMovingAverage))
    #print(occupancyMovingAverage)
    return occupancyMovingAverage

def calculateProbabilitys(results):
    
    probDep = []
    probDiff = []
    probDes = []

    for i in range(0,len(results[0])):
        kTot = results[4][i][3]
        probDep.append((results[4][i][0]/kTot))
        probDiff.append((results[4][i][1]/kTot))
        probDes.append((results[4][i][2]/kTot))

    #print(probDes)
    return probDep, probDiff, probDes

def visualizeAnimation(results, kDep, kHop, kDesorb):
    size = len(results[1][0])
    fig, ax = plt.subplots()

    
    matrice = ax.matshow(results[1][-1], cmap="inferno")
    #Update function for visualization
    def update(i):
        surfaceX = results[1][i]
        #print(surfaceX)
        matrice.set_array(surfaceX)
        
    description = f"yellow: occupied by species \nblack: empty  \n \nused rate constants: \nkDeposition = {kDep} [1/s], \nkHopping = {kHop} [1/s], \nkDesorption = {kDesorb} [1/s]"
    ani = anim.FuncAnimation(fig, update, frames=len(results[0]), interval =10, repeat = False)
    fig.set_size_inches(9,5)
    plt.title(f'KMC on a {size} x {size} lattice')
    plt.text(10, 5.5, description)
    plt.show()
    
def visualizeOccupancy(results, avgOccup1, lastpoints, kDep, kHop, kDesorb, timeStart, timeEnd, size):
    #print(results[0])
    avgOccup2 = calculateMovingAverage(results, lastpoints*10)
    x = np.linspace(timeStart, timeEnd, 1000)
    y = (((size*kDep)/kDesorb) * (1-1/(np.exp(kDesorb*x))))/size

    constantlimit = []
    for i in range(0,len(x)):
        constantlimit.append(((size*kDep)/kDesorb)/size)
    

    plt.plot(results[0], results[2], '.-', linewidth=3, alpha = 0.3, color = "grey", label = "occupancy")
    plt.plot(results[0], avgOccup1, '-', linewidth=3, label = 'moving average (last ' + str(lastpoints) + ' points)')
    plt.plot(results[0], avgOccup2, 'r-', linewidth=3, label = 'moving average (last ' + str(lastpoints*10) + ' points)')
    plt.plot(x, y, '-', linewidth = 3, color= "black", label = "analytical solution")
    plt.plot(x, constantlimit, '--', linewidth = 3, label = f"analytical limit (= {((size*kDep)/kDesorb)/size})")

    plt.title(f"kDeposition = {kDep} [1/s], \nkHopping = {kHop} [1/s], \nkDesorption = {kDesorb} [1/s]")
    plt.axis([0, results[0][len(results[0])-1], 0, 0.5])
    plt.xlabel('time t [s]', fontsize=20)
    plt.legend(loc="lower right", fontsize=20)
    plt.ylabel('share of occupied places [-]', fontsize=20)
    plt.suptitle(f'Occupancy of a quadratic lattice with size {size} x {size}', fontsize=20)
    plt.grid(True)
    
    plt.show()

'''
def visualizeOccupancy(results, kDep, kHop, kDesorb):
    size = len(results[1][0])
    plt.title(f"kDeposition = {kDep} [1/s], \nkHopping = {kHop} [1/s], \nkDesorption = {kDesorb} [1/s]")
    plt.plot(results[0], results[2], '.-', linewidth=0.5, alpha = 0.9, color = "grey", label = "occupancy")
    plt.axis([0, results[0][len(results[0])-1], 0, 1])
    plt.xlabel('time t [s]')
    plt.legend(loc="lower right")
    plt.ylabel('share of occupied places [-]')
    plt.suptitle(f'Occupancy of a quadratic lattice with size {size} x {size}')
    plt.grid(True)
    
    plt.show()
'''

def plotInfo(probDep, probDiff, probDes, results, kDep, kHop, kDesorb):
    size = len(results[1][0])
    
    plt.title(f"kDeposition = {kDep} [1/s], \nkHopping = {kHop} [1/s], \nkDesorption = {kDesorb} [1/s]")
    plt.plot(results[0], probDep, '--', linewidth=3, alpha=0.9, label='depositions', markersize = 2)        
    plt.plot(results[0], probDiff, '--', linewidth=3, alpha=0.9, label='diffusions', markersize = 2)
    plt.plot(results[0], probDes, '--', linewidth=3, alpha=0.9, label = 'desorptions', markersize = 2)
    plt.legend(loc='lower right', fontsize=20)
    plt.axis([0, results[0][len(results[0])-1], 0, 1])
    plt.xlabel('time t [s]', fontsize=20)
    plt.ylabel('probability of respective event [-]', fontsize=20)
    plt.grid(True)
    plt.suptitle(f'probability of depositions, diffusions and desorptions over time on a {size} x {size} lattice', fontsize=20)
    plt.show()