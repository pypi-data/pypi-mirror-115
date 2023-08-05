from io import BytesIO
import base64

import numpy as np
import math as mt
import sympy as sym
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from IPython.display import Image
from IPython.core.display import HTML

def ivps(ode_equations, time_span, initial_y, steps_stepsize = ['n', 10], ivp_method = 'rk4', show_iterations = None, decimal_points = 8):
    
    '''
    Solve initial value problems of a single or systems of ordinary differential equations (ODEs).
    
    Returns the approximated values of a single ODE or systems of ODEs at the time points evaluated from the specified initial time point, final time point and number of steps or interval.
    
    Parameters
    ----------
    ode_equation: list or tuple
        A list/tuple of the form [ode equation, exact solution].
        
    time_span: 1D list / arrays
        Left and right end time points.
        
    initial_y: float or integer
        Value of y at initial time point.
         
    steps_stepsize: 1D array, optional
        steps_stepsize = ['h', 0.2] or [hmin, hmax, tolerance] if adaptive methods.
        First element is a string which can either be n or h for number of steps or stepsize respectively.
        If fist element is 'h' then the second value should be a float representing the step size (interval),
        otherwise, it should be an integer representing the number of steps.
        
    ivp_method: list or tuple, optional ['Method', None]
        The first element is a string specifying the initial value problem.
        The second element depends on the initial value specified.
            - For Taylor method, the second element specifies a list of derivatives of the ODE.
            - If multi-step or predictor corrector methods, then second element specifies the starting values.
            
        Available initial value methods
        =========================================================================================
        Valid value                           Description
        =========================================================================================
        'taylor1' ............................... Taylor order 1
        'taylor2' ............................... Taylor order 2
        'taylor3' ............................... Taylor order 3
        'taylor4' ............................... Taylor order 4
        'taylor5' ............................... Taylor order 5
        'explicit euler' or 'foward euler' ...... Explicit Euler
        'implicit euler' or 'backward euler' .... Implicit Euler
        'modified euler' ........................ Modified Euler
        'midpoint' .............................. Midpoint Runge-Kutta
        'modified euler rk' ..................... Modified Euler Runge-Kutta
        'second order ralston' .................. Second order Heun Runge-Kutta
        'third order heun' ...................... Third order Heun Runge-Kutta
        'third order nystrom' ................... Third order Nystrom Runge-Kutta
        'third order  ........................... Classical third order Runge-Kutta
        'fourth order' .......................... Classical fourth order Runge-Kutta
        'fourth order runge kutta mersen' ....... Fourth order Runge-Kutta-Mersen
        'fourth order runge kutta 3/8' .......... Fourth order Runge-Kutta 3/8
        'fifth order' ........................... Classical fifth order Runge-Kutta
        'backward euler rk' ..................... Implicit backward Euler Runge-Kutta
        'trapezoidal' ........................... Implicit implicit Trapezoidal Runge-Kutta
        'two stage gauss legendre' .............. Implicit two-stage Gauss-Legendre Runge-Kutta
        'three stage gauss legendre' ............ Implicit three-stage Gauss-Legendre Runge-Kutta
        'runge kutta fehlberg' .................. Adaptive Runge-Kutta-fehlberg
        'runge kutta verner' .................... Adaptive Runge-Kutta-Verner
        'adam bashforth 2 step' ................. Explicit Adam-Bashforth 2 step
        'adam bashforth 3 step' ................. Explicit Adam-Bashforth 3 step
        'adam bashforth 4 step' ................. Explicit Adam-Bashforth 4 step
        'adam bashforth 5 step' ................. Explicit Adam-Bashforth 5 step
        'adam moulton 2 step' ................... Implicit Adam-Moulton 2 step
        'adam moulton 3 step' ................... Implicit Adam-Moulton 3 step
        'adam moulton 4 step' ................... Implicit Adam-Moulton 4 step
        'adam bashforth moulton 2 step' ......... Adam-Bashforth-Moulton 2 step predictor-corrector
        'adam bashforth moulton 3 step' ......... Adam-Bashforth-Moulton 3 step predictor-corrector
        'adam bashforth moulton 4 step' ......... Adam-Bashforth-Moulton 4 step predictor-corrector
        'adam bashforth moulton 5 step' ......... Adam-Bashforth-Moulton 5 step predictor-corrector
        'euler heun' ............................ Euler-Heun predictor-corrector
        'milne simpson' ......................... Milne-Simpson predictor-corrector
        'modified milne simpson'................. Modified Milne-Simpson predictor-corrector
        'hamming' .............................. Hammings predictor-corrector
        
    show_iterations: integer, optional
        Integer representing the number of iterations to be displayed.
        Valid values: None or 1 <= x <= n.
        if None, then all iterations are displayed.
       
    decimal_points: integer, optional
        Integer representing number of decimal points to display in result (does not affect internal precision).
    
    Examples
    --------
    >> ode_function = '-1.2 * y + 7 * exp(-0.3 * t)'
    >> exact_solution = '70/9 * exp(-0.3 * t) - 43/9 * exp(-1.2 * t)'
    >> ivps(ode_equations = [ode_function, exact_solution],
    time_span = [0, 1],
    initial_y = 3,
    steps_stepsize = ['h', 0.12],
    ivp_method = 'rk4', 
    show_iterations = None, 
    decimal_points = 8)
    
    >> ivp_methods = ['euler', 'feuler', 'meuler', 'ieuler', 'beuler', 'midpoint', 'meuler-rk', 'ralston2', 'heun3', 'nystrom3', 'rk3', 'rk4', 'rkm', 'rk38', 'rk5', 'beuler-rk', 'trapezoidal', 'glegender1', 'glegender2', 'glegender3', 'ab2', 'ab3', 'ab4', 'ab5', 'am2', 'am3', 'am4', 'abm2', 'abm3', 'abm4', 'abm5', 'eh', 'ms', 'mms', 'hamming']
    >> ode_function = 'y - t ** 2 + 1'
    >> exact_solution = '(t+1) ** 2 - 1/2 * exp(t)'
    >> for k, method in enumerate(ivp_methods):
    results = ivps(ode_equations = [ode_function, exact_solution],
    time_span = [0, 2],
    initial_y = 0.5,
    steps_stepsize = ['h', 0.2],
    ivp_method = method,
    show_iterations = None,
    decimal_points = 8)
    display(method, results)
    '''
    
    # -------------------------------------------------------------------------
        # Capture and validate inputs
    # -------------------------------------------------------------------------
    
    valid_ivp_methods = ['taylor1', 'taylor2', 'taylor3', 'taylor4', 'taylor5', 'taylor6', 'taylor7', 'taylor8', 'taylor9', 'euler', 'feuler', 'meuler', 'ieuler', 'beuler', 'midpoint', 'meuler-rk', 'ralston2', 'heun3', 'nystrom3', 'rk3', 'rk4', 'rkm', 'rk38', 'rk5', 'beuler-rk', 'trapezoidal', 'glegender1', 'glegender2', 'glegender3', 'rkf', 'rkv', 'ab2', 'ab3', 'ab4', 'ab5', 'am2', 'am3', 'am4', 'abm2', 'abm3', 'abm4', 'abm5', 'eh', 'ms', 'mms', 'hamming', 'systems']  
    
    taylor_n = ['taylor1', 'taylor2', 'taylor3', 'taylor4', 'taylor5', 'taylor6', 'taylor7', 'taylor8', 'taylor9']
    
    multistep_predictor = ['ab2', 'ab3', 'ab4', 'ab5', 'am2', 'am3', 'am4', 'abm2', 'abm3', 'abm4', 'abm5', 'eh', 'ms', 'mms', 'hamming']
    
    approximate_methods = ['euler', 'meuler', 'heun3', 'rk4']
    
    if isinstance(ode_equations, str):
        ode_equations = [ode_equations]
    
    if len(ode_equations) == 1:
        ode_equations.insert(1, None)
       
    if isinstance(ivp_method, str):
        ivp_method = [ivp_method]
     
    if len(ivp_method) == 1:
        if ivp_method[0] in multistep_predictor:
            ivp_method.insert(1, 'rk4')
        else:
            ivp_method.insert(1, None)
    
    if ivp_method[0].lower() in multistep_predictor:
        if ivp_method[1] is not None:
            if ivp_method[1] not in approximate_methods:
                raise Exception('%s is an invalid method for approximating starting values. Valid methods are: %s' %(ivp_method[1], approximate_methods))
    
    if ivp_method[0].lower() in taylor_n:
        if ivp_method[1] is None:
            raise Exception('Please enter %s ODE derivative(s) for the %s method you have entered.' %(ivp_method[0][-1], ivp_method[0]))
        else:
            ode_derivatives = ivp_method[1]
        
    t, y = sym.symbols('t, y')
    # ode equation

    if len(ode_equations) > 2:
        raise ValueError('Please enter a list of at most 2 elements for ode_equations.')
    ode_equation = list(ode_equations)[0]
    try:
        fty = sym.sympify(ode_equation)
        f = sym.lambdify([t, y], sym.sympify(ode_equation), 'numpy')
        f_latex = sym.latex(sym.sympify(ode_equation))
    except:
        raise Exception('An error occurred while creating the ODE equation %s.' %(ode_equation))
    # exact solution
    if len(list(ode_equations)) == 2:
        exact_solution = ode_equations[1] 
        if exact_solution is not None:
            try:
                ft = sym.lambdify(t, sym.sympify(exact_solution), 'numpy')
            except:
                raise Exception('An error occurred while creating the exaction solution equation %s.' %(exact_solution))
       
    # time span
     
    if len(time_span) == 2:
        if isinstance(time_span[0], (int, float)):
            t0 = time_span[0]
        else:
            raise ValueError('Please enter a single integer or float value for initial time.')
        
        if isinstance(time_span[1], (int, float)):
            tf = time_span[1]
        else:
            raise ValueError('Please enter a single integer or float value for final time.')
        
        if t0 >= tf:
            raise ValueError('Final time must be greater than initial time.')
    else:
        raise ValueError('Please enter 2 values for time_span.')
    
    # initial value of y
    
    if isinstance(initial_y, (int, float)):
        y0 = initial_y
    else:
        raise ValueError('Please enter a single integer or float value for initial_y.')
    
    # initial value methods
            
    ivp_method_temp = ivp_method
    if len(ivp_method_temp) > 2:
        raise ValueError('Please enter atmost 2 elements for ivp_method.')
    elif len(ivp_method_temp) == 2:
        ivp_method = ivp_method[0].replace('  ', ' ').replace(' ', '-').replace('_', '-').lower()
        if ivp_method not in valid_ivp_methods:
            raise ValueError('%s is an invalid method for ivp_method. Valid methods are: %s.' %(ivp_method, valid_ivp_methods))
        # multi-step and predictor
        if ivp_method in multistep_predictor:
            if ivp_method_temp[1] is None:
                starting_values = 'rk4'
            else:
                if isinstance(ivp_method_temp[1], (list, tuple)):
                    starting_values = ivp_method_temp[1]
                elif isinstance(ivp_method_temp[1], str):
                    starting_values = ivp_method_temp[1]
                else:
                    raise ValueError('Please enter a list/tuple or IVP method to use for starting values (second element in ivp_method list/tuple).')
    else:
        raise ValueError('%s --- Please enter a list or tuple of atmost 2 elemets for ivp_method.' %(len(ivp_method_temp)))
        
    # Start step size or interval options
    
    if ivp_method != 'rkf' and ivp_method != 'rkv' :
        if len(steps_stepsize) == 2:
            if isinstance(steps_stepsize[1], (int, float)):
                if steps_stepsize[0] == 'h':
                    h = steps_stepsize[1]
                    if h > 0:
                        n = int(np.ceil((tf - t0) / float(h)))
                    else:
                        raise('h must be a positive number.') 
                elif steps_stepsize[0] == 'n':
                    n = steps_stepsize[1]
                    if n > 0:
                        if isinstance(n, int):
                            h = float((tf - t0) / int(n))
                        else:
                            raise ValueError('n must be an integer.')
                    else:
                        raise ValueError('n must be a positive integer.')
                else:
                    raise ValueError('\'%s\' is an invalid option for first element of steps_stepsize. First element of steps_stepsize can only be \'h\' or \'n\'.' %(steps_stepsize[0]))
            else:
                raise ValueError('Please enter a single integer or float value for number of steps / stepsize.')
        else:
            raise ValueError("Please enter 2 values for steps_stepsize e.g. ['n', 10] or ['h', 0.2].")
    else: # adaptive methods
        if len(steps_stepsize) == 3:
            if isinstance(steps_stepsize[0], (int, float)):
                hmin = steps_stepsize[0]
            else:
                raise ValueError('Please enter a single integer or float value hmin.')
            
            if isinstance(steps_stepsize[1], (int, float)):
                hmax = steps_stepsize[1]
            else:
                raise ValueError('Please enter a single integer or float value hmax.')
            
            if hmin >= hmax:
                raise ValueError('hmax must be greater than hmin.')
            
            if isinstance(steps_stepsize[2], (int, float)):
                tolerance = steps_stepsize[2]
            else:
                raise ValueError('Please enter a single integer or float value tolerance.')
            
        else:
            raise ValueError('Please enter steps_stepsize as: steps_stepsize = [hmin, hmax, tolerance] for %s.' %(ivp_method))
    
    # exact solution is not allowered for systems of equations
    if ivp_method_temp[0] == 'systems':
        if exact_solution is not None:
            raise Exception('A system of equation does not allow the exact solution to be given. Please set it to none (seond element of %s).' %(ode_equations))
        else:
            ode_systems = ode_equations[0]
            if len(ode_systems) < 2:
                raise ValueError('Please enter atleast 2 ordinary differential equations.')
            else:
                gf = np.zeros(0)
                for k, ode_system in enumerate(ode_systems):
                    try:
                        g = sym.lambdify(t, sym.sympify(ode_systems), 'numpy')
                        gf = np.append(gf, g)
                    except:
                        raise Exception('An error occurred while creating equation %s: %s.' %(k+1, ode_system))
                        
    # iterations to show
    
    if 'fehlberg' not in ivp_method and 'verner' not in ivp_method:
        if show_iterations is not None:
            if show_iterations < 1 or show_iterations > n:
                raise ValueError('The number of iterations must be between 1 and %s.' %(n))
            else:
                N = int(show_iterations)
        else:
            N = n+1
    
    # decimal points
    
    if isinstance(decimal_points, int):
        if decimal_points < 0 or decimal_points > 14:
            raise ValueError('The number of decimals must be an integer value between 0 and 14 inclusive.')
    else:
        raise ValueError('The number of decimals must be an integer value.')
    
    pd.set_option('display.precision', decimal_points)
    
    # initialize
    
    if 'fehlberg' not in ivp_method and 'verner' not in ivp_method:
        if steps_stepsize[0] == 'h':
            t = np.append(np.arange(t0, tf, h), tf)
            n = len(t)-1
        elif steps_stepsize[0] == 'n':
            t = np.linspace(t0, tf, n+1)
        else:
            raise ValueError('%s is an invalid option for steps_stepsize.' %(steps_stepsize)) 
            
        y = np.zeros(n+1)
        y[0] = y0
    
    # -------------------------------------------------------------------------
        # Begin calculations
    # -------------------------------------------------------------------------
    
    # Runge-Kutta for multi-step and predictor corrector methods
    
    if ivp_method in multistep_predictor:
        start_values = [y0]
        m = 5
        if isinstance(ivp_method_temp[1], str): # approximate method is given, otherwise they are values.
            
            if ivp_method_temp[1] == 'euler':
            
                for i in range(m):
                    h = t[i+1] - t[i]
                    y[i+1] = y[i] + h * f(t[i], y[i])
            
            elif ivp_method_temp[1] == 'meuler':
                    
                for i in range(m):
                    h = t[i+1] - t[i]
                    k1 = h * f(t[i], y[i])
                    k2 = h * f(t[i] + h, y[i] + k1)
                    y[i+1] = y[i] + (1/2) * (k1 + k2)
                
            elif ivp_method_temp[1] == 'heun3':
                    
                for i in range(m):
                    h = t[i+1] - t[i]
                    k1 = h * f(t[i], y[i])
                    k2 = h * f(t[i] + (1/3) * h, y[i] + (1/3) * k1)
                    k3 = h * f(t[i] + (2/3) * h, y[i] + (2/3) * k2)
                    y[i+1] = y[i] + (1/4) * (k1 + 3 *  k3)
                
            elif ivp_method_temp[1] == 'rk4':
                    
                for i in range(m):
                    h = t[i+1] - t[i]
                    k1 = h * f(t[i], y[i])
                    k2 = h * f(t[i] + h/2, y[i] + k1/2)
                    k3 = h * f(t[i] + h/2, y[i] + k2/2)
                    k4 = h * f(t[i] + h, y[i] + k3)
                    y[i+1] = y[i] + 1/6 * (k1 + 2 * k2 + 2 * k3 + k4)
        else:
            y[:len(ivp_method_temp[1])] = ivp_method_temp[1]
    
    if 'taylor' in ''.join(ivp_method):
        taylor_equations = [ode_equations[0]] + ode_derivatives
            
