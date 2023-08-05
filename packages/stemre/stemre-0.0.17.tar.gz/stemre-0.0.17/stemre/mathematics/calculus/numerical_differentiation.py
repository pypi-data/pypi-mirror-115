import numpy as np
import pandas as pd

def richardson(f, x, n, h):
    
    '''
    function richardson( f, x, n, h ): 
             Approximates the first derivative f'(x) at at the point x = x0.

    Inputs:
          f - function to find derivative of
          x - value of x to find derivative at
          n - number of levels of extrapolation
          h - initial stepsize
    Output:
          N  - 2D numpy array of extrapolation values.
          dx - value of the derivative f'(x) at x
    '''
    
    N = np.zeros((n+1, n+1), dtype = np.float64)
    N[N == 0] = np.nan
    for i in range(n+1):
        N[i,0] = 0.5 * (f(x+h) - f(x-h)) / h
        p4powerj = 1
        for j in range(1, i+1):
            p4powerj = 4 * p4powerj
            N[i, j] = N[i, j-1] + (N[i, j-1] - N[i-1, j-1]) / (p4powerj - 1)
        h = 0.5 * h
    row_names = ['\(\\frac{h}{%s}\)' %(2 ** k) for k in range(N.shape[1])]
    col_names = ['\(R_{(m, \, %s)}\)' %(k+1) for k in range(N.shape[1])]
    df = pd.DataFrame(N, index = row_names, columns = col_names)
    df.fillna('', inplace = True)
    dx = N[n, n]
    return N, df, dx