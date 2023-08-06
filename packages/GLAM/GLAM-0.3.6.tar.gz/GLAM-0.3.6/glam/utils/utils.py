import pandas as pd
import numpy as np
import importlib
import sys

def load_linz(path = None):
    if path is None:
        print('No path supplied to LINZ datafile')
        return None
    return pd.read_csv(path, dtype=str).fillna('')

def choose(option1 = lambda: None, option2 = lambda: None, chance1 = 0.5):
    """
    randomly choose either option1 function or option 2
    
    Inputs:
        option1:           option 1 callable - default None
        option2:           option 2 callable - default None
        chance1:           probability for option 1 to be selected. Defaults to 50/50 odds
    Outputs:
        return:            output of randomly chosen function
    """
    if np.random.uniform() <= chance1:
        return option1()
    else:
        return option2()

def build_address(
    unit = '',
    first_number = '',  
    first_number_suffix = '',
    second_number = '',    
    street_name = '',  
    suburb = '',
    town_city = '',
    postcode = '',
):

    head = ''
    if len(unit) > 0:
        head += unit 
    if len(unit) > 0 and len(first_number) > 0:
        head += '/'
    head += first_number + first_number_suffix

    if len(second_number) > 0 and len(head) > 0:
        head += '-' + second_number
    else:
        head += second_number


    middle_parts = [street_name,suburb,town_city]
    middle_parts = [x for x in middle_parts if len(x) > 0]
    middle_parts = ', '.join(middle_parts) 

    addy_parts = [head, middle_parts, postcode]
    addy_parts = [x for x in addy_parts if len(x) > 0]

    addy = ' '.join(addy_parts) 

    return addy
    
def check_package_dependency(package, version=None):

    if package in sys.modules:
        return None
    
    found = sys.modules.get(package,None) 
    if found is None:
        if version is not None:
            raise ValueError(f"Missing optional dependency: {package}=={version}")
        else:
            raise ValueError(f"Missing optional dependency: {package}")
    
    if version is not None:
        if version != found.__version__:
            raise ValueError(f"Missing optional dependency: {package}=={version}")

    return None


