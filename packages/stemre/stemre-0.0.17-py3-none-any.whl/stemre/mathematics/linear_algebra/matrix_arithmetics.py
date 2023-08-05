import numpy as np
import sympy as sym

def element_wise(A, B, operation = 'division', library = 'sympy'):
    
    if A.shape != B.shape :
        raise TypeError('Matrices can not be divided because they are of different sizes.')
        
    r, c = A.shape
    M = sym.zeros(r, c)
    if library == 'Numpy':
        M = np.zeros(r, c)
    for i in range(r):
        for j in range(c):
            if operation == 'addition':
                M[i, j] = A[i, j] + B[i, j]
            elif operation == 'subtraction':
                M[i, j] = A[i, j] - B[i, j]
            elif operation == 'multiplication':
                M[i, j] = A[i, j] * B[i, j]
            elif operation == 'division':
                M[i, j] = A[i, j] / B[i, j]
            elif operation == 'power':
                M[i, j] = A[i, j] ** B[i, j]
            else:
                raise Exception('%s is an invalid method.' %(operation))
    return M