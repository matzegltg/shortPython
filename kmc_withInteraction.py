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

#chooses random coordinate from a given Matrix which contains coordinates of e.g. all Position of 0 = no grain or 1 = grain on surface
def choosePosition(coordinateMatrix):
    return coordinateMatrix[random.randint(0, len(coordinateMatrix)-1)]

#chooses random direction by creating two random numbers between -1 and 1
def chooseRandomDiffusionDirection():
    return [random.randint(-1,1), random.randint(-1,1)]

#performs deposition. basically just changing at specific position value from 0 to 1
def performDeposition(position, surface):
    print(f'deposition at: ({position[0]}, {position[1]})')
    surface[position[0], position[1]] = 1

#performs desorption. basically just changing at specifc position value from 1 to 0
def performDesorption(position, surface):
    print(f'desorption at: ({position[0]}, {position[1]})')
    surface[position[0], position[1]] = 0

#def checkEnvironmentalSpecies(position, surface):
    
#chooses random Position around selected, if position empty change values
def performDiffusionAtNoBorder(position, surface):
    check = False
    while check == False:
        direction = chooseRandomDiffusionDirection()
        #question is diffusion on same point possible? --> Assumption neccessary otherwise problems with infinity while loop if environment
        #of atom is occupied with other atoms 
        if direction == [0,0]:
            check = True
            print(f'diffusion at same place ({position[0]}, {position[1]})')
        if surface[position[0] + direction[0], position[1] + direction[1]] == 0:
            #switch position -> diffusion
            surface[position[0], position[1]] = 0
            surface[position[0] + direction[0], position[1] + direction[1]] = 1
            check = True
            print(f'diffusion from ({position[0]}, {position[1]}) to ({position[0] + direction[0]},{position[1] + direction[1]})')

#performs diffusion. executing diffusion event, taking care of periodic boundary
def performBoundaryDiffusion(position, surface, borderValues):
    hasPerformedAction = False

    while hasPerformedAction == False:
        direction = chooseRandomDiffusionDirection()
        if direction == [0,0]:
                hasPerformedAction = True
                break
        
        for i in range(0,len(borderValues)):
            #checks wheter direction is critical (goes out of map) -> set surface to zero
            if direction == [borderValues[i,0], borderValues[i,1]]:
                surface[position[0], position[1]] = 0
                print(f'diffusion from ({position[0]}, {position[1]}) to ({position[0] + direction[0]},{position[1] + direction[1]} -> disappears)')
                hasPerformedAction = True
                break
        
        else:
            hasPerformedAction = performBoundaryDiffusionIntoMap(position, surface, direction)
            
#subfunction of performBoundaryDiffusion, if difussion direction's not out of surface
def performBoundaryDiffusionIntoMap(position, surface, direction):
    if direction == [0,0]:
        print(f'boundary diffusion at same place ({position[0]}, {position[1]})')
        return True
        
    if surface[position[0] + direction[0], position[1] + direction[1]] == 0:
        surface[position[0], position[1]] = 0
        surface[position[0] + direction[0], position[1] + direction[1]] = 1
        print(f'boundary diffusion from ({position[0]}, {position[1]}) to ({position[0] + direction[0]},{position[1] + direction[1]})')
        return True

#returns a String of border situation around current position
def getBorder(position, surface):
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
        return np.array([[+1,-1, position[0], size-1], [0, -1, position[0], size-1], [-1, -1, size-1, size-1], [-1,0, size-1, position[1]], [-1, +1, size-1, position[1] +1 ]])
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
def performEvent(eventNumber):
    #matrices which contain positions with no grain and grain on surface
    coordinatesZero = []
    coordinatesOne = []

    #scans surface
    for i in range(size):
        for j in range(size):
            if surface[i,j] == 0:
                coordinatesZero.append([i,j])
            else:
                coordinatesOne.append([i,j])

    #Deposition
    if eventNumber == 1:
        if len(coordinatesZero) > 0:
            performDeposition(choosePosition(coordinatesZero), surface)
        else:
            print('no deposition possible')

    #Diffusion
    if eventNumber == 2:
        if len(coordinatesOne) > 0:
            position = choosePosition(coordinatesOne)
            border = getBorder(position, surface)

            if border == 'NOBORD':
                performDiffusionAtNoBorder(position, surface)
            else:
                performBoundaryDiffusion(position, surface, getBorderValues(border, position, surface))
        else:
            print('no difffusion possible')
    
    #Desorption indepent of environmental atoms -> boundary unnecessary, otherwise individual desorptionRates
    if eventNumber == 3:
        if len(coordinatesOne) > 0:
            performDesorption(choosePosition(coordinatesOne), surface)
        else:
            print('no desorption possible')
    
    return surface
    


#event = 1: deposition, event = 2: diffusion, event = 3: desorption
def chooseEvent(rDep, rHop, rDesorb, kTot):
    
    #randint returns n; 1 <= n <= kTot
    x = random.randint(1,kTot)
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
        print('try again')
    else:
        return - (math.log(x))/kTot

#returns occupancy
def calculateOccupancy(surface):
    size = len(surface)
    return checkNumberOfSpecies(surface)/(size*size)

"""
surface/lattice of grain, at start each position is empty
atoms of grain do not vibrate etc.
have fixed position but can diffuse
"""

#input parameters

#size of lattice
size = 5

#surface (lattice)
#periodic border: infinite borders
#e.g. diffusion in upper right corner -> comes back in downleft corner
surface = np.zeros((size, size))

#store final data 0: time, 1: surfaces, 2: occupancy, 3: event Number
results = [[],[],[],[]]
results[0].append(0)
results[1].append(surface.copy())
results[2].append(0)
results[3].append(0)

# time
t=0

#unit?


kDep = 1
kHop = 1
kDesorb = 2


while t < 1:
    
    
    #calculate Rates
    #Assumption: species on grain can either desorb or diffuse 
    #question? rate of Deposition depends on number of empty position
    rDep = ((size*size))*kDep
    rDiff = checkNumberOfSpecies(surface)*kHop
    rDesorb = checkNumberOfSpecies(surface)*kDesorb
    kTot = rDep + rDiff + rDesorb
    
    #print(f'(rDep: {rDep}, rDiff: {rDiff}, rDesorb: {rDesorb}, kTot: {kTot}')

    #choose and perform Event
    t = t + timeStep(kTot)
    eventNumber = chooseEvent(rDep, rDiff, rDesorb,kTot)
    surface = performEvent(eventNumber)
    print(surface)
    #store data in results matrix
    results[0].append(t)
    results[1].append(surface.copy())
    results[2].append(calculateOccupancy(surface))
    results[3].append(eventNumber)

print(results[1])
vis.visualizeOccupancy(results)
vis.visualizeAnimation(results)
vis.plotInfo(results)