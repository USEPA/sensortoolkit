# -*- coding: utf-8 -*-
"""
This module contains a method for detailing the deployment period (start,
end, and duration) for sensor testing.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Fri Aug 28 08:45:53 2020
Last Updated:
  Tue Jul 13 09:30:40 2021
"""
import pandas as pd


def deployment_period(df_list, sensor_name, sensor_serials):
    """Returns a dataframe detailing the beginning, end, and duration of each
    sensor deployment.

    Args:
        df_list (list):
            List of sensor dataframes recorded at original sampling frequency.
        sensor_name (str):
            The make and model of the sensor being evaluated.
        sensor_serials (dict):
            A dictionary of sensor serial identifiers for each unit in a
            testing group.
    Returns:
        deployment_df (pandas DataFrame):
            A data frame containing the start time (‘Begin’), end time (‘End’),
            and total duration of evaluation period for each sensor in a
            deployment group.

    """

    deployment_df = pd.DataFrame(columns=['Sensor Name', 'Sensor_Number',
                                          'Sensor_Serial', 'Begin', 'End',
                                          'Duration'])

    sensor_serial_keys = list(sensor_serials.keys())
    for i, df in enumerate(df_list):

        df = df.dropna(how='all', axis=0)#.tz_localize(None)

        begin_time = df.index[0]
        end_time = df.index[-1]
        length = end_time - begin_time

        sensor_num = sensor_serial_keys[i]

        deployment_df.loc[i] = [sensor_name, sensor_num,
                                list(sensor_serials.values())[i],
                                begin_time, end_time, length]

    return deployment_df
