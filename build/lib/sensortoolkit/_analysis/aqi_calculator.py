# -*- coding: utf-8 -*-
"""
This module is used to calculate the air quality index (AQI) as defined by U.S.
EPA for fine particulate matter (PM2.5).

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


def AQI_Calculator(data):
    """Calculate US EPA's air quality index for PM2.5.

    Information about EPA's AQI scale here:
        https://aqs.epa.gov/aqsweb/documents/codetables/aqi_breakpoints.html

    EPA defines breakpoints for concentrations with a precision of 0.1 ug/m^3.
    Since most PM2.5 concentration datasets tend to have higher reporting
    precision than 0.1 ug/m^3, this introduces some ambiguity regarding how AQI
    is calculated for concentration values in between breakpoints set at 0.1
    ug/m^3 precision.

    Here, the breakpoints are set so that the concentration values adhere to
    the AQI catagory at the breakpoints by following rounding conventions
    (values within the range of category high breakpoint + 0.05 (e.g.,
    'Good' C_h = 12.05) are assigned to the lower category, if
    high breakpoint + 0.05 < concentration value < high breakpoint + 0.10 then
    set as upper category AQI value).

    **Concentration values < 0 and > 99,999 are ignored by this module (both
    the AQI value and category return null)**

    Args:
        data (float, int, numpy array, or pandas dataframe): PM2.5 concentration
            value(s), if dataframe, column must be labeled 'PM25'.

    Returns:
        dataframe: A pandas dataframe with PM25 concentrations, AQI
            values, and corresponding AQI category names.

    Raises:
        KeyError: If passed data object is type pandas dataframe and the column
            header 'PM25' is not found.
    """
    AQI_dict = {'Good': {'I_h': 50,
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

    data_type = type(data)
    if data_type is not pd.core.frame.DataFrame:
        data = pd.Series(data).to_frame(name='PM25')

    if 'PM25' not in data:
        raise KeyError('Column header "PM25" not in passed dataframe.')

    for cat in AQI_dict:
        conc_max = AQI_dict[cat]['C_h']
        conc_min = AQI_dict[cat]['C_l']
        index_max = AQI_dict[cat]['I_h']
        index_min = AQI_dict[cat]['I_l']

        cat_conc = data[(data.PM25 >= conc_min) & (data.PM25 < conc_max)].PM25
        cat_idx = cat_conc.index

        slope = (index_max - index_min)/(conc_max - conc_min)
        aqi = round(slope*(cat_conc - conc_min) + index_min)

        data.loc[cat_idx, 'AQI'] = aqi
        data.loc[cat_idx, 'AQI_Category'] = cat

    return data
