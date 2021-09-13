# -*- coding: utf-8 -*-
"""
@Author:
  Samuel Frederick, NSSC Contractor (ORAU)
  U.S. EPA, Office of Research and Development
  Center for Environmental Measurement and Modeling
  Air Methods and Characterization Division, Source and Fine Scale Branch
  109 T.W Alexander Drive, Research Triangle Park, NC 27711
  Office: 919-541-4086 | Email: frederick.samuel@epa.gov

Created:
  Fri Sep 10 09:11:01 2021
Last Updated:
  Fri Sep 10 09:11:01 2021
"""
import pandas as pd

def convert_temp(data, from_unit='F', to_unit='C'):
    """Convert temperature from one unit basis to another.

    Can convert from Fahrenheit to Celsius or vice versa.

    Args:
        data (TYPE): DESCRIPTION.
        from_unit (TYPE, optional): DESCRIPTION. Defaults to 'F'.
        to_unit (TYPE, optional): DESCRIPTION. Defaults to 'C'.

    Raises:
        KeyError: DESCRIPTION.
        AttributeError: DESCRIPTION.

    Returns:
        converted_data (TYPE): DESCRIPTION.

    """
    # Convert input type to pandas dataframe
    data_type = type(data)
    if data_type is not pd.core.frame.DataFrame:
        data = pd.Series(data).to_frame(name='Temp')

    # Passed datatype is pandas dataframe but expected header not found
    if 'Temp' not in data:
        raise KeyError('Column header "Temp" not in passed dataframe.')

    f_to_c = lambda x: (x - 32.0) / 1.8
    c_to_f = lambda x: 1.8*(x) + 32.0

    if from_unit == 'F' and to_unit == 'C':
        print('..converting from Fahrenheit to Celsius')
        converted_data = f_to_c(data)
    elif from_unit == 'C' and to_unit == 'F':
        print('..converting from Celsius to Fahrenheit')
        converted_data = c_to_f(data)
    else:
        raise AttributeError('Invalid conversion. Arguments for "from_unit"'
                             ' and "to_unit" must be either "C" or "F" and'
                             ' should not be the same unit.')

    return converted_data
