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
  Mon Nov 12 08:50:00 2020
"""
import numpy as np
import pandas as pd
from Sensor_Evaluation._format.format_date import Get_Date
from Sensor_Evaluation._analysis.synoptic_idx import Synoptic_Index


def Regression_Stats(hourly_df_obj=None, daily_df_obj=None, hourly_ref_df=None,
                     daily_ref_df=None, deploy_dict=None, param=None,
                     sensor_name=None, ref_name=None, serials=None,
                     path=None, write_to_file=False):
    """
    """
    if hourly_df_obj is None and daily_df_obj is None:
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
                            list(ref_df[param + '_Method'].dropna().unique()))
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
                avg_int = 'Daily'
            if (df.index[1] - df.index[0]) == pd.Timedelta('1 hour'):
                avg_int = 'Hourly'

            if combine_df.empty:
                print('..Warning: Linear regression not possible for sensor '
                      + str(sensor_num) + '. Sensor or reference data are '
                      'null.')
                r_square = np.nan
                slope = np.nan
                intercept = np.nan
                RMSE = np.nan
                N = np.nan
                param_min = np.nan
                param_max = np.nan
                param_mean = np.nan

            else:
                N = int(len(combine_df))

                if N <= 2:
                    print('..Warning: Linear regression not possible for' +
                          ' sensor ' + str(sensor_num) +
                          '. Insufficient number of data points')
                    r_square = np.nan
                    slope = np.nan
                    intercept = np.nan
                    RMSE = np.nan
                    N = np.nan
                    param_min = np.nan
                    param_max = np.nan
                    param_mean = np.nan

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
    """
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
