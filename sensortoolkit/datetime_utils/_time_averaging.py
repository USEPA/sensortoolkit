# -*- coding: utf-8 -*-
"""
This module calculates 1-hour and 24-hour averaged datasets from sensor and
FRM/FEM recorded datasets.

U.S. EPA's Performance Targets Reports stipulate that a 75% data completeness
requirement for each averaging interval should be imposed. For example, a
:math:`PM_{2.5}` sensor recording concentration measurements every hour would
require a minimum of 18 valid measurements in order to calculate a valid
24-hour averaged concentration [i.e., (18/24) * 100% = 75%].

U.S. EPA's Performance Targets Reports calculate averages as

.. math::

    x_{kpj} = \\frac{1}{n}\\sum_{i=1}^{n}c_{ij}

where:

    :math:`x_{kpj}` = 1-hour or 24-hour averaged measurement k for hour/day p
    and instrument j

    :math:`n` = number of instrument measurements per averaging interval

    :math:`c_{ij}` = measurement from instrument j for time i of the averaging
    interval

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Oct 21 14:46:27 2020
Last Updated:
  Tue Jul 13 16:32:44 2021
"""
import os
import pandas as pd
import numpy as np
from sensortoolkit.qc._duplicate_removal import remove_duplicates


def sensor_averaging(full_df_list, sensor_serials=None, name='',
                     write_to_file=True, path=None, **kwargs):
    """Write full (recorded), hourly, and daily averaged datasets to csv.

    Wrapper function for computing hourly and daily averaged DataFrames.

    Args:
        full_df_list (list):
            List of sensor DataFrames at original recorded sampling frequency.
        sensor_serials (dict):
            A dictionary of unique serial identifiers for each sensor in the
            testing group.
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

    **Keyword Arguments:**

    :param float threshold:
        The completeness threshold for averaging datasets to 1-hour or
        24-hour intervals. Defaults to 75% (``0.75``).

    Returns:
        (tuple): Two-element tuple containing:

            - **hourly_df_list** (*list of pandas DataFrames*): List of sensor
              data frames of length N (where N is the number of sensor units in
              a testing group). frames indexed by DateTime at 1-hour averaged
              sampling frequency.
            - **daily_df_list** (*list of pandas DataFrames*): List of sensor
              data frames of length N (where N is the number of sensor units in
              a testing group). frames indexed by DateTime at 24-hour averaged
              sampling frequency.

    """
    print('Averaging datasets to 1-hour and 24-hour intervals:')
    data_dict = {'full': {},
                 '1-hour': {},
                 '24-hour': {}}

    if sensor_serials is None:
        n_sensors = len(full_df_list)
        sensor_serials = {i: 'Sensor '+str(i) for i in
                          np.linspace(1, n_sensors, n_sensors, dtype=int)}

    # Loop over each recorded sensor dataset and compute hourly, daily averages
    for i, (full_df, sensor_n) in enumerate(zip(full_df_list, sensor_serials)):
        serial_id = sensor_serials[sensor_n]

        for interval in data_dict:
            data_dict[interval][serial_id] = None

        full_df = remove_duplicates(full_df,
                                    agg_numeric_by='mean',
                                    agg_object_by='first',
                                    print_indent=2)

        # Compute timedelta between successive timestamps
        delta = (full_df.index[1:] - full_df.index[0:-1]).to_frame()
        if delta.index.name is None:
            delta.index.name = 'DateTime'
        idx_name = delta.index.name

        # Use mode of timedelta to extrapolate # of datapoints recorded per hr
        time_delta = delta[idx_name].mode()[0]
        hr_count = pd.to_timedelta(1, unit='H') / time_delta
        day_count = pd.to_timedelta(1, unit='D') / time_delta

        # Use a 75% threshold
        hr_thres = kwargs.get('threshold', 0.75)
        day_thres = kwargs.get('threshold', 0.75)

        # Print the mode of the sampling interval for recorded sensor data and
        # the number of counts within each hour interval.
        print('..{0:s} recording interval mode: {1:s}, '
              '{2:4.1f} counts per hour'.format(serial_id,
                                                str(time_delta),
                                                hr_count,))

        hourly_df = interval_averaging(full_df,
                                       freq='H',
                                       interval_count=hr_count,
                                       thres=hr_thres)

        if full_df.attrs != {} and hourly_df.attrs == {}:
            hourly_df.attrs = full_df.attrs

        daily_df = interval_averaging(full_df,
                                      freq='D',
                                      interval_count=day_count,
                                      thres=day_thres)

        if full_df.attrs != {} and daily_df.attrs == {}:
            daily_df.attrs = full_df.attrs

        data_dict['full'][serial_id] = full_df
        data_dict['1-hour'][serial_id] = hourly_df
        data_dict['24-hour'][serial_id] = daily_df

        if write_to_file is True:
            print('....writing full, hourly, and daily datasets to .csv files')

            # check if sensor-specific subfolder exists
            if not os.path.exists(path):
                os.makedirs(path)

            # Add ISO8601 formatting. Not sure if copy of datasets are needed,
            # but applying in case applying directly to original versions would
            # modify datasets in place (converting to ISO8601 changes the
            # data type of the index from datetime64 to object, so modifying
            # original may cause issues when trying to utilize index in
            # date/time fashion).
            full_cp = full_df.copy()
            full_cp.index = full_cp.index.to_series().apply(
                                        pd.Timestamp.isoformat)

            hourly_cp = hourly_df.copy()
            hourly_cp.index = hourly_cp.index.to_series().apply(
                                            pd.Timestamp.isoformat)

            daily_cp = daily_df.copy()
            daily_cp.index = daily_cp.index.to_series().apply(
                                            pd.Timestamp.isoformat)

            full_cp.to_csv(path + name + '_' + serial_id + '_full.csv')
            hourly_cp.to_csv(path + name + '_' + serial_id + '_hourly.csv')
            daily_cp.to_csv(path + name + '_' + serial_id + '_daily.csv')

    return data_dict


