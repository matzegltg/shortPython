import numpy as np

def createGivens(c_ij, s_ij, k, l):
    #print(k, l)
    G = np.eye(4)
    G[k][k]= c_ij
    G[k][l] = s_ij
    G[l][k] = -s_ij
    G[l][l]= c_ij
    return G

def QRZerlegung (A, b):
    for j in range(0,3):
        for i in range(j+1,4):
            if A[i][j] != 0:

                r_ij = (np.sqrt((A[j][j]**2 + A[i][j]**2)))
                c_ij = A[j][j]/r_ij
                s_ij =  A[i][j]/r_ij
                print(f"Das ist ungefähr rij: {np.round(r_ij, 4)}")
                print(f"Das ist ungefähr cij: {np.round(c_ij, 4)}")
                print(f"Das ist ungefähr sij: {np.round(s_ij, 4)}")
                
                #create givens matrix
                G = createGivens(c_ij, s_ij, j, i)

                #aktualisiere A und rechte Seite
                b = np.dot(G,b)
                A = np.dot(G,A)
                print(f"Und das wurde aus A: \n {str(np.round(A, 4))}")
                print("---------------------------------\n")
                
                
    return A, b



def rueckSub(R, rechteSeite):
    x = []
    for i in range(2,-1,-1): 
        if (i == 2):
            xi = rechteSeite[i]/R[i][i]
            x.append(xi)
        else:
            sum = 0
            for j in range(0,2-i):
                sum = sum - (R[i][2-j]*x[j])
            xi = (rechteSeite[i]+sum)/R[i][i]
            x.append(xi)
    
    result = np.array(np.flip(x))[np.newaxis]
            
    return str(result.T)


if __name__ == "__main__":
    #Eingabedaten
    A = np.array([[2, 3, 1], [-1,-2,-2], [2,5,3], [1,2,0]])
    b = np.array([20, -20, -20, 10])
    print(f"Das ist die Anfangsmatrix: \n {str(A)}\n")
    
    print("Starte Iteration:")
    R, rechteSeite = QRZerlegung(A, b)

    print(f"Das ist die Lösung von Rx = QTb: \n x = {rueckSub(R, rechteSeite)}")