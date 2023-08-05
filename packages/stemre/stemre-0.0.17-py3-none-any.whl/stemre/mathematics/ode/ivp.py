from datetime import datetime
import numpy as np
import math as mt
import sympy as sym
import pandas as pd
import matplotlib.pyplot as plt

def ivp(F, t, y, n, h, method):
    
    # =========================================================================
        # Taylor methods
    # =========================================================================
    f = F
    ivp_method = method
    
    if ivp_method[:6] == 'taylor':
        if isinstance(int(ivp_method[-1]), int) is True:
            taylor_order = int(ivp_method[-1])
            if taylor_order == 0:
                raise ValueError('A value of 0 for the taylor order (%s) is not allowed.' %(ivp_method))
        else:
            raise ValueError('The last digit of taylor method must be an integer between 1 and 9 representing the taylor order.')
        # taylor_terms = 'h * D[0] + ' + ' + '.join(['h ** ' + str(k) + ' * D[' + str(k-1) + '] / mt.factorial('+ str(k) +')' for k in range(2, taylor_order+1)])  
        for i in range(n):
            h = t[i+1] - t[i]
            D = df(t[i], y[i])
            if taylor_order == 1:
                y[i+1] = y[i] + h * D[0]
            elif taylor_order == 2:
                y[i+1] = y[i] + h * D[0] + h ** 2 * D[1] / mt.factorial(2)
            elif taylor_order == 3:
                y[i+1] = y[i] + h * D[0] + h ** 2 * D[1] / mt.factorial(2) + h ** 3 * D[2] / mt.factorial(3)
            elif taylor_order == 4:
                y[i+1] = y[i] + h * D[0] + h ** 2 * D[1] / mt.factorial(2) + h ** 3 * D[2] / mt.factorial(3) + h ** 4 * D[3] / mt.factorial(4)
            elif taylor_order == 5:
                y[i+1] = y[i] + h * D[0] + h ** 2 * D[1] / mt.factorial(2) + h ** 3 * D[2] / mt.factorial(3) + h ** 4 * D[3] / mt.factorial(4) + h ** 5 * D[4] / mt.factorial(5)
            elif taylor_order == 6:
                y[i+1] = y[i] + h * D[0] + h ** 2 * D[1] / mt.factorial(2) + h ** 3 * D[2] / mt.factorial(3) + h ** 4 * D[3] / mt.factorial(4) + h ** 5 * D[4] / mt.factorial(5) + h ** 6 * D[5] / mt.factorial(6)
            elif taylor_order == 7:
                y[i+1] = y[i] + h * D[0] + h ** 2 * D[1] / mt.factorial(2) + h ** 3 * D[2] / mt.factorial(3) + h ** 4 * D[3] / mt.factorial(4) + h ** 5 * D[4] / mt.factorial(5) + h ** 6 * D[5] / mt.factorial(6) + h ** 7 * D[6] / mt.factorial(7)
            elif taylor_order == 8:
                y[i+1] = y[i] + h * D[0] + h ** 2 * D[1] / mt.factorial(2) + h ** 3 * D[2] / mt.factorial(3) + h ** 4 * D[3] / mt.factorial(4) + h ** 5 * D[4] / mt.factorial(5) + h ** 6 * D[5] / mt.factorial(6) + h ** 7 * D[6] / mt.factorial(7) + h ** 8 * D[7] / mt.factorial(8)
            elif taylor_order == 9:
                y[i+1] = y[i] + h * D[0] + h ** 2 * D[1] / mt.factorial(2) + h ** 3 * D[2] / mt.factorial(3) + h ** 4 * D[3] / mt.factorial(4) + h ** 5 * D[4] / mt.factorial(5) + h ** 6 * D[5] / mt.factorial(6) + h ** 7 * D[6] / mt.factorial(7) + h ** 8 * D[7] / mt.factorial(8) + h ** 9 * D[8] / mt.factorial(9)
                
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
            fs_symbolic = fty.replace('t', '(' + str(t[i+1]) + ')')
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
    
    elif ivp_method == 'fourth order runge kutta':
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
        # Implicit Runge-Kutta methods
    # =========================================================================
        
    # -------------------------------------------------------------------------
        # Backward euler
    # -------------------------------------------------------------------------
    
    elif ivp_method == 'backward euler':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/4, y[i] + (1/4) * k1)
            k3 = h * f(t[i] + h/4, y[i] + (1/8) * k1 + (1/8) * k2)
            k4 = h * f(t[i] + h/2, y[i] - (1/2) * k2 + k3)
            k5 = h * f(t[i] + (3 * h)/4, y[i] + (3/16) * k1 + (9/16) * k4)
            k6 = h * f(t[i] + h, y[i] - (3/7) * k1 + (2/7) * k2 + (12/7) * k3 - (12/7) * k4 + (8/7) * k5)
            y[i+1] = y[i] + (1/90) * (7 * k1 + 32 * k3 + 12 * k4 + 32 * k5 + 7 * k6)
        
    # -------------------------------------------------------------------------
        # Trapezoidal
    # -------------------------------------------------------------------------
    
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
        
    # -------------------------------------------------------------------------
        # Two stage gauss legendre
    # -------------------------------------------------------------------------
    
    elif ivp_method == 'two stage gauss legendre':
        
        for i in range(n):
            h = t[i+1] - t[i]
            k1 = h * f(t[i], y[i])
            k2 = h * f(t[i] + h/4, y[i] + (1/4) * k1)
            k3 = h * f(t[i] + h/4, y[i] + (1/8) * k1 + (1/8) * k2)
            k4 = h * f(t[i] + h/2, y[i] - (1/2) * k2 + k3)
            k5 = h * f(t[i] + (3 * h)/4, y[i] + (3/16) * k1 + (9/16) * k4)
            k6 = h * f(t[i] + h, y[i] - (3/7) * k1 + (2/7) * k2 + (12/7) * k3 - (12/7) * k4 + (8/7) * k5)
            y[i+1] = y[i] + (1/90) * (7 * k1 + 32 * k3 + 12 * k4 + 32 * k5 + 7 * k6)
      
    elif ivp_method == 'three stage gauss legendre':
        
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
      
    elif ivp_method == 'runge kutta felhberg':
        
        y = tolerance, approximate
     
    elif ivp_method == 'runge kutta verner':
        
        y = tolerance, approximate
    
    # =========================================================================
        # Variable stepsize methods
    # =========================================================================
      
    elif ivp_method == 'variable':
        
        y = tolerance, approximate
     
    elif ivp_method == 'variable':
        
        y = tolerance, approximate
     
    # =========================================================================
        # Multistep methods
    # =========================================================================
               
    # -------------------------------------------------------------------------
        # Explicit Adams-Bashforth methods
    # -------------------------------------------------------------------------
    
    elif ivp_method == 'adam bashforth 2 step':
        
        for i in range(1, n):
            h = t[i+1] - t[i]
            y[i+1] = y[i] + (h/2) * (3 * f(t[i], y[i]) - f(t[i-1], y[i-1]))
    
    elif ivp_method == 'adam bashforth 3 step':
        
        for i in range(2, n):
            h = t[i+1] - t[i]
            y[i+1] = y[i] + (h/12) * (23 * f(t[i], y[i]) - 16 * f(t[i-1], y[i-1]) + 5 * f(t[i-2], y[i-2]))
    
    elif ivp_method == 'adam bashforth 4 step':
        
        for i in range(3, n):
            h = t[i+1] - t[i]
            y[i+1] = y[i] + (h/24) * (55 * f(t[i], y[i]) - 59 * f(t[i-1], y[i-1]) + 37 * f(t[i-2], y[i-2]) - 9 * f(t[i-3], y[i-3]))
    
    elif ivp_method == 'adam bashforth 5 step':
        
        for i in range(4, n):
            h = t[i+1] - t[i]
            y[i+1] = y[i] + (h/720) * (1901 * f(t[i], y[i]) - 2774 * f(t[i-1], y[i-1]) + 2616 * f(t[i-2], y[i-2]) - 1274 * f(t[i-3], y[i-3]) + 251 * f(t[i-4], y[i-4]))
             
    # -------------------------------------------------------------------------
        # Implicit Adams-moulton methods
    # -------------------------------------------------------------------------
    
    elif ivp_method == 'adam moulton 2 step':
        
        for i in range(1, n):
            h = t[i+1] - t[i]
            fty_symbolic = fty.replace('t', '(' + str(t[i+1]) + ')')
            fty_symbolic = fty_symbolic.replace('y', 'y' + str(i))
            fty_symbolic = 'y' + str(i) + ' - (' + str(y[i]) + ' + ' + str(h/12) + ' * (5 * (' + str(fty_symbolic) + ') + ' + str(8 * f(t[i], y[i]) - f(t[i-1], y[i-1])) + '))'
            y[i+1] = sym.solve(fty_symbolic)[0]
    
    elif ivp_method == 'adam moulton 3 step':
        
        for i in range(2, n):
            h = t[i+1] - t[i]
            fty_symbolic = fty.replace('t', '(' + str(t[i+1]) + ')')
            fty_symbolic = fty_symbolic.replace('y', 'y' + str(i))
            fty_symbolic = 'y' + str(i) + ' - (' + str(y[i]) + ' + ' + str(h/24) + ' * (9 * (' + str(fty_symbolic) + ') + ' + str(19 * f(t[i], y[i]) - 5 * f(t[i-1], y[i-1]) + f(t[i-2], y[i-2])) + '))'
            y[i+1] = sym.solve(fty_symbolic)[0]
    
    elif ivp_method == 'adam moulton 4 step':
        
        for i in range(3, n):
            h = t[i+1] - t[i]
            fty_symbolic = fty.replace('t', '(' + str(t[i+1]) + ')')
            fty_symbolic = fty_symbolic.replace('y', 'y' + str(i))
            fty_symbolic = 'y' + str(i) + ' - (' + str(y[i]) + ' + ' + str(h/720) + ' * (251 * (' + str(fty_symbolic) + ') + ' + str(646 * f(t[i], y[i]) - 264 * f(t[i-1], y[i-1]) + 106 * f(t[i-2], y[i-2]) - 19 * f(t[i-3], y[i-3])) + '))'
            y[i+1] = sym.solve(fty_symbolic)[0]
    
    # =========================================================================
        # Predictor-corrector methods
    # =========================================================================
      
    elif ivp_method == 'adam bashforth moulton 2 step':
        
        for i in range(1, n):
            h = t[i+1] - t[i]
            # Adams-Bashforth 2-step as predictor
            y[i+1] = y[i] + (h/2) * (3 * f(t[i], y[i]) - f(t[i-1], y[i-1]))
            # Adams-Moulton 2-step as corrector
            y[i+1] = y[i] + (h/2) * (f(t[i+1], y[i+1]) + f(t[i], y[i]))
    
    elif ivp_method == 'adam bashforth moulton 3 step':
        
        for i in range(2, n):
            h = t[i+1] - t[i]
            # Adams-Bashforth 3-step as predictor
            y[i+1] = y[i] + (h/12) * (23 * f(t[i], y[i]) - 16 * f(t[i-1], y[i-1]) + 5 * f(t[i-2], y[i-2]))
            # Adams-Moulton 2-step as corrector
            y[i+1] = y[i] + (h/12) * (5 * f(t[i+1], y[i+1]) + 8 * f(t[i], y[i]) - f(t[i-1], y[i-1]))
    
    elif ivp_method == 'adam bashforth moulton 4 step':
        
        for i in range(3, n):
            h = t[i+1] - t[i]
            # Adams-Bashforth 4-step as predictor
            y[i+1] = y[i] + (h/24) * (55 * f(t[i], y[i]) - 59 * f(t[i-1], y[i-1]) + 37 * f(t[i-2], y[i-2]) - 9 * f(t[i-3], y[i-3]))
            # Adams-Moulton 3-step as corrector
            y[i+1] = y[i] + (h/24) * (9 * f(t[i+1], y[i+1]) + 19 * f(t[i], y[i]) - 5 * f(t[i-1], y[i-1]) + f(t[i-2], y[i-2]))
    
    elif ivp_method == 'adam bashforth moulton 5 step':
        
        for i in range(4, n):
            h = t[i+1] - t[i]
            # Adams-Bashforth 5-step as predictor
            y[i+1] = y[i] + (h/720) * (1901 * f(t[i], y[i]) - 2774 * f(t[i-1], y[i-1]) + 2616 * f(t[i-2], y[i-2]) - 1274 * f(t[i-3], y[i-3]) + 251 * f(t[i-4], y[i-4]))
            # Adams-Moulton 4-step as corrector
            y[i+1] = y[i] + (h/720) * (251 * f(t[i+1], y[i+1]) + 646 * f(t[i], y[i]) - 264 * f(t[i-1], y[i-1]) + 106 * f(t[i-2], y[i-2]) - 19 * f(t[i-3], y[i-3]))
       
    elif ivp_method == 'euler heun':
        
        for i in range(n):
            h = t[i+1] - t[i]
            # Explicit Euler as predictor
            y[i+1] = y[i] + h * f(t[i], y[i])
            # Heun as corrector
            y[i+1] = y[i] + (h/2) * (f(t[i+1], y[i+1]) + f(t[i], y[i]))
       
    elif ivp_method == 'milne simpson':
        
        for i in range(3, n):
            h = t[i+1] - t[i]
            # Milne as predictor
            y[i+1] = y[i-3] + (4 * h/3) * (2 * f(t[i], y[i]) - f(t[i-1], y[i-1]) + 2 * f(t[i-2], y[i-2]))
            # Simpson as corrector
            y[i+1] = y[i-1] + (h/3) * (f(t[i+1], y[i+1]) + 4 * f(t[i], y[i]) + f(t[i-1], y[i-1]))
       
    elif ivp_method == 'modified milne simpson':
        
        for i in range(3, n):
            h = t[i+1] - t[i]
            # Milne as predictor
            y[i+1] = y[i-3] + (4 * h/3) * (2 * f(t[i], y[i]) - f(t[i-1], y[i-1]) + 2 * f(t[i-2], y[i-2]))
            # Modifier
            y[i+1] = y[i+1] + (28/29) * (y[i] - y[i-1])
            # Simpson as corrector
            y[i+1] = y[i-1] + (h/3) * (f(t[i+1], y[i+1]) + 4 * f(t[i], y[i]) + f(t[i-1], y[i-1]))
       
    elif ivp_method == 'hammings':
        
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
        
        y = 4
     
    return y