def interval_averaging(df, freq='H', interval_count=60, thres=0.75):
    """Average DataFrame to the specified sampling frequency ('freq').

    Numeric columns are averaged for for each interval and a completeness
    threshold (default 75%) must be met, otherwise averages are null. Columns
    of type 'object' (i.e. text) are aggregated within each interval by the
    mode of unique object values.

    Args:
        df (pandas DataFrame or pandas Series):
            Dataframe or Series for which averages will be computed.
        freq (str):
            The frequency (averaging interval) to which the DataFrame will
            be averaged. Defaults to ``H``. Pandas refers to these as
            'offset aliases', and a list is found here
            (https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases).
        interval_count (int):
            The number of datapoints expected within the passed DataFrame for
            the specified averaging interval ('freq'). Defaults to 60 for
            1-hour averages. E.g., if computing 1-hour averages (freq='H') an
            the passed DataFrame is for a sensor that recorded measurements at
            1-minute sampling frequency, interval_count will equal 60 (expect
            60 non-null data points per averaging interval).
        thres (float):
            Threshold (ranging from 0 to 1) for ratio of the number of
            data points recorded within a given averaging interval vs. the
            number of expected data points. Defaults to ``0.75`` (i.e., 75%).

    Return:
        avg_df (pandas DataFrame):
            Dataframe averaged to datetimeindex interval specified by 'freq'.

    """
    n_thres = interval_count*thres

    # If Series object passed, convert to DataFrame
    data_type = type(df)
    if data_type is not pd.core.frame.DataFrame:
        df = pd.Series(df).to_frame()

    # List of unique column names with the column order preserved
    col_list = list(dict.fromkeys(df.columns))

    # Split DataFrame in to object-like columns and numeric-like columns
    obj_df = df.select_dtypes(include=['object', 'datetime'])
    num_df = df.select_dtypes(exclude=['object', 'datetime'])

    # Merge object columns by using the instance in the first non-null instance
    obj_df = column_merger(obj_df, by='first')
    # Merge numeric columns with same name by mean
    num_df = column_merger(num_df, by='mean')

    num_df_cols = list(num_df.columns)
    obj_df_cols = list(obj_df.columns)

    num_df = num_df.dropna(axis=1, how='all')

    # index at specified interval for empty DataFrames (all NaNs)
    nan_df_idx = pd.date_range(start=obj_df.index[0],
                               end=obj_df.index[-1],
                               freq=freq, normalize=True)

    # Sample object-like data at specified interval by the mode
    obj_df = obj_df.dropna(how='all', axis=1).fillna('')

    if obj_df.empty:
        avg_obj_df = pd.DataFrame(np.nan, index=nan_df_idx,
                                  columns=obj_df_cols)
    else:
        avg_obj_df = obj_df.groupby([pd.Grouper(freq=freq)]
                            ).agg(lambda x: object_grouper(x, n_thres))

    dropped_objcols = [col for col in obj_df_cols if col not in avg_obj_df]
    for col in dropped_objcols:
        avg_obj_df[col] = np.nan

    if num_df.empty:
        avg_num_df = pd.DataFrame(np.nan, index=nan_df_idx,
                                  columns=num_df_cols)
    else:

        # Mean param values for each averaging interval
        mean_df = num_df[:].groupby(
                            [pd.Grouper(freq=freq)]).mean()

        # Counts for each param and each averaging interval
        counts_df = num_df[:].groupby(
                            [pd.Grouper(freq=freq)]).count().add_suffix(
                                                            '_count' + freq)

        avg_num_df = mean_df.join(counts_df).sort_index(axis=1)

        # List of columns containing count for each averaging interval
        count_list = list(avg_num_df.columns[[col.endswith('count' + freq)
                                              for col in avg_num_df.columns]])

        # Set null param vals for averaging intervals below completeness thres
        for col in count_list:
            mean_col = col.replace('_count' + freq, '')

            avg_num_df[mean_col] = avg_num_df[mean_col].where(
                                        avg_num_df[col] > n_thres, np.nan)

    # Rejoin non-numeric columns on averaging interval
    avg_df = avg_num_df.join(avg_obj_df)

    # Ensure that any columns with all NaNs in passed df are in avg_df
    # (Numeric type columns that were dropped)
    dropped_numcols = [col for col in col_list if col not in avg_df.columns]
    for col in dropped_numcols:
        avg_df[col] = np.nan

    # reorder columns before return
    avg_df = avg_df[col_list]

    return avg_df


