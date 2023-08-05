import numpy as np
import stemre as stm
import pandas as pd
import scipy.stats.mstats as ssm
import scipy.stats as sst

def mode(data):
    '''
    >> data_array = np.array([41, 62, 34, 74, 53, 41, 83, 28, 62, 56, 75, 41])
    >> mode(data_array)
    '''
    if isinstance(data, (list, tuple)):
        data_array = np.array(data)
    elif isinstance(data, np.ndarray):
        data_array = data
    else:
        raise TypeError('Data type can only be list, tuple or ndarray.')
        
    try:
        mode_frequency = ssm.mode(data_array)
        if mode_frequency[1][0] == 1:
            result = np.nan
        else:
            mode_value = np.round(mode_frequency[0][0], 16)
            frequency = int(mode_frequency[1][0])
            result = mode_value, frequency
    except:
        raise NotImplementedError('Evaluation of the mode failed.')
        
    return result

def location(data_array, location_measure = 'mean', decimal_points = 8):
    '''
    >> import sympy as sym
    >> sym.init_printing()
    >> data_array = np.array([41, 62, 34, 74, 53, 41, 83, 28, 62, 56, 75, 41])
    >> measures = ['sum', 'mean', 'gmean', 'hmean', 'median', 'mode']
    >> for k, item in enumerate(measures):
        result = stm.location(data_array, location_measure = item)
        display(sym.sympify(measures[k] + '_'), result)
    '''

    location_measure = location_measure.lower()
    data_array = np.array(data_array, dtype = np.float64)
    
    if location_measure == 'sum':
        result = np.round(np.sum(data_array), decimal_points)
    elif location_measure == 'mean':
        result = np.round(np.mean(data_array), decimal_points)
    elif location_measure == 'gmean':
        result = np.round(ssm.gmean(data_array), decimal_points)
    elif location_measure == 'hmean':
        result = np.round(ssm.hmean(data_array), decimal_points)
    elif location_measure == 'median':
        result = np.round(np.median(data_array), decimal_points)
    elif location_measure == 'mode':
        result = np.round(mode(data_array), decimal_points)
        row_names = ['Mode', 'Frequency']
        result = pd.DataFrame(result, index = row_names, columns = ['Value'])
    elif location_measure == 'all':
        result = np.sum(data_array), np.mean(data_array), ssm.gmean(data_array), ssm.hmean(data_array), np.median(data_array), stm.mode(data_array)
        result = [np.round(item, decimal_points) for _, item in enumerate(result)]
        row_names = ['Sum', 'Mean', 'Geometric mean', 'Harmonic mean', 'Median', 'Mode']
        result = pd.DataFrame(result, index = row_names, columns = ['Value'])
    else:
        raise Exception("'%s' is an invalid value for 'location_measure'." %(location_measure))
    
    return result
    
