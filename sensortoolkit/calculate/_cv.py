# -*- coding: utf-8 -*-
"""
This module computes the coefficient of variation (CV), a measure of precision,
for collocated sensors recording data concurrently.

.. note::

    CV as defined by U.S. EPA's Performance Targets Reports is measured for
    periods where all sensors in the evaluation group are measuring
    concurrently.

    For example, if three sensors are included in a deployment group,
    the CV will only be calculated for periods where all three sensors are operating
    normally and recording values simultaneously.

U.S. EPA's Performance Targets Reports calculate CV as

.. math::

    CV = \\frac{SD}{\\bar{x}}\\times 100

where :math:`\\bar{x}` is the deployment averaged sensor concentration for a
field test, and :math:`SD`, the standard deviation, is defined as

.. math::

    SD = \\sqrt{\\frac{1}{(N\\times M)-1}\\sum_{j=1}^{M}\\left[
    \\sum_{i=1}^{N}(x_{ij} - \\bar{x_i})^2\\right]}

and where:

    :math:`M` = number of identical sensors operated simultaneously during a
    field test

    :math:`N` = number of measurement intervals during which all identical
    instruments are operating and returning valid averages over the duration of
    the field test

    :math:`x_{ij}` = Sensor concentration for measurement interval :math:`i` and
    sensor unit :math:`j`.

    :math:`\\bar{x_i}` = Intersensor average sensor concentration for
    measurement interval :math:`i`. **All sensor units deployed for testing**
    **must have recorded non-null values for measurement interval** :math:`i`
    **to compute** :math:`\\bar{x_i}`.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Jan 29 10:03:27 2020
Last Updated:
  Tue Jul 13 09:21:40 2021
"""
import numpy as np
import pandas as pd
from sensortoolkit.datetime_utils import deploy_timestamp_index


def _calculate_cv(cv_df, sensor_numbers, param):
    """Compute CV for a group of collocated, concurrently recording sensors.

    Args:
        cv_df (pandas dataframe):
            Dataframe with parameter concentration values, used to
            calculate CV. Only rows (unique timestamps) are kept where all
            deployment group sensors are concurrently recording for calculating
            CV.
        sensor_numbers
            serial identifiers for sensors in the deployment group.
        param (str):
            Parameter name to evaluate

    Returns:
        (tuple): four-element tuple containing:

            - cv_df (pandas DataFrame): Modified cv_df, dropped rows were not
              all sensors measuring concurrently, add columns for computing CV.
            - CV (float): The coefficient of variation of concurrent sensor
              measurements. Calculated as the 100*(standard deviation / mean of
              all concurrent sensor measurements).
            - st_dev (float): The standard deviation of concurrent sensor
              measurements.
            - n_concurr (int): Number of concurrent hours with all sensors
              reporting pollutant values.

    """
    if cv_df.index[1] - cv_df.index[0] == pd.Timedelta('0 days 01:00:00'):
        time_interval = "1-Hour"
    elif cv_df.index[1] - cv_df.index[0] == pd.Timedelta('1 days 00:00:00'):
        time_interval = "24-Hour"

    print("Computing CV for " + time_interval + " averaged " + param)

    cv_df[param + '_sensor_mean'] = cv_df.mean(axis=1)

    for sensor_number in sensor_numbers:
        cv_df[str(sensor_number)+'_val-avg_val_sqrd'] = \
            (cv_df[str(sensor_number)+'_' + param] -
             cv_df[param + '_sensor_mean'])**2

    sum_sqrd_diff = 0
    total_n_vals = 0
    pollutant_avg = 0

    before_drop_n = len(cv_df)
    cv_df = cv_df.dropna(axis=1, how='all')  # drop empty columns
    cv_df = cv_df.dropna(how='any')  # drop rows with any missing data values
    after_drop_n = len(cv_df)
    n_excluded = before_drop_n - after_drop_n

    print("..N excluded:", n_excluded, "out of", before_drop_n, "total")
    print("..N concurrent:", after_drop_n)
    print("..Concurrent measurement timeframe:", cv_df.index[0], '-',
          cv_df.index[-1])

    n_sensors = 0
    for sensor_n in sensor_numbers:
        try:
            sum_sqrd_diff += cv_df[str(sensor_n)+'_val-avg_val_sqrd'].sum()
            total_n_vals += cv_df[str(sensor_n)+'_val-avg_val_sqrd'].count()
            pollutant_avg += cv_df[str(sensor_n)+'_' + param].mean()
            n_sensors += 1
        except KeyError:
            continue

    # number of concurrent hours with all sensors reporting pollutant values
    n_concurr = total_n_vals / n_sensors

    pollutant_avg /= n_sensors
    st_dev = np.sqrt(sum_sqrd_diff/(total_n_vals - 1))
    CV = (st_dev / pollutant_avg)*100  # CV reported in percentage

    return cv_df, CV, st_dev, n_concurr


