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
  Fri Aug 28 08:45:53 2020
Last Updated:
  Tue Jul 13 09:30:40 2021
"""
import pandas as pd


def Deployment_Period(df_list, sensor_name, sensor_serials):
    """Returns a dataframe detailing the beginning, end, and duration of each
    sensor deployment at AIRS.

    Args:
        df_list (list):
            List of sensor dataframes recorded at original sampling frequency.
        sensor_name (str):
            The make and model of the sensor being evaluated.
        sensor_serials (dict):
            A dictionary of sensor serial identifiers for each unit in a
            testing group.
    Returns:
        deployment_df (pandas dataframe):
            A data frame containing the start time (‘Begin’), end time (‘End’),
            and total duration of evaluation period for each sensor in a
            deployment group.

    """

    deployment_df = pd.DataFrame(columns=['Sensor Name', 'Sensor_Number',
                                          'Sensor_Serial', 'Begin', 'End',
                                          'Duration'])

    sensor_serial_keys = list(sensor_serials.keys())
    for i, df in enumerate(df_list):

        df = df.dropna(how='all', axis=0).tz_localize(None)

        begin_time = df.index[0]
        end_time = df.index[-1]
        length = end_time - begin_time

        sensor_num = sensor_serial_keys[i]

        deployment_df.loc[i] = [sensor_name, sensor_num,
                                list(sensor_serials.values())[i],
                                begin_time, end_time, length]

    return deployment_df