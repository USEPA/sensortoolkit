# -*- coding: utf-8 -*-
"""
@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Fri Sep 10 09:11:01 2021
Last Updated:
  Fri Sep 10 09:11:01 2021
"""
import pandas as pd

def convert_temp(data, from_unit='F', to_unit='C', **kwargs):
    """Convert temperature from one unit basis to another.

    Can convert from Fahrenheit to Celsius or vice versa.

    Args:
        data (pandas DataFrame or pandas Series): DESCRIPTION.
        from_unit (str, optional): DESCRIPTION. Defaults to 'F'.
        to_unit (str, optional): DESCRIPTION. Defaults to 'C'.

    Raises:
        KeyError: DESCRIPTION.
        AttributeError: DESCRIPTION.

    Returns:
        converted_data (pandas DataFrame): DESCRIPTION.

    """
    verbose = kwargs.get('verbose', True)
    # # Convert input type to pandas dataframe
    # data_type = type(data)
    # if data_type is not pd.core.frame.DataFrame:
    #     data = pd.Series(data).to_frame(name='Temp_Value')

    # # Passed datatype is pandas dataframe but expected header not found
    # if 'Temp_Value' not in data:
    #     raise KeyError('Column header "Temp_Value" not in passed dataframe.')

    f_to_c = lambda x: (x - 32.0) / 1.8
    c_to_f = lambda x: 1.8*(x) + 32.0

    if from_unit == 'F' and to_unit == 'C':
        if verbose:
            print('....converting from Fahrenheit to Celsius')
        converted_data = f_to_c(data)
    elif from_unit == 'C' and to_unit == 'F':
        if verbose:
            print('....converting from Celsius to Fahrenheit')
        converted_data = c_to_f(data)
    else:
        raise AttributeError('Invalid conversion. Arguments for "from_unit"'
                             ' and "to_unit" must be either "C" or "F" and'
                             ' should not be the same unit.')

    return converted_data
