# -*- coding: utf-8 -*-
"""
This module estimates dewpoint via ambient temperature and relative humidity
measurements made by independent temperature and relative humidity instruments
running alonside sensors and FRM/FEM instrumentation at the evaluation site.

.. caution::

    DP should **not** be calculated using on-board temperature and relative
    humidity sensor measurements (if applicable), as these measurements may not
    accurately represent ambient temperature and relative humidity conditions.

Calculation
-----------

Dewpoint is estimated via the Magnus Formula,

.. math::

    DP_{d} = \\lambda \\times \\left[ \\frac{\\ln(\\frac{RH_i}{100}) + \\frac{
    \\beta\\times T_i}{\\lambda + T_i} }{\\beta - \\ln(\\frac{RH_i}{100} -
    \\frac{\\beta\\times T_i}{\\lambda + T_i})} \\right]

where

    :math:`\\beta` = 17.625

    :math:`\\lambda` = 243.04

    :math:`DP_i` = valid ambient dewpoint for measurement interval
    :math:`i` (°C).

    :math:`RH_i` = valid ambient relative humidity for measurement interval
    :math:`i` (%).

    :math:`T_i` = valid ambient temperature for measurement interval
    :math:`i` (°C).

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Mon Jan 27 11:42:49 2020
Last Updated:
  Tue Jul 13 09:35:33 2021
"""
import numpy as np
import pandas as pd


def dewpoint(data):
    """Calculate dewpoint using the Magnus Formula.

    Constants via U.S EPA Performance Targets reports for evaluating sensors
    measuring fine particulate matter and ozone.

    Args:
        data:
            Pandas dataframe or list of pandas dataframes
    Returns:
        data (Pandas DataFrame or list of pandas DataFrames):
            Modified dataframe containing calculated dewpoint (column header
            ``DP_Calculated_Value``).

    """
    BETA = 17.625
    LBDA = 243.04  # degrees C

    # Coerce input type to pandas dataframe
    data_type = type(data)
    if data_type is not pd.core.frame.DataFrame and data_type is not list:
        raise TypeError('Passed data must be in the form of a pandas dataframe'
                        ' or list of dataframes')

    # temporarily place dataframe in list for calculation
    if data_type is pd.core.frame.DataFrame:
        data = [data]

    for i, df in enumerate(data):

        # Passed datatype is pandas dataframe but expected header not found
        if 'Temp_Value' not in df:
            raise KeyError('Column header "Temp_Value" not in passed '
                           'dataframe.')
        if 'RH_Value' not in df:
            raise KeyError('Column header "RH_Value" not in passed dataframe.')

        temp = df.Temp_Value
        rel_hum = df.RH_Value

        numerator = LBDA*(np.log(rel_hum/100) + (BETA*temp)/(LBDA+temp))
        denominator = BETA - (np.log(rel_hum/100) + (BETA*temp)/(LBDA+temp))
        calc_dp = numerator / denominator

        df['DP_Calculated_Value'] = calc_dp
        df['DP_Calculated_Unit'] = 'Degrees Celsius'

        data[i] = df

    # Extract dataframe from list if input type was dataframe
    if data_type is pd.core.frame.DataFrame:
        data = data[0]

    return data
