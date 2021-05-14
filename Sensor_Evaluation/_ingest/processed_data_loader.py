# -*- coding: utf-8 -*-
"""
@Author:
  Samuel Frederick, NSSC Contractor to U.S EPA, Office of Research and
  Development (ORD), Center for Environmental Measurement and Modeling (CEMM)
Created:
  Fri Jan 31 09:28:30 2020
Last Updated:
  Thu Oct 29 09:10:46 2020
"""
import os
import pandas as pd


def Processed_Data_Search(processed_path, sensor_serials):
    """
    Determines whether processed data files exist and can be loaded into
    dataframes. Full time-resolution, hour-averaged, and 24-hour averaged
    data files are loaded into separate data frame lists.

    Parameters
    ----------
    processed_path: string
      Directory path where the processed data files are stored.

    Returns
    -------
    full_df_list: list
      List of pandas dataframe objects, one for each sensor dataset
      containing processed full time-resolution data.
    hourly_df_list: list
      List of pandas dataframe objects, one for each sensor dataset
      containing processed hourly averaged time-resolution data.
    daily_df_list: list
      List of pandas dataframe objects, one for each sensor dataset
      containing processed daily (24-hr) averaged time-resolution data.
    """
    full_df_list, hourly_df_list, daily_df_list = [], [], []

    # Check if files in processed file directory
    if len(os.listdir(processed_path)) == 0:
        print('No processed files exist.')
        # Return empty dataframe lists
        return full_df_list, hourly_df_list, daily_df_list

    else:
        print('Loading processed sensor data')
        for sensor_id in list(sensor_serials.values()):
            for filename in os.listdir(processed_path):

                if filename.endswith(sensor_id + '_full.csv'):
                    print('..' + filename)
                    idx_fmt = '%Y-%m-%d %H:%M:%S'
                    df = pd.read_csv(processed_path+filename)
                    df = Time_Index_Search(df, idx_fmt=idx_fmt)
                    full_df_list.append(df)

                if filename.endswith(sensor_id + '_hourly.csv'):
                    print('..' + filename)
                    idx_fmt = '%Y-%m-%d %H:%M:%S'
                    df = pd.read_csv(processed_path+filename)
                    df = Time_Index_Search(df, idx_fmt=idx_fmt)
                    hourly_df_list.append(df)

                if filename.endswith(sensor_id + '_daily.csv'):
                    print('..' + filename)
                    idx_fmt = '%Y-%m-%d'
                    df = pd.read_csv(processed_path+filename)
                    df = Time_Index_Search(df, idx_fmt=idx_fmt)
                    daily_df_list.append(df)

        return full_df_list, hourly_df_list, daily_df_list


def Time_Index_Search(df, idx_fmt=None):
    """
    Due to inconsistencies in labeling the column corresponding to timestamp,
    i.e. date and time information, various options are provided to set index
    to datetime format
    """
    try:
        for name in ['Time', 'DateTime', 'localDateTime', 'timeUtc',
                     'DateTime_UTC', 'timestamp']:
            if name in df:
                df = df.set_index(pd.to_datetime(df[name],
                                                 format=idx_fmt)
                                  ).drop(columns={name})
    except NameError:
        print('Error: Sensor timestamp header name not in list'
              'of previously identified timestamp nameschemes')
    return df
