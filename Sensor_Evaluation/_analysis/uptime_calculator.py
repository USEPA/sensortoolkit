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


def Uptime_Calculator(dataframe_object, key=None):
    """
    dataframe_object:
        single Pandas dataframe or a list of dataframes
    """

    # Check whether dataframe object is single dataframe or list of dataframes
    if isinstance(dataframe_object, pd.core.frame.DataFrame):
        df_list = [dataframe_object]
    else:
        df_list = dataframe_object

    # List of column names to check data source (reference or sensor)
    ref_names = ['BC_AE33_880nm', 'T640_2_PM10', 'T640_2_PM25',
                 'UV_633_370nm', 'Relative_Humid', 'Temperature',
                 'CAPS NO2', 'O3-API T265']

    # Check if any of the above ref column names are in the passed dataframe(s)
    if df_list[0].columns.isin(ref_names).any() == True:
        ref_data = True
    else:
        ref_data = False

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
