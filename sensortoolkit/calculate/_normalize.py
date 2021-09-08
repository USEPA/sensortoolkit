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
  Tue Mar 17 14:41:13 2020
Last Updated:
  Wed Jul 14 08:20:29 2021
"""
import numpy as np


def normalize(df_list, ref_df, param=None, ref_name=None):
    """Normalize sensor measurements at 1-hour or 24-hour intervals by
    concurrent measurements from a collocated FRM/FEM monitor.

    Args:
        df_list (list):
            List of sensor dataframes with datetimeindex at either 1-hour or
            24-hour averaging intervals.

        ref_df (pandas dataframe):
            Dataframe with FRM/FEM measurements from a reference monitor
            collocated alongside sensors at a monitoring site. Dataframe at
            either 1-hour or 24-hour averaging intervals, matches interval of
            df_list.
        param (str):
            The evaluation parameter.
        ref_name (str):
            The make and model of the FRM/FEM monitor.
    Returns
        df_list (list):
            Modified list of sensor dataframes with a column added for
            normalized parameter values.
    """
    print('Computing normalized', param, 'values (by', ref_name + ')')

    for i, df in enumerate(df_list):
        try:
            df['Normalized_'+param] = df[param] / ref_df[param + '_Value']
        except KeyError as k:
            print('...Warning', k, 'not found in dataframe at index ', str(i))
            df['Normalized_' + param] = np.nan
        df_list[i] = df

    return df_list
