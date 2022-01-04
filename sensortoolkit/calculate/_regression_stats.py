# -*- coding: utf-8 -*-
"""
This module computes statistical metrics for the Ordinary Least Squares linear
regression between sensor and FRM/FEM datasets (FRM/FEM as the dependent
variable along the x-axis and sensor data as the independent variable along
the y-axis).

Bias and linearity
------------------

U.S. EPA's Performance Targets Reports recommend using a linear regression
model, relating sensor and FRM/FEM measurements, to determine the magnitude
of bias and linearity. The regression model takes the form

.. math::

    y = mx + b

where

    :math:`y` = sensor measurements

    :math:`x` = FRM/FEM measurements

    :math:`m` = regression slope

    :math:`y` = regression intercept


The slope :math:`m` and intercept :math:`y` indicate the degree of systematic
bias between sensor and reference measurements.

Linearity is measured via the coefficient of determination (:math:`R^2`).

===============================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Tue Mar 3 13:47:32 2020
Last Updated:
  Tue Jul 13 11:09:13 2021
"""
import os
import sys
import numpy as np
import pandas as pd
from sensortoolkit.datetime_utils import get_todays_date
from sensortoolkit.lib_utils import check_type


def regression_stats(sensor_df_obj, ref_df_obj, deploy_dict, param, serials,
                     verbose=True):
    """Compute OLS regression statistics.

    Module is used to compute the following regressions:

    - Sensor vs. FRM/FEM
    - Sensor vs. Inter-sensor average

    For each instance, the dependent and independent variables are assigned as
    **hourly/daily sensor data vs. hourly/daily reference data**; please note
    the ``ref_df_obj`` object can be either a DataFrame containg FRM/FEM
    concentratons, or a DataFrame containing intersensor averages depending on
    the use case. The 'ref' label refers moreso to the fact that the dataset is
    used as the independent variable for regressions.

    .. note::

      The DataFrames within the ``sensor_df_obj`` and ``ref_df_obj`` arguments
      should contain data reported at the same sampling frequency (e.g., if a
      sensor DataFrame containing data at 1-hour averaged intervals is passed
      to the ``sensor_df_obj``, the reference DataFrame passed to
      ``ref_df_obj`` must also contain data at 1-hour averaged intervals).

    Args:
        sensor_df_obj (pandas DataFrame or list of pandas DataFrames):
            Either a DataFrame or list of DataFrames containg sensor parameter
            measurements. Data corresponding to passed parameter name are used
            as the dependent variable.
        ref_df_obj (pandas DataFrame):
            Reference DataFrame (either FRM/FEM OR Inter-sensor averages). Data
            corresponding to passed parameter name are used as the independent
            variable.
        deploy_dict (dict):
            A dictionary containing descriptive statistics and
            textual information about the deployment (testing agency, site,
            time period, etc.), sensors tested, and site conditions during the
            evaluation.
        param (str):
            Parameter name for which to compute regression statistics.
        serials (dict):
            A dictionary of sensor serial identifiers for each unit
            in a testing group.
        verbose (bool):
            If true, print statements will be displayed in the console output.
            Defaults to True.

    Returns:
        stats_df (pandas DataFrame):
            Statistics DataFrame for either sensor vs. FRM/FEM or sensor vs.
            intersensor mean OLS regression.

    """

    stats_cols = ['Sensor Name', 'Sensor_Number', 'Sensor_Serial',
                  'Averaging Interval', 'Param', 'Reference', 'R$^2$',
                  'Slope', 'Intercept', 'Sensor RMSE', 'N', 'Sensor_Min',
                  'Sensor_Max', 'Sensor_Mean']

    stats_df = pd.DataFrame(columns=stats_cols)

    sensor_name = deploy_dict['Sensor Name']
    sensor_nums = list(serials.keys())

    sensor_dtype = check_type(sensor_df_obj,
                             accept_types=[pd.core.frame.DataFrame, list])
    check_type(ref_df_obj, accept_types=[pd.core.frame.DataFrame])

    if sensor_dtype is pd.core.frame.DataFrame:
        df_list = [sensor_df_obj]
    if sensor_dtype is list:
        df_list = sensor_df_obj

    # Loop over dataframes for sensors, compute regression stats
    for i, (df, sensor_num) in enumerate(zip(df_list, sensor_nums)):

        ydata = df[param + '_Value']
        if 'mean_' + param + '_Value' in ref_df_obj:
            xdata = ref_df_obj['mean_' + param + '_Value']
            ref_name = 'Intersensor_mean_' + param
        else:
            xdata = ref_df_obj[param + '_Value']
            ref_name = ''.join(
                        list(ref_df_obj[param + '_Method'].dropna().apply(
                                        lambda x: str(x)).unique()[0]))

        # Locate the union of non-nan sensor (y) and reference (x) data
        # False if either is nan and true if both are finite
        # idx = np.isfinite(xdata) & np.isfinite(ydata)

        # X = pd.Series(xdata)
        # Y = pd.Series(ydata)

        combine_df = pd.DataFrame()
        combine_df['ref_data'] = xdata
        combine_df['sensor_data'] = ydata
        combine_df = combine_df.dropna()


        # Determine the averaging interval for the supplied dataset
        if (df.index[1] - df.index[0]) == pd.Timedelta('1 days'):
            avg_int = '24-hour'
        if (df.index[1] - df.index[0]) == pd.Timedelta('1 hour'):
            avg_int = '1-hour'

        if i == 0 and verbose:
            print('Computing {0} regression statistics for {1} vs.'
                  ' {2}'.format(avg_int, sensor_name, ref_name))

        if verbose:
            print('..{0}'.format(list(serials.values())[i]))

        if combine_df.empty:
            print('..Warning: Linear regression not possible for sensor '
                  + str(sensor_num) + '. Sensor or reference data are '
                  'null.')
            r_square = slope = intercept = rmse = N = np.nan
            param_min = param_max = param_mean = np.nan
        else:
            N = int(len(combine_df))

            if N <= 2:
                print('..Warning: Linear regression not possible for' +
                      ' sensor ' + str(sensor_num) +
                      '. Insufficient number of data points')
                r_square = slope = intercept = rmse = N = np.nan
                param_min = param_max = param_mean = np.nan

            else:
                # Compute linear regress. for the union of finite x and y data
                fit = np.polyfit(combine_df.ref_data, combine_df.sensor_data, 1)
                slope = fit[0]
                intercept = fit[1]
                pearson_coeff = combine_df.ref_data.corr(combine_df.sensor_data, method='pearson')
                r_square = pearson_coeff*pearson_coeff

                sensor_val = combine_df.sensor_data
                ref_val = combine_df.ref_data
                MSE = (1/N)*sum((sensor_val-ref_val)**2)
                rmse = np.sqrt(MSE)

                param_min = combine_df.sensor_data.min()
                param_max = combine_df.sensor_data.max()
                param_mean = combine_df.sensor_data.mean()

        serial_id = serials[str(sensor_num)]

        row_df = pd.DataFrame([sensor_name,
                               sensor_num,
                               serial_id,
                               avg_int,
                               param,
                               ref_name,
                               r_square,
                               slope,
                               intercept,
                               rmse,
                               N,
                               param_min,
                               param_max,
                               param_mean])

        row_df.index = stats_df.columns
        row_df = row_df.T

        stats_df = pd.concat([stats_df, row_df]).reset_index(drop=True)

    # Add metric averages if multiple sensor datasets passed to function
    if sensor_dtype is list:
        metric_list = ['R$^2$', 'Slope', 'Intercept', 'Sensor RMSE',
                       'N', 'Sensor_Min', 'Sensor_Max', 'Sensor_Mean']
        avg_data = stats_df.where(stats_df['Averaging Interval'] == avg_int
                                  ).dropna(how='all', axis=0)

        avg_df = pd.DataFrame(np.nan, columns=stats_cols, index=[0])
        avg_df['Reference'] = 'Metric Average:'

        for col_i, metric in enumerate(metric_list, 6):
            metric_data = avg_data.iloc[:, col_i]
            metric_mean = metric_data.mean()
            avg_df.iloc[0, col_i] = metric_mean

        stats_df = pd.concat([stats_df, avg_df]).reset_index(drop=True)

        stats_df[stats_df.columns[6:]] = stats_df[stats_df.columns[6:]
                                                  ].astype('float64')

    return stats_df


