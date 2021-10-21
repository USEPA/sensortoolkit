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


def regression_stats(sensor_df_obj, ref_df_obj, deploy_dict, param, serials):
    """Compute OLS regression statistics.

    Module is used to compute the following regressions:
        Sensor vs. FRM/FEM
        Sensor vs. Inter-sensor average

    For each instance, the dependent and independent variables are assigned as
    {hourly/daily_df_obj vs. hourly/daily_ref_df}; please note that the
    '..ref_df' object can be either a dataframe containg FRM/FEM concentratons,
    or a dataframe containing intersensor averages depending on the use case.
    The 'ref' label refers moreso to the fact that the dataset is used as the
    independent variable for regressions.

    If sensor and reference dataframes are passed at both hourly and daily
    averaging intervals (i.e., hourly_df_obj, daily_df_obj, hourly_ref_df,
    daily_ref_df), regression statistics will be computed for both averaging
    intervals (looping over hourly and then daily regressions) and are returned
    in the same statistics dataframe.

    Args:
        hourly_df_obj (pandas dataframe object):
            Sensor dataframe at 1-hour averaged intervals. Data corresponding
            to passed parameter name are used as the dependent variable.
        daily_df_obj (pandas dataframe object):
            Sensor dataframe at 24-hour averaged intervals. Data corresponding
            to passed parameter name are used as the dependent variable.
        hourly_ref_df (pandas dataframe object):
            Reference dataframe (either FRM/FEM OR Inter-sensor averages) at
            1-hour averaged intervals. Data corresponding to passed parameter
            name are used as the independent variable.
        daily_ref_df (pandas dataframe object):
            Reference dataframe (either FRM/FEM OR Inter-sensor averages) at
            24-hour averaged intervals. Data corresponding to passed parameter
            name are used as the independent variable.
        deploy_dict (dict):
            A dictionary containing descriptive statistics and
            textual information about the deployment (testing agency, site,
            time period, etc.), sensors tested, and site conditions during the
            evaluation.
        param (str):
            Parameter name for which to compute regression statistics.
        sensor_name (str):
            The make and model of the sensor being evaluated.
        ref_name (str):
            The name of the dataset assigned as the independent variable. This
            may either be FRM/FEM concentrations in the case of sensor vs.
            FRM/FEM regression, or it may be the inter-sensor average in the
            case of sensor vs. inter-sensor average regression statistics.
        serials (dict):
            A dictionary of sensor serial identifiers for each unit
            in a testing group.
        path (str):
            The full directory path to evaluation statistics for a
            given sensor make and model.
        write_to_file (str):
            If true, the statistics dataframe will be saved to the path
            location.

    Returns:
        stats_df: (pandas dataframe)
            Statistics dataframe for either sensor vs. FRM/FEM or sensor vs.
            intersensor mean OLS regression. Results are organized by averaging
            interval if both 1-hour and 24-hour averaged datasets passed to
            module.
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
        idx = np.isfinite(xdata) & np.isfinite(ydata)

        X = pd.Series(xdata)
        Y = pd.Series(ydata)

        combine_df = pd.DataFrame()
        combine_df['ref_data'] = xdata
        combine_df['sensor_data'] = ydata
        combine_df = combine_df.dropna()

        # Determine the averaging interval for the supplied dataset
        if (df.index[1] - df.index[0]) == pd.Timedelta('1 days'):
            avg_int = '24-hour'
        if (df.index[1] - df.index[0]) == pd.Timedelta('1 hour'):
            avg_int = '1-hour'

        if i == 0:
            print('Computing {0} regression statistics for {1} vs.'
                  ' {2}'.format(avg_int, sensor_name, ref_name))

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
                fit = np.polyfit(xdata[idx], ydata[idx], 1)
                slope = fit[0]
                intercept = fit[1]
                pearson_coeff = X.corr(Y, method='pearson')
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


def join_stats(hourly_stats, daily_stats, write_to_file=False, stats_path=None):

    stats_df = hourly_stats.append(daily_stats)

    ref_name = stats_df.Reference[stats_df.Reference!='Metric Average:'
                                  ].value_counts().keys()[0]
    sensor_name =  stats_df['Sensor Name'].value_counts().keys()[0]
    param =  stats_df['Param'].value_counts().keys()[0]

    # Save the statistics dataframe
    if write_to_file is True:
        if stats_path is None:
            sys.exit('No directory path specified for saving dataframe')

        today = get_todays_date()
        ref_name = ref_name.replace(' ', '_')
        filename = (sensor_name + '_' + param + '_vs_' + ref_name +
                    '_stats_df_' + today + '.csv')

        dataframe_to_csv(stats_df,
                         parent_path=stats_path,
                         filename=filename)

    return stats_df


def check_type(obj, accept_types):

    obj_type = type(obj)

    if obj_type not in accept_types:
        raise TypeError('Invalid object type. Received '
                        'type {0} but expected one of the following '
                        'types: {1}'.format(obj_type, accept_types))
    return obj_type


def dataframe_to_csv(obj, parent_path, filename, **kwargs):
    check_type(obj, accept_types=[pd.core.frame.DataFrame])
    filepath = os.path.join(parent_path, filename)
    print('..Saving dataset to the following path: {0}'.format(filepath))
    obj.to_csv(filepath, index=kwargs.get('index', False))
