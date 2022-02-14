# -*- coding: utf-8 -*-
"""
This module constructs and populates the deployment dictionary data
structure ``deploy_dict``. Below is an overview of the deployment dictionary:

* Testing organization
    * Organization name, contact information
* Testing Location
    * Site name, address, coordinates, and AQS site identifier
* Deployment Information and Statistics
    * Unique deployment groups
        * Description of sensor uptime for each sensor unit
    * Evaluation parameter statistics
        * Precision
        * Error
        * Description of reference monitor, measured range during
          deployment period at 1-hour and 24-hour averages
    * Meteorological conditions
        * Description of temperature instrument, measured range during
          deployment period at 1-hour and 24-hour averages
        * Description of relative humidity instrument, measured range during
          deployment period at 1-hour and 24-hour averages

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Mon Nov  9 10:47:56 2020
Last Updated:
  Tue Jul 12 13:38:00 2021
"""
import pandas as pd
import numpy as np
from datetime import datetime
from sensortoolkit.calculate import uptime
from sensortoolkit.lib_utils import _get_version
from sensortoolkit.param import Parameter
from sensortoolkit.datetime_utils import (deploy_timestamp_index,
                                          get_timestamp_interval)


def construct_deploy_dict(deploy_df, full_df_list, hourly_df_list,
                          daily_df_list, sensor_name, **kwargs):
    """Create the deployment dictionary, initialize with sensor group info,
    time period of deployment, testing agency and location, and library version
    and time at which the dictionary were constructed.

    Determines which sensors match the beginning and end dates for deployment
    (provided a timedelta padding window of 1 day around the begin and end
    timestamps). Sensors measuring concurrently are grouped together as a
    `deployment group`. Sensors with beginning and end deployment dates that
    differ from the identified deployment group are assigned ``True`` for the
    ``deploy_dict`` sensor unit entry ``deploy_issues``.

    Args:
        deploy_df (pandas dataframe):
            A data frame containing the start time (`Begin`), end time (`End`),
            and total duration of evaluation period for each sensor in a
            deployment group.
        full_df_list (list):
            List of sensor data frames of length N (where N is the number of
            sensor units in a testing group). Data frames indexed by
            at recorded sampling frequency.
        hourly_df_list (list):
            List of sensor data frames of length N (where N is the number of
            sensor units in a testing group). Data frames indexed by
            DateTime at 1-hour averaged sampling frequency.
        daily_df_list (list):
            List of sensor data frames of length N (where N is the number of
            sensor units in a testing group). Data frames indexed by
            DateTime at 24-hour averaged sampling frequency.
        sensor_name (str):
            The make and model of the sensor being evaluated.

    **Keyword Arguments**

    :param dict testing_org:
        A dictionary containing the information about the testing organization.
    :param dict testing_loc:
        A dictionary containing information about the testing site. If the site
        is part of U.S. EPA’s Air Quality System (AQS), the AQS Site ID should
        be specified.

    Returns:
        deploy_dict (dict):
            Dictionary containing separate deployment group start and
            end times (based on the latest (max) start timestamp and earliest
            (min) end timestamp in group), deployment duration, and sensor
            serial IDs for devices within each deployment group.

    """

    # Testing organization information
    testing_org = kwargs.get('testing_org',
                             {'Deployment name': '[Name of Deployment]',
                              'Org name': ['[Organization name line 1]',
                                           '[Organization name line 2]'],
                              'Website': {'website name': '[Website Name]',
                                          'website link': '[Website Link]'},
                              'Contact email': '[Contact Email]',
                              'Contact phone': '[Contact Phone Number]'})

    # Testing location information
    testing_loc = kwargs.get('testing_loc',
                             {'Site name': '[Site Name]',
                              'Site address': '[Site Address]',
                              'Site lat': '[Site Latitude]',
                              'Site long': '[Site Longitude]',
                              'Site AQS ID': '[Site AQS ID]'})

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S %p')
    deploy_dict = {'sensortoolkit Version': _get_version(),
                   'Date of Analysis': current_time,
                   'Sensor Name': sensor_name,
                   'Sensor Firmware Version': 'Unspecified',  # TODO
                   'Deployment Groups': {},
                   'Testing Organization': testing_org,
                   'Testing Location': testing_loc}

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
            deploy.Begin.min().strftime("%Y-%m-%dT%H:%M:%S%z")
        deployments['Group ' + str(deploy_grp_n)]['eval_end'] = \
            deploy.End.max().strftime("%Y-%m-%dT%H:%M:%S%z")
        deployments['Group ' + str(deploy_grp_n)]['eval_duration'] = \
            str(abs(deploy.Begin.min() - deploy.End.max()))

        start = deployments['Group ' + str(deploy_grp_n)]['eval_start']
        end = deployments['Group ' + str(deploy_grp_n)]['eval_end']

        # round timestamp down to nearest hour
        start = pd.to_datetime(start).floor(freq='H')
        # round timestamp up to nearest hour
        end = pd.to_datetime(end).ceil(freq='H')

        for sensor_n in list(sensor_info.keys()):
            i = int(sensor_n) - 1

            full_df = full_df_list[i]
            hourly_df = hourly_df_list[i]
            daily_df = daily_df_list[i]

            # Record whether sensor encountered issues during deployment, ended
            # deployment early
            sensor_df = deploy[deploy.Sensor_Number == sensor_n]
            sensor_df = sensor_df.reset_index(drop=True)
            sensor_info[sensor_n]['deploy_issues'] = str(bool(
                                                        sensor_df.Issues[0]))

            # Compute recording interval for data
            time_delta = get_timestamp_interval(full_df)
            sensor_info[sensor_n]['recording_interval'] = time_delta

            # 1-hr uptime
            sensor_h_uptime = uptime(hourly_df.loc[start:end, :],  key=sensor_n)
            sensor_info[sensor_n]['uptime_1-hour'] = sensor_h_uptime[sensor_n]['Uptime']

            # 24-hr uptime
            sensor_d_uptime = uptime(daily_df.loc[start:end, :], key=sensor_n)
            sensor_info[sensor_n]['uptime_24-hour'] = sensor_d_uptime[sensor_n]['Uptime']

        deploy_df = deploy_df.drop(deploy.index, axis=0)
        deploy_grp_n += 1

    return deploy_dict


