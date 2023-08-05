import numpy as np
import sympy as sym

def polynomial_from_roots(polynomial_roots, polynomial_variable, expand_factors = True):
    
    polynomial_equation = sym.sympify(' * '.join(['(%s - %s)' %(polynomial_variable, item) for _, item in enumerate(polynomial_roots)]))
    if expand_factors:
        polynomial_equation = polynomial_equation.expand()

    return polynomial_equation

def remove_zeros(f, truncate_value = 1e-6):
    
    x = sym.symbols('x')
    g = np.array(sym.Poly(f).all_coeffs()); 
    g = np.fliplr(np.array([g]))
    g[abs(g) < truncate_value] = 0
    g = np.trim_zeros(np.ravel(g), 'f') # 'b' 'bf'
    g = [str(g[k]) + ' * x ** ' + str(k) for k in range(len(g))]
    g = ' + '.join(map(str, g))
    g = sym.sympify(g)
    
    return g