# -*- coding: utf-8 -*-
"""
This module computes the uptime for sensor or reference datasets.

U.S. EPA's Performance Targets Reports define uptime in the following way:

    A measure of the amount of valid data obtained by all tested sensors
    relative to the amount of data that was expected to be obtained under
    correct, normal operation for the entire length of a test. For example, if
    valid data is collected by all three sensors for 29 days of a 30-day base
    test field deployment the uptime for the deployment can be expressed as
    96.7% (i.e., 29 days/30 days * 100%). Operation may be interrupted by
    sensor failure, connectivity issues, equipment maintenance, extreme weather
    events, etc. No matter the reason for missing data, all downtime should be
    included in the uptime calculation. However, tests may report more
    information such as specifying the percent of downtime attributed to
    various types of interruptions.

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Fri Apr 24 13:03:32 2020
Last Updated:
  Tue Nov 24 16:58:00 2020
"""
import pandas as pd


def uptime(dataframe_object, key=None):
    """Compute uptime for either sensor or reference data.

    Uptime calculated as the number of non-null data points recorded within the
    deployment period divided by the total number of data points (null + non-
    null).

    Args:
        dataframe_object (pandas dataframe or a list of dataframes):
            Sensor dataframe or list of sensor dataframes
        key (str):
            A unique identifier corresponding to the dataframe passed (either
            a serial ID, number, or other string).

    Returns:
        uptime_dict (dict):
            A dictionary containing entries for each sensor in the testing group
            and sub-dictionaries for each sensor indicating the uptime, as well
            as how many hourly periods met or did not meet the completeness
            threshold and the total number of hours that the sensors were
            sampling.

    """

    # Check whether dataframe object is single dataframe or list of dataframes
    if isinstance(dataframe_object, pd.core.frame.DataFrame):
        df_list = [dataframe_object]
    else:
        df_list = dataframe_object

    # Check if any of the above ref column names are in the passed dataframe(s)
    ref_data = bool(any(header.endswith('_Value') for header in df_list[0]))

    uptime_dict = {}

    # Compute uptime ratio for each sensor dataframe and parameter
    for sensor_number, df in enumerate(df_list, 1):
        if ref_data is True:
            if key is None:
                key = 'ref'
        else:
            if key is None:
                key = str(sensor_number)

        uptime_dict.update({key: {}})

        meets_thres = df.count().mode()[0]
        below_thres = df.isna().sum().mode()[0]
        total_hrs = meets_thres + below_thres
        uptime_value = (float(meets_thres) / total_hrs)*100

        uptime_dict[key]['Uptime'] = float("{0:.3f}".format(uptime_value))
        uptime_dict[key]['Meets Threshold'] = meets_thres
        uptime_dict[key]['Below Threshold'] = below_thres
        uptime_dict[key]['Total Hours'] = total_hrs

    return uptime_dict
