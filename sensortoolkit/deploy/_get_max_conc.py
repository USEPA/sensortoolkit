# -*- coding: utf-8 -*-
"""
This module contains a method for determining the highest concentration recorded
by passed dataframes within the testing period (including sensor and/or
reference data).

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Sep  8 12:11:43 2021
Last Updated:
  Wed Sep  8 12:11:43 2021
"""
import numpy as np

def get_max_conc(param, df_list=None, ref_df=None, bdate=None, edate=None):
    """Determine maximum concentration measured across passed dataframes.

    If both sensor dataframes are passed to ``df_list`` and a reference
    dataframe is passed to ``ref_df``, the maximum will be computed across
    both sensor and reference concentrations.

    Args:
        param (str): The name of the evaluation parameter.
        df_list (list of pandas dataframes, optional): A list of sensor
            dataframes. Defaults to None.
        ref_df (pandas dataframe, optional): Reference dataframe. Defaults to
            None. If dataframe passed, will be considered in calculation of
            maximum concentration.
        bdate (str, optional): The starting timestamp to begin search. Defaults
            to None, will use the earliest timestamp recorded in datasets.
        edate (str, optional): The ending timestamp to end search. Defaults
            to None, will use the latest timestamp recorded in datasets.

    Returns:
        max_conc (float):
            The maximum concentration indicated by the dataframes passed to the
            function for the specified parameter.

    Raises:
        TypeError: If `df_list` and `ref_df` are both ``None`` (i.e., no
            dataframes passed to function).

    """
    if df_list is None and ref_df is None:
        raise TypeError('Get_Max() missing required dataframe objects: '
                        '"df_list" and/or "ref_df"')

    max_list = [df.loc[bdate:edate, param + '_Value'].max() for df in df_list]

    if ref_df is not None:
        ref_max = ref_df.loc[bdate:edate, param + '_Value'].max()
        max_list.append(ref_max)

    # Remove nans
    max_list = [i for i in max_list if not np.isnan(i)]
    max_conc = max(max_list)

    return max_conc