def deploy_ref_stats(deploy_dict, ref_df, cal_check_dict=None, param=None,
                  ref_name=None):
    """Add reference monitor statistics to the parameter statistics subfield in
    the deployment dictionary.

    Details added include:

    * The FRM/FEM monitor name
    * The minimum concentration recorded at the specified interval
      averaging.
    * The maximum concentration recorded at the specified interval
      averaging.
    * The number of intervals during which the FRM/FEM exceeds the goal
      concentration recommended by the performance targets testing report
      for elevated concentrations (goal :math:`\\geq`` three days).

    Args:
        deploy_dict (dict):
            Dictionary containing separate deployment group start and end times
            (based on the latest (max) start timestamp and earliest (min)
            end timestamp in group), deployment duration, and sensor serial IDs
            for devices within each deployment group.
    	ref_df (pandas dataframe):
            Dataframe for reference concentrations at either 1-hour or 24-hour
            averaging depending on the performance targets recommeneded
            averaging interval.
    	cal_check_dict (dict):
            [Future feature] Dictionary for housing dates and descriptions of QC
            calibration checks as part of regularly scheduled and cataloged QC
            procedures.
        param_obj (str):
            The evaluation parameter
        ref_name (str):
            The name of the FRM/FEM monitor (make and model).

    Returns:
        deploy_dict:
            Dictionary containing separate deployment group start and end times
            (based on the latest (max) start timestamp and earliest (min)
            end timestamp in group), deployment duration, and sensor serial IDs
            for devices within each deployment group.

    """
    param_obj = Parameter(param)
    param_name = param_obj.name
    #fmt_param = param_obj.format_name
    #fmt_param_units = param_obj.units

    date_index, avg_suffix = deploy_timestamp_index(ref_df,
                                                    averaging_suffix=True)

    if param_name == 'PM25':
        conc_goal = 25  # Concentration goal: 25 ug/m^3 for at least one day
        #cal_check_dict = cal_check_dict['PM cal checks'][ref_name]
    elif param_name == 'O3':
        conc_goal = 60  # Concentration goal: 60 ppbv for at least one day
        #cal_check_dict = cal_check_dict['Gas cal checks'][ref_name]
    else:
        conc_goal = None
        #cal_check_dict = None

    for group in deploy_dict['Deployment Groups']:
        deploy = deploy_dict['Deployment Groups'][group]
        start = deploy['eval_start']
        end = deploy['eval_end']

        ref_data = ref_df.loc[start:end, param_name + '_Value']

        if param_name not in deploy:
            deploy[param_name] = {}
            deploy[param_name]['Reference'] = {}

        if 'Reference' not in deploy[param_name]:
            deploy[param_name]['Reference'] = {}

        stats_loc = deploy[param_name]['Reference']

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


