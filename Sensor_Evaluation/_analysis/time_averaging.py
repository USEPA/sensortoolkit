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
  Wed Oct 21 14:46:27 2020
Last Updated:
  Tue Jul 13 16:32:44 2021
"""
import pandas as pd
import numpy as np
import os


def Sensor_Averaging(full_df_list, sensor_serials=None, name='',
                     write_to_file=True, path=None,):
    """Wrapper function for computing hourly and daily averaged dataframes,
    writes full (recorded), hourly, and daily averaged datasets to .csv files.

    Args:
        full_df_list (list):
            List of sensor dataframes at original recorded sampling frequency.
        sensor_serials (dict):
        name (str):
            The make and model of the sensor being evaluated.
        write_to_file (bool):
            If true, datasets will be written to the path for data at original
            recorded sampling frequency (files ending in '_full.csv'), 1-hour
            averaged datasets (files ending in '_hourly.csv'), and 24-hour
            averaged datasets (files ending in '_daily.csv').
        path (str):
            The full directory path to processed sensor data for a given sensor
            make and model.
    Returns:
        hourly_df_list (list of pandas dataframes): List of sensor data frames
            of length N (where N is the number of sensor units in a testing
            group). frames indexed by DateTime_UTC at 1-hour averaged sampling
            frequency.
        daily_df_list (list of pandas dataframes): List of sensor data frames
            of length N (where N is the number of sensor units in a testing
            group). frames indexed by DateTime_UTC at 24-hour averaged sampling
            frequency.
    """
    hourly_df_list, daily_df_list = [], []

    if sensor_serials is None:
        n_sensors = len(full_df_list)
        sensor_serials = {i: 'Sensor '+str(i) for i in
                          np.linspace(1, n_sensors, n_sensors, dtype=int)}

    # Loop over each recorded sensor dataset and compute hourly, daily averages
    for full_df, sensor_n in zip(full_df_list, sensor_serials):
        serial_id = sensor_serials[sensor_n]

        # Compute timedelta between successive timestamps
        delta = (full_df.index[1:] - full_df.index[0:-1]).to_frame()
        if delta.index.name is None:
            delta.index.name = 'DateTime'
        idx_name = delta.index.name

        # Use mode of timedelta to extrapolate # of datapoints recorded per hr
        time_delta = delta[idx_name].mode()[0]
        hr_count = pd.to_timedelta(1, unit='h') / time_delta

        if hr_count <= 4:
            # Use a 75% threshold for recording intervals of 15-min or longer
            hr_thres = 0.75
        else:
            # 90% completeness threshold for 1-hour averages
            hr_thres = 0.75

        # Print the mode of the sampling interval for recorded sensor data and
        # the number of counts within each hour interval.
        print('..{0:s} recording interval mode: {1:s}, '
              '{2:4.1f} counts per hour'.format(serial_id,
                                                str(time_delta),
                                                hr_count,))

        hourly_df = Interval_Averaging(full_df,
                                       freq='H',
                                       interval_count=hr_count,
                                       thres=hr_thres,
                                       return_counts=False)

        hourly_df_list.append(hourly_df)

        day_count = 24
        day_thres = 0.75  # 75% completeness threshold for daily averages

        daily_df = Interval_Averaging(hourly_df,
                                      freq='D',
                                      interval_count=day_count,
                                      thres=day_thres,
                                      return_counts=False)

        daily_df_list.append(daily_df)

        if write_to_file is True:
            print('....writing full, hourly, and daily datasets to .csv files')

            # check if sensor-specific subfolder exists
            if not os.path.exists(path):
                os.makedirs(path)

            full_df.to_csv(path + name + '_' + serial_id + '_full.csv')
            hourly_df.to_csv(path + name + '_' + serial_id + '_hourly.csv')
            daily_df.to_csv(path + name + '_' + serial_id + '_daily.csv')

    return hourly_df_list, daily_df_list


def Interval_Averaging(df, freq='H', interval_count=60, thres=0.75,
                       return_counts=False):
    """Average dataframe to the specified sampling frequency ('freq').

    Numeric columns are averaged for for each interval and a completeness
    threshold (default 75%) must be met, otherwise averages are null. Columns
    of type 'object' (i.e. text) are aggregated within each interval by the
    mode of unique object values.

    Args:
        df (pandas dataframe):
            Dataframe with datetimeindex
        freq (str):
            The frequency (averaging interval) to which the dataframe will
            be averaged. Pandas refers to these as 'offset aliases', and a list
            is found at the following link:
                https://pandas.pydata.org/pandas-docs/stable/user_guide/
                timeseries.html#offset-aliases
        interval_count (int):
            The number of datapoints expected within the passed dataframe for
            the specified averaging interval ('freq'). E.g., if computing
            1-hour averages (freq='H') and the passed dataframe is for a sensor
            that recorded measurements at 1-minute sampling frequency,
            interval_count will equal 60 (expect 60 non-null data points per
            averaging interval).
        thres (float):
            Threshold (ranging from 0 to 1) for ratio of the number of
            data points recorded within a given averaging interval vs. the
            number of expected data points. For example, if a sensor has a
            sampling frequency of 1-minute per data point and
        return_counts (bool):

    Return:
        averaged_df (pandas dataframe):
            Dataframe averaged to datetimeindex interval specified by 'freq'.
    """

    # Split dataframe in to object-like columns and numeric-like columns
    obj_df = df.select_dtypes(include=['object', 'datetime'])
    num_df = df.select_dtypes(exclude=['object', 'datetime'])

    obj_df_cols = list(obj_df.columns)
    num_df_cols = list(num_df.columns)

    num_df = num_df.dropna(axis=1, how='all')

    # index at specified interval for empty dataframes (all NaNs)
    nan_df_idx = pd.date_range(start=obj_df.index[0],
                               end=obj_df.index[-1],
                               freq=freq, normalize=True)

    # Sample object-like data at specified interval by the mode
    try:
        averaged_obj_df = obj_df.groupby(
                        [pd.Grouper(freq=freq)]).agg(pd.Series.mode)
    except Exception:
        # Dataframe is full of NaNs
        averaged_obj_df = pd.DataFrame(np.nan, index=nan_df_idx,
                                       columns=obj_df_cols)

    if num_df.empty:
        averaged_num_df = pd.DataFrame(np.nan, index=nan_df_idx,
                                       columns=num_df_cols)
    else:

        # Mean param values for each averaging interval
        mean_df = num_df[:].groupby(
                            [pd.Grouper(freq=freq)]).mean()

        # Counts for each param and each averaging interval
        counts_df = num_df[:].groupby(
                        [pd.Grouper(freq=freq)]).count().add_suffix(
                                                            '_count' + freq)

        averaged_num_df = mean_df.join(counts_df).sort_index(axis=1)

        # List of columns containing count for each averaging interval
        count_list = list(averaged_num_df.columns[
                        [col.endswith('count' + freq) for col in
                         averaged_num_df.columns]])

        n_thres = interval_count*thres

        # Set null param vals for averaging intervals below completeness thres
        for col in count_list:
            mean_col = col.replace('_count' + freq, '')

            averaged_num_df[mean_col] = averaged_num_df[mean_col].where(
                                        averaged_num_df[col] > n_thres, np.nan)

        if return_counts is False:
            averaged_num_df = averaged_num_df.drop(columns=count_list)

    # Rejoin non-numeric columns on averaging interval
    averaged_df = averaged_num_df.join(averaged_obj_df)

    return averaged_df
