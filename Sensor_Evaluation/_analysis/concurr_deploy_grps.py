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
  Mon Nov  9 10:47:56 2020
Last Updated:
  Tue May 11 16:22:00 2021
"""
import pandas as pd
import numpy as np
from Sensor_Evaluation._format.format_names import Format_Param_Name
from Sensor_Evaluation._analysis.synoptic_idx import Synoptic_Index
from Sensor_Evaluation._analysis.uptime_calculator import Uptime_Calculator


def Deployment_Groups(deploy_df, full_df_list, hourly_df_list, daily_df_list,
                      sensor_name):
    """
    Determine which sensors were deployed concurrently. Identify beginning,
    end, and duration of concurrent deployment group.

    Method: Step through deployment dataframe and determine which sensors match
    the beginning and end dates for deployment (provided a timedelta padding
    window of 1 day around the begin and end timestamps). As groups are
    identified, the group is subtracted from the deployment dataframe to
    reduce redudant iteration over sensors for which the deployment group has
    been identified.

    Return: Dictionary deploy_dict containing separate deployment group start
    and end times (based on the latest (max) start timestamp and earliest (min)
    end timestamp in group), deployment duration, and sensor serial IDs for
    devices within each deployment group.
    """
    deploy_dict = {'Sensor Name': sensor_name,
                   'Deployment Groups': {}
                   }
    deploy_grp_n = 1

    while deploy_df.empty is False:
        i = deploy_df.index[0]

        match_begin = abs(deploy_df.loc[i, 'Begin'] - deploy_df.loc[:, 'Begin']
                          ) < pd.Timedelta('1 day')

        deploy = deploy_df[match_begin]

        # Date (YYYY-MM-DD) of deployment group end, calculate mode
        end_date = deploy.loc[:, "End"].dt.strftime("%Y-%m-%d")
        end_date_mode = end_date.mode()[0]

        # Sensors that concluded deployment before end of majority of group
        deploy['Issues'] = end_date != end_date_mode

        serials = {str(i): serial for i, serial in zip(
                   deploy.Sensor_Number, deploy.Sensor_Serial)}

        deployments = deploy_dict['Deployment Groups']

        deployments['Group ' + str(deploy_grp_n)] = {}
        deployments['Group ' + str(deploy_grp_n)]['sensors'] = {}

        sensor_info = {i: {'serial_id': j} for i, j in zip(serials.keys(),
                                                           serials.values())}

        deployments['Group ' + str(deploy_grp_n)]['sensors'] = sensor_info

        deployments['Group ' + str(deploy_grp_n)]['eval_start'] = \
            deploy.Begin.min().strftime("%Y-%m-%d %H:%M:%S")
        deployments['Group ' + str(deploy_grp_n)]['eval_end'] = \
            deploy.End.max().strftime("%Y-%m-%d %H:%M:%S")
        deployments['Group ' + str(deploy_grp_n)]['eval_duration'] = \
            str(abs(deploy.Begin.min() - deploy.End.max()))

        start = deployments['Group ' + str(deploy_grp_n)]['eval_start']
        end = deployments['Group ' + str(deploy_grp_n)]['eval_end']

        hourly_idx = pd.to_datetime(
                        pd.date_range(start, end,
                                      freq='H').strftime('%Y-%m-%d %H:00:00'))
        daily_idx = pd.to_datetime(
                        pd.date_range(start, end,
                                      freq='D').strftime('%Y-%m-%d'))

        for sensor_n in list(sensor_info.keys()):
            i = int(sensor_n) - 1

            full_df = full_df_list[i]
            hourly_df = hourly_df_list[i]
            daily_df = daily_df_list[i]

            # Record whether sensor encountered issues during deployment, ended
            # deployment early
            sensor_df = deploy.where(
                        deploy['Sensor_Number'].astype('int') == int(sensor_n)
                                ).dropna().reset_index(drop=True)
            sensor_info[sensor_n]['deploy_issues'] = str(bool(
                                                        sensor_df.Issues[0]))

            # Compute recording interval for data
            time_delta = Measure_Recording_Interval(full_df)
            sensor_info[sensor_n]['recording_interval'] = time_delta

            # 1-hr uptime
            sensor_h_uptime = Uptime_Calculator(hourly_df.loc[hourly_idx, :],
                                                key=sensor_n)
            sensor_info[sensor_n]['uptime_hourly'] = \
                sensor_h_uptime[sensor_n]['Uptime']

            # 24-hr uptime
            sensor_d_uptime = Uptime_Calculator(daily_df.loc[daily_idx, :],
                                                key=sensor_n)
            sensor_info[sensor_n]['uptime_daily'] = \
                sensor_d_uptime[sensor_n]['Uptime']

        deploy_df = deploy_df.drop(deploy.index, axis=0)
        deploy_grp_n += 1

    return deploy_dict


def Reference_Stats(deploy_dict, ref_df, cal_check_dict=None, param='PM25',
                    ref_name=None):

    fmt_param, fmt_param_units = Format_Param_Name(param)

    date_index, avg_suffix = Synoptic_Index(ref_df, averaging_suffix=True)

    if param == 'PM25':
        conc_goal = 25  # Concentration goal: 25 ug/m^3 for at least one day
        #cal_check_dict = cal_check_dict['PM cal checks'][ref_name]
    if param == 'O3':
        conc_goal = 60  # Concentration goal: 60 ppbv for at least one day
        #cal_check_dict = cal_check_dict['Gas cal checks'][ref_name]
    else:
        conc_goal = None
        #cal_check_dict = None

    for group in deploy_dict['Deployment Groups']:
        deploy = deploy_dict['Deployment Groups'][group]
        start = deploy['eval_start']
        end = deploy['eval_end']

        ref_data = ref_df.loc[start:end, param + '_Value']

        if param not in deploy:
            deploy[param] = {}
            deploy[param]['Reference'] = {}

        if 'Reference' not in deploy[param]:
            deploy[param]['Reference'] = {}

        stats_loc = deploy[param]['Reference']

        stats_loc['reference_name'] = ref_name
        stats_loc['conc_min' + avg_suffix] = \
            float("{0:.3f}".format(ref_data.min()))
        stats_loc['conc_max' + avg_suffix] = \
            float("{0:.3f}".format(ref_data.max()))
        stats_loc['n_exceed_conc_goal' + avg_suffix] = \
            int(ref_data.where(ref_data > conc_goal).count())
        #stats_loc['cal_check_dates'] = cal_check_dict

        if ref_data.dropna().empty:
            stats_loc['conc_min' + avg_suffix] = None
            stats_loc['conc_max' + avg_suffix] = None
            stats_loc['n_exceed_conc_goal' + avg_suffix] = None

    return deploy_dict


def Meteorological_Stats(deploy_dict, df_list, met_ref_df,
                         cal_check_dict=None):

    met_str = 'Meteorological Conditions'
    date_index, avg_suffix = Synoptic_Index(met_ref_df, averaging_suffix=True)

    #cal_check_dict = cal_check_dict['Met cal checks']

    for param in ['Temp', 'RH']:
        fmt_param, fmt_param_units = Format_Param_Name(param)

        try:
            ref_name = met_ref_df[param + '_Method'].dropna().unique()[0]
        except IndexError:
            ref_name = 'Unknown Reference'

        if param == 'Temp':
            max_criterion = 40  # provisional criterion for upper lim (deg C)
            min_criterion = -20  # provisional criterion for lower lim (deg C)
        if param == 'RH':
            max_criterion = 90  # provisional criterion for upper lim (%)
            min_criterion = 10  # provisional criterion for lower lim (%)

        for group in deploy_dict['Deployment Groups']:
            deploy = deploy_dict['Deployment Groups'][group]
            start = deploy['eval_start']
            end = deploy['eval_end']

            ref_data = met_ref_df.loc[start:end,  param + '_Value']

            grp_idx = [int(i) - 1 for i in deploy['sensors'].keys()]

            data_pairs = []
            for idx in grp_idx:
                df = df_list[idx]
                data_pairs.append(
                            met_ref_df.loc[df.index,
                                           param + '_Value'].dropna().size)

            if met_str not in deploy:
                deploy[met_str] = {}

            if fmt_param not in deploy[met_str]:
                deploy[met_str][fmt_param] = {}

            stats_loc = deploy[met_str][fmt_param]

            stats_loc['instrument_name'] = ref_name
            stats_loc['min' + avg_suffix] = \
                float("{0:.3f}".format(ref_data.min()))
            stats_loc['max' + avg_suffix] = \
                float("{0:.3f}".format(ref_data.max()))
            stats_loc['n_exceed_target_criteria' + avg_suffix] = \
                int(ref_data.where((ref_data > max_criterion) |
                                   (ref_data < min_criterion)).count())
            stats_loc['n_measurement_pairs' + avg_suffix] = \
                np.mean(data_pairs)

            #deploy[met_str]['cal_check_dates'] = cal_check_dict

    return deploy_dict


def Measure_Recording_Interval(df):
    """
    Compute recording interval for dataframe. Compute time delta between
    successive timestamps and take the mode of recorded time deltas to be the
    device recording interval.
    """
    delta = (df.index[1:] - df.index[0:-1]).to_frame()
    idx_name = delta.index.name
    t_delta = delta[idx_name].mode()[0]

    #delta_std = delta.std()[0].seconds

    t_delta_comps = ['days', 'hours', 'minutes', 'seconds',
                     'milliseconds', 'microseconds', 'nanoseconds']

    delta_df = pd.DataFrame(t_delta.components, columns=['value'],
                            index=t_delta_comps)

    delta_df = delta_df.where(delta_df != 0).dropna()

    interval_str = ''
    for i, (index, row) in enumerate(delta_df.iterrows(), 1):
        # If the interval has a value of one, remove the plural 's'
        if row.value == 1:
            index = index[:-1]
        interval_str += str(row.value) + ' ' + str(index)
        if i < delta_df.size:
            interval_str += ', '

#    if delta_std > 0:
#        interval_str += ' +/- ' + str(delta_std) + ' seconds'

    return interval_str
