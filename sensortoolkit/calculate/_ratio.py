# -*- coding: utf-8 -*-
"""
This module contains methods to calculate the PM2.5/PM10 ratio for the PM10
report.

U.S. EPA's Performance Targets Reports calculate the ratio as

.. math::

    \\frac{PM_{2.5}}{PM_{10}} = \\frac{R_{h, PM_{2.5}}}{R_{h, PM_{10}}}

where :math:`R_{h, PM_{2.5}}` are valid 1-hour average FRM/FEM PM_{2.5} 
concentrations for hour h (\\mu g/m^3) and where :math:`R_{h, PM_{10}}` are 
valid 1-hour average FRM/FEM PM_{10} concentrations for hour h (\\mu g/m^3)

================================================================================

@Author:
  | Menaka Kumar, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Sep  4 09:04:18 2024
Last Updated:
  Wed Sep  26 09:04:18 2024
"""

import os
import sys
import pandas as pd
import numpy as np

def calculate_ratio(data_dict, serial_id, **kwargs):

    """Compute sensors' PM2.5/PM10 ratio.

    Args:
        data_dict(tuple): Three-element tuple containing:

            - **full_df_list** (*list*): List of pandas dataframe objects, one
              for each sensor dataset containing processed full time-resolution
              data.
            - **hourly_df_list** (*list*): List of pandas dataframe objects, one
              for each sensor dataset containing processed hourly averaged
              time-resolution data.
            - **daily_df_list** (*list*): List of pandas dataframe objects, one
              for each sensor dataset containing processed daily (24-hr)
              averaged time-resolution data.
        serial_id(str)
            serial identifier of sensor in the deployment group.
    
    Returns:
        data_dict(tuple): Three-element tuple containing:

            - **full_df_list** (*list*): List of pandas dataframe objects, one
              for each sensor dataset containing processed full time-resolution
              data. Last column now contains PM2.5/PM10 ratio at full-time resolution.
            - **hourly_df_list** (*list*): List of pandas dataframe objects, one
              for each sensor dataset containing processed hourly averaged
              time-resolution data. Last column now contains PM2.5/PM10 ratio at
              hourly averaged time resolution.
            - **daily_df_list** (*list*): List of pandas dataframe objects, one
              for each sensor dataset containing processed daily (24-hr)
              averaged time-resolution data. Last column now contains PM2.5/PM10 ratio at
              daily (24-hr) averaged time resolution.

    """

    full_df = data_dict['full'][serial_id]
    hourly_df = data_dict['1-hour'][serial_id]
    daily_df = data_dict['24-hour'][serial_id]

    # check if with one of the lists in data_dict if it has columns for BOTH PM2.5 and PM10
    # If so, then calculate the PM2.5/PM10 ratio and put it in a new column named "ratio_value"
    if set(['PM10_Value','PM25_Value']).issubset(full_df.columns):
        full_df = full_df.assign(ratio_value = full_df['PM25_Value'] / full_df['PM10_Value'])
        hourly_df = hourly_df.assign(ratio_value = hourly_df['PM25_Value'] / hourly_df['PM10_Value'])
        daily_df = daily_df.assign(ratio_value = daily_df['PM25_Value'] / daily_df['PM10_Value'])
        
        # If PM10=0 anywhere it will produce a -inf or inf. Replace these values with NaN in the data list
        full_df['ratio_value'].replace([np.inf, -np.inf], np.nan, inplace=True)
        hourly_df['ratio_value'].replace([np.inf, -np.inf], np.nan, inplace=True)
        daily_df['ratio_value'].replace([np.inf, -np.inf], np.nan, inplace=True)

    # Put the modified lists back into the data_dict dictionary
    data_dict['full'][serial_id] = full_df
    data_dict['1-hour'][serial_id] = hourly_df
    data_dict['24-hour'][serial_id] = daily_df

    return data_dict


def calculate_ref_ratio(month_df):

    """Compute reference monitor's PM2.5/PM10 ratio.

    Args:
        month_df(df): Reference DataFrames that were ingested into SDFS format.

    Returns:
        month_df(df): Reference DataFrames that were ingested into SDFS format.
        The last column contains PM2.5/PM10 ratio values.

    """
    # check if with one of the lists in data_dict if it has columns for BOTH PM2.5 and PM10
    # If so, then calculate the PM2.5/PM10 ratio and put it in a new column named "ratio_value"
    if set(['PM10_Value','PM25_Value']).issubset(month_df.columns):
        month_df = month_df.assign(ratio_value = month_df['PM25_Value'] / month_df['PM10_Value'])
        
        # If PM10=0 anywhere it will produce a -inf or inf. Replace these values with NaN in the data list
        month_df['ratio_value'].replace([np.inf, -np.inf], np.nan, inplace=True)

    return month_df


def ratio_count(data_dict, serial_id, **kwargs):

    """Computes the number of times a sensor's PM2.5/PM10 ratio values is equal to or
    less than 0.4 for at least one hour. This value is asked for by the U.S. EPA's 
    Performance Targets Reports for FRM/FEM monitors.

    Args:
        data_dict(tuple): Three-element tuple containing:

            - **full_df_list** (*list*): List of pandas dataframe objects, one
              for each sensor dataset containing processed full time-resolution
              data.
            - **hourly_df_list** (*list*): List of pandas dataframe objects, one
              for each sensor dataset containing processed hourly averaged
              time-resolution data.
            - **daily_df_list** (*list*): List of pandas dataframe objects, one
              for each sensor dataset containing processed daily (24-hr)
              averaged time-resolution data.
        serial_id(str)
            serial identifier of sensor in the deployment group.
    
    Returns:
        count(int): The number of times a sensor's PM2.5/PM10 ratio values is equal to or
        less than 0.4 for at least one hour as asked by the U.S. EPA's Performance Targets Reports
        for FRM/FEM monitors.

    """

    hourly_df = data_dict['1-hour'][serial_id]
    count = [np.nan]
    # Make sure there is a ratio_value col in the data. If so, count the number of times a sensor's 
    # PM2.5/PM10 ratio values is equal to or less than 0.4 for at least one hour. If not, the function
    # will return [np.nan].
    if 'ratio_value' in hourly_df.columns:
        count = len(hourly_df[hourly_df.ratio_value <= 0.4])

    return count


def ratio_ref_count(month_df):
    """Computes the number of times a reference monitors PM2.5/PM10 ratio values is equal to or
    less than 0.4 for at least one hour as asked by the U.S. EPA's Performance Targets Reports
    for FRM/FEM monitors.

    Args:
        month_df(df): Reference DataFrames that were ingested into SDFS format.
    
    Returns:
        count(int): The number of times a FRM/FEM monitor's PM2.5/PM10 ratio values is equal to or
        less than 0.4 for at least one hour as asked by the U.S. EPA's Performance Targets 
        for FRM/FEM monitors.

    """

    count = [np.nan]
    # Make sure there is a ratio_value col in the data. If so, count the number of times a FRM/FEM's 
    # PM2.5/PM10 ratio values is equal to or less than 0.4 for at least one hour. If not, the function
    # will return [np.nan].
    if 'ratio_value' in month_df.columns:
        count = len(month_df[month_df.ratio_value <= 0.4])
        
    return count