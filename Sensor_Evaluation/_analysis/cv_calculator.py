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
  Wed Jan 29 10:03:27 2020
Last Updated:
  Tue Nov 10 13:43:00 2020
"""
import numpy as np
import pandas as pd
from Sensor_Evaluation._analysis.synoptic_idx import Synoptic_Index


def CV_Calculator(cv_df, sensor_numbers, param):

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

    print("...N excluded:", n_excluded, "out of", before_drop_n, "total.")
    print("...N concurrent:", after_drop_n)
    print("...Concurrent Measurement Timeframe:", cv_df.index[0], '-',
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
    n = total_n_vals / n_sensors

    pollutant_avg /= n_sensors
    st_dev = np.sqrt(sum_sqrd_diff/(total_n_vals - 1))
    CV = (st_dev / pollutant_avg)*100  # CV reported in percentage

    return cv_df, CV, st_dev, n


def Compute_CV(df_list, deploy_dict, param='PM25', return_deploy_dict=True):
    """
    Wrapper function for computing CV for generalized set of dataframes and
    parameter.
    """

    date_index, avg_suffix = Synoptic_Index(df_list, averaging_suffix=True)

    cv_df = pd.DataFrame(index=date_index)

    for i, df in enumerate(df_list):
        df = df_list[i]
        sensor_number = i + 1
        try:
            cv_df[str(sensor_number)+'_'+param] = df[param]
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

        start = deploy['eval_start']
        end = deploy['eval_end']

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

        deploy_cv_df, CV, st_dev, n = CV_Calculator(deploy_cv_df,
                                                    serials,
                                                    param=param)

        stats_loc['cv' + avg_suffix] = float("{0:.3f}".format(CV))
        stats_loc['std' + avg_suffix] = float("{0:.3f}".format(st_dev))
        stats_loc['n' + avg_suffix] = int(n)

    if return_deploy_dict is True:
        return deploy_dict
    else:
        return CV
