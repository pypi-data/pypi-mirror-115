import numpy as np
import sympy as sym

def parametric_differentiation(f, g, dependent_variable, n, simplification_method = 'None'):
    
    '''
    Performs differentiation on two parametric equations.
    
    Parameters
    ----------
    f: Sympy Mul
        A Sympy Mul object containing the first parametric equation.
        
    g: Sympy Mul
        A Sympy Mul object containing the second parametric equation.
        
    dependent_variable: Sympy Symbol
        Dependent variable.
    n: integer
        Order of differentiation.
        
    simplification_method: str (or list if method is 'collect'), optional
        Simplification method to be applied to the final answer.
        
    Example
    -------
    >> t = sym.symbols('t')
    >> x = t ** 3 - 3 * t ** 2
    >> y = t ** 4 - 8 * t ** 2
    >> parametric_differentiation(f = x, g = y, 
                                  dependent_variable = t, n = 3)
    
    >> t = sym.symbols('t')
    >> x = sin(t)
    >> y = cos(t)
    >> parametric_differentiation(f = x, g = y, 
                                  dependent_variable = t, n = 2,
                                  simplification_method = 'simplify')
    '''
    
    t = dependent_variable
    # check that a positive integer
    if np.mod(n, 1) != 0 or n < 0:
        raise ValueError('n must be a positive integer')
    else:
        if n == 1:
            para_derivative = sym.diff(g, t) / sym.diff(f, t)
        else:
            # perform the normal differentiation recurssively
            para_derivative = sym.diff(parametric_differentiation(g, f, t, n-1), t) / sym.diff(f, t)
    numerator, denominator = sym.numer(para_derivative), sym.denom(para_derivative)
    # perform simplification according to the simplification method specfied
    if simplification_method == 'None':
        result = sym.factor(numerator) / sym.factor(denominator)
    elif simplification_method == 'simplify':
        result = sym.simplify(numerator) / sym.simplify(denominator)
    elif simplification_method == 'factor':
        result = sym.factor(numerator) / sym.factor(denominator)
    elif simplification_method == 'expand':
        result = sym.expand(numerator) / sym.expand(denominator)
    elif 'collect' in simplification_method:
        # stop and return an error if simplification method is not a list
        if not isinstance(simplification_method, list):
            raise ValueError('Specifiy the simplification_method argument as a list.')
        result = sym.collect(numerator, simplification_method[1]) / sym.collect(denominator, simplification_method[1])
    elif simplification_method == 'together':
        result = sym.together(numerator) / sym.together(denominator)
    elif simplification_method == 'cancel':
        result = sym.cancel(numerator) / sym.cancel(denominator)
    else:
        raise ValueError("%s is an invalid value for the argument 'simplification_method'" %(simplification_method))
    return result