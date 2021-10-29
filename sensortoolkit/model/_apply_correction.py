# -*- coding: utf-8 -*-
"""
This module contains a method for applying a linear correction to an individual
sensor dataset based off the ordinary least-squares regression between
collocated sensor and FRM/FEM measurements. 

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Fri Oct 30 08:53:18 2020
Last Updated:
  Wed Jul 14 10:29:53 2021
"""


def individual_corr(param=None, df_list=None, stats_df=None):
    """Apply an individual correction to each sensor dataset based on the
    OLS regression slope and intercept values in the passed statistics
    dataframe.

    Args:
        param (str):
            The evaluation parameter.
        df_list (list):
            List of sensor dataframes.
        stats_df (pandas dataframe):
            Statistics dataframe containing OLS regression statisitcs including
            slope and intercept for either sensor vs. FRM/FEM regression or
            sensor vs. intersensor regression.
    Return:
        df_list (list):
            List of modified dataframes with column added for corrected
            parameter values.

    """
    for i, (df, m, b) in enumerate(zip(df_list, stats_df.Slope,
                                       stats_df.Intercept)):
        corr = (df[param + '_Value'] - b) / m

        df[param + '_indiv_corr'] = corr
        df_list[i] = df

    return df_list
