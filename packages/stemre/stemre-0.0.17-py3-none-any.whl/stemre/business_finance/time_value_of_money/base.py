import numpy as np
import pandas as pd

def pv(years, interest, future_value):
    
    present_value = future_value / (1 + interest/100) ** years
    
    return present_value