# -*- coding: utf-8 -*-
"""
@Author:
  Samuel Frederick, NSSC Contractor (ORAU)
  U.S. EPA, Office of Research and Development
  Center for Environmental Measurement and Modeling
  Air Methods and Characterization Division, Source and Fine Scale Branch
  109 T.W. Alexander Drive, Research Triangle Park, NC 27711
  Office: 919-541-4086 | Email: frederick.samuel@epa.gov

Created:
  Fri Jan 31 09:28:30 2020
Last Updated:
  Wed Jul 14 09:11:15 2021
"""
import os
import sys
import pandas as pd
from sensortoolkit.datetime_utils import set_datetime_index


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
        in a testing group

    Returns:
    full_df_list (list):
      List of pandas dataframe objects, one for each sensor dataset
      containing processed full time-resolution data.
    hourly_df_list (list):
      List of pandas dataframe objects, one for each sensor dataset
      containing processed hourly averaged time-resolution data.
    daily_df_list (list):
      List of pandas dataframe objects, one for each sensor dataset
      containing processed daily (24-hr) averaged time-resolution data.
    """
    start = kwargs.get('deploy_bdate', None)
    end = kwargs.get('deploy_edate', None)

    full_df_list, hourly_df_list, daily_df_list = [], [], []

    # Check if files in processed file directory
    if len(os.listdir(processed_path)) == 0:
        sys.exit('No processed files exist. Process recorded sensor datasets '
                 'by setting "load_raw_data" to True')

    else:
        print('Loading processed sensor data')
        for sensor_id in list(sensor_serials.values()):
            for filename in os.listdir(processed_path):

                if filename.endswith(sensor_id + '_full.csv'):
                    print('..' + filename)
                    idx_fmt = '%Y-%m-%d %H:%M:%S'
                    df = pd.read_csv(processed_path+filename)
                    df = set_datetime_index(df, idx_fmt=idx_fmt)
                    if start is not None:
                        df = df.loc[start:, :]
                    if end is not None:
                        df = df.loc[:end, :]
                    full_df_list.append(df)

                if filename.endswith(sensor_id + '_hourly.csv'):
                    print('..' + filename)
                    idx_fmt = '%Y-%m-%d %H:%M:%S'
                    df = pd.read_csv(processed_path+filename)
                    df = set_datetime_index(df, idx_fmt=idx_fmt)
                    if start is not None:
                        df = df.loc[start:, :]
                    if end is not None:
                        df = df.loc[:end, :]
                    hourly_df_list.append(df)

                if filename.endswith(sensor_id + '_daily.csv'):
                    print('..' + filename)
                    idx_fmt = '%Y-%m-%d'
                    df = pd.read_csv(processed_path+filename)
                    df = set_datetime_index(df, idx_fmt=idx_fmt)
                    if start is not None:
                        df = df.loc[start:, :]
                    if end is not None:
                        df = df.loc[:end, :]
                    daily_df_list.append(df)

        return full_df_list, hourly_df_list, daily_df_list
