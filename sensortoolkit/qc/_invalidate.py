# -*- coding: utf-8 -*-
"""
This module contains a method for invalidating (set null or empty) a period of
data recorded at consecutive timestamps for a specified time frame and 
parameter.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Tue Aug 17 15:25:16 2021
Last Updated:
  Tue Aug 17 15:25:16 2021
"""
import numpy as np

def invalidate_period(df, param, bdate, edate):
    """Invalidate data by manually indicating a period of time.

    Data within the indicated start and end timestamps will be invaldiated
    (i.e., values set np.nan) and the parameter QAQC column will indicate data
    have been modified by flagging as type #2

    # TODO: Come back to flagging number scheme

    Args:
        df (pandas DataFrame):
            Dataset containing timeseries data that will be invalidated.
        param (str):
            The name of the parmeter to invalidate.
        bdate (str):
            The beginning timestamp for data invalidation in
            'YYYY-MM-DD HH:MM:SS' format.
        edate (str):
            The ending timestamp for data invalidation in 'YYYY-MM-DD HH:MM:SS'
            format.

    Returns:
        df (pandas DataFrame):
            Modified dataset with invalidated data.

    """
    df.loc[bdate:edate, param + '_Value'] = np.nan
    df.loc[bdate:edate, param + '_QAQC_Code'] = 2  # temporary flag
    return df
