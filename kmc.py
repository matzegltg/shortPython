import numpy as np
import collections as coll
import random
print('-----------------------------------------------')

#Assumptions
#rates per species e. g. certain atom per 
#typical rates in universe? <-> idealistic model?
#neglect katalytic effect of surface -> neglect reaction rates (just one species)
#temperature is constant

kDesorb = 1
kHop = 1
kDep = 1

#probability -> sum should lead one
probDesorb = kDesorb/(kDesorb + kHop + kDep)
probHop = kHop/(kDesorb + kHop + kDep)
probDep = kDep/(kDesorb + kHop + kDep)

#event = 1: deposition, event = 2: desorption, event = 3: diffusion
def chooseEvent():
    x = random.random()
    if x < probDep:
        return 1
    if probDep <= x < probDesorb:
        return 2
    if x >= probDesorb:
        return 3

def chooseEvent(x):
    return x

#number of KMC iteration
n = 100

#size of lattice
size = 20
"""
surface/lattice of grain, at start each position is empty
assumption nodynamic surface, atoms of grain do not vibrate etc.
have fixed position
"""
surface = np.zeros((size, size))

#store final data (Occupancy about time)
result = coll.deque()

# time
t=0


#check number of species on the grain
def checkNumberOfSpecies(surface):
    return np.count_nonzero(surface)

#choose random coordinates
def choosePosition(coordinateMatrix):
    position = coordinateMatrix[random.randint(0, len(coordinateMatrix)-1)]
    return position

def performDeposition(position, surface):
    print('deposition')
    surface[position[0], position[1]] = 1

def performDesorption(position, surface):
    print('desorption')
    surface[position[0], position[1]] = 0

#choose random Position around selected, if position empty change values
def performDiffusionAtNoBorder(position, surface):
    while check == False:
        print('search location')
        dircection = chooseRandomDiffusionDirection()
        #question is diffusion on same point possible?
        if direction[0] == 0 and direction[1] == 0:
            check = True
        
        if surface[position[0] + direction[0], position[1] + direction[1]] == 0:
            #switch position -> diffusion
            surface[position[0], position[1]] = 0
            surface[position[0] + direction[0], position[1] + direction[1]] = 1
            check = True

def chooseRandomDiffusionDirection():
    direction = [random.randint(-1,1), ranodm.randint(-1,1)]
    return direction

