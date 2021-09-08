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
        df (TYPE): DESCRIPTION.
        param (TYPE): DESCRIPTION.
        tolerance (TYPE, optional): The number of consecutive entries for
        repeated/persistent values required to flag a data point. Defaults
        to 3.
        freq (TYPE, optional): DESCRIPTION. Defaults to 'H'.
        invalidate (TYPE, optional): DESCRIPTION. Defaults to False.

    Returns:
        df (TYPE): DESCRIPTION.

    """
    if param + '_QAQC_Code' not in df:
        df.loc[:, param + '_QAQC_Code'] = np.nan

    if df[df[param].diff() == 0].empty:
        print('..not persistant values found for ' + param)
        return df

    print('..flagging persistant values for ' + param)
    data = df[param].copy().to_frame()

    # take the difference between consequtive data points and shift n times
    # where n is the tolerance
    window_df = pd.DataFrame()
    for i in np.arange(1, tolerance + 1, 1, dtype=int):
        window_df[param + '_diff_' + str(i)] = \
            data[param].diff().shift(i, freq=freq)

    window_df['z_count'] = (window_df == 0).astype(int).sum(axis=1)

    flag_idx = window_df[window_df.z_count == tolerance].index

    df.loc[flag_idx, param + '_QAQC_Code'] = 1  # temporary flag

    if invalidate is True:
        df.loc[flag_idx, param] = np.nan

    return df
