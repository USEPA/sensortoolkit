# -*- coding: utf-8 -*-
"""
This module computes the root mean square error for quantifying the error
between sensor and FRM/FEM measurements.

U.S. EPA's Performance Targets Reports recommend the root mean square error
(RMSE), where RMSE is calculated as

.. math::

    RMSE = \\sqrt{\\frac{1}{N\\times M}\\sum_{j=1}^{M}\\left[
    \\sum_{d=1}^{N}\\left(x_{dj}-R_{d}\\right)^2\\right]}

where:
    :math:`RMSE` = root mean square error

    :math:`N` = number of 1-hour/24-hour periods during which all identical instruments
    are operating and returning valid averages over the duration of the field
    test

    :math:`N` = number of identical sensors operated simultaneously during a field test

    :math:`x_{pj}` = valid 1-hour/24-hour averaged sensor PM2.5 concentration for
    averaging interval p and instrument j

    :math:`R_{p}` = valid 1-hour/24-hour averaged FRM/FEM PM2.5 concentration for
    averaging interval p

This equation assumes only one FRM/FEM instrument will be running. If multiple
FRM/FEM instruments are running, separate testing reports can be generated for
each.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Sep  8 10:34:51 2021
Last Updated:
  Wed Sep  8 10:34:51 2021
"""
import pandas as pd
import numpy as np
from sensortoolkit.datetime_utils import deploy_timestamp_index


def rmse(df_list, ref_df, deploy_dict, param=None, return_deploy_dict=True):
    """Compute the root mean square error for concurrent sensor measurements in
    each testing deployment groups.

    Loops over the unique deployment groups and computes RMSE for each
    group of concurrently collocated and recording sensors.

    Args:
        df_list (list):
            List of sensor dataframes (either 1-hour or 24-hour averages)
        ref_df (pandas dataframe):
            dataframe with FRM/FEM values (either 1-hour or 24-hour averages)
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
        updated error statistics, else return ``RMSE`` (float)

    """
    date_index, avg_suffix = deploy_timestamp_index(df_list,
                                                    averaging_suffix=True)

    for group in deploy_dict['Deployment Groups']:
        grp_info = deploy_dict['Deployment Groups'][group]
        start = grp_info['eval_start']
        end = grp_info['eval_end']
        grp_sensor_nums = list(grp_info['sensors'].keys())

        if param not in grp_info:
            grp_info[param] = {}
            grp_info[param]['Error'] = {}

        if 'Error' not in grp_info[param]:
            grp_info[param]['Error'] = {}

        stats_loc = grp_info[param]['Error']

        rmse_df = pd.DataFrame(index=date_index)

        for i, df in enumerate(df_list, 1):
            rmse_df[str(i) + '_' + param] = df[param + '_Value']

        ref_data = ref_df.loc[start:end, param + '_Value']

        # Check if issues with individual sensors during deployment, remove
        # from serial dictionary and sensor number list used to pop CV df
        for i, n in enumerate(grp_info['sensors']):
            if grp_info['sensors'][n]['deploy_issues'] == 'True':
                grp_sensor_nums.remove(n)
                print('Sensor', n, 'indicates issues during deployment')
                print('Excluding sensor', n, 'from RMSE calculation')

        # Set analysis dataframe for computing RMSE
        grp_avg_cols = [i + '_' + param for i in grp_sensor_nums]
        grp_rmse = rmse_df.loc[start:end, grp_avg_cols]
        grp_rmse = grp_rmse.dropna(axis=1, how='all').dropna(axis=0, how='any')

        N = grp_rmse.count().unique()[0]
        M = len(grp_rmse.columns.to_list())

        grp_rmse['ref'] = ref_data
        grp_rmse = grp_rmse.dropna(axis=0, how='any')

        # Calculate RMSE
        Err = 0
        for col in grp_rmse:
            Err += sum((grp_rmse[col]-grp_rmse['ref'])**2)

        RMSE = np.sqrt((1/(N*M))*Err)

        if param not in grp_info:
            grp_info[param] = {}

        stats_loc['rmse' + avg_suffix] = float("{0:.3f}".format(RMSE))

        if ref_data.dropna().empty:
            stats_loc['rmse' + avg_suffix] = None
            stats_loc['nrmse' + avg_suffix] = None
        else:
            nRMSE = (RMSE / ref_data.mean())*100
            stats_loc['nrmse' + avg_suffix] = float("{0:.3f}".format(nRMSE))

    if return_deploy_dict is True:
        return deploy_dict

    return RMSE
