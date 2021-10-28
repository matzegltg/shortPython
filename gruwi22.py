# LaplaceT = 0 auf ]0;1[**2

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm



class FiniteDifferenzen(object):
    def __init__(self, h) -> None:
        super().__init__()
        self.h = h
    
    def createSystemMatrix(self, nrow, ncol) -> np.ndarray:
        """returns system matrix A of finit differences"""
        
        # geht schöner :(
        A = np.eye(nrow, k=-1) + np.eye(nrow, dtype=int) * -4 + np.eye(nrow, dtype=int, k=+1)
        print(A)
        Ones = np.eye(ncol)
        Zeros = np.zeros((ncol, nrow))
        A1 = np.concatenate((A, Ones, Zeros, Zeros, Zeros, Zeros, Zeros, Zeros, Zeros), axis=1)
        A2 = np.concatenate((Ones, A, Ones, Zeros, Zeros, Zeros, Zeros, Zeros, Zeros), axis=1)
        A3 = np.concatenate((Zeros, Ones, A, Ones, Zeros, Zeros, Zeros, Zeros, Zeros), axis=1)
        A4 = np.concatenate((Zeros, Zeros, Ones, A, Ones, Zeros, Zeros, Zeros, Zeros), axis=1)
        A5 = np.concatenate((Zeros, Zeros, Zeros, Ones, A, Ones, Zeros, Zeros, Zeros), axis=1)
        A6 = np.concatenate((Zeros, Zeros, Zeros, Zeros, Ones, A, Ones, Zeros, Zeros), axis = 1)
        A7 = np.concatenate((Zeros, Zeros, Zeros, Zeros, Zeros, Ones, A, Ones, Zeros), axis=1)
        A8 = np.concatenate((Zeros, Zeros, Zeros, Zeros, Zeros, Zeros, Ones, A, Ones), axis=1)
        A9 = np.concatenate((Zeros, Zeros, Zeros, Zeros, Zeros, Zeros, Zeros, Ones, A), axis=1)
        result = np.concatenate((A1, A2, A3, A4, A5, A6, A7, A8, A9))
        
        return result
    
    def createRightSide(self, nrow, ncol) -> np.ndarray:
        """returns right side of finit differences task"""

        rightSide = np.full((nrow*ncol), 0)
        for i in range(9):
            rightSide[i] = -10
        
        return rightSide * 1/((0.1)**2)

    def modifySystemMatrix(self, systemMatrix) -> np.ndarray:
        """because the double neumann border first and last diagonal entree of A core has to be three"""
        # geht auch schöner
        for i in range(82):
            if i % 9 == 0:
                if i == 0:
                    systemMatrix[i][i] = -3
                elif i == 81:
                    systemMatrix[i-1][i-1] = -3
                    
                elif i != 0 and i!= 81:
                    systemMatrix[i][i] = -3
                    systemMatrix[i-1][i-1] = -3

                    
        print(systemMatrix)
        return systemMatrix
   
    def plotSolutions(self, solution) -> None:
        x = np.arange(0 + self.h, 1, self.h)
        y = np.arange(0 + self.h, 1, self.h)
        X, Y = np.meshgrid(x, y)

        # nehmen unsere Loesung
        Z = solution.reshape(9, 9)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("temperature")
        ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=2, antialiased=True)
        
        plt.show()

if __name__ == "__main__":
    fd = FiniteDifferenzen(h = (0.1))
    A = fd.createSystemMatrix(9,9)
    A = fd.modifySystemMatrix(A)
    print(f'Das ist A: \n {A}')
    
    rightSide = fd.createRightSide(9,9)
    print(f'Das ist die rechte Seite: \n {rightSide}')

    x = np.linalg.solve( 1/((0.1) ** 2 ) * A, rightSide)
    print(f'Das ist die Lösung: \n {x}')

    fd.plotSolutions(x)

