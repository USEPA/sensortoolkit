# -*- coding: utf-8 -*-
"""
This module estimates dewpoint via ambient temperature and relative humidity
measurements made by independent temperature and relative humidity instruments
running alonside sensors and FRM/FEM instrumentation at the evaluation site.

.. caution::

    DP should not be calculated using on-board temperature and relative humidity
    sensor measurements (if applicable), as these measurements may not accurately
    represent ambient temperature and relative humidity conditions.

Calculation
-----------

Dewpoint is estimated via the Magnus Formula,

.. math::

    DP_{d} = \\lambda \\times \\left[ \\frac{\\ln(\\frac{RH_d}{100}) + \\frac{
    \\beta\\times T_d}{\\lambda + T_d} }{\\beta - \\ln(\\frac{RH_d}{100} -
    \\frac{\\beta\\times T_d}{\\lambda + T_d})} \\right]

where

    :math:`\\beta` = 17.625

    :math:`\\lambda` = 243.04

    :math:`DP_d` = valid 24-hour averaged ambient dewpoint for day d (°C)

    :math:`RH_d` = valid 24-hour averaged ambient relative humidity for day d (%)

    :math:`T_d` = valid 24-hour averaged ambient temperature for day d (°C)

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


def Dewpoint(df_list):
    """Calculate dewpoint using the Magnus Formula.

    Constants via U.S EPA Performance Targets reports for evaluating sensors
    measuring fine particulate matter and ozone.

    Args:
        df_list:
            List of sensor dataframes.
    Returns:
        df_list:
            List of modified sensor dataframes with calulcated dewpoint
            ('DP_Calculated').
    """
    for i, df in enumerate(df_list):

        beta = 17.625
        lbda = 243.04  # degrees C

        if 'Temp' and 'RH' in df:
            T = df.Temp
            RH = df.RH
        else:
            print('Warning, Temperature and RH labels not recognized, DP not '
                  'computed')
            return df_list

        numerator = lbda*(np.log(RH/100) + (beta*T)/(lbda+T))
        denominator = beta - (np.log(RH/100) + (beta*T)/(lbda+T))
        Dp = numerator / denominator

        df['DP_calculated'] = Dp

        df_list[i] = df

    return df_list
