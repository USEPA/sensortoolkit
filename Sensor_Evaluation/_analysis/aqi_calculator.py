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
  Mon Jan 27 13:11:40 2020
Last Updated:
  Mon May 18 10:49:00 2020
"""
import pandas as pd
import numpy as np


def AQI_Calculator(concentration_value):
    """
    5/18/20
    The breakpoints defined by EPA at the following link assume that
    concentration values are provided in 0.1 ug/m^3 increments:
    https://aqs.epa.gov/aqsweb/documents/codetables/aqi_breakpoints.html

    This introduces an issue with datasets where the concentration resolution
    is higher than 0.1 ug/m^3, such that values between the high breakpoint for
    one category and the low breakpoint for the subsequent AQI category result
    in undefined AQI values.

    Here, I've set the breakpoints so that the concentration values adhere to
    the AQI catagory at the breakpoints by following rounding conventions
    (values within the range of category high breakpoint + 0.05 (e.g.,
    'Good' C_h = 12.05) are assigned to the lower category, if
    high breakpoint + 0.05 < concentration value < high breakpoint + 0.10 then
    set as upper category AQI value).
    """
    AQI_dict = {'Good': {
                    'I_h': 50,
                    'I_l': 0,
                    'C_l': 0.0,
                    'C_h': 12.05,
                        },
                'Moderate': {
                    'I_h': 100,
                    'I_l': 51,
                    'C_l': 12.05,
                    'C_h': 35.45,
                        },
                'Unhealthly_sensitive': {
                    'I_h': 150,
                    'I_l': 101,
                    'C_l': 35.45,
                    'C_h': 55.45,
                        },
                'Unhealthly': {
                    'I_h': 200,
                    'I_l': 151,
                    'C_l': 55.45,
                    'C_h': 150.45,
                        },
                'Very_Unhealthly': {
                    'I_h': 300,
                    'I_l': 201,
                    'C_l': 150.45,
                    'C_h': 250.45,
                        },
                'Hazardous_1': {
                    'I_h': 400,
                    'I_l': 301,
                    'C_l': 250.45,
                    'C_h': 350.45,
                        },
                'Hazardous_2': {
                   'I_h': 500,
                   'I_l': 401,
                   'C_l': 350.45,
                   'C_h': 500.0,
                       }
                }

    for i, catagory in enumerate(AQI_dict, 1):
        cat = AQI_dict[catagory]
        C_high = cat['C_h']
        C_low = cat['C_l']
        I_high = cat['I_h']
        I_low = cat['I_l']

        # Handle instances where the pm conc exceeds the upper limit of
        # AQI catagories by calculating AQI using same slope as hazardous cat
        if catagory == 'Hazardous_2' and concentration_value > C_high:
            const = (I_high - I_low)/(C_high - C_low)
            AQI = round(const*(concentration_value - C_low) + I_low)
            return pd.Series((AQI, i))

        # Compute AQI if conc value falls within the range of each AQI cat
        if (concentration_value >= C_low and concentration_value < C_high):
            const = (I_high - I_low)/(C_high - C_low)
            AQI = round(const*(concentration_value - C_low) + I_low)
            return pd.Series((AQI, i))

        if pd.isnull(concentration_value) or concentration_value < 0:
            AQI = np.nan
            i = np.nan
            return pd.Series((AQI, i))
