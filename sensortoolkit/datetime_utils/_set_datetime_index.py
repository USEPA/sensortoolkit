# -*- coding: utf-8 -*-
"""
This module contains a method for assigning the ``DateTime`` column
as the pandas DataFrame index.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Sep  8 11:42:00 2021
Last Updated:
  Wed Sep  8 11:42:00 2021
"""
import pandas as pd

def set_datetime_index(df, idx_fmt=None):
    """Set the ``DateTime`` timestamp column as the index.

    Args:
        df (pandas DataFrame):
            Sensor DataFrame for which the index is being assigned.
        idx_fmt (str):
            The formatting for the timestamp index. If none, date/time format
            will be inferred (slower). Explicitly specifying the format speeds
            up index assignment as ``pandas.to_datetime()`` doesn't have to
            search for the appropriate formatting.

    Return:
        df (pandas DataFrame):
            Modified sensor DataFrame with the index assigned as the
            ``DateTime`` column.

    Raises:
        NameError: If the column header ``DateTime`` is not found in the
            DataFrame (may occur if the user assigns a label other than
            ``DateTime`` to the time-like index during the process of data
            ingestion.)

    """
    try:

        df = df.set_index(pd.to_datetime(df['DateTime'], format=idx_fmt)
                          ).drop(columns={'DateTime'})
    except NameError:
        print('Error: Sensor timestamp header "DateTime" not in passed '
              'DataFrame. Please save processed DataFrame with timestamp index'
              'header named "DateTime"')
    return df
