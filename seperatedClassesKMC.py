import numpy as np
import math
import random 
class Position():
    def __init__(self, x, y):
        self.xPos = x
        self.yPos = y
    
    def __str__(self):
        return '(' + str(self.xPos) + ',' + str(self.yPos) + ')'


surface = np.zeros((5,5))


coordinatesZero = []
coordinatesOne = []





dim= np.shape(surface)
size = dim[0]
surface[size-1, 3] = 1
surface[2, size-1] = 1


for i in range(size):
        for j in range(size):
            if surface[i,j] == 0:
                coordinatesZero.append([i,j])
            else:
                coordinatesOne.append([i,j])

def performEvent(eventNumber):
    coordinatesZero = []
    coordinatesOne = []

    for i in range(size):
        for j in range(size):
            if surface[i,j] == 0:
                coordinatesZero.append([i,j])
            else:
                coordinatesOne.append([i,j])

    #Deposition with periodic boundary
    if eventNumber == 1:
        print('deposition')
        print(coordinatesZero)

        #chooses random elements of coordnatesZeroMatrix to perform deposition event
        [pi, pj] = coordinatesZero[random.randint(0, len(coordinatesZero)-1)]
        print([pi,pj])
        surface[pi,pj] = 1
        
    #Desorption indepent of environmental atoms -> boundary unnecessary, otherwise individual desorptionRates
    if eventNumber == 2:
        print('desorption')
        print(coordinatesOne)
        [pi, pj] = coordinatesOne[random.randint(0, len(coordinatesOne)-1)]
        print([pi,pj])
        surface[pi,pj] = 0
    
    #Diffusion
    if eventNumber == 3:
        print('diffusion')
        print(coordinatesOne)
        [pi, pj] = coordinatesOne[random.randint(0, len(coordinatesOne)-1)]
        print([pi,pj])
        if [pi,pj] == [0,0] or [pi,pj] == [0,size-1] or [pi,pj] == [size-1,0] or [pi,pj] == [size-1,size-1]:
            print("diffusion in corner -> until now, not possible")
        else:
            check = False
            if [pi,pj] == [0,pj]:
                while check == False:
                    randomPi = random.randint(-1,1)
                    randomPj = random.randint(-1,1)
                    
                    #up left
                    if (randomPi == -1 and randomPj == -1) and surface[size-1,pj-1] == 0:
                        surface[0,pj] = 0
                        surface[size-1, pj-1]= 1
                        check = True
                    
                    #up
                    if (randomPi == -1 and randomPj == 0) and surface[size-1,pj] == 0:
                        surface[0,pj] = 0
                        surface[size-1,pj] = 1
                        check = True
                    
                    #up right
                    if (randomPi == -1 and randomPj == +1) and surface[size-1,pj+1] == 0:
                        surface[0,pj] = 0
                        surface[size-1,pj+1] = 1
                        check = True
                
            #east side
            if [pi,pj] == [pi,size-1]:
                while check == False:
                    randomPi = random.randint(-1,1)
                    randomPj = random.randint(-1,1)
                    
                    #top right
                    if (randomPi == -1 and randomPj == +1) and surface[pi-1,0] == 0:
                        surface[pi,size-1] = 0
                        surface[pi-1, 0]= 1
                        check = True
                    
                    #right
                    if (randomPi == 0 and randomPj == +1) and surface[pi,0] == 0:
                        surface[pi,size-1] = 0
                        surface[pi,0] = 1
                        check = True
                    
                    #down right
                    if (randomPi == +1 and randomPj == +1) and surface[pi+1,0] == 0:
                        surface[pi,size-1] = 0
                        surface[pi+1,0] = 1
                        check = True
        
            #southborder
            if [pi,pj] == [size-1,pj]:
                while check == False:
                    randomPi = random.randint(-1,1)
                    randomPj = random.randint(-1,1)
                    
                    #down left
                    if (randomPi == +1 and randomPj == -1) and surface[0,pj-1] == 0:
                        surface[size-1,pj] = 0
                        surface[0,pj-1]= 1
                        check = True
                    
                    #down
                    if (randomPi == +1 and randomPj == 0) and surface[0,pj] == 0:
                        surface[size-1,pj] = 0
                        surface[0,pj] = 1
                        check = True
                    
                    #down right
                    if (randomPi == +1 and randomPj == +1) and surface[0,pj+1] == 0:
                        surface[size-1,pj] = 0
                        surface[0,pj+1] = 1
                        check = True
            
            #border west
            if [pi,pj] == [pi,0]:
                while check == False:
                    randomPi = random.randint(-1,1)
                    randomPj = random.randint(-1,1)
                    
                    #up left
                    if (randomPi == -1 and randomPj == -1) and surface[pi-1,size-1] == 0:
                        surface[pi,0] = 0
                        surface[pi-1,size-1]= 1
                        check = True
                    
                    #left
                    if (randomPi == 0 and randomPj == -1) and surface[pi, size-1] == 0:
                        surface[pi,0] = 0
                        surface[pi, size-1] = 1
                        check = True
                    
                    #down left
                    if (randomPi == +1 and randomPj == -1) and surface[pi+1,size-1] == 0:
                        surface[pi,0] = 0
                        surface[pi+1,size-1] = 1
                        check = True

            else:
                #choose random Position around selected, if position empty change values
                #question is diffusion on same point possible?
                print(f'thats the location: {[pi,pj]}')
                while check == False:
                    randomPi = random.randint(-1,1)
                    randomPj = random.randint(-1,1)
                    print(f'randomPi: {randomPi}')
                    print(f'randomPj: {randomPj}')
                    
                    print('search location')
                    
                    if surface[pi + randomPi, pj + randomPj] == 0:
                        #switch position -> diffusion
                        surface[pi, pj] = 0
                        surface[pi + randomPi, pj + randomPj] = 1
                        check = True


           
        


performEvent(3)
print(surface)


"""
if (i == 0) or (i == size):
if (j == 0) or (j == size):"""