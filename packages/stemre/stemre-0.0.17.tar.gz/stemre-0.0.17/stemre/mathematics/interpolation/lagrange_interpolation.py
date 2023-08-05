
from io import BytesIO
import base64

import math as mt
import numpy as np
import stemre as stm
import sympy as sym
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def newton_differences(x, y, x0, poly_variable = 'x', difference_method = 'divided', plot_x0 = False, differentiatiation_order = 0, plot_derivative = False, decimal_points = 12):
    
    x_values = x
    y_values = y
    
    n = len(x)
    
    N = np.zeros((n,n+1))

    N[N == 0] = np.nan
    
    N[:,0] = x_values
    
    N[:,1] = y_values
    
    if difference_method == "forward":
        col_names = ['\( x \)', '\( y \)'] + ['\( \\Delta^{%s}f \)' %(k+1) for k in range(N.shape[1]-2)]
        col_names[2] = '\( \\Delta \, f\)'
        ff = str(N[0,1])
        fp = ff
        fi = ' * p'
        x = x_values 
        P = (x0 - x[0]) / (x[1] - x[0])
        for j in range(1,n):
            for k in range(j,n):
                N[k,j+1] = N[k,j] - N[k-1,j]
            if (j == 1):
                fi = fi
            else:
                fi = fi + ' * (p - ' + str(j-1) + ')'
            
            fp = fp + ' + ' + str(N[j,j+1]) + fi + '/' + str(mt.factorial(j))
          
        ff = sym.sympify(fp.replace('p', '((x - ' + str(x[0]) + ') / (' + str(x[1] - x[0]) + '))'))
        
    elif difference_method == "backward":
        col_names = ['\( x \)', '\( y \)'] + ['\( \\nabla^{\,%s}f \)' %(k+1) for k in range(N.shape[1]-2)]
        col_names[2] = '\( \\nabla \, f \)'
        ff = str(N[n-1, 1])
        fp = ff
        fi = ' * p'
        P = (x0 - x[n-1]) / (x[1] - x[0])
        for j in range(1,n):
            for k in range(j,n):
                N[k,j+1] = N[k,j] - N[k-1,j]
            if (j == 1):
                fi = fi
            else:
                fi = fi + ' * (p + ' + str(j-1) + ')'
               
            fp = fp + ' + ' + str(N[n-1,j+1]) + '' + fi + '/' + str(mt.factorial(j))
             
        ff = sym.sympify(fp.replace('p', '((x - ' + str(x[n-1]) + ') / (' + str(x[1] - x[0]) + '))'))
        
    elif difference_method == "divided":
        col_names = ['\( x \)', '\( y \)'] + ['\( N_{i, \, %s} \)' %(k+1) for k in range(N.shape[1]-2)]
        ff = str(N[0,1])
        fi = ''
        x = x_values
        for j in range(1,n):
            for k in range(j,n):
                N[k,j+1] = (N[k,j] - N[k-1,j]) / (x[k] - x[k-j])
            fi = fi + ' * (x - ' + str(x[j-1]) + ')'
            ff = ff + ' + ' + str(N[j,j+1]) + '' + fi
    else:
        raise Exception('%s is an invalid difference method.', difference_method)
        
    x = sym.symbols('x')
    
    ff = stm.remove_zeros(ff, truncate_value = 1e-6)
        
    px = sym.sympify(ff)
    fx = px
    px = px.subs(x, x0)
    
    # -------------------------------------------------------------------------
        # Display table
    # -------------------------------------------------------------------------
    
    pd.set_option('display.precision', decimal_points)
    df = stm.insert_na_array(N)
    dfN = np.round(df, decimal_points)
    results_table = np.array(dfN, dtype = np.float64)
    row_names = stm.insert_na_list(list(range(N.shape[0])))
    row_names = [str(item).replace('nan', '') for k, item in enumerate(row_names)]
    results_table = pd.DataFrame(dfN, index = row_names, columns = col_names)
    results_table = results_table.fillna('')
    
    fx_eqtn = fx.evalf(decimal_points).expand().subs(x, poly_variable)
    fx_eqtn_value = px.evalf(decimal_points)
    
    if differentiatiation_order != 0:
        dfdx = ff.diff(x, differentiatiation_order)
        dfx0 = dfdx.subs(x, x0)
        dfx_eqtn = dfdx.evalf(decimal_points).expand().subs(x, poly_variable)
        dfx_eqtn_value = dfx0.evalf(decimal_points)
    
    # -------------------------------------------------------------------------
        # Plot figure
    # -------------------------------------------------------------------------
    
    x = sym.symbols('x')
    f = sym.lambdify(x, fx, 'numpy')
    xv = np.linspace(float(min(x_values)), float(max(x_values)), 101)
    fx = f(xv)
    
    plt.clf() # clear before plotting
    
    plt.scatter(x_values, y_values, color = 'blue', marker = 'D')
    
    plt.plot(xv, fx, color = 'blue', label = 'Function, f(' + str(poly_variable) + ')')
    
    if plot_derivative and sym.degree(dfdx) > 0:
        g = sym.lambdify(x, dfdx, 'numpy')
        xv = np.linspace(float(min(x_values)), float(max(x_values)), 101)
        gx = g(xv)
    
        plt.plot(xv, gx, color = 'orange', linestyle = 'dashed', label = 'Derivative, g(' + str(poly_variable) + ')')
        
        plt.legend(loc = 'best')
    
    if plot_x0 and x0 < x_values[n-1] and x0 > x_values[0]:
        plt.plot(x0, px, color = 'red', marker = '*', markersize = 12)
        plt.text(x0, px, '  (' + str(np.round(float(x0), decimal_points)) +  ', ' + str(np.round(float(px), decimal_points)) + ')', fontsize = 12, bbox = dict(facecolor = 'gray', alpha = 0.075), horizontalalignment = 'left')
    
    plt.xlabel(poly_variable)
    plt.ylabel('y')
    plt.title('Newton ' + difference_method.lower() + ' method')
    plt.tight_layout()
    
    figure_file = BytesIO()
    plt.savefig(figure_file, format = 'png')
    figure_file.seek(0)
    plotted_figure = base64.b64encode(figure_file.getvalue()).decode('ascii')
    
    html_code = 'data:image/png;base64,' + plotted_figure
    
    if differentiatiation_order == 0:
        return results_table, fx_eqtn, fx_eqtn_value, html_code
    else:
        return results_table, fx_eqtn, fx_eqtn_value, dfx_eqtn, dfx_eqtn_value, html_code