def cv(df_list, deploy_dict, param=None, return_deploy_dict=True):
    """Compute CV for set of sensor dataframes and indicated parameter.

    Loops over the unique deployment groups and constructs a dataframe of
    concurrently recorded sensor measurements which is passed to CV_Calculator
    to determine CV.

    Args:
        df_list (list):
            List of sensor dataframes
        deploy_dict (dict):
            A dictionary containing descriptive statistics and
            textual information about the deployment (testing agency, site,
            time period, etc.), sensors tested, and site conditions during the
            evaluation.
        param (str):
            Parameter name to evaluate
        return_deploy_dict (bool):
            If true, return modified deployment dictionary with precision
            statisitcs (CV, standard deviation, N concurrent datapoints across
            all sensors).

    Returns:
        If ``return_deploy_dict`` is ``True``, return ``deploy_dict`` with
        updated precision statistics, else return ``CV`` (float).

    """
    date_index, avg_suffix = deploy_timestamp_index(df_list,
                                                    averaging_suffix=True)

    cv_df = pd.DataFrame(index=date_index)

    for i, df in enumerate(df_list):
        df = df_list[i]
        sensor_number = i + 1
        try:
            cv_df[str(sensor_number)+'_'+param] = df[param+ '_Value']
        except KeyError as param_not_found:
            print('Parameter name not found in passed dataframes:',
                  param_not_found)
            continue

    for group in deploy_dict['Deployment Groups']:
        deploy = deploy_dict['Deployment Groups'][group]
        deploy_sensor_nums = list(deploy['sensors'].keys())

        if param not in deploy:
            deploy[param] = {}
            deploy[param]['Precision'] = {}

        if 'Precision' not in deploy[param]:
            deploy[param]['Precision'] = {}

        stats_loc = deploy[param]['Precision']

        start = date_index.min().floor(freq='H')
        end = date_index.max().ceil(freq='H')

        serials = {str(i): deploy['sensors'][str(i)]['serial_id'] for
                   i in list(deploy['sensors'].keys())}

        # Check if issues with individual sensors during deployment, remove
        # from serial dictionary and sensor number list used to pop. CV df
        for i, n in enumerate(deploy['sensors']):
            if deploy['sensors'][n]['deploy_issues'] == 'True':
                serials.pop(n)
                deploy_sensor_nums.remove(n)
                print('Sensor', n, 'indicates issues during deployment')
                print('Excluding sensor', n, 'from CV calculation')

        # Set analysis dataframe for computing CV
        deploy_cols = [i + '_' + param for i in deploy_sensor_nums]
        deploy_cv_df = cv_df.loc[start:end, deploy_cols]

        deploy_cv_df, CV, st_dev, n_concurr = _calculate_cv(deploy_cv_df,
                                                            serials,
                                                            param=param)

        stats_loc['cv' + avg_suffix] = float("{0:.3f}".format(CV))
        stats_loc['std' + avg_suffix] = float("{0:.3f}".format(st_dev))
        stats_loc['n' + avg_suffix] = int(n_concurr)

    if return_deploy_dict is True:
        return deploy_dict

    return CV
