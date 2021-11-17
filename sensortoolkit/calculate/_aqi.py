# -*- coding: utf-8 -*-
"""
This module is used to calculate the air quality index (AQI) as defined by U.S.
EPA for fine particulate matter (PM2.5).

Resources
---------

* `AirNow - Using the Air Quality Index <https://www.airnow.gov/aqi/aqi-basics/
  using-air-quality-index/>`_
* `AirNow - AQI Basics <https://www.airnow.gov/aqi/aqi-basics/>`_
* `AQI Breakpoint Table <https://aqs.epa.gov/aqsweb/documents/codetables/
  aqi_breakpoints.html>`_
* `Technical Assistance Document for the Reporting of Daily Air Quality – the
  Air Quality Index (AQI) <https://www.airnow.gov/sites/default/files/2020-05/
  aqi-technical-assistance-document-sept2018.pdf>`_

Calculation
-----------

The AQI is calculated via the following equation:

.. math::

    I_p = \\frac{I_{Hi} - I_{Lo}}{BP_{Hi} - BP_{Lo}}\\left(C_p -
    BP_{Lo}\\right) + I_{Lo}

where

    :math:`I_p` = the index for pollutant p

    :math:`C_p` = the truncated concentration of pollutant p

    :math:`BP_{Hi}` = the concentration breakpoint that is greater than or equal
    to :math:`C_p`

    :math:`BP_{Lo}` = the concentration breakpoint that is less than or equal to
    :math:`C_p`

    :math:`I_{Hi}` = the AQI value corresponding to :math:`BP_{Hi}`

    :math:`I_{Lo}` = the AQI value corresponding to :math:`BP_{Lo}`

More detail about the AQI calculation, as well as a detailed description, are
included in the `Technical Assistance Document` listed above.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Mon Jan 27 13:11:40 2020
Last Updated:
  Tue Jul 13 08:43:27 2021
"""
import pandas as pd


def aqi(data, column=None):
    """Calculate US EPA's air quality index for fine particulate matter.

    Information about EPA's AQI scale here:
        https://aqs.epa.gov/aqsweb/documents/codetables/aqi_breakpoints.html

    EPA defines breakpoints for concentrations with a precision of 0.1 µg/m³.
    Since most PM2.5 concentration datasets tend to have higher reporting
    precision than 0.1 µg/m³, this introduces some ambiguity regarding how AQI
    is calculated for concentration values in between breakpoints set at 0.1
    µg/m³ precision.

    Here, the breakpoints are set so that the concentration values adhere to
    the AQI catagory at the breakpoints by following rounding conventions
    (values within the range of category high breakpoint + 0.05 (e.g.,
    'Good' C_h = 12.05) are assigned to the lower category, if
    high breakpoint + 0.05 < concentration value < high breakpoint + 0.10 then
    set as upper category AQI value).

    **Concentration values < 0 and > 99,999 are ignored by this module (both
    the AQI value and category return null)**

    Args:
        data (float, int, numpy array, or pandas dataframe):
            PM2.5 concentration value(s). If dataframe, column must be labeled
            ``PM25_Value``.
        column (str, optional):
            If the passed data object is type pandas DataFrame, the name of the
            column in the dataset corresponding to fine particulate matter
            concentration data.

    Returns:
        data (pandas DataFrame):
            A pandas dataframe with PM25 concentrations, AQI
            values, and corresponding AQI category names.

    Raises:
        KeyError: If passed data object is type pandas dataframe and the
            column argument is null.

    """
    breakpoints = {'Good': {'I_h': 50,
                            'I_l': 0,
                            'C_l': 0.0,
                            'C_h': 12.05},
                   'Moderate': {'I_h': 100,
                                'I_l': 51,
                                'C_l': 12.05,
                                'C_h': 35.45},
                   'Unhealthly for Sensitive Groups': {'I_h': 150,
                                                       'I_l': 101,
                                                       'C_l': 35.45,
                                                       'C_h': 55.45},
                   'Unhealthly': {'I_h': 200,
                                  'I_l': 151,
                                  'C_l': 55.45,
                                  'C_h': 150.45},
                   'Very Unhealthly': {'I_h': 300,
                                       'I_l': 201,
                                       'C_l': 150.45,
                                       'C_h': 250.45},
                   'Hazardous 1': {'I_h': 400,
                                   'I_l': 301,
                                   'C_l': 250.45,
                                   'C_h': 350.45},
                   'Hazardous 2': {'I_h': 500,
                                   'I_l': 401,
                                   'C_l': 350.45,
                                   'C_h': 500.45},
                   'Hazardous 3': {'I_h': 999,
                                   'I_l': 501,
                                   'C_l': 500.45,
                                   'C_h': 99999.9}}

    # Convert input type to pandas dataframe
    data_type = type(data)
    if data_type is not pd.core.frame.DataFrame:
        column = 'PM25_Value'
        data = pd.Series(data).to_frame(name=column)

    # Passed datatype is pandas dataframe but expected header not found
    if column is None and data_type is pd.core.frame.DataFrame:
        raise AttributeError('Column header for fine PM data not specified')

    for cat, cat_bpoints in breakpoints.items():
        conc_max = cat_bpoints['C_h']
        conc_min = cat_bpoints['C_l']
        index_max = cat_bpoints['I_h']
        index_min = cat_bpoints['I_l']

        cat_conc = data[(data[column] >= conc_min) &
                        (data[column] < conc_max)][column]
        cat_idx = cat_conc.index

        slope = (index_max - index_min)/(conc_max - conc_min)
        aqi_value = round(slope*(cat_conc - conc_min) + index_min)

        data.loc[cat_idx, 'AQI'] = aqi_value
        data.loc[cat_idx, 'AQI_Category'] = cat

    return data
