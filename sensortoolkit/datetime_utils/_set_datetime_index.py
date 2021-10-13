# -*- coding: utf-8 -*-
"""
Description.

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
    """Set the DateTime_UTC timestamp column as the index.

    Args:
        df (pandas dataframe):
            Sensor dataframe for which the index is being assigned
        idx_fmt (str):
            The foramtting for the timestamp index. Explicitly specifying the
            format speeds up index assignment as pd.to_datetime doesn't have to
            search for the appropriate formatting.

    Return:
        df (pandas dataframe):
            Modified sensor dataframe with the index assigned as the
            'DateTime_UTC' column.

    Raises:
        NameError: If the column header 'DateTime_UTC' is not found in the
        dataframe (may occur if the user assigns a label other than
        'DateTime_UTC' to the time-like index during the process of data
        ingestion.)
    """
    try:

        df = df.set_index(pd.to_datetime(df['DateTime_UTC'], format=idx_fmt)
                          ).drop(columns={'DateTime_UTC'})
    except NameError:
        print('Error: Sensor timestamp header "DateTime_UTC" not in passed '
              'dataframe. Please save processed dataframe with timestamp index'
              'header named "DateTime_UTC"')
    return df
