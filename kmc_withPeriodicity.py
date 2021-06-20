import numpy as np
import random
import math
import KmcVisualization as vis

print('-----------------------------------------------')

#Assumptions
#rates per species e. g. certain atom per time, unit of time?
#typical rates in universe? <-> idealistic model?
#neglect katalytic effect of surface -> neglect reaction rates (just one species)
#temperature is constant

#returns number of species on the grain
def checkNumberOfSpecies(surface):
    return np.count_nonzero(surface)

#chooses random coordinate from a given Matrix which contains coordinates of e.g. 
#all Position of 0 = no grain or 1 = grain on surface
def choosePosition(coordinateMatrix):
    return coordinateMatrix[random.randint(0, len(coordinateMatrix)-1)]

#chooses random direction
#by creating two random numbers between -1 and 1
def chooseRandomDiffusionDirection():
    return [random.randint(-1,1), random.randint(-1,1)]

#performs deposition. basically just changing at specific position value from 0 to 1
def performDeposition(position, surface):
    surface[position[0], position[1]] = 1

#performs desorption. basically just changing at specifc position value from 1 to 0
def performDesorption(position, surface):
    surface[position[0], position[1]] = 0

#chooses random Position around selected, if position empty change values
def performDiffusionAtNoBorder(position, surface):
    check = False
    while check == False:
        direction = chooseRandomDiffusionDirection()
        #diffusion at same place also possible
        if direction == [0,0]:
            check = True
        if surface[position[0] + direction[0], position[1] + direction[1]] == 0:
            surface[position[0], position[1]] = 0
            surface[position[0] + direction[0], position[1] + direction[1]] = 1
            check = True

#performs diffusion. executing diffusion event, taking care of periodic boundary
def performBoundaryDiffusion(position, surface, borderValues):
    hasPerformedAction = False
    counter = 0

    while hasPerformedAction == False:
        direction = chooseRandomDiffusionDirection()
        if direction == [0,0]:
                hasPerformedAction = True
                break
        
        for i in range(0,len(borderValues)):
            #checks wheter direction is critical
            if direction == [borderValues[i,0], borderValues[i,1]]:
                #checks wheater choosen target is empty
                if surface[borderValues[i,2], borderValues[i,3]] == 0:
                    #perform diffusion
                    surface[position[0], position[1]] = 0
                    surface[borderValues[i,2],borderValues[i,3]] = 1
                    hasPerformedAction = True
                    break

                else:
                    hasPerformedAction = False
        
        #subsection checks wheter direction is not 'critical'
        counter = 0
        for i in range(0,len(borderValues)):
            if direction == [borderValues[i,0], borderValues[i,1]]:
                counter = counter +1
        
        #if direction is not critical -> mentions towards center of lattice perform diffusion into map
        if counter == 0:
            hasPerformedAction = performBoundaryDiffusionIntoMap(position, surface, direction)

#subfunction of performBoundaryDiffusion, if difussion direction's not out of surface
def performBoundaryDiffusionIntoMap(position, surface, direction):
    if direction == [0,0]:
        #print('boundary diffusion from at same place')
        return True
        
    if surface[position[0] + direction[0], position[1] + direction[1]] == 0:
        surface[position[0], position[1]] = 0
        surface[position[0] + direction[0], position[1] + direction[1]] = 1
        #print(f'boundary diffusion from ({position[0]}, {position[1]}) to ({position[0] + direction[0]},{position[1] + direction[1]}')
        return True

#returns a String of border situation around current position
def getBorder(position, surface):
    size = len(surface)
    if [position[0],position[1]] == [0,position[1]]:
        if [position[0],position[1]] == [0,size-1]:
            return 'NORTHEAST'
        elif [position[0],position[1]] == [0,0]:
            return 'NORTHWEST'
        else:
            return 'NORTH'

    if [position[0],position[1]] == [size-1,position[1]]:
        if [position[0],position[1]] == [size-1,size-1]:
            return 'SOUTHEAST'
        if [position[0],position[1]] == [size-1,0]:
            return 'SOUTHWEST'
        else:
            return 'SOUTH'
    
    if [position[0],position[1]] == [position[0],size-1]:
        return 'EAST'
    if [position[0],position[1]] == [position[0],0]:
        return 'WEST'
    else:
        return 'NOBORD'

