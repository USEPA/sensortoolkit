# -*- coding: utf-8 -*-
"""
This module calculates normalized sensor concentrations.

..
    PM2.5 Performance Targets Report Section 3.1.6.2

Calculation
-----------

Normalized 1-hour and 24-hour averaged sensor concentrations are derived
by dividing the 1-hour or 24-hour averaged sensor concentration by the
paired 1-hour or 24-hour averaged FRM/FEM concentration. This
equation assumes only one FRM/FEM instrument will be running. If multiple
FRM/FEM instruments are running, separate testing reports can be generated for
each.


.. math::

    NormC_{ij} = \\frac{x_{ij}}{R_i}

where

    :math:`NormC_{ij}`` = normalized 1-hour or 24-hour averaged sensor
    concentration for interval i and instrument j

    :math:`x_{ij}` = valid 1-hour or 24-hour averaged sensor concentration
    for interval i and instrument j

    :math:`R_{i}` = valid 1-hour or 24-hour averaged FRM/FEM concentration for
    interval i

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Tue Mar 17 14:41:13 2020
Last Updated:
  Wed Jul 14 08:20:29 2021
"""
import numpy as np


def normalize(df_list, ref_df, param=None, ref_name=None):
    """Normalize sensor measurements at 1-hour or 24-hour intervals by
    concurrent measurements from a collocated FRM/FEM monitor.

    Args:
        df_list (list):
            List of sensor dataframes with datetimeindex at either 1-hour or
            24-hour averaging intervals.

        ref_df (pandas dataframe):
            Dataframe with FRM/FEM measurements from a reference monitor
            collocated alongside sensors at a monitoring site. Dataframe at
            either 1-hour or 24-hour averaging intervals, matches interval of
            df_list.
        param (str):
            The evaluation parameter.
        ref_name (str):
            The make and model of the FRM/FEM monitor.

    Returns:
        df_list (list of pandas DataFrames):
            Modified list of sensor dataframes with a column added for
            normalized parameter values.

    """
    print('Computing normalized', param, 'values (by', ref_name + ')')

    for i, df in enumerate(df_list):
        try:
            df['Normalized_'+param + '_Value'] = df[param + '_Value'] / ref_df[param + '_Value']
        except KeyError as k:
            print('...Warning', k, 'not found in dataframe at index ', str(i))
            df['Normalized_' + param + '_Value'] = np.nan
        df['Normalized_' + param + '_Unit'] = 'Unitless'
        df_list[i] = df

    return df_list
