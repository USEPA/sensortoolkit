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
  Tue Mar 3 13:47:32 2020
Last Updated:
  Tue Jul 13 11:09:13 2021
"""
import numpy as np
import pandas as pd
from sensortoolkit._format.format_date import Get_Date
from sensortoolkit._analysis.synoptic_idx import Synoptic_Index


def Regression_Stats(hourly_df_obj=None, daily_df_obj=None, hourly_ref_df=None,
                     daily_ref_df=None, deploy_dict=None, param=None,
                     sensor_name=None, ref_name=None, serials=None,
                     path=None, write_to_file=False):
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
    if not hourly_df_obj and not daily_df_obj:
        print('No sensor data passed to function.')
        return
    elif hourly_df_obj is None:  # Compute only daily regression statistics
        df_obj = [daily_df_obj]
        ref_obj = [daily_ref_df]
    elif daily_df_obj is None:  # Compute only hourly regression statistics
        df_obj = [hourly_df_obj]
        ref_obj = [hourly_ref_df]
    else:  # Compute both hourly and daily regression statistics
        df_obj = [hourly_df_obj, daily_df_obj]
        ref_obj = [hourly_ref_df, daily_ref_df]

    stats_cols = ['Sensor Name', 'Sensor_Number', 'Sensor_Serial',
                  'Averaging Interval', 'Param', 'Reference', 'R$^2$',
                  'Slope', 'Intercept', 'Sensor RMSE', 'N', 'Sensor_Min',
                  'Sensor_Max', 'Sensor_Mean']

    stats_df = pd.DataFrame(columns=stats_cols)

    sensor_name = deploy_dict['Sensor Name']
    sensor_nums = list(serials.keys())

    # Loop over passed dataframe for sensors and compute regression stats for
    # each sensor dataset
    for df_list, ref_df in zip(df_obj, ref_obj):
        for i, (df, sensor_num) in enumerate(zip(df_list, sensor_nums)):

            ydata = df[param]
            if 'mean_' + param in ref_df:
                xdata = ref_df['mean_' + param]
                ref_name = 'Intersensor_mean_' + param
            else:
                xdata = ref_df[param + '_Value']
                ref_name = ''.join(
                            list(ref_df[param + '_Method'].dropna().apply(
                                            lambda x: str(x)).unique()[0]))
            if i == 0:
                print('Computing regression statistics for ' + sensor_name
                      + ' vs ' + ref_name)

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

            if combine_df.empty:
                print('..Warning: Linear regression not possible for sensor '
                      + str(sensor_num) + '. Sensor or reference data are '
                      'null.')
                r_square = slope = intercept = RMSE = N = np.nan
                param_min = param_max = param_mean = np.nan
            else:
                N = int(len(combine_df))

                if N <= 2:
                    print('..Warning: Linear regression not possible for' +
                          ' sensor ' + str(sensor_num) +
                          '. Insufficient number of data points')
                    r_square = slope = intercept = RMSE = N = np.nan
                    param_min = param_max = param_mean = np.nan

                else:
                    # Compute linear regress. for the union of finite
                    # x and y data
                    fit = np.polyfit(xdata[idx], ydata[idx], 1)
                    slope = fit[0]
                    intercept = fit[1]
                    pearson_coeff = X.corr(Y, method='pearson')
                    r_square = pearson_coeff*pearson_coeff

                    sensor_val = combine_df.sensor_data
                    ref_val = combine_df.ref_data
                    MSE = (1/N)*sum((sensor_val-ref_val)**2)
                    RMSE = np.sqrt(MSE)

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
                                   RMSE,
                                   N,
                                   param_min,
                                   param_max,
                                   param_mean])

            row_df.index = stats_df.columns
            row_df = row_df.T

            stats_df = pd.concat([stats_df, row_df]).reset_index(drop=True)

        # Add Metric averages
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

    if write_to_file is True:
        today = Get_Date()
        ref_name = ref_name.replace(' ', '_')
        filename = (sensor_name + '_' + param + '_vs_' + ref_name +
                    '_stats_df_' + today + '.csv')
        print('../Data and Figures/eval_stats/' + sensor_name + '/' + filename)
        stats_df.to_csv(path + filename, index=False)

    return stats_df


def Compute_RMSE(df_list, ref_df, deploy_dict, stats_df=None,
                 param='PM25', return_deploy_dict=True):
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
        stats_df (pandas dataframe):
            Dataframe containing OLS regression statisitcs.
        param (str):
            Parameter name to evaluate
        return_deploy_dict (bool):
            If true, return modified deployment dictionary with precision
            statisitcs (CV, standard deviation, N concurrent datapoints across
            all sensors).

    Returns:
        If return_deploy_dict:
            Returns deploy_dict with updated error statistics
        else:
            Return RMSE (float)
    """
    date_index, avg_suffix = Synoptic_Index(df_list, averaging_suffix=True)

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
            rmse_df[str(i) + '_' + param] = df[param]

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
    else:
        return RMSE
