# -*- coding: utf-8 -*-
"""
This module contains a method for flagging consecutive data values where the
recorded value repeats multiple times.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Tue Aug 17 15:24:31 2021
Last Updated:
  Tue Aug 17 15:24:31 2021
"""
import pandas as pd
import numpy as np


def persistent_values(df, param, tolerance=3, freq='H', invalidate=False):
    """Flag data points where consecutive timestamp parameter values repeat.

    Values persisting for N or greater consecutive timestamps will be flagged
    (N is the integer value set for the tolerance).
    If invalidate is true, corresponding values will be set null (np.nan).

    Args:
        df (pandas DataFrame):
            Dataset containing parameter data to check for repeating values.
        param (str):
            The name of the parameter to check for repeating values.
        tolerance (int, optional):
            The number of consecutive entries for repeated/persistent values
            required to flag a data point. Defaults to 3.
        freq (TYPE, optional):
            The sampling frequency or averaging interval of the passed dataset,
            expressed as a pandas offset alias (see a list here
            https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases).
            Defaults to 'H' for 1-hour averaged datasets.
        invalidate (bool, optional):
            If True, repeated entries will be set null (np.nan). Defaults to
            False.

    Returns:
        df (pandas DataFrame):
            Modified dataset with flagged entries for repeated data entries.

    """
    if param + '_QAQC_Code' not in df:
        df.loc[:, param + '_QAQC_Code'] = np.nan

    if df[df[param + '_Value'].diff() == 0].empty:
        print('..no persistant values found for ' + param)
        return df

    print('..flagging persistant values for ' + param)
    data = df[param + '_Value'].copy().to_frame()

    # take the difference between consequtive data points and shift n times
    # where n is the tolerance
    window_df = pd.DataFrame()
    for i in np.arange(1, tolerance + 1, 1, dtype=int):
        window_df[param + '_diff_' + str(i)] = data[param + '_Value'].diff()

    window_df['z_count'] = (window_df == 0).astype(int).sum(axis=1)

    flag_idx = window_df[window_df.z_count == tolerance].index

    flag_idx = df.index.intersection(flag_idx)

    df.loc[flag_idx, param + '_QAQC_Code'] = 'persist'  # temporary flag

    if invalidate is True:
        df.loc[flag_idx, param + '_Value'] = np.nan

    return df


