import random
import numpy

surface = numpy.ones((5,5))

def getBorderValues(border, position, surface):
    #evt. -1
    size = len(surface)
    if border == 'NORTH':
        borderValues = numpy.array([ [-1, -1, size-1,position[1]-1], [-1, 0, size-1, position[1]], [-1,1,size-1, position[1]+1]])
        print(borderValues)
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
    
    if border == 'NOBORDER':
        return []
    

print(getBorderValues('NORTH', [0, 2], surface)[0,1])
