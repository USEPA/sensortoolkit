# -*- coding: utf-8 -*-
"""
This module computes the average of parameter values across all conurrently
recorded sensor measurements for each timestamp in the passed list of
dataframes.

For instance, say you have the following sensor datasets:

>>> sensor_data_a = df_list[0]
>>> df_list[0]
                     PM25
2021-01-01 00:00:00   2.3
2021-01-01 01:00:00   5.4
2021-01-01 02:00:00   8.5
2021-01-01 03:00:00   4.7
2021-01-01 04:00:00   3.4

>>> sensor_data_b = df_list[1]
>>> df_list[1]
                       PM25
2021-01-01 00:00:00    1.62
2021-01-01 01:00:00    4.41
2021-01-01 02:00:00    7.20
2021-01-01 03:00:00  np.nan
2021-01-01 04:00:00    2.61

>>> sensor_data_c = df_list[2]
>>> df_list[2]
                      PM25
2021-01-01 00:00:00   2.31
2021-01-01 01:00:00   6.34
2021-01-01 02:00:00  10.37
2021-01-01 03:00:00   5.43
2021-01-01 04:00:00   3.74

Computing the average for each hour where all sensors are measuring concurrently,
we find the intersensor average to be:

>>> intersensor_average_df = sensortoolkit.calculate.intersensor_mean(df_list, deploy_dict)
>>> intersensor_average_df
                     PM25_avg
2021-01-01 00:00:00     2.076
2021-01-01 01:00:00     5.383
2021-01-01 02:00:00     8.690
2021-01-01 03:00:00    np.nan
2021-01-01 04:00:00     3.250

Note that no average is computed for the 3:00 timestamp, as sensor_data_b contains
a null value for this timestamp. Intersensor averages are only computed for instances
where all sensors are recording concurrently. 
================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Tue Mar 10 08:38:24 2020
Last Updated:
  Tue Jul 13 09:45:24 2021
"""
import pandas as pd
import numpy as np
from sensortoolkit.datetime_utils import deploy_timestamp_index


def intersensor_mean(df_list, deploy_dict):
    """Compute the average of each parameter across concurrently recorded
    sensor datasets.

    Args:
        df_list (list):
            List of sensor dataframes at either 1-hour or 24-hour averaging
            interval.
        deploy_dict (dict):
            A dictionary containing descriptive statistics and
            textual information about the deployment (testing agency, site,
            time period, etc.), sensors tested, and site conditions during the
            evaluation.
    Returns:
        avg_df (pandas dataframe):
            Dataframe to contain intersensor average for each parameter at
            either 1-hour or 24-hour averaging interval.
    """
    print('Computing mean parameter values across concurrent sensor datasets')
    # List of unique column headers
    param_list = []
    for df in df_list:
        for item in df.columns.to_list():
            param_list.append(item)
    param_list = list(dict.fromkeys(param_list))

    date_index, avg_suffix = deploy_timestamp_index(df_list,
                                                    averaging_suffix=True)

    # Dataframe to contain intersensor average for each parameter
    avg_df = pd.DataFrame(index=date_index)

    for group in deploy_dict['Deployment Groups']:
        deploy_details = deploy_dict['Deployment Groups'][group]
        start = deploy_details['eval_start']
        end = deploy_details['eval_end']
        group_sensor_nums = list(deploy_details['sensors'].keys())

        # Check if issues with individual sensors during deployment, remove
        # from serial dictionary and sensor number list used to pop. avg df
        for i, n in enumerate(deploy_details['sensors']):
            if deploy_details['sensors'][n]['deploy_issues'] == 'True':
                group_sensor_nums.remove(n)
                print('...Sensor', n, 'indicates issues during deployment')
                print('...Excluding sensor', n, 'from intersensor parameter '
                      'average dataframe')

        for param in param_list:
            combine_df = pd.DataFrame(index=date_index)

            for i, df in enumerate(df_list, 1):
                try:
                    combine_df[str(i) + '_' + param] = df[param]
                except KeyError as k:
                    print('...Warning', k, 'not found in dataframe at index ',
                          str(i-1))
                    combine_df[str(i) + '_' + param] = np.nan

            deploy_avg_cols = [i + '_' + param for i in group_sensor_nums]
            deploy_avg = combine_df.loc[start:end, deploy_avg_cols]

            deploy_n = deploy_avg.count(axis=1)

            # Compute intersensor averages for times where all sensors are
            # measuring concurrently
            deploy_avg = deploy_avg.dropna(axis=0, how='any')
            deploy_avg = deploy_avg.mean(axis=1, skipna=False)

            avg_df.loc[start:end, 'deploy_group'] = group
            avg_df.loc[start:end, 'sensor_count'] = deploy_n
            avg_df.loc[start:end, 'mean_'+param] = deploy_avg

    return avg_df
