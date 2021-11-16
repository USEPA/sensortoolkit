# -*- coding: utf-8 -*-
"""
This module calculates U.S.EPA's NowCast for fine particulate matter
(:math:`PM_{2.5}`) for data recorded or averaged to 1-hour measurement
intervals.

For reporting changes in air quality at high time-resolution, U.S.
EPA’s NowCast calculates hourly :math:`PM_{2.5}` concentration values via a
12-hour window of hourly :math:`PM_{2.5}` measurements. Values are weighted
based on the range of concentration levels observed within the 12-hour window,
whereby large changes result in greater weighting of recent hours while steady
air conditions result in more evenly distributed weighting of hourly
concentrations.

Module Dependencies
-------------------
* Python (version >= 3.7):
    Programming language. Module tested with Python versions 3.7 and
    version 3.8.
* NumPy (version >= 1.16.5):
    Mathematical operations library. Module tested with versions 1.16.5
    through 1.20.1.
* Pandas (version >= 0.25.1):
    Data analysis library. Module tested with versions 0.25.1 through
    1.2.4.


Calculation
-----------

The NowCast for a selected (current) hour is computed via the following steps:

    1. Select a 12-hour window of PM measurements whereby the oldest hour in the
       selection is 11 hours preceding the current hour. The most recent
       (current) hour is the hour for which the NowCast will be computed. **At
       least two of the last three hours (including the current hour) must have
       concentration values to compute the NowCast.**

    2. From this 12-hour window, select the maximum and minimum PM
       concentrations present. Compute the range by subtracting the minimum from
       the maximum.

    3. Normalize the range by dividing by the maximum concentration value. This
       gives a measure of the rate of change of PM values within the 12-hour
       window.

    4. Compute the weight factor by subtracting the normalized rate of change
       from 1.

    5. If the weight factor is less than 0.5, round the value up to 0.5. The
       weight factor must fall within the range 0.5 to 1.0.

    6. Multiply each hour in the 12-hour window by the weight factor raised to
       the power of the number of hours ago that the value was recorded. The
       most recent (current) hour in the series is raised to the zeroth power
       and the oldest hour is raised to the 11th power.

    7. Sum the weighted PM values computed in the previous step for each hour
       in the 12-hour window.

    8. In a similar method to steps 6 and 7, compute the sum of the weight
       factor raised to the 0th through 11th power. This sum includes 12 terms,
       whereby the power of each term corresponds to the number of hours ago
       that a concentration value was recoded.

    9. Divide the weighted concentration sum calculated in step 7 by the sum
       determined in step 8. The result is the NowCast for the zeroth (current)
       hour in the 12-hour window.

Resources
---------

    `Technical information about the NowCast algorithm
    <https://usepa.servicenowservices.com/airnow?id=kb_article_view&
    sys_id=fed0037b1b62545040a1a7dbe54bcbd4>`_

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Fri Jun 19 08:25:11 2020
Last Updated:
  Thu Sep 7 16:41:00 2021
"""
import sys
import numpy as np
import pandas as pd
from sensortoolkit.calculate import aqi

def nowcast_pm25(df, column=None):
    """Compute NowCast values for fine particulate matter (:math:`PM_{2.5}`)
    1-hour averages.

    **Resources:**

        * `Technical information about the NowCast algorithm
          <https://usepa.servicenowservices.com/airnow?id=kb_article_view&
          sys_id=fed0037b1b62545040a1a7dbe54bcbd4>`_

        * The presentation titled `Transitioning to a new NowCast Method` by
          Mintz, Stone, and Davis (June 15, 2013)

    Args:
        df (Pandas dataframe object): DataFrame containing hourly PM2.5 data.
        column (str): The name of the column to NowCast.

    Returns:
        nowcasted_df (pandas DataFrame):
            Dataframe passed to function with added column for nowcasted values.
            The index is set to time. Data columns include the passed hourly
            PM2.5 data and the corresponding Nowcast values ('nowcast').

    """
    if column is None:
        sys.exit('No column header name specified to nowcast')

    df_idx = df.index
    idx_name = df_idx.name
    # Use standard index naming scheme
    if idx_name is None:
        df.index.name = 'DateTime'

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

    # Compute NowCast AQI
    df = aqi(df, column='nowcast')

    nowcast_df = df[['nowcast', 'AQI', 'AQI_Category']]
    nowcast_df = nowcast_df.rename(
                    columns={'nowcast': column + '_nowcast',
                             'AQI': column + '_nowcast_aqi',
                             'AQI_Category': column + '_nowcast_aqi_category'})

    nowcasted_df = passed_df.join(nowcast_df)

    return nowcasted_df