#creates 2D Matrix, with 3 (one border site) resp. 5 (corner) lines and 4 columns. Each line contains the "critical" diffusion direction, and corresponding target position
def getBorderValues(border, position, surface):
    size = len(surface)
    if border == 'NORTHWEST':
        return np.array([[+1,-1, position[0], size-1], [0, -1, position[0], size-1],
        [-1, -1, size-1, size-1], [-1,0, size-1, position[1]], [-1, +1, size-1, position[1] +1 ]])
    if border == 'NORTHEAST':
        return np.array([[-1,-1, size-1, position[1]-1], [-1,0, size-1, position[1]], [-1,1,size-1,size-1], [0,1,position[0], 0], [1,1,position[0]+1,0]])
    if border == 'SOUTHEAST':
        return np.array([[-1,1,position[0]-1,0], [0,1,position[0],0], [1,1,0,0], [1,0,0,position[1]], [1,-1,0,position[1]-1]])
    if border == 'SOUTHWEST':
        return np.array([[1,1,0,position[1]+1], [1,0,0,position[1]], [1,-1,0,size-1], [0,-1,position[0],size-1], [-1,-1,position[0]-1,size-1]])      
    if border == 'NORTH':
        return np.array([[-1, -1, size-1,position[1]-1], [-1, 0, size-1, position[1]], [-1,1,size-1,position[1]+1]])    
    if border == 'EAST':
        return np.array([[-1, 1, position[0]-1,0], [0,1,position[0], 0], [1,1,position[0]+1,0]])
    if border == 'SOUTH':
        return np.array([[1,-1,0,position[1]-1], [1,0,0,position[1]], [1,1,0,position[1]+1]])
    if border == 'WEST':
        return np.array( [[-1, -1, position[0],size-1], [0,-1,position[0], size-1], [1, -1, position[0]+1,size-1]])
    if border == 'NOBORD':
        return []

#performs specific event
def performEvent(eventNumber, surface, size):
    
    #matrices which contain positions with no grain and grain on surface
    coordinates = [[],[]]
    coordinates[0] = np.argwhere(np.array(surface) == 0)
    coordinates[1] = np.argwhere(np.array(surface) == 1)

    #Deposition
    if eventNumber == 1:
        if len(coordinates[0]) > 0:
            coordinates = performDeposition(choosePosition(coordinates[0]), surface)

    #Diffusion
    if eventNumber == 2:
        if len(coordinates[1]) > 0:
            position = choosePosition(coordinates[1])
            border = getBorder(position, surface)

            if border == 'NOBORD':
                performDiffusionAtNoBorder(position, surface)
            else:
                performBoundaryDiffusion(position, surface, getBorderValues(border, position, surface))
    
    #Desorption indepent of environmental atoms -> boundary unnecessary, otherwise individual desorptionRates
    if eventNumber == 3:
        if len(coordinates[1]) > 0:
            performDesorption(choosePosition(coordinates[1]), surface)

    return surface
    
#event = 1: deposition, event = 2: diffusion, event = 3: desorption
def chooseEvent(rDep, rHop, rDesorb, kTot):
    
    #random returns x: 0 <= x < 1
    x = random.random() * kTot
    if x <= rDep:
        return 1
    if rDep < x <= rDep+rHop:
        return 2
    if x > rHop+rDep:
        return 3

#calculate timeStep, 
#param x: probability that event should not occur
def timeStep(kTot):
    x = random.random()
    if x == 0:
        timeStep(kTot)
    else:
        return - (math.log(x))/kTot

#returns occupancy
def calculateOccupancy(surface):
    size = len(surface)
    return checkNumberOfSpecies(surface)/(size*size)

def performKMC(size, timeStart, timeEnd, kDep, kHop, kDesorb):
    #periodic border
    #e.g. diffusion in upper right corner -> particle comes back
    #in bottom left corner
    surface = np.zeros((size, size))

    #store final data 0: time, 1: surfaces, 2: occupancy, 3: event Number, 4: rates, (table of events)
    results = [[],[],[],[], []]

    #just for readability
    t = timeStart
   
    while t < timeEnd:

        #calculate rates
        rDep = (size*size)*kDep
        rDiff = checkNumberOfSpecies(surface)*kHop
        rDesorb = checkNumberOfSpecies(surface)*kDesorb
        kTot = rDep + rDiff + rDesorb

        #choose event
        eventNumber = chooseEvent(rDep, rDiff, rDesorb, kTot)

        #store data in results matrix 
        results[0].append(t)
        results[1].append(surface.copy())
        results[2].append(calculateOccupancy(surface))
        results[3].append(eventNumber)
        results[4].append([rDep, rDiff, rDesorb])

        #choose and perform event
        t = t + timeStep(kTot)
        surface = performEvent(eventNumber, surface, size)
    
    return results

def doVisualizations(results, kDep, kHop, kDesorb, lastpoints=10):
    #vis.visualizeOccupancy(results, vis.calculateMovingAverage(results, lastpoints), vis.calculateMovingAverage(results, lastpoints*100), vis.calculateMovingAverage(results, lastpoints*1000), lastpoints, kDep, kHop, kDesorb)
    vis.visualizeOccupancy(results, kDep, kHop, kDesorb)
    x, y, z = vis.calculateProbabilitys(results)
    vis.visualizeAnimation(results, kDep, kHop, kDesorb)
    vis.plotInfo(x, y, z, results, kDep, kHop, kDesorb)

if __name__ == "__main__":
    """
    surface/lattice of grain, at start each position is empty
    atoms of grain do not vibrate etc.
    have fixed position but can diffuse
    """

    #input parameters
    #size of lattice
    size = 10

    # time [s]
    timeStart=0
    timeEnd=100

    #rate constansts [1/s]
    kDep = 1
    kHop = 10
    kDesorb = 4

    results = performKMC(size, timeStart, timeEnd, kDep, kHop, kDesorb)
    doVisualizations(results, kDep, kHop, kDesorb)