def object_grouper(series, number_threshold):
    """Group columns of type `object` by the mode of values within each
    averaging interval.

    Args:
        series (pandas Series):
            An array of values with type object (typically textual information)
            alongside an associated datetime index.
        number_threshold (int or float):
            The number of counts for the modal value within a given averaging
            interval required to assign the modal value to the averaging
            interval. This can be expressed as a completeness threshold
            (typically 70%) multiplied by the number of expected counts
            within a given averaging interval.

    Returns:
        val (str or numpy.nan):
            The mode of the object-type series within the specified averaging
            interval. If the number of counts for the modal value is less than
            the number threshold (70% x expected counts within an averaging
            interval), return numpy.nan (null).

    """
    try:
        counts = series.value_counts().values[0]
        if counts >= number_threshold:
            val = series.value_counts().index[0]
        else:
            val = np.nan
    except IndexError:
        val = np.nan
    return val


def column_merger(df, by='first'):
    """Group duplicated column names if detected in passed dataset.


    Args:
        df (pandas DataFrame):
            Dataset containing columns with the same name.
        by (str, optional):
            Method for how to keep entries from duplicated columns. Either
            ``'first'`` (keep the first non-null entries, good for
            columns of dtype object - i.e., strings) or ``'mean'`` (compute
            the mean of entries for duplicated columns (good for numeric type
            columns). Defaults to 'first'.

    Returns:
        df (pandas DataFrame):
            Modified dataset with duplicated column entries merged.

    """

    col_counts = {col: list(df.columns).count(col) for col in df.columns
                  if list(df.columns).count(col) > 1}

    if col_counts != {}:
        print('....duplicate column names found in dataset:')
        for col_name, occurrences in col_counts.items():
            print(f'......column name: "{col_name}", occurrences: {occurrences}')
        if by == 'first':
            grouped_df = df.groupby(level=0, axis=1).first()
        if by == 'mean':
            grouped_df = df.groupby(level=0, axis=1).mean()

        print(f'....duplicate column occurrences grouped by {by}')

        df = grouped_df

    return df
