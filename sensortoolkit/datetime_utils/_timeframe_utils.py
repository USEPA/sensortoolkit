# -*- coding: utf-8 -*-
"""
This module contains various methods for determining the overall (deployment)
timeframe during which testing occurred by locating the extrema of recorded
timestamps across all sensor datasets.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Tue Nov 10 14:31:42 2020
Last Updated:
  Tue Jul 13 11:42:22 2021
"""
import pandas as pd


def timeframe_search(sensor_df_list):
    """Determines the timeframe for which data should be loaded.

    Locates the beginning and end date of each hourly averaged sensor dataframe
    and subsequently determines the eariest and latest date within all recorded
    sensor datasets

    Args:
        sensor_df_list (list): List of sensor dataframes

    Returns:
        (tuple): Two-element tuple containing:

            - **overall_begin** (*datetime.date object*): Earliest recorded date
              in the passed sensor dataframe list.
            - **overall_end** (*datetime.date object*): Latest recorded date in
              the passed sensor dataframe list.

    """
    # Determine begin and end timestamp for sensor datasets. Choose earliest
    # begin and latest end timestamp.
    begin_times = []
    end_times = []

    for df in sensor_df_list:

        begin_time = df.index.min()
        end_time = df.index.max()

        begin_times.append(begin_time)
        end_times.append(end_time)

    overall_begin = min(begin_times)
    overall_end = max(end_times)

    return overall_begin, overall_end


def deploy_timestamp_index(df_obj, averaging_suffix=True):
    """Create a timestamp index that spans the total duration of time during
    which sensors in an evaluation group were deployed.

    Searches for the eariest and latest timestamp in sensor datasets and
    creates a datetime index at the indicated averaging interval spanning the
    time period of testing.

    Args:
        df_obj (either pandas dataframe or list of dataframes):
            Sensor dataframe(s)
        averaging_suffix (bool):
            If true, a string suffix will be returned indicating the averaging
            interval of the passed dataframe object.

    Returns:
        (tuple): One- or two-element tuple containing:

            - **timestamp_idx** (*pandas DatetimeIndex*): Index at either 1-hour
              or 24-hour averaging intervals spanning the entire evaluation
              period.
            - **avg_suffix** (*str*): If averaging_suffix is true, return suffix
              indicating the averaging interval of the timestamp index.

    """
    if type(df_obj) is list:
        df = df_obj[0]  # Use the first dataframe in the list as model
        df_list = df_obj

    if type(df_obj) is pd.core.frame.DataFrame:
        df = df_obj
        df_list = [df]

    # Compute timedelta between successive timestamps
    delta = (df.index[1:] - df.index[0:-1]).to_frame()

    idx_name = delta.index.name
    if idx_name is None:
        idx_name = 'DateTime'
        delta.index.name = idx_name

    # Use mode of timedelta to extrapolate # of datapoints recorded per hr
    time_delta = delta.index.to_series().mode()[0]

    # Check time interval (1hr or 24hr)
    deploy_begin, deploy_end = timeframe_search(df_list)

    if time_delta == pd.Timedelta('1 H'):
        timestamp_idx = pd.date_range(start=deploy_begin,
                                      end=deploy_end,
                                      freq='H')
        avg_suffix = '_1-hour'

    elif time_delta == pd.Timedelta('1 D'):
        timestamp_idx = pd.date_range(start=deploy_begin,
                                      end=deploy_end,
                                      freq='D')
        avg_suffix = '_24-hour'

    #timestamp_idx = timestamp_idx.tz_localize('UTC')

    if averaging_suffix is True:
        return timestamp_idx, avg_suffix
    else:
        return timestamp_idx
