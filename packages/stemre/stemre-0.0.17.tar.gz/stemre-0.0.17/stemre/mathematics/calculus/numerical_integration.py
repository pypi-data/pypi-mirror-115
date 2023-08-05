import scipy.special as spe

def gauss_legendre(f, a, b, n):
    
    '''
    function GaussLegendre(f, a, b, n):
             evaluates the integral of f from a to b 
             using Gauss-Legendre method
     Inputs:
           f - function to be integrated
           a - lower limit of integration
           b - upper limit of integration
           n - number of points to use
    '''
    
    if a >= b:
        raise ValueError('Lower integration limit can not be greater than upper integration limit.')
    if not isinstance(n, int) or n < 2:
        raise ValueError('Number of points n must be a positive integer greater than 1.')
    
    x, w = spe.roots_legendre(n)
    
    t = 1/2 * (a + b) + 1/2 * (b - a) * x # transformation
    dt = 1/2 * (b - a) # derivative of transformed variable
    I = dt * sum(w * f(t))
    return I