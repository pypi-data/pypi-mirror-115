import numpy as np
import sympy as sym

def insert_na_list(M):
    na = np.repeat(np.nan, len(M))
    L = []
    for i in range(len(M)):
        L.append(M[i])
        L.append(na[i])
    L = L[:len(L)-1]
    return L

def insert_na_array(M):
    # row 1
    na = np.repeat(np.nan, len(M[:, 0]))
    L = []
    for i in range(len(M[:, 0])):
        L.append(M[i, 0])
        L.append(na[i])
    L = L[:len(L)-1]
    M1 = np.array([L]).T
    # from row 2
    M = M[:, 1:]
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if i < j:
                M[i, j] = np.nan
    N = np.zeros((M.shape[0] * 2 - 1, M.shape[1]))
    for j in range(M.shape[1]):
        Mi = M[:, j]
        na = np.repeat(np.nan, len(Mi))
        L = []
        for i in range(len(Mi)):
            L.append(Mi[i])
            L.append(na[i])
        L = L[:len(L)-1]
        LNew = L[j:] + [np.nan] * j # shift values up
        N[:, j] = LNew
    N = np.hstack([M1, N])
    return N
    
def matrix_rationals(A, row_matrix):
    
    create_matrix = 'sym.Matrix(%s)' %(row_matrix)
    count_rational = 0
    r, c = A.shape
    for i in range(r):
        for j in range(c):
            if not isinstance(A[i,j], sym.Integer) and not isinstance(A[i,j], sym.Float):
                A[i,j] = "'%s'" %(A[i,j])
                count_rational = count_rational + 1
    if count_rational > 0:
        create_matrix = "sym.Matrix(%s)" %(A.tolist())
    
    return create_matrix