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
  Tue Mar 10 08:38:24 2020
Last Updated:
  Tue Jul 13 09:45:24 2021
"""
import pandas as pd
import numpy as np
from sensortoolkit._analysis.synoptic_idx import Synoptic_Index


def Intersensor_Mean(df_list, deploy_dict):
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

    date_index, avg_suffix = Synoptic_Index(df_list, averaging_suffix=True)

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