def deploy_met_stats(deploy_dict, df_list, met_ref_df, cal_check_dict=None):
    """Add meteorological instrument statistics to the parameter statistics
    subfield in the deployment dictionary.

    Details added include:

    * The name of the instrument collocated nearby sensor deployment location.
    * The minimum value recorded at the specified interval averaging.
    * The maximum value recorded at the specified interval averaging.
    * The number of intervals during which the instrument exceeds the
      manufacturer's recommended target range for instrument performance.
      This is provisionally set for RH (exceedence when :math:`\\leq` 10% or
      :math:`\\geq` 90%) and Temp (exceedence when :math:`\\leq` -20 C or
      :math:`\\geq` 40 C).

    Args:
    	deploy_dict (dict):
            Dictionary containing separate deployment group start and end times
            (based on the latest (max) start timestamp and earliest (min)
            end timestamp in group), deployment duration, and sensor serial IDs
            for devices within each deployment group.
    	df_list (list):
            List of pandas dataframes for sensor measurements at either 1-hr or
            24-hr averaging intervals.
        met_ref_df (pandas dataframe):
            A dataframe containing meteorological parameters recorded at the
            testing site during the evaluation period (either 1-hr or 24-hr
            averaging intervals).
    	cal_check_dict (dict):
            [Future feature] Dictionary for housing dates and descriptions of QC
            calibration checks as part of regularly scheduled and cataloged QC
            procedures.

    Returns:
        deploy_dict:
            Dictionary containing separate deployment group start and end times
            (based on the latest (max) start timestamp and earliest (min)
            end timestamp in group), deployment duration, and sensor serial IDs
            for devices within each deployment group.

    """
    met_str = 'Meteorological Conditions'
    date_index, avg_suffix = deploy_timestamp_index(met_ref_df,
                                                    averaging_suffix=True)

    #cal_check_dict = cal_check_dict['Met cal checks']
    for name in ['Temp', 'RH']:
        param_obj = Parameter(name)
        param_name = param_obj.name
        fmt_param = param_obj.format_name
        #fmt_param_units = param_obj.units

        no_data = False
        try:
            ref_name = met_ref_df.loc[:, param_name + '_Method'].dropna().apply(
                                            lambda x: str(x)).unique()[0]
        except IndexError:
            ref_name = 'Unknown Reference'
        except KeyError:
            # No met parameter data in passed reference dataframe
            no_data = True

        if param_name == 'Temp':
            max_criterion = 40  # provisional criterion for upper lim (deg C)
            min_criterion = -20  # provisional criterion for lower lim (deg C)
        if param_name == 'RH':
            max_criterion = 90  # provisional criterion for upper lim (%)
            min_criterion = 10  # provisional criterion for lower lim (%)

        for group in deploy_dict['Deployment Groups']:
            deploy = deploy_dict['Deployment Groups'][group]
            start = deploy['eval_start']
            end = deploy['eval_end']

            if met_str not in deploy:
                deploy[met_str] = {}

            if fmt_param not in deploy[met_str]:
                deploy[met_str][fmt_param] = {}

            stats_loc = deploy[met_str][fmt_param]

            if not no_data:
                ref_data = met_ref_df.loc[start:end,  param_name + '_Value']

                grp_idx = [int(i) - 1 for i in deploy['sensors'].keys()]
                data_pairs = []
                for idx in grp_idx:
                    df = df_list[idx]
                    start = df.index.min()
                    end = df.index.max()
                    data_pairs.append(
                                met_ref_df.loc[start:end,
                                               param_name + '_Value'].dropna().size)

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
            else:
                stats_loc['instrument_name'] = ''
                stats_loc['min' + avg_suffix] = ''
                stats_loc['max' + avg_suffix] = ''
                stats_loc['n_exceed_target_criteria' + avg_suffix] = ''
                stats_loc['n_measurement_pairs' + avg_suffix] = ''

    return deploy_dict
