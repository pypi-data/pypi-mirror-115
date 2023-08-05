import numpy as np
import sympy as sym

def newton_differences(x, y, x0, poly_variable, decimals_points = 8):
    
    x_values = x
    y_values = y
    
    n = len(x)
    
    N = np.zeros((n,n+1))

    N[N == 0] = np.nan
    
    N[:,0] = x_values
    
    N[:,1] = y_values
    
    
    ff = str(np.round(N[0,1],decimals = decimals_points))
    
    fi = ''
    
    x = x_values # original value of x
    
    method = "forward"
    
    if method == "forward":
        for k in range(j,n):
            N[k,j+1] = N[k,j] - N[k-1,j]
                
            fi = fi + ' * (x - ' + str(x[j-1]) + ')'
                
            ff = ff + ' + ' + str(np.round(N[j,j+1],decimals = decimals_points)) + '' + fi 
    elif method == "backward":
        for k in range(j,n):
                
            N[k,j+1] = N[k,j] - N[k-1,j]
                
            fi = fi + ' * (x - ' + str(x[j-1]) + ')'
                
            ff = ff + ' + ' + str(np.round(N[j,j+1],decimals = decimals_points)) + '' + fi 
    elif method == "divided":
        for j in range(1,n):
            
            for k in range(j,n):
                
                N[k,j+1] = (N[k,j] - N[k-1,j]) / (x[k] - x[k-j])
                
            fi = fi + ' * (x - ' + str(x[j-1]) + ')'
                
            ff = ff + ' + ' + str(np.round(N[j,j+1],decimals = decimals_points)) + '' + fi 
    else:
        raise Exception("Wrong value encountered.")
        
    xcopy = x
    
    x = sym.symbols('x')
    
    px = sym.simplify(sym.sympify(ff))
    
    fx = px # simplified form
    
    px = round(px.subs(x,x0),decimals_points) # np.round does not work
    
    px = px
    
    return np.round(N, decimals_points), fx.evalf(decimals_points), sym.degree(fx), px