def performBoundaryDiffusion(direction, position, surface, borderValues):
    check = False

    while check == False:
        for i in range(0,3):
            if(direction[0] == borderValues[i,0] and direction[1] == borderValues[i,1]) and surface[borderValues[i,2], borderValues[i,3]:
                surface[position[0],position[1]] = 0
                surface[borderValues[i,2],borderValues[i,3]] = 1
                check = True
        
        if direction != [borderValues[0,0], borderValues[0,1]] or direction != [borderValues[1,0], borderValues[1,1]] or direction != [borderValues[2,0], borderValues[2,1]]:
            if direction == [0,0]:
                check = True
            
            if surface[position[0] + direction[0], position[1] + direction[1]] == 0:
                surface[position[0], position[1]] = 0
                surface[position[0] + direction[0], position[1] + direction[1]] = 1
                check = True

def getBorder(position, surface):
    if [position[0],position[1]] == [0,position[1]]:
        return 'NORTH'
    if [position[0],position[1]] == [position[0],size-1]:
        return 'EAST'
    if [position[0],position[1]] == [size-1,position[1]]:
        return 'SOUTH'
    if [position[0],position[1]] == [position[0],0]:
        return 'WEST'
    else:
        return 'NOBORDER'

def getBorderValues(border, position, surface):
    #evt. -1
    size = len(surface)
    if border == 'NORTH':
        borderValues = [[-1, -1, size-1,position[1]-1], [-1, 0, size-1, position[1]], [-1,1,size-1,position[1]+1]]
        return borderValues
    
    if border == 'EAST':
        borderValues = [[-1, 1, position[0]-1,0], [0,1,position[0], 0], [1,1,position[0]+1,0]]
        return borderValues

    if border == 'SOUTH':
        borderValues = [[1,-1,0,position[1]-1], [1,0,0,position[1]], [1,1,0,position[1]+1]]
        return borderValues
    
    if border == 'WEST':
        borderValues = [[-1, -1, position[0],size-1], [0,-1,position[0], size-1], [1, -1, position[0]+1,size-1]]
        return borderValues
    
    if getBorder(position,surface) == 'NOBORDER':
        return []

def performEvent(eventNumber):
    coordinatesZero = []
    coordinatesOne = []

    for i in range(size):
        for j in range(size):
            if surface[i,j] == 0:
                coordinatesZero.append([i,j])
            else:
                coordinatesOne.append([i,j])

    #Deposition
    if eventNumber == 1:
        if len(coordinatesZero)-1 > 0:
            performDeposition(choosePosition(coordinatesZero), surface)
        else:
            print('no deposition possible')

    #Desorption indepent of environmental atoms -> boundary unnecessary, otherwise individual desorptionRates
    if eventNumber == 2:
        if len(coordinatesOne)-1 > 0:
            performDesorption(choosePosition(coordinatesOne), surface)
        else:
            print('no desorption possible')
    
    #Diffusion
    #since now corners cant diffuse
    if eventNumber == 3:
        if len(coordinatesOne)-1 > 0:
            position = choosePosition(coordinatesOne)
            
            if [position[0], position[1]] == [0,0] or [position[0], position[1]] == [0,size-1] or [position[0], position[1]] == [size-1,0] or [position[0], position[1]] == [size-1,size-1]:
                print("diffusion in corner -> until now, not possible")

            else:
                check = False
                #north
                if getBorder(position, surface) == 'NORTH':
                    
                    while check == False: 
                        direction =  chooseRandomDiffusionDirection()
                        #up left
                        if (direction[0] == -1 and direction[1] == -1) and surface[size-1,position[1]-1] == 0:
                            surface[0,position[1]] = 0
                            surface[size-1, position[1]-1]= 1
                            check = True
                        
                        #up
                        if (direction[0] == -1 and direction[1] == 0) and surface[size-1,position[1]] == 0:
                            surface[0,position[1]] = 0
                            surface[size-1,position[1]] = 1
                            check = True
                        
                        #up right
                        if (direction[0] == -1 and direction[1] == +1) and surface[size-1,position[1]+1] == 0:
                            surface[0,position[1]] = 0
                            surface[size-1,position[1]+1] = 1
                            check = True
                        
                        #other directions??
                        if  direction[0] != -1:
                            #question is diffusion on same point possible?
                            if direction[0] == 0 and direction[1] == 0:
                                check = True
                            if surface[position[0] + direction[0], position[1] + direction[1]] == 0:
                                #switch position -> diffusion
                                surface[position[0], position[1]] = 0
                                surface[position[0] + direction[0], position[1] + direction[1]] = 1
                                check = True
                        
                    
                #east
                if getBorder(position, surface) == 'EAST':
                    while check == False:
                        direction[0] = random.randint(-1,1)
                        direction[1] = random.randint(-1,1)
                        
                        #top right
                        if (direction[0] == -1 and direction[1] == +1 and surface[position[0]-1,0] == 0):
                            surface[position[0],size-1] = 0
                            surface[position[0]-1, 0]= 1
                            check = True
                        
                        #right
                        if (direction[0] == 0 and direction[1] == +1 and surface[position[0],0] == 0):
                            surface[position[0],size-1] = 0
                            surface[position[0],0] = 1
                            check = True
                        
                        #down right
                        if (direction[0] == +1   and direction[1] == +1 and surface[position[0]+1,0] == 0):
                            surface[position[0],size-1] = 0
                            surface[position[0]+1,0] = 1
                            check = True

                        #other directions
                        if direction[1] != 1:
                            #question is diffusion on same point possible?
                            if direction[0] == 0 and direction[1] == 0:
                                check = True
                                
                            if surface[position[0] + direction[0], position[1] + direction[1]] == 0:
                                #switch position -> diffusion

                                surface[position[0], position[1]] = 0
                                surface[position[0] + direction[0], position[1] + direction[1]] = 1
                                check = True
            
                #south
                if getBorder(position, surface) == 'SOUTH':
                    while check == False:
                        direction[0] = random.randint(-1,1)
                        direction[1] = random.randint(-1,1)
                        
                        #down left
                        if (direction[0] == +1 and direction[1] == -1 and surface[0,position[1]-1] == 0):
                            surface[size-1,position[1]] = 0
                            surface[0,position[1]-1]= 1
                            check = True
                        
                        #down
                        if (direction[0] == +1 and direction[1] == 0 and surface[0,position[1]] == 0):
                            surface[size-1,position[1]] = 0
                            surface[0,position[1]] = 1
                            check = True
                        
                        #down right
                        if (direction[0] == +1 and direction[1] == +1 and surface[0,position[1]+1] == 0):
                            surface[size-1,position[1]] = 0
                            surface[0,position[1]+1] = 1
                            check = True
                        
                        #other directions
                        if direction[0] != +1:
                            #question is diffusion on same point possible?
                            if direction[0] == 0 and direction[1] == 0:
                                check = True    
                            if surface[position[0] + direction[0], position[1] + direction[1]] == 0:
                                #switch position -> diffusion
                                surface[position[0], position[1]] = 0
                                surface[position[0] + direction[0], position[1] + direction[1]] = 1
                                check = True
                
                #west
                if getBorder(position, surface) == 'WEST':
                    while check == False:
                        direction[0] = random.randint(-1,1)
                        direction[1] = random.randint(-1,1)
                        
                        #up left
                        if (direction[0] == -1 and direction[1] == -1 and surface[position[0]-1,size-1] == 0):
                            surface[position[0],0] = 0
                            surface[position[0]-1,size-1]= 1
                            check = True
                        
                        #left
                        if (direction[0] == 0 and direction[1] == -1 and surface[position[0], size-1] == 0):
                            surface[position[0],0] = 0
                            surface[position[0], size-1] = 1
                            check = True
                        
                        #down left
                        if (direction[0] == +1 and direction[1] == -1 and surface[position[0]+1,size-1] == 0):
                            surface[position[0],0] = 0
                            surface[position[0]+1,size-1] = 1
                            check = True
                        
                        #other 
                        if direction[1] != -1:
                            #question is diffusion on same point possible?
                            if direction[0] == 0 and direction[1] == 0:
                                check = True
                            if surface[position[0] + direction[0], position[1] + direction[1]] == 0:
                                #switch position -> diffusion
                                surface[position[0], position[1]] = 0
                                surface[position[0] + direction[0], position[1] + direction[1]] = 1
                                check = True

                #not at Border
                if getBorder(position, surface) == 'NOBORDER':
                    performDiffusionAtNoBorder(position, surface)
            
        else:
            print('no difffusion possible')

for i in range(1,5):
    print(surface)
    #calculate Rates
    #Assumption: species on grain can either desorb or diffuse 
    rDesorb = checkNumberOfSpecies(surface)*kDesorb
    rDiff = checkNumberOfSpecies(surface)*kHop
    #question: (1- occupied size NOT each position?)
    rDep = (1-checkNumberOfSpecies(surface))*kDep

    kTot = rDesorb + rDiff + rDep


    #choose and perform Event
    performEvent(chooseEvent(1))    
    performEvent(chooseEvent(2))
    

    #what do with time

print('---------------------------')