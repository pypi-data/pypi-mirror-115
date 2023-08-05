from datetime import datetime
import numpy as np
import math as mt
import sympy as sym
import pandas as pd
import matplotlib.pyplot as plt

def ivps(ode_equations, time_span, initial_y, steps_stepsize = ['n', 10], ivp_method = ['Fourth order', None], show_iterations = None, show_figure = True, decimal_points = 8, **figure_properties):
    
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
            .
            .
            .
        'taylor9' ............................... Taylor order 9
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
        'hammings' .............................. Hammings predictor-corrector
        
    show_iterations: integer, optional
        Integer representing the number of iterations to be displayed.
        Valid values: None or 1 <= x <= n.
        if None, then all iterations are displayed.
       
    figure_properties = 1D list, optional
        List representing the plot StyleSheet, figure width, figure height, figure title, x-label, y-label and font-size.
        Example of valid values: None, 7, 5, None, 'Time (t)', 'Approximate values (y)', 20.
       
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
    ivp_method = ['Fourth order', None], 
    show_iterations = None, 
    decimal_points = 8)
    
    >> ivp_methods = ['explicit euler', 'forward euler', 'modified euler', 'implicit euler', 'backward euler', 'midpoint', 'modified euler rk', 'second order ralston', 'third order heun', 'third order nystrom', 'third order', 'fourth order', 'fourth order runge kutta mersen', 'fourth order runge kutta 3/8', 'fifth order']
    >> ode_function = 'y - t ** 2 + 1'
    >> exact_solution = '(t+1) ** 2 - 1/2 * exp(t)'
    >> for k, kth_ivp_method in enumerate(ivp_methods):
    results = ivps(ode_equations = [ode_function, exact_solution],
    time_span = [0, 2],
    initial_y = 0.5,
    steps_stepsize = ['h', 0.2],
    ivp_method = [kth_ivp_method, None],
    show_iterations = None,
    figure_title = kth_ivp_method, figure_xtitle = 'Time (t)', figure_ytitle = 'y', figure_fontsize = 15, figure_width = 7, figure_height = 5,
    decimal_points = 8)
    print('\n' + str(k+1) + '. ' + kth_ivp_method + '\n\n',results)
    '''
    
    # -------------------------------------------------------------------------
        # Capture and validate inputs
    # -------------------------------------------------------------------------
    
    # equations
    
    t, y = sym.symbols('t, y')
    # ode equation
    if len(list(ode_equations)) > 2:
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
        if isinstance(time_span[0], int) or isinstance(time_span[0], float):
            t0 = time_span[0]
        else:
            raise ValueError('Please enter a single integer or float value for initial time.')
        
        if isinstance(time_span[1], int) or isinstance(time_span[1], float):
            tf = time_span[1]
        else:
            raise ValueError('Please enter a single integer or float value for final time.')
        
        if t0 >= tf:
            raise ValueError('Final time must be greater than initial time.')
    else:
        raise ValueError('Please enter 2 values for time_span.')
    
    # initial value of y
    
    if isinstance(initial_y, int) or isinstance(initial_y, float):
        y0 = initial_y
    else:
        raise ValueError('Please enter a single integer or float value for initial_y.')
    
    # initial value methods
            
    valid_ivp_methods = ['taylor1', 'taylor2', 'taylor3', 'taylor4', 'taylor5', 'taylor6', 'taylor7', 'taylor8', 'taylor9', 'explicit euler', 'forward euler', 'modified euler', 'implicit euler', 'backward euler', 'midpoint', 'modified euler rk', 'second order ralston', 'third order heun', 'third order nystrom', 'third order', 'fourth order', 'fourth order runge kutta mersen', 'fourth order runge kutta 3/8', 'fifth order', 'backward euler rk', 'trapezoidal', 'one stage gauss legendre', 'two stage gauss legendre', 'three stage gauss legendre', 'runge kutta fehlberg', 'runge kutta verner', 'adam bashforth 2 step', 'adam bashforth 3 step', 'adam bashforth 4 step', 'adam bashforth 5 step', 'adam moulton 2 step', 'adam moulton 3 step', 'adam moulton 4 step', 'adam bashforth moulton 2 step', 'adam bashforth moulton 3 step', 'adam bashforth moulton 4 step', 'adam bashforth moulton 5 step', 'euler heun', 'milne simpson', 'modified milne simpson', 'hammings', 'systems']  
    ivp_method_temp = list(ivp_method)
    if len(ivp_method_temp) > 2:
        raise ValueError('Please enter atmost 2 elements for ivp_method.')
    elif len(list(ivp_method_temp)) == 1:
        ivp_method = ivp_method_temp[0]
        ivp_method = ivp_method[0].replace(' ', ' ').replace('-', ' ').replace('_', ' ').lower()
        if ivp_method not in valid_ivp_methods:
            raise ValueError('You have entered an invalid value for ivp_method. Valid values are: %s.' %(valid_ivp_methods))
        # if a list of one element is given, then it the method can not be Taylor, multistep or predictor
        if ivp_method in valid_ivp_methods[1:10]:
            raise ValueError('Please enter %s derivative(s) for the %s method you have entered.' %(int(ivp_method[-1]), ivp_method))
        if ivp_method in valid_ivp_methods[-15:]:
            raise ValueError('Please enter starting values for the %s method you have entered.' %(ivp_method))
    elif len(ivp_method_temp) == 2:
        ivp_method = ivp_method[0].replace(' ', ' ').replace('-', ' ').replace('_', ' ').lower()
        if ivp_method not in valid_ivp_methods:
            raise ValueError('You have entered an invalid value for ivp_method. Valid values are: %s.' %(valid_ivp_methods))
        # taylor methods
        if ivp_method in valid_ivp_methods[:9]:
            if ivp_method_temp[1] is None:
                raise ValueError('Please enter %s derivative(s) for the %s method you have entered.' %(int(ivp_method[-1]), ivp_method))
            else:
                gf = np.zeros(0)
                ode_derivatives = list(ivp_method_temp[1])
                if len(ode_derivatives) == 0 or len(ode_derivatives) > 9:
                    raise ValueError('Please enter %s derivative(s) for the %s method you have entered.' %(int(ivp_method[-1]), ivp_method))
                for k, ode_derivative in enumerate(ode_derivatives):
                    try:
                        g = sym.lambdify(['t', 'y'], sym.sympify(ode_derivative), 'numpy')
                        gf = np.append(gf, g)
                    except:
                        raise Exception('An error occurred while creating derivaritive %s: %s.' %(k+1, ode_derivative))
                def df(t, y):
                    return gf
        # multistep / predictor methods
        if ivp_method in valid_ivp_methods[-15:]:
            if ivp_method_temp[1] is None:
                starting_values = 'rk_approximation'
            else:
                if isinstance(ivp_method_temp[1], list) or isinstance(ivp_method_temp[1], tuple):
                    starting_values = ivp_method_temp[1]
                else:
                    raise ValueError('Please enter a list or tuple for starting values (second element in ivp_method list/tuple).')
    else:
        raise ValueError('Please enter a list or tuple of atmost 2 elemets for ivp_method.')
        
    # Start step size or interval options
    
    if 'fehlberg' not in ivp_method and 'verner' not in ivp_method:
        if len(steps_stepsize) == 2:
            if isinstance(steps_stepsize[1], int) or isinstance(steps_stepsize[1], float):
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
            if isinstance(steps_stepsize[0], int) or isinstance(steps_stepsize[0], float):
                hmin = steps_stepsize[0]
            else:
                raise ValueError('Please enter a single integer or float value hmin.')
            
            if isinstance(steps_stepsize[1], int) or isinstance(steps_stepsize[1], float):
                hmax = steps_stepsize[1]
            else:
                raise ValueError('Please enter a single integer or float value hmax.')
            
            if hmin >= hmax:
                raise ValueError('hmax must be greater than hmin.')
            
            if isinstance(steps_stepsize[2], int) or isinstance(steps_stepsize[2], float):
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
      
    # figure properties
    
    # ****************** See plot figure section towards the end **********************
    
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
    if ivp_method in valid_ivp_methods[-15:]:
        if starting_values == 'rk_approximation':
            starting_values = [0] * 5
            try:
                for i in range(5):
                    h = t[i+1] - t[i]
                    k1 = h * f(t[i], y[i])
                    k2 = h * f(t[i] + h/2, y[i] + k1/2)
                    k3 = h * f(t[i] + h/2, y[i] + k2/2)
                    k4 = h * f(t[i] + h, y[i] + k3)
                    starting_values[i+1] = y[i] + 1/6 * (k1 + 2 * k2 + 2 * k3 + k4)
            except:
                raise ValueError('Something went wrong while computing starting values with the fourth order Runge-Kutta scheme. Just ensure that your value for n is greater than the steps for multi-step/predictor methods.')
            
    # =========================================================================
        # Euler methods
    # =========================================================================
    
    if ivp_method == 'explicit euler' or ivp_method == 'forward euler':
      
        for i in range(n):
            h = t[i+1] - t[i]
            y[i+1] = y[i] + h * f(t[i], y[i])
    
    if ivp_method == 'modified euler':
        
        for i in range(n):
            h = t[i+1] - t[i]
            ynew = y[i] + h * f(t[i], y[i])
            y[i+1] = y[i] + (h/2) * (f(t[i], y[i]) + f(t[i+1], ynew))
            
    if ivp_method == 'implicit euler' or ivp_method == 'backward euler':
        for i in range(n):
            h = t[i+1] - t[i]
            fs_symbolic = str(fty).replace('t', '(' + str(t[i+1]) + ')')
            fs_symbolic = fs_symbolic.replace('y', 'y' + str(i))
            fs_symbolic = 'y' + str(i) + ' - (' + str(y[i]) + ' + ' + str(h) + ' * (' + str(fs_symbolic) + '))'
            y[i+1] = sym.solve(fs_symbolic)[0]
    
    # =========================================================================
        # Explicit Runge-Kutta methods
    # =========================================================================

    if ivp_method == 'midpoint':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/2, y[i] + k1/2)
            y[i+1] = y[i] + k2
       
    # -------------------------------------------------------------------------
       
    elif ivp_method == 'modified euler rk':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h, y[i] + k1)
            y[i+1] = y[i] + (1/2) * (k1 + k2)
        
    # -------------------------------------------------------------------------
      
    elif ivp_method == 'second order ralston':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + (3/4) * h, y[i] + (3/4) * k1)
            y[i+1] = y[i] + (1/3) * (k1 + 2 * k2)
        
    # -------------------------------------------------------------------------
      
    elif ivp_method == 'third order heun':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + (1/3) * h, y[i] + (1/3) * k1)
            k3 = h * f(t[i] + (2/3) * h, y[i] + (2/3) * k2)
            y[i+1] = y[i] + (1/4) * (k1 + 3 *  k3)
        
    # -------------------------------------------------------------------------
    
    elif ivp_method == 'third order nystrom':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + 2/3 * h, y[i] + 2/3 * k1)
            k3 = h * f(t[i] + 2/3 * h, y[i] + 2/3 * k2)
            y[i+1] = y[i] + (1/8) * (2 * k1 + 3 * k2 + 3 * k3)
       
    # -------------------------------------------------------------------------
    
    elif ivp_method == 'third order':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/2, y[i] + 1/2 * k1)
            k3 = h * f(t[i] + h, y[i] - k1 + 2 * k2)
            y[i+1] = y[i] + (1/6) * (k1 + 4 * k2 + k3)
   
    # -------------------------------------------------------------------------
    
    elif ivp_method == 'fourth order':
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/2, y[i] + k1/2)
            k3 = h * f(t[i] + h/2, y[i] + k2/2)
            k4 = h * f(t[i] + h, y[i] + k3)
            y[i+1] = y[i] + 1/6 * (k1 + 2 * k2 + 2 * k3 + k4)
       
    # -------------------------------------------------------------------------
    
    elif ivp_method == 'fourth order runge kutta mersen':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/3, y[i] + k1/3)
            k3 = h * f(t[i] + h/2, y[i] + k1/6 + k2/6)
            k4 = h * f(t[i] + h/2, y[i] + k1/8 + 3/8 * k3)
            k5 = h * f(t[i] + h, y[i] + k1/2 - 3/2 * k3 + 2 * k4)
            y[i+1] = y[i] + (1/6) * (k1 + 4 * k2 + k5)
       
    # -------------------------------------------------------------------------
    
    elif ivp_method == 'fourth order runge kutta 3/8':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + 1/3 * h, y[i] + 1/3 * k1)
            k3 = h * f(t[i] + 2/3 * h, y[i] - 1/3 * k1 + k2)
            k4 = h * f(t[i] + h, y[i] + k1 - k2 + k3)
            y[i+1] = y[i] + (1/8) * (k1 + 3 * k2 + 3 * k3 + k4)
        
    # -------------------------------------------------------------------------
    
    elif ivp_method == 'fifth order':
        
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
      
    elif ivp_method == 'runge kutta fehlberg':
        
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
    
    # -------------------------------------------------------------------------
        # Exact solution
    # -------------------------------------------------------------------------

    if exact_solution is not None:
        t_exact = np.linspace(t0, tf, 250)
        y_exact = ft(t_exact)
        y_time_span = ft(t)
        absolute_error = abs(y_time_span - y)
        table_results = np.vstack([t, y_time_span, y, absolute_error]).T
        table_results = table_results[0:N+1, :]    
        table_results = pd.DataFrame(table_results, columns = ['Time (t)','Exact solution(y)', 'Approximated (yi)', 'Error: | y - yi |'])
    else:
        table_results = np.vstack([t, y]).T
        table_results = table_results[0:N+1, :]
        table_results = pd.DataFrame(table_results, columns = ['Time (t)', 'Approximated (yi)'])
    
    tab_results = np.array(table_results.iloc[:N, :])
    
    # -------------------------------------------------------------------------
        # Plot figure
    # -------------------------------------------------------------------------
    
    if show_figure:
        valid_figure_styles = plt.style.available
        figure_property_value = np.zeros((0, 2), dtype = '<U')
        for property_key, property_value in figure_properties.items():
            figure_property_value = np.vstack([figure_property_value, [property_key, property_value]])
        
        if figure_property_value.size != 0:
            figure_property_value = pd.DataFrame(figure_property_value)
            figure_property_value.index = figure_property_value.iloc[:, 0]
            if 'figure_style' in figure_property_value.index:
                figure_style = figure_property_value.loc['figure_style', 1]
                if figure_style not in valid_figure_styles:
                    raise ValueError('%s is an invalid value for figure_style. Valid values include: %s.' %(figure_style, valid_figure_styles))
            else:
                figure_style = 'fast'
            
            if 'figure_width' in figure_property_value.index:
                try:
                    figure_width = int(figure_property_value.loc['figure_width', 1])
                    if figure_width < 3 or figure_width > 15:
                        raise ValueError('Enter a value between 3 and 15 inclusive for figure_width.')
                except:
                    raise ValueError('Something is wrong with the value %s you have entered as figure_width.' %(figure_width))
            else:
                figure_width = 7
             
            if 'figure_height' in figure_property_value.index:
                try:
                    figure_height = int(figure_property_value.loc['figure_height', 1])
                    if figure_height < 3 or figure_height > 15:
                        raise ValueError('Enter a value between 3 and 15 inclusive for figure_height.')
                except:
                    raise ValueError('Something is wrong with the value %s you have entered as figure_height.' %(figure_height))
            else:
                figure_height = 5
            
            if 'figure_marker' in figure_property_value.index:
                valid_marker_symbols = ['.', ',', 'v', 'o', 'v', '<', '>', '2', '3', '4', 's', 'p', 'h', 'H', '+', 'x', 'D', 'd', '_']
                figure_marker = figure_property_value.loc['figure_marker', 1]
                if isinstance(figure_marker, str):
                    figure_marker = figure_property_value.loc['figure_marker', 1]
                    if figure_marker not in valid_marker_symbols:
                        raise ValueError('\'%s\' is an invalid value for figure_marker. Valid values include: %s. Run the command plt.plot? to see help on Matplotlib plotting arguments.' %(figure_marker, valid_marker_symbols))
                else:
                    raise ValueError('Please enter a string value for figure_marker.')
            else:
                figure_marker = 'D'
              
            if 'figure_markerfacecolor' in figure_property_value.index:
                valid_linestyles = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'] + ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white']
                figure_markerfacecolor = figure_property_value.loc['figure_markerfacecolor', 1]
                if isinstance(figure_markerfacecolor, str):
                    figure_markerfacecolor = figure_property_value.loc['figure_markerfacecolor', 1]
                    if figure_markerfacecolor not in valid_marker_symbols:
                        raise ValueError('\'%s\' is an invalid value for figure_markerfacecolor. Valid values include: %s. Run the command plt.plot? to see help on Matplotlib plotting arguments.' %(figure_markerfacecolor, valid_linestyles))
                else:
                    raise ValueError('Please enter a string value for figure_markerfacecolor.')
            else:
                figure_markerfacecolor = 'b'
             
            if 'figure_markersize' in figure_property_value.index:
                try:
                    figure_markersize = int(figure_property_value.loc['figure_markersize', 1])
                    if figure_markersize < 3 or figure_markersize > 50:
                        raise ValueError('Enter a value between 3 and 50 inclusive for figure_markersize.')
                except:
                    raise ValueError('Something is wrong with the value %s you have entered as figure_width.' %(figure_markersize))
            else:
                figure_markersize = 8
              
            if 'figure_linestyle' in figure_property_value.index:
                valid_linestyles = ['-', '--', '-.', ':']
                figure_linestyle = figure_property_value.loc['figure_linestyle', 1]
                if isinstance(figure_linestyle, str):
                    figure_linestyle = figure_property_value.loc['figure_linestyle', 1]
                    if figure_linestyle not in valid_linestyles:
                        raise ValueError('\'%s\' is an invalid value for figure_linestyle. Valid values include: %s. Run the command plt.plot? to see help on Matplotlib plotting arguments.' %(figure_linestyle, valid_linestyles))
                else:
                    raise ValueError('Please enter a string value for figure_linestyle.')
            else:
                figure_linestyle = '-'
              
            if 'figure_color' in figure_property_value.index:
                valid_linestyles = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'] + ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white']
                figure_color = figure_property_value.loc['figure_color', 1]
                if isinstance(figure_color, str):
                    figure_color = figure_property_value.loc['figure_color', 1]
                    if figure_color not in valid_marker_symbols:
                        raise ValueError('\'%s\' is an invalid value for figure_color. Valid values include: %s. Run the command plt.plot? to see help on Matplotlib plotting arguments.' %(figure_color, valid_linestyles))
                else:
                    raise ValueError('Please enter a string value for figure_color.')
            else:
                figure_color = 'b'
             
            if 'figure_linewidth' in figure_property_value.index:
                try:
                    figure_linewidth = int(figure_property_value.loc['figure_linewidth', 1])
                    if figure_linewidth < 0 or figure_linewidth > 10:
                        raise ValueError('Enter a value between 1 and 10 inclusive for figure_linewidth.')
                except:
                    raise ValueError('Something is wrong with the value %s you have entered as figure_width.' %(figure_linewidth))
            else:
                figure_linewidth = 2
                
            if 'figure_title' in figure_property_value.index:
                figure_title = figure_property_value.loc['figure_title', 1]
                if isinstance(figure_title, str):
                    figure_title = figure_property_value.loc['figure_title', 1]
                else:
                    raise ValueError('Please enter a string value for figure_tittle.')
            else:
                figure_title = r'$ f(t, y) = ' + f_latex + '$'
             
            if 'figure_xtitle' in figure_property_value.index:
                figure_xtitle = figure_property_value.loc['figure_xtitle', 1]
                if isinstance(figure_xtitle, str):
                    figure_xtitle = figure_property_value.loc['figure_xtitle', 1]
                else:
                    raise ValueError('Please enter a string value for figure_xtitle.')
            else:
                figure_xtitle = 'Time (t)'
             
            if 'figure_ytitle' in figure_property_value.index:
                figure_ytitle = figure_property_value.loc['figure_ytitle', 1]
                if isinstance(figure_ytitle, str):
                    figure_ytitle = figure_property_value.loc['figure_ytitle', 1]
                else:
                    raise ValueError('Please enter a string value for figure_ytitle.')
            else:
                figure_ytitle = 'Approximate values (y)'
             
            if 'figure_fontcolor' in figure_property_value.index:
                figure_fontcolors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'] + ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white']
                figure_fontcolor = figure_property_value.loc['figure_fontcolor', 1]
                if isinstance(figure_fontcolor, str):
                    figure_fontcolor = figure_property_value.loc['figure_fontcolor', 1]
                    if figure_fontcolor not in valid_marker_symbols:
                        raise ValueError('\'%s\' is an invalid value for figure_fontcolor. Valid values include: %s. Run the command plt.plot? to see help on Matplotlib plotting arguments.' %(figure_fontcolor, figure_fontcolors))
                else:
                    raise ValueError('Please enter a string value for figure_fontcolor.')
            else:
                figure_fontcolor = 'k'
              
            if 'figure_fontsize' in figure_property_value.index:
                try:
                    figure_fontsize = int(figure_property_value.loc['figure_fontsize', 1])
                    if figure_fontsize < 3 or figure_fontsize > 15:
                        raise ValueError('Enter a value between 6 and 25 inclusive for figure_width.')
                except:
                    raise ValueError('Something is wrong with the value %s you have entered as figure_fontsize.' %(figure_fontsize))
            else:
                figure_fontsize = 13
               
        else:
            figure_properties = ['fast', 7, 5, 'D', 'b', 8, '--', 'b', 2, r'$ f(t, y) = ' + f_latex + '$', 'Time (t)', 'Approximate values (y)','k', 13]
            figure_style, figure_width, figure_height, figure_marker, figure_markerfacecolor, figure_markersize, figure_linestyle, figure_color, figure_linewidth, figure_title, figure_xtitle, figure_ytitle, figure_fontcolor, figure_fontsize = figure_properties
        
        with plt.style.context(figure_style):
            plt.figure(figsize = (figure_width, figure_height))
            if exact_solution is not None:
                plt.plot(t_exact, y_exact, 'r')
            
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
            date_time = datetime.now().strftime('%Y%m%d%H%M%S')
            plt.savefig('ivps_figure' + date_time + '.png', dpi = 150) # comes before plot.show()
        
        plt.show()
    
    # -------------------------------------------------------------------------
        # return_results
    # -------------------------------------------------------------------------

    return table_results