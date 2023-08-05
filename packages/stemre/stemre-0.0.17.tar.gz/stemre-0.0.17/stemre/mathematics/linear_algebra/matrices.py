import numpy as np
import scipy.sparse as spa
import sympy as sym
    
def rosser_matrix():
    M = np.array([[ 611,  196, -192,  407,   -8,  -52,  -49,   29], 
                  [ 196,  899,  113, -192,  -71,  -43,   -8,  -44], 
                  [-192,  113,  899,  196,   61,   49,    8,   52], 
                  [ 407, -192,  196,  611,    8,   44,   59,  -23], 
                  [  -8,  -71,   61,    8,  411, -599,  208,  208], 
                  [ -52,  -43,   49,   44, -599,  411,  208,  208], 
                  [ -49,   -8,    8,   59,  208,  208,   99, -911], 
                  [  29,  -44,   52,  -23,  208,  208, -911,   99]])
    return M
    
def wilkinson_matrix(size):
    if size < 1 or not isinstance(size, int):
        raise ValueError('Size must be a positive integer')
    if size == 1:
        W = np.array([[0]])
    elif size == 2:
        W = np.array([[0.5, 1], [1, 0.5]])
    else:
        n = size - 1
        if size % 2 == 0:
            a = 0.5
        else:
            a = 0
        lower_diagonal, major_diagonal = [[1] * n] * 2
        upper_diagonal = list(np.hstack([np.arange(n/2, 0, -1), np.arange(a, n/2+0.1, 1)]))
        W = spa.diags([lower_diagonal, upper_diagonal, major_diagonal], [-1, 0, 1], shape = (size, size)).toarray()
    return W
    
def row_echelon_form(M):
    M = sym.Matrix(M)
    r = M.shape[0]
    for j in range(0, r-1):
        # pivotting
        for z in range(1, r):
            if (M[j, j] == 0):
                # get row j
                t = sym.Matrix([M[j, :]])
                # swap
                M[j, :] = M[z, :]
                # replace
                M[z, :] = t
        # Lower triangle elimination
        for i in range(j+1, r):
            M[i, :] = M[i, :] - M[j, :] * (M[i, j] / M[j, j])
    # reduce major diagonal to unity
    for s in range(0, r):
        if (M[s, s] != 1):
            M[s, :] = M[s, :] / M[s, s]
    return M