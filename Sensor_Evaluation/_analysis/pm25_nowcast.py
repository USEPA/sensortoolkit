# -*- coding: utf-8 -*-
"""
@Author:
  Samuel Frederick, NSSC Contractor (ORAU)
  U.S. EPA, Office of Research and Development
  Center for Environmental Measurement and Modeling
  Air Methods and Characterization Division, Source and Fine Scale Branch
  109 T.W. Alexander Drive, Research Triangle Park, NC 27711
  Office: 919-541-4086 | Email: frederick.samuel@epa.gov

Created:
  Fri Jun 19 08:25:11 2020
Last Updated:
  Thu Aug 13 11:25:00 2020
"""
import numpy as np
import pandas as pd
import sys


def PM25NowCast(df, column=None):
    """Generate NowCast values for PM2.5 1-hour averages.

    References
    ----------
    https://usepa.servicenowservices.com/airnow?id=kb_article_view&sys_id=
    fed0037b1b62545040a1a7dbe54bcbd4

    The presentation tited 'Transitioning to a new NowCast Method' by
    Mintz, Stone, and Davis (June 15, 2013)

    Dependencies
    ------------
    NumPy (version >= 1.16.5):
        Mathematical operations library
    Pandas (version >= 0.25.1):
        Data analysis library
    Sys (Python version >= 3.7):
        Python base package for system specified parameters

    Arguments
    ----------
    df (Pandas dataframe object):
        DataFrame containing hourly PM2.5 data.
    column (str):
        The name of the column to NowCast.

    Returns
    -------
    nowcast_df: Pandas Dataframe
        Dataframe passed to function with added column for nowcasted values.
        The index is set  to time. Data columns include the passed hourly PM2.5
        data and the corresponding Nowcast values ('nowcast').
    """
    if column is None:
        sys.exit('No column header name specified to nowcast')

    df_idx = df.index
    idx_name = df_idx.name
    # Use standard index naming scheme
    if idx_name is None:
        df.index.name = 'DateTime_UTC'

    # Check type of index column, must be datetime formatted
    if type(df_idx) != pd.core.indexes.datetimes.DatetimeIndex:
        sys.exit('Index must be data type '
                 'pandas.core.indexes.datetimes.DatetimeIndex')

    # Reindex to evenly spaced 1-hour intervals
    df_idx_min = df.index.min()
    df_idx_max = df.index.max()
    idx = pd.date_range(start=df_idx_min, end=df_idx_max, freq='H')
    reindex_df = pd.DataFrame(index=idx)
    df = df.combine_first(reindex_df)

    # subset passed dataframe to specified column for nowcasting, set aside
    # copy of passed dataframe for merging before returning dataframe.
    passed_df = df
    df = df[[column]].copy()

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

    nowcast_df = df[['nowcast']].rename(columns={'nowcast':
                                                 column + '_nowcast'})

    return passed_df.join(nowcast_df)
