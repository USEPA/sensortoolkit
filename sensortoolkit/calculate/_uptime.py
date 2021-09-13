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
        key ():
            A unique identifier corresponding to the dataframe passed (either
            a serial ID, number, or other string).
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
        uptime = (float(meets_thres) / total_hrs)*100

        uptime_dict[key]['Uptime'] = float("{0:.3f}".format(uptime))
        uptime_dict[key]['Meets Threshold'] = meets_thres
        uptime_dict[key]['Below Threshold'] = below_thres
        uptime_dict[key]['Total Hours'] = total_hrs

    return uptime_dict
