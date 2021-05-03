import numpy 

def thatsAreallyCoolFunction():
    for i in range(1, 6):
        print('time printed')

thatsAreallyCoolFunction()
print('as')


probDesorb = 1/2
probHop = 1/6
probDep = 1/3

#event = 1: deposition, event = 2: desorption, event = 3: diffusion
def chooseEvent():
    x = random.random()
    if x < probDep:
        return 1
    if probDep <= x < probDesorb:
        return 2
    if x >= probDesorb:
        return 3


counter1 = 0
counter2 = 0
counter3 = 0

for i in range(10000):


    x = chooseEvent()
    if x == 1:
        counter1 = counter1 + 1
    if x == 2:
        counter2 = counter2 + 1
    if x == 3:
        counter3 = counter3 + 1


print(f'counter1{counter1}')

print(f'counter2{counter2}')

print(f'counter3{counter3}')