# -----------------------------------------------------------------------------
    # Taylor method
# -----------------------------------------------------------------------------
    
    fty = str(ode_equations[0])

    if ivp_method == 'taylor1':
        
        f1 = sym.lambdify(['t, y'],sym.sympify(taylor_equations[0]),'numpy')

        for i in range(0,n):
            
            h = t[i+1] - t[i]
            d1f = f1(t[i],y[i])
            
            y[i+1] = y[i] + (h/mt.factorial(1)) * d1f
        
    elif ivp_method == 'taylor2':
         
        f1 = sym.lambdify(['t, y'],sym.sympify(taylor_equations[0]),'numpy')
        f2 = sym.lambdify(['t, y'],sym.sympify(taylor_equations[1]),'numpy')

        for i in range(0,n):
            
            h = t[i+1] - t[i]
            d1f = f1(t[i],y[i])
            d2f = f2(t[i],y[i])
            
            y[i+1] = y[i] + (h/mt.factorial(1)) * d1f + (h**2/mt.factorial(2)) * d2f
        
    elif ivp_method == 'taylor3':
         
        f1 = sym.lambdify(['t, y'],sym.sympify(taylor_equations[0]),'numpy')
        f2 = sym.lambdify(['t, y'],sym.sympify(taylor_equations[1]),'numpy')
        f3 = sym.lambdify(['t, y'],sym.sympify(taylor_equations[2]),'numpy')

        for i in range(0,n):
            
            h = t[i+1] - t[i]
            d1f = f1(t[i],y[i])
            d2f = f2(t[i],y[i])
            d3f = f3(t[i],y[i])
            
            y[i+1] = y[i] + (h/mt.factorial(1)) * d1f + (h**2/mt.factorial(2)) * d2f + (h**3/mt.factorial(3)) * d3f
    
    elif ivp_method == 'taylor4':
        
        f1 = sym.lambdify(['t, y'],sym.sympify(taylor_equations[0]),'numpy')
        f2 = sym.lambdify(['t, y'],sym.sympify(taylor_equations[1]),'numpy')
        f3 = sym.lambdify(['t, y'],sym.sympify(taylor_equations[2]),'numpy')
        f4 = sym.lambdify(['t, y'],sym.sympify(taylor_equations[3]),'numpy')

        for i in range(0,n):
            
            h = t[i+1] - t[i]
            d1f = f1(t[i],y[i])
            d2f = f2(t[i],y[i])
            d3f = f3(t[i],y[i])
            d4f = f4(t[i],y[i])
            
            y[i+1] = y[i] + (h/mt.factorial(1)) * d1f + (h**2/mt.factorial(2)) * d2f + (h**3/mt.factorial(3)) * d3f + (h**4/mt.factorial(4)) * d4f
    
    elif ivp_method == 'taylor5':
        
        f1 = sym.lambdify(['t, y'],sym.sympify(taylor_equations[0]),'numpy')
        f2 = sym.lambdify(['t, y'],sym.sympify(taylor_equations[1]),'numpy')
        f3 = sym.lambdify(['t, y'],sym.sympify(taylor_equations[2]),'numpy')
        f4 = sym.lambdify(['t, y'],sym.sympify(taylor_equations[3]),'numpy')
        f5 = sym.lambdify(['t, y'],sym.sympify(taylor_equations[4]),'numpy')

        for i in range(0,n):
            
            h = t[i+1] - t[i]
            d1f = f1(t[i],y[i])
            d2f = f2(t[i],y[i])
            d3f = f3(t[i],y[i])
            d4f = f4(t[i],y[i])
            d5f = f5(t[i],y[i])
            
            y[i+1] = y[i] + (h/mt.factorial(1)) * d1f + (h**2/mt.factorial(2)) * d2f + (h**3/mt.factorial(3)) * d3f + (h**4/mt.factorial(4)) * d4f + (h**5/mt.factorial(5)) * d5f
          
    # =========================================================================
        # Euler methods
    # =========================================================================
    
    elif ivp_method == 'feuler' or ivp_method == 'euler' or ivp_method == 'eeuler':
      
        for i in range(n):
            h = t[i+1] - t[i]
            y[i+1] = y[i] + h * f(t[i], y[i])
    
    elif ivp_method == 'meuler':
        
        for i in range(n):
            h = t[i+1] - t[i]
            ynew = y[i] + h * f(t[i], y[i])
            y[i+1] = y[i] + (h/2) * (f(t[i], y[i]) + f(t[i+1], ynew))
            
    elif ivp_method == 'beuler' or ivp_method == 'ieuler':
        for i in range(n):
            h = t[i+1] - t[i]
            fs_symbolic = str(fty).replace('t', '(' + str(t[i+1]) + ')')
            fs_symbolic = fs_symbolic.replace('y', 'y' + str(i))
            fs_symbolic = 'y' + str(i) + ' - (' + str(y[i]) + ' + ' + str(h) + ' * (' + str(fs_symbolic) + '))'
            y[i+1] = sym.solve(fs_symbolic)[0]
    
    # =========================================================================
        # Explicit Runge-Kutta methods
    # =========================================================================

    elif ivp_method == 'midpoint':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/2, y[i] + k1/2)
            y[i+1] = y[i] + k2
       
    # -------------------------------------------------------------------------
       
    elif ivp_method == 'meuler-rk':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h, y[i] + k1)
            y[i+1] = y[i] + (1/2) * (k1 + k2)
        
    # -------------------------------------------------------------------------
      
    elif ivp_method == 'ralston2':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + (3/4) * h, y[i] + (3/4) * k1)
            y[i+1] = y[i] + (1/3) * (k1 + 2 * k2)
        
    # -------------------------------------------------------------------------
      
    elif ivp_method == 'heun3':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + (1/3) * h, y[i] + (1/3) * k1)
            k3 = h * f(t[i] + (2/3) * h, y[i] + (2/3) * k2)
            y[i+1] = y[i] + (1/4) * (k1 + 3 *  k3)
        
    # -------------------------------------------------------------------------
    
    elif ivp_method == 'nystrom3':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + 2/3 * h, y[i] + 2/3 * k1)
            k3 = h * f(t[i] + 2/3 * h, y[i] + 2/3 * k2)
            y[i+1] = y[i] + (1/8) * (2 * k1 + 3 * k2 + 3 * k3)
       
    # -------------------------------------------------------------------------
    
    elif ivp_method == 'rk3':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/2, y[i] + 1/2 * k1)
            k3 = h * f(t[i] + h, y[i] - k1 + 2 * k2)
            y[i+1] = y[i] + (1/6) * (k1 + 4 * k2 + k3)
   
    # -------------------------------------------------------------------------
    
    elif ivp_method == 'rk4':
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/2, y[i] + k1/2)
            k3 = h * f(t[i] + h/2, y[i] + k2/2)
            k4 = h * f(t[i] + h, y[i] + k3)
            y[i+1] = y[i] + 1/6 * (k1 + 2 * k2 + 2 * k3 + k4)
       
    # -------------------------------------------------------------------------
    
    elif ivp_method == 'rkm':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/3, y[i] + k1/3)
            k3 = h * f(t[i] + h/2, y[i] + k1/6 + k2/6)
            k4 = h * f(t[i] + h/2, y[i] + k1/8 + 3/8 * k3)
            k5 = h * f(t[i] + h, y[i] + k1/2 - 3/2 * k3 + 2 * k4)
            y[i+1] = y[i] + (1/6) * (k1 + 4 * k2 + k5)
       
    # -------------------------------------------------------------------------
    
    elif ivp_method == 'rk38':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + 1/3 * h, y[i] + 1/3 * k1)
            k3 = h * f(t[i] + 2/3 * h, y[i] - 1/3 * k1 + k2)
            k4 = h * f(t[i] + h, y[i] + k1 - k2 + k3)
            y[i+1] = y[i] + (1/8) * (k1 + 3 * k2 + 3 * k3 + k4)
        
    # -------------------------------------------------------------------------
    
    elif ivp_method == 'rk5':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/4, y[i] + (1/4) * k1)
            k3 = h * f(t[i] + h/4, y[i] + (1/8) * k1 + (1/8) * k2)
            k4 = h * f(t[i] + h/2, y[i] - (1/2) * k2 + k3)
            k5 = h * f(t[i] + (3 * h)/4, y[i] + (3/16) * k1 + (9/16) * k4)
            k6 = h * f(t[i] + h, y[i] - (3/7) * k1 + (2/7) * k2 + (12/7) * k3 - (12/7) * k4 + (8/7) * k5)
            y[i+1] = y[i] + (1/90) * (7 * k1 + 32 * k3 + 12 * k4 + 32 * k5 + 7 * k6)
    
    # =========================================================================
        # Adaptive Runge-Kutta methods
    # =========================================================================
      
    elif ivp_method == 'rkf':
        
        t = t0
        y = y0
        h = hmax
    
        T = np.array([t])
        Y = np.array([y])
    
        while t < tf:
    
            if t + h > tf:
                h = tf - t
    
            k1 = h * f(t, y)
            k2 = h * f(t + h/4, y + 1/4 * k1)
            k3 = h * f(t + 3/8 * h, y + 3/32 * k1 + 9/32 * k2)
            k4 = h * f(t + 12/13 * h, y + 1932/2197 * k1 - 7200/2197 * k2 + 7296/2197 * k3)
            k5 = h * f(t + h, y + 439/216 * k1 - 8 * k2 + 3680/513 * k3 - 845/4104 * k4)
            k6 = h * f(t +h/2, y - 8/27 * k1 + 2 * k2 - 3544/2565 * k3 + 1859/4104 * k4 - 11/40 * k5)
    
            R = (1/h) * abs(1/360 * k1 - 128/4275 * k3 - 2197/75240 * k4 + 1/50 * k5 + 2/55 * k6)
            
            if len(np.shape(R)) > 0:
                R = max(R)
            if R <= tolerance:
                t = t + h
                y = y + 25/216 * k1 + 1408/2565 * k3 + 2197/4104 * k4 - 1/5 * k5
                
                T = np.append(T, t)
                Y = np.append(Y, y)
                
            h = h * min(max(0.84 * (tolerance / R) ** (1/4), 0.1), 4.0)
    
            if h > hmax:
                h = hmax
            elif h < hmin:
                break
        y = Y
        t = T
        n = len(y)
        if show_iterations != None:
            N = show_iterations
        else:
            N = n
    
    elif ivp_method == 'beuler-rk':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/4, y[i] + (1/4) * k1)
            k3 = h * f(t[i] + h/4, y[i] + (1/8) * k1 + (1/8) * k2)
            k4 = h * f(t[i] + h/2, y[i] - (1/2) * k2 + k3)
            k5 = h * f(t[i] + (3 * h)/4, y[i] + (3/16) * k1 + (9/16) * k4)
            k6 = h * f(t[i] + h, y[i] - (3/7) * k1 + (2/7) * k2 + (12/7) * k3 - (12/7) * k4 + (8/7) * k5)
            y[i+1] = y[i] + (1/90) * (7 * k1 + 32 * k3 + 12 * k4 + 32 * k5 + 7 * k6)
       
    elif ivp_method == 'trapezoidal':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/4, y[i] + (1/4) * k1)
            k3 = h * f(t[i] + h/4, y[i] + (1/8) * k1 + (1/8) * k2)
            k4 = h * f(t[i] + h/2, y[i] - (1/2) * k2 + k3)
            k5 = h * f(t[i] + (3 * h)/4, y[i] + (3/16) * k1 + (9/16) * k4)
            k6 = h * f(t[i] + h, y[i] - (3/7) * k1 + (2/7) * k2 + (12/7) * k3 - (12/7) * k4 + (8/7) * k5)
            y[i+1] = y[i] + (1/90) * (7 * k1 + 32 * k3 + 12 * k4 + 32 * k5 + 7 * k6)
        
    elif ivp_method == 'glegendre2':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/4, y[i] + (1/4) * k1)
            k3 = h * f(t[i] + h/4, y[i] + (1/8) * k1 + (1/8) * k2)
            k4 = h * f(t[i] + h/2, y[i] - (1/2) * k2 + k3)
            k5 = h * f(t[i] + (3 * h)/4, y[i] + (3/16) * k1 + (9/16) * k4)
            k6 = h * f(t[i] + h, y[i] - (3/7) * k1 + (2/7) * k2 + (12/7) * k3 - (12/7) * k4 + (8/7) * k5)
            y[i+1] = y[i] + (1/90) * (7 * k1 + 32 * k3 + 12 * k4 + 32 * k5 + 7 * k6)
      
    elif ivp_method == 'glegendre3':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/4, y[i] + (1/4) * k1)
            k3 = h * f(t[i] + h/4, y[i] + (1/8) * k1 + (1/8) * k2)
            k4 = h * f(t[i] + h/2, y[i] - (1/2) * k2 + k3)
            k5 = h * f(t[i] + (3 * h)/4, y[i] + (3/16) * k1 + (9/16) * k4)
            k6 = h * f(t[i] + h, y[i] - (3/7) * k1 + (2/7) * k2 + (12/7) * k3 - (12/7) * k4 + (8/7) * k5)
            y[i+1] = y[i] + (1/90) * (7 * k1 + 32 * k3 + 12 * k4 + 32 * k5 + 7 * k6)
    
    elif ivp_method == 'rkf':
        
        y = tolerance, approximate
     
    elif ivp_method == 'rkv':
        
        y = tolerance, approximate
    
    # =========================================================================
        # Variable stepsize methods
    # =========================================================================
      
    elif ivp_method == 'variable':
        
        y = tolerance, approximate
     
    elif ivp_method == 'variable':
        
        y = tolerance, approximate
     
    elif ivp_method == 'ab2':
        
        for i in range(1, n):
            h = t[i+1] - t[i]
            y[i+1] = y[i] + (h/2) * (3 * f(t[i], y[i]) - f(t[i-1], y[i-1]))
    
    elif ivp_method == 'ab3':
        
        for i in range(2, n):
            h = t[i+1] - t[i]
            y[i+1] = y[i] + (h/12) * (23 * f(t[i], y[i]) - 16 * f(t[i-1], y[i-1]) + 5 * f(t[i-2], y[i-2]))
    
    elif ivp_method == 'ab4':
        
        for i in range(3, n):
            h = t[i+1] - t[i]
            y[i+1] = y[i] + (h/24) * (55 * f(t[i], y[i]) - 59 * f(t[i-1], y[i-1]) + 37 * f(t[i-2], y[i-2]) - 9 * f(t[i-3], y[i-3]))
    
    elif ivp_method == 'ab5':
        
        for i in range(4, n):
            h = t[i+1] - t[i]
            y[i+1] = y[i] + (h/720) * (1901 * f(t[i], y[i]) - 2774 * f(t[i-1], y[i-1]) + 2616 * f(t[i-2], y[i-2]) - 1274 * f(t[i-3], y[i-3]) + 251 * f(t[i-4], y[i-4]))
    
    elif ivp_method == 'am2':
        
        for i in range(1, n):
            h = t[i+1] - t[i]
            fty_symbolic = fty.replace('t', '(' + str(t[i+1]) + ')')
            fty_symbolic = fty_symbolic.replace('y', 'y' + str(i))
            fty_symbolic = 'y' + str(i) + ' - (' + str(y[i]) + ' + ' + str(h/12) + ' * (5 * (' + str(fty_symbolic) + ') + ' + str(8 * f(t[i], y[i]) - f(t[i-1], y[i-1])) + '))'
            y[i+1] = sym.solve(fty_symbolic)[0]
    
    elif ivp_method == 'am3':
        
        for i in range(2, n):
            h = t[i+1] - t[i]
            fty_symbolic = fty.replace('t', '(' + str(t[i+1]) + ')')
            fty_symbolic = fty_symbolic.replace('y', 'y' + str(i))
            fty_symbolic = 'y' + str(i) + ' - (' + str(y[i]) + ' + ' + str(h/24) + ' * (9 * (' + str(fty_symbolic) + ') + ' + str(19 * f(t[i], y[i]) - 5 * f(t[i-1], y[i-1]) + f(t[i-2], y[i-2])) + '))'
            y[i+1] = sym.solve(fty_symbolic)[0]
    
    elif ivp_method == 'am4':
        
        for i in range(3, n):
            h = t[i+1] - t[i]
            fty_symbolic = fty.replace('t', '(' + str(t[i+1]) + ')')
            fty_symbolic = fty_symbolic.replace('y', 'y' + str(i))
            fty_symbolic = 'y' + str(i) + ' - (' + str(y[i]) + ' + ' + str(h/720) + ' * (251 * (' + str(fty_symbolic) + ') + ' + str(646 * f(t[i], y[i]) - 264 * f(t[i-1], y[i-1]) + 106 * f(t[i-2], y[i-2]) - 19 * f(t[i-3], y[i-3])) + '))'
            y[i+1] = sym.solve(fty_symbolic)[0]
    
    elif ivp_method == 'am5':
        
        for i in range(4, n):
            h = t[i+1] - t[i]
            y[i+1] = np.nan
    
    # =========================================================================
        # Predictor-corrector methods
    # =========================================================================
      
    elif ivp_method == 'abm2':
        
        for i in range(1, n):
            h = t[i+1] - t[i]
            # Adams-Bashforth 2-step as predictor
            y[i+1] = y[i] + (h/2) * (3 * f(t[i], y[i]) - f(t[i-1], y[i-1]))
            # Adams-Moulton 2-step as corrector
            y[i+1] = y[i] + (h/2) * (f(t[i+1], y[i+1]) + f(t[i], y[i]))
    
    elif ivp_method == 'abm3':
        
        for i in range(2, n):
            h = t[i+1] - t[i]
            # Adams-Bashforth 3-step as predictor
            y[i+1] = y[i] + (h/12) * (23 * f(t[i], y[i]) - 16 * f(t[i-1], y[i-1]) + 5 * f(t[i-2], y[i-2]))
            # Adams-Moulton 2-step as corrector
            y[i+1] = y[i] + (h/12) * (5 * f(t[i+1], y[i+1]) + 8 * f(t[i], y[i]) - f(t[i-1], y[i-1]))
    
    elif ivp_method == 'abm4':
        
        for i in range(3, n):
            h = t[i+1] - t[i]
            # Adams-Bashforth 4-step as predictor
            y[i+1] = y[i] + (h/24) * (55 * f(t[i], y[i]) - 59 * f(t[i-1], y[i-1]) + 37 * f(t[i-2], y[i-2]) - 9 * f(t[i-3], y[i-3]))
            # Adams-Moulton 3-step as corrector
            y[i+1] = y[i] + (h/24) * (9 * f(t[i+1], y[i+1]) + 19 * f(t[i], y[i]) - 5 * f(t[i-1], y[i-1]) + f(t[i-2], y[i-2]))
    
    elif ivp_method == 'abm5':
        
        for i in range(4, n):
            h = t[i+1] - t[i]
            # Adams-Bashforth 5-step as predictor
            y[i+1] = y[i] + (h/720) * (1901 * f(t[i], y[i]) - 2774 * f(t[i-1], y[i-1]) + 2616 * f(t[i-2], y[i-2]) - 1274 * f(t[i-3], y[i-3]) + 251 * f(t[i-4], y[i-4]))
            # Adams-Moulton 4-step as corrector
            y[i+1] = y[i] + (h/720) * (251 * f(t[i+1], y[i+1]) + 646 * f(t[i], y[i]) - 264 * f(t[i-1], y[i-1]) + 106 * f(t[i-2], y[i-2]) - 19 * f(t[i-3], y[i-3]))
       
    elif ivp_method == 'eh':
        
        for i in range(n):
            h = t[i+1] - t[i]
            # Explicit Euler as predictor
            y[i+1] = y[i] + h * f(t[i], y[i])
            # Heun as corrector
            y[i+1] = y[i] + (h/2) * (f(t[i+1], y[i+1]) + f(t[i], y[i]))
       
    elif ivp_method == 'ms':
        
        for i in range(3, n):
            h = t[i+1] - t[i]
            # Milne as predictor
            y[i+1] = y[i-3] + (4 * h/3) * (2 * f(t[i], y[i]) - f(t[i-1], y[i-1]) + 2 * f(t[i-2], y[i-2]))
            # Simpson as corrector
            y[i+1] = y[i-1] + (h/3) * (f(t[i+1], y[i+1]) + 4 * f(t[i], y[i]) + f(t[i-1], y[i-1]))
       
    elif ivp_method == 'mms':
        
        for i in range(3, n):
            h = t[i+1] - t[i]
            # Milne as predictor
            y[i+1] = y[i-3] + (4 * h/3) * (2 * f(t[i], y[i]) - f(t[i-1], y[i-1]) + 2 * f(t[i-2], y[i-2]))
            # Modifier
            y[i+1] = y[i+1] + (28/29) * (y[i] - y[i-1])
            # Simpson as corrector
            y[i+1] = y[i-1] + (h/3) * (f(t[i+1], y[i+1]) + 4 * f(t[i], y[i]) + f(t[i-1], y[i-1]))
       
    elif ivp_method == 'hamming':
        
        for i in range(3, n):
            h = t[i+1] - t[i]
            # Milne as predictor
            y[i+1] = y[i-3] + (4 * h/3) * (2 * f(t[i], y[i]) - f(t[i-1], y[i-1]) + 2 * f(t[i-2], y[i-2]))
            # Hamming as corrector
            y[i+1] = (9 * y[i] - y[i-2]) / 8 + (3 * h/8) * (f(t[i+1], y[i+1]) + 2 * f(t[i], y[i]) - f(t[i-1], y[i-1]))
    
    # =========================================================================
        # Systems of ODEs
    # =========================================================================
       
    elif ivp_method == 'systems':
        
        for i in range(4, n):
            h = t[i+1] - t[i]
            y[i+1] = np.nan
    
    # -------------------------------------------------------------------------
        # Exact solution
    # -------------------------------------------------------------------------

    if exact_solution is not None:
        t_exact = np.linspace(t0, tf, 250)
        y_exact = ft(t_exact)
        y_time_span = ft(t)
        absolute_error = abs(y_time_span - y)
        table_results = np.vstack([t, y, y_time_span, absolute_error]).T
        table_results = table_results[0:N+1, :]    
        table_results = pd.DataFrame(table_results, columns = ['Time (t)', 'Approximated (yi)', 'Exact solution(y)', 'Error: | y - yi |'])
    else:
        table_results = np.vstack([t, y]).T
        table_results = table_results[0:N+1, :]
        table_results = pd.DataFrame(table_results, columns = ['Time (t)', 'Approximated (yi)'])
    
    tab_results = np.array(table_results.iloc[:N, :])
    
    # -------------------------------------------------------------------------
        # Plot figure
    # -------------------------------------------------------------------------
     
    valid_figure_styles = plt.style.available
    
    figure_properties = ['fast', 7, 5, 'D', 'b', 6, '-', 'b', 1.5, r'$ f(t, y) = ' + f_latex + '$', 'Time (t)', 'Solution (y)', 'k', 13]
    figure_style, figure_width, figure_height, figure_marker, figure_markerfacecolor, figure_markersize, figure_linestyle, figure_color, figure_linewidth, figure_title, figure_xtitle, figure_ytitle, figure_fontcolor, figure_fontsize = figure_properties
    
    with plt.style.context(figure_style):
        plt.figure(figsize = (figure_width, figure_height))
        if exact_solution is not None:
            plt.plot(t_exact, y_exact, 'r', linewidth = 2)
        
        if ivp_method == 'systems':
            tab_results = table_results[:N, :]
            if n <= 30:
                for i in range(tab_results.shape[1]):
                    plt.plot(tab_results[:, 0], tab_results[:, i], marker = figure_marker)
            else:
                for i in range(tab_results.shape[1]):
                    plt.plot(tab_results[:, 0], tab_results[:, i])
        else:
            if n <= 30:
                plt.plot(tab_results[:, 0], tab_results[:, 1], linestyle = figure_linestyle, color = figure_color, linewidth = figure_linewidth, marker = figure_marker, markersize = figure_markersize, markerfacecolor = figure_markerfacecolor)
            else: 
                plt.plot(tab_results[:, 0], tab_results[:, 1], linestyle = figure_linestyle, color = figure_color, linewidth = figure_linewidth)
        
        figure_fontdict = {'color': figure_fontcolor, 'size': figure_fontsize}
        plt.title(figure_title, fontdict = figure_fontdict)
        plt.xlabel(figure_xtitle, fontdict = figure_fontdict)
        plt.ylabel(figure_ytitle, fontdict = figure_fontdict)
        plt.tight_layout()
                
        figure_file = BytesIO()
        plt.savefig(figure_file, format = 'png')
        figure_file.seek(0)
        plotted_figure = base64.b64encode(figure_file.getvalue()).decode('ascii')
        figure_link = 'data:image/png;base64, ' + str(plotted_figure)
    
    return table_results, Image(url = figure_link)