def dispersion(data_array, dispersion_measure = 'ssd', percentile = 50, decimal_points = 8):
    '''
    >> import sympy as sym
    >> sym.init_printing()
    >> data_array = np.array([41, 62, 34, 74, 53, 41, 83, 28, 62, 56, 75, 41])
    >> measures = ['minimum', 'maximum', 'range', 'svariance', 'pvariance', 'ssd', 'psd', 'cv', 'sem', 'percentile', 'quartiles', 'iqr', 'iqd', 'all']
    >> for k, item in enumerate(measures):
        result = stm.dispersion(data_array, dispersion_measure = item)
        display(sym.sympify(measures[k] + '_'), result)
    '''
    
    pd.set_option('display.precision', decimal_points)
    
    dispersion_measure = dispersion_measure.lower()
    data_array = np.array(data_array, dtype = np.float64)
    
    if isinstance(percentile, (float, int)):
        percentile_value = [percentile]
    elif isinstance(percentile, np.ndarray):
        percentile_value = percentile.flatten()
    elif isinstance(percentile, (list, tuple)):
        percentile_value = percentile
    else:
        raise TypeError("'%s' is an invalid data type. Can only be list, tuple, ndarray, interger or float.")
        
    if dispersion_measure == 'minimum':
        result = np.round(np.min(data_array), decimal_points)
    elif dispersion_measure == 'maximum':
        result = np.round(np.max(data_array), decimal_points)
    elif dispersion_measure == 'range':
        result = np.round(np.max(data_array) - np.min(data_array), decimal_points)
    elif dispersion_measure == 'svariance':
        result = np.round(np.var(data_array, ddof = 1), decimal_points)
    elif dispersion_measure == 'pvariance':
        result = np.round(np.var(data_array, ddof = 0), decimal_points)
    elif dispersion_measure == 'ssd':
        result = np.round(np.std(data_array, ddof = 1), decimal_points)
    elif dispersion_measure == 'psd':
        result = np.round(np.std(data_array, ddof = 0), decimal_points)
    elif dispersion_measure == 'cv':
        result = np.round(ssm.variation(data_array), decimal_points)
    elif dispersion_measure == 'sem':
        result = np.round(ssm.sem(data_array), decimal_points)
    elif dispersion_measure == 'percentile':
        result = np.round(np.percentile(data_array, percentile_value), decimal_points)
        N = np.round(np.array(result, dtype = np.float64), decimal_points)
        row_names = [str(item) + '%' for _, item in enumerate(percentile_value)]
        result = pd.DataFrame(N, index = row_names, columns = ['Percentile value'])
    elif dispersion_measure == 'quartiles':
        result = np.round(np.percentile(data_array, [25, 75]), decimal_points)
        N = np.round(np.array(result, dtype = np.float64), decimal_points)
        row_names = ['Lower Quartile: \(Q_{1}\)', 'Upper Quartile: \(Q_{3}\)']
        result = pd.DataFrame(N, index = row_names, columns = ['Quartile value'])
    elif dispersion_measure == 'iqr':
        result = np.round(np.percentile(data_array, 75) - np.percentile(data_array, 25), decimal_points)
    elif dispersion_measure == 'iqd':
        result = np.round((np.percentile(data_array, 75) - np.percentile(data_array, 25)) / 2, decimal_points)
    elif dispersion_measure == 'all':
        percentile_ = [float(item) for _, item in enumerate(stm.flatten_list(stm.string_to_list(str(list(np.percentile(data_array, percentile_value))))))]
        result = np.min(data_array), np.max(data_array), np.max(data_array) - np.min(data_array), np.var(data_array, ddof = 1), np.var(data_array, ddof = 0), np.std(data_array, ddof = 1), np.std(data_array, ddof = 0), ssm.variation(data_array), ssm.sem(data_array), percentile_, np.percentile(data_array, [25, 75])[0], np.percentile(data_array, [25, 75])[1], np.percentile(data_array, 75) - np.percentile(data_array, 25), (np.percentile(data_array, 75) - np.percentile(data_array, 25)) / 2
        result = [np.round(item, decimal_points) for _, item in enumerate(result)]
        percentile_table = ', '.join([str(item) + '%' for _, item in enumerate(percentile_value)])
        row_names = ['Minimum', 'Maximum', 'Range', 'Sample variance', 'Population variance', 'Sample std. deviation', 'Population std. deviation', 'Coefficient of variation', 'Standard error of mean', 'Percentile(s): %s' %(percentile_table), 'Lower quartile: \(Q_{1}\)', 'Upper quartile: \(Q_{3}\)', 'Interquartile range', 'Interquartile deviation']
        result = pd.DataFrame(result, index = row_names, columns = ['Value'])
    else:
        raise Exception("'%s' is an invalid value for 'dispersion_measure'." %(dispersion_measure))
    
    return result
   
def distribution(data_array, distribution_measure = 'skewness', decimal_points = 8):
    '''
    >> import sympy as sym
    >> sym.init_printing()
    >> data_array = np.array([41, 62, 34, 74, 53, 41, 83, 28, 62, 56, 75, 41])
    >> measures = ['skewness', 'kurtosis', 'all']
    >> for k, item in enumerate(measures):
        result = stm.distribution(data_array, distribution_measure = item)
        display(sym.sympify(measures[k] + '_'), result)
    '''

    distribution_measure = distribution_measure.lower()
    data_array = np.array(data_array, dtype = np.float64)
    
    if distribution_measure == 'skewness' or distribution_measure == 'skew':
        result = np.round(sst.skew(data_array), decimal_points)
    elif distribution_measure == 'kurtosis' or distribution_measure == 'kurt':
        result = np.round(sst.kurtosis(data_array), decimal_points)
    elif distribution_measure == 'kurtosis+3' or distribution_measure == 'kurt+3':
        result = np.round(sst.kurtosis(data_array) + 3, decimal_points)
    elif distribution_measure == 'all':
        result = sst.skew(data_array), sst.kurtosis(data_array), sst.kurtosis(data_array) + 3
        result = [np.round(item, decimal_points) for _, item in enumerate(result)]
        row_names = ['Skewness', 'Kurtosis', 'Kurtosis+3']
        result = pd.DataFrame(result, index = row_names, columns = ['Value'])
    else:
        raise Exception("'%s' is an invalid value for 'distribution_measure'." %(distribution_measure))
    
    return result