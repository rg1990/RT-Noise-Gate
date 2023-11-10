import numpy as np

def ramp_linear_increase(num_points: int) -> [float]:
    ''' Function defining a linear increase from 0 to 1 in num_points samples '''
    return np.linspace(0, 1, num_points)


def ramp_linear_decrease(num_points: int) -> [float]:
    ''' Function defining a linear decrease from 1 to 0 in num_points samples '''
    return np.linspace(1, 0, num_points)


def ramp_poly_increase(num_points: int) -> [float]:
    ''' Generate an array of coefficient values for the attack period '''
    x = np.arange(num_points, 0, -1)
    attack_coef_arr = 1 - (x/num_points)**4
    
    # Make sure the start and end are 0 and 1, respectively
    attack_coef_arr[0] = 0
    attack_coef_arr[-1] = 1
    
    return attack_coef_arr


def ramp_poly_decrease(num_points: int) -> [float]:
    ''' Generate an array of coefficient values for the release period '''
    x = np.arange(num_points)
    release_coef_arr = 1 - (x/num_points)**4
    
    # Make sure the start and end are 1 and 0, respectively
    release_coef_arr[0] = 1
    release_coef_arr[-1] = 0
    
    return release_coef_arr