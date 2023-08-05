import numpy as np
import sympy as sym
from sympy.parsing.sympy_parser import parse_expr
import pandas as pd

def pm_sign(expr):
    sign_string = '+'
    if (np.sign(expr) == -1):
        sign_string = '-'
    return sign_string

def array_to_latex(M, align = 'right', brackets = '['):
    
    try:
        if isinstance(M, (list, tuple)):
            M = sym.Matrix(M)
        else:
            M = sym.Matrix([M])
    except:
        raise TypeError('An error was encountered.')
    
    array_m_latex = sym.latex(M, mat_delim = brackets).replace("begin{matrix}", "begin{array}{'%s'}" %(align[0] * M.shape[1])).replace("end{matrix}", "end{array}")
    if '{cc' in array_m_latex: # large matrices
        array_m_latex = array_m_latex.replace('c' * M.shape[1], 'r' * M.shape[1], M.shape[1]) # replaces the first M.shape[1] occurances of 'c' with 'r'
    return array_m_latex

def string_to_equation(expression, evaluate = True):
    
    expression = expression.replace('^', '**').replace('lambda', 'lamda')
    
    equation = parse_expr(expression, evaluate = evaluate)
    
    return equation

def string_to_list(string, evaluate = True, data_type = float):
    
    string = string.replace('^', '**')
    _list = parse_expr(string, evaluate = evaluate)
    
    if not isinstance(_list, list):
        if isinstance(_list, tuple):
            _list = list(_list)
        else:
            _list = [data_type(str(_list))]
    
    return _list
 
def string_to_tuple(string, evaluate = True, data_type = float):
    
    string = string.replace('^', '**')
    _tuple = parse_expr(string, evaluate = evaluate)
    
    if not isinstance(_tuple, tuple):
        if isinstance(_tuple, list):
            _tuple = tuple(_tuple)
        else:
            _tuple = [data_type(str(_tuple))]
    
    return _tuple
     
def convert_list_data_type(_list, data_type = float):
    
    if any(isinstance(item, list) for item in _list): # nested list
        nested_list = True
        converted_list = [list(map(data_type, item)) for item in _list]
    else: # 1d list
        converted_list = [data_type(item) for _, item in enumerate(_list)]
    
    return converted_list
 
def nested_list(_list):
    
    nested_list = False
    if any(isinstance(item, list) for item in _list):
        nested_list = True
        
    return nested_list
                                                     
def flatten_list(_list):
    
    if any(isinstance(item, list) for item in _list):
        flattened_list = [item for element in _list for item in element]
    else:
        flattened_list = _list
    
    return flattened_list

def disp(**display_results):
    for key, value in display_results.items():
        if isinstance(value, list) or isinstance(value, tuple):
            display(sym.sympify(key), sym.Matrix(value))
        else:
            display(sym.sympify(key), value)