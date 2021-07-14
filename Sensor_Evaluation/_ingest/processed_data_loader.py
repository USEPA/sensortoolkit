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
import pandas as pd


def Processed_Data_Search(processed_path, sensor_serials):
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
                    df = Set_DateTime_Index(df, idx_fmt=idx_fmt)
                    full_df_list.append(df)

                if filename.endswith(sensor_id + '_hourly.csv'):
                    print('..' + filename)
                    idx_fmt = '%Y-%m-%d %H:%M:%S'
                    df = pd.read_csv(processed_path+filename)
                    df = Set_DateTime_Index(df, idx_fmt=idx_fmt)
                    hourly_df_list.append(df)

                if filename.endswith(sensor_id + '_daily.csv'):
                    print('..' + filename)
                    idx_fmt = '%Y-%m-%d'
                    df = pd.read_csv(processed_path+filename)
                    df = Set_DateTime_Index(df, idx_fmt=idx_fmt)
                    daily_df_list.append(df)

        return full_df_list, hourly_df_list, daily_df_list


def Set_DateTime_Index(df, idx_fmt=None):
    """Set the DateTime_UTC timestamp column as the index.

    Args:
        df (pandas dataframe):
            Sensor dataframe for which the index is being assigned
        idx_fmt (str):
            The foramtting for the timestamp index. Explicitly specifying the
            format speeds up index assignment as pd.to_datetime doesn't have to
            search for the appropriate formatting.

    Return:
        df (pandas dataframe):
            Modified sensor dataframe with the index assigned as the
            'DateTime_UTC' column.

    Raises:
        NameError: If the column header 'DateTime_UTC' is not found in the
        dataframe (may occur if the user assigns a label other than
        'DateTime_UTC' to the time-like index during the process of data
        ingestion.)
    """
    try:

        df = df.set_index(pd.to_datetime(df['DateTime_UTC'], format=idx_fmt)
                          ).drop(columns={'DateTime_UTC'})
    except NameError:
        print('Error: Sensor timestamp header "DateTime_UTC" not in passed'
              'dataframe. Please save processed dataframe with timestamp index'
              'header named "DateTime_UTC"')
    return df