def join_stats(hourly_stats, daily_stats, write_to_file=False, stats_path=None,
               stats_type='individual'):
    """Combine 1-hour and 24-hour regression statistics DataFrames.

    Args:
        hourly_stats (pandas DataFrame):
            DataFrame containing 1-hour averaged
            sensor vs. reference regression statistics, returned by call to
            regression_stats().
        daily_stats (pandas DataFrame):
            DataFrame containing 24-hour averaged
            sensor vs. reference regression statistics, returned by call to
            regression_stats().
        write_to_file (bool, optional):
            If True, the merged statistics dataframe will be written to a csv
            file. Defaults to False.
        stats_path (str, optional):
            The full path to the statistics directory where the dataset will be
            saved if ``write_to_file`` is True. Defaults to None.
        stats_type (str, optional):
            The type of regression statistics dataframes that are being joined
            ('individual' indicates individual sensor vs. reference
            regression, 'average' indicates sensor vs. intersensor average
            regression statistics)

    Returns:
        stats_df (pandas DataFrame):
            DataFrame containing both 1-hour and 24-hour averaged statistics.

    """
    if stats_type not in ['average', 'individual']:
        raise ValueError(f'Invalid value {stats_type} passed to stats_type. '
                         'Choose from either "individual" or "average"')

    if stats_type == 'individual':
        stats_type = 'stats_df'
    if stats_type == 'average':
        stats_type = 'avg_stats_df'

    stats_df = hourly_stats.append(daily_stats)

    ref_name = stats_df.Reference[stats_df.Reference != 'Metric Average:'
                                  ].value_counts().keys()[0]
    sensor_name = stats_df['Sensor Name'].value_counts().keys()[0]
    param = stats_df['Param'].value_counts().keys()[0]

    # Save the statistics DataFrame
    if write_to_file is True:
        if stats_path is None:
            sys.exit('No directory path specified for saving DataFrame')

        today = get_todays_date()
        ref_name = ref_name.replace(' ', '_')

        filename = '_'.join([sensor_name, param, 'vs', ref_name, stats_type,
                             today])
        filename += '.csv'

        dataframe_to_csv(stats_df,
                         parent_path=stats_path,
                         filename=filename)

    return stats_df


def dataframe_to_csv(obj, parent_path, filename, **kwargs):
    """Save a pandas DataFrame to a comma-separated value file.

    Args:
        obj (pandas DataFrame): The DataFrame to write to a .csv file.
        parent_path (str): The path to the folder where the file will be saved.
        filename (str): The name of the resulting .csv file.
        **kwargs (dict): Keyword arguments passed to the pandas ``to_csv()``
            method.

    Returns:
        None.

    """
    check_type(obj, accept_types=[pd.core.frame.DataFrame])
    filepath = os.path.join(parent_path, filename)
    print('..Saving dataset to the following path: {0}'.format(filepath))
    obj.to_csv(filepath, index=kwargs.get('index', False))
