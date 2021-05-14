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
  Fri Jun 19 08:25:11 2020
Last Updated:
  Thu Aug 13 11:25:00 2020
"""
import numpy as np


def NowCast(df, column=None, return_window_df=False):
    """
    Definition
    ----------
      Generates NowCast values for PM 2.5 hourly values. Calculation referenced
      via https://airnow.zendesk.com/hc/en-us/articles/212303417-How-is-the-
      NowCast-algorithm-used-to-report-current-air-quality-

      The presentation tited 'Transitioning to a new NowCast Method' by Mintz,
      Stone, and Davis (June 15, 2013) was also used as reference for this
      function.

    Dependencies
    ------------
    NumPy:
      Mathematical operations library (written using version 1.16.5)

    Parameters
    ----------
    df: Pandas Dataframe
      The Pandas DataFrame in which PM2.5 hourly data are located. Nowcast
      values will be computed from these data.
    column: string
      The name of the column for which NowCast values will be generated. Using
      this variable over "source" is preferred, as the column varible can be
      used to identify any column header in a generalizable sense without need
      for renaming columns before and after passing to the NowCast function.
    return_window_df: Boolean
      Optional boolean parameter for return the window_df dataframe, a Pandas
      dataframe containing various columns used to compute the hourly NowCast
      value, and is particularly helpful for debugging purposes. Default is
      false.

    Returns
    -------
    window_df: Pandas Dataframe
      A dataframe containing data used to compute the hourly NowCast
      value. The index is set to time (1-hour intervals), and the columns are
      assigned by value of PM2.5 at 0 to -11 hours from particular index time.
      An additional row is included for the weight factor for each NowCast
      value. The values in columns -11 to 0 hours are actually the PM2.5 value
      for each hour multiplied by the row weight raised to the power of the
      absolute value of the hour (see references for detailed context).
    nowcast_df: Pandas Dataframe
      The nowcast dataframe for the input PM2.5 hourly data. The index is set
      to time. Data columns include the passed hourly PM2.5 data and
      the corresponding Nowcast values ('nowcast').
    """
    if column is None:
        column = df.columns[0]

    # Use standard index naming scheme
    if df.index.name != 'DateTime':
        df.index.name = 'DateTime'

    df = df[[column]]

    # Create 11 columns with PM data, each shifted by i hours (i = 1 to 11)
    for i in np.linspace(1, 11, 11, dtype=int):
        df.loc[:, column + 'shift_'+str(i)] = df[column].shift(i)

    # Compute max and min for each 12-hr window
    df['Max'] = df.max(axis=1)
    df['Min'] = df.min(axis=1)

    # Compute weight factor for each 12-hr window
    df['weight_factor'] = 1 - (df.Max - df.Min) / (df.Max)
    df['weight_factor'].values[df.weight_factor < 0.5] = 0.5

    # Count NaNs for most recent 3 hrs (including present hr data in column)
    df['row_3hr_nan_count'] = df[[column,
                                  column + 'shift_1',
                                  column + 'shift_2']].isnull().sum(axis=1)

    denom = 0
    # Multiply each column with pm data by weight factor**i, compute denom
    for i in np.linspace(1, 11, 11, dtype=int):
        df[column + 'shift_'+str(i)] = \
            df[column + 'shift_'+str(i)]*(df.weight_factor)**i

        if i == 1:
            # Determine boolean condition (not NaN) for zeroth hour PM values
            df['denom_const_0'] = df[column].notna().astype(int)
            # Denom val for zeroth hour
            denom += df['denom_const_0']*(df.weight_factor)**0

        # Determine boolean condition (not NaN) for ith hour PM values
        df['denom_const_'+str(i)] = \
            df[column + 'shift_'+str(i)].notna().astype(int)

        # Compute denominator terms for weight raised to ith power
        denom += df['denom_const_'+str(i)]*(df.weight_factor)**i

    # Column names for zeroth to 11th hour PM with weights applied
    weighted_pm_cols = list(df)[0:12]

    # Denominator and numerator for each hourly nowcast value
    df['denom'] = denom
    df['num'] = df[weighted_pm_cols].sum(axis=1)

    # Compute NowCast, set NaN where not-NaN count for 3 most recent hours < 2
    df['nowcast'] = df.num / df.denom
    df.nowcast = df.nowcast.where(df.row_3hr_nan_count < 2)

    nowcast_df = df[[column, 'nowcast']]
    window_df = df.drop(columns=['nowcast'])

    if return_window_df is True:
        return nowcast_df, window_df
    else:
        return nowcast_df
