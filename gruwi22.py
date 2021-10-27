# LaplaceT = 0 auf ]0;1[**2

import numpy as np
from numpy.core.defchararray import upper

class FinitDifferenzen(object):
    def __init__(self) -> None:
        super().__init__()
    
    def createSystemMatrix(self, nrow, ncol) -> np.ndarray:
        """returns system matrix A of finit differences"""
        A = np.eye(nrow, k=-1) + np.eye(nrow, dtype=int) * -4 + np.eye(nrow, dtype=int, k=+1)
        for col in range(ncol):
            A = np.stack(A, np.eye(nrow))
        return A

if __name__ == "__main__":
    fd = FinitDifferenzen()
    A = fd.createSystemMatrix(9,9)
    print(A)