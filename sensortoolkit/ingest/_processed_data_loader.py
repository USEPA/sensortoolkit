# -*- coding: utf-8 -*-
"""
This module is used to load previously generated SDFS sensor datasets. Datasets
are imported for three time intervals, including data at the orginally recorded
sampling frequency, datasets that have been averaged to 1-hour intervals, and
datasets that have been averaged to 24-hour intervals.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Fri Jan 31 09:28:30 2020
Last Updated:
  Wed Jul 14 09:11:15 2021
"""
import os
import sys
import pandas as pd


def processed_data_search(processed_path, sensor_serials, **kwargs):
    """Load processed data files at recorded sampling frequency, 1-hour
    averaged, and 24-hour averaged intervals.

    Determines whether processed data files exist and can be loaded into
    dataframes. Full time-resolution, hour-averaged, and 24-hour averaged
    data files are loaded into separate data frame lists.

    Args:
        processed_path (str):
            Directory path where the processed data files are stored.
        sensor_serials (dict):
            A dictionary of sensor serial identifiers for each unit
            in a testing group.

    **Keyword Arguments**

    :param str deploy_bdate:
        The timestamp (date) marking the beginning of the sensor testing period,
        formatted as ``'YYYY-MM-DD HH:MM:SS'``. Sensor datasets will be
        concatenated to begin at this timestamp.
    :param str deploy_edate:
        The timestamp (date) marking the end of the sensor testing period,
        formatted as ``'YYYY-MM-DD HH:MM:SS'``. Sensor datasets will be
        concatenated to end at this timestamp.

    Returns:
        (tuple): Three-element tuple containing:

            - **full_df_list** (*list*): List of pandas dataframe objects, one
              for each sensor dataset containing processed full time-resolution
              data.
            - **hourly_df_list** (*list*): List of pandas dataframe objects,
              one for each sensor dataset containing processed hourly averaged
              time-resolution data.
            - **daily_df_list** (*list*): List of pandas dataframe objects, one
              for each sensor dataset containing processed daily (24-hr)
              averaged time-resolution data.

    """
    start = kwargs.get('deploy_bdate', None)
    end = kwargs.get('deploy_edate', None)

    data_dict = {'full': {},
                 '1-hour': {},
                 '24-hour': {}}

    # Check if files in processed file directory
    if len(os.listdir(processed_path)) == 0:
        sys.exit('No processed files exist. Process recorded sensor datasets '
                 'by setting "load_raw_data" to True')

    else:
        print('Loading processed sensor data')
        for serial_id in list(sensor_serials.values()):
            for interval in data_dict:
                data_dict[interval][serial_id] = pd.DataFrame()

            for filename in os.listdir(processed_path):

                if filename.endswith(serial_id + '_full.csv'):
                    print('..' + filename)
                    # Assert index formatting is ISO8601
                    df = pd.read_csv(processed_path+filename,
                                     index_col=0, parse_dates=True)
                    if start is not None:
                        df = df.loc[start:, :]
                    if end is not None:
                        df = df.loc[:end, :]
                    data_dict['full'][serial_id] = df

                if filename.endswith(serial_id + '_hourly.csv'):
                    print('..' + filename)
                    # Assert index formatting is ISO8601
                    df = pd.read_csv(processed_path+filename,
                                     index_col=0, parse_dates=True)
                    if start is not None:
                        df = df.loc[start:, :]
                    if end is not None:
                        df = df.loc[:end, :]
                    data_dict['1-hour'][serial_id] = df

                if filename.endswith(serial_id + '_daily.csv'):
                    print('..' + filename)
                    # Assert index formatting is ISO8601
                    df = pd.read_csv(processed_path+filename,
                                     index_col=0, parse_dates=True)
                    if start is not None:
                        df = df.loc[start:, :]
                    if end is not None:
                        df = df.loc[:end, :]
                    data_dict['24-hour'][serial_id] = df

        return data_dict
