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
  Tue Nov 10 14:31:42 2020
Last Updated:
  Tue Jul 13 11:42:22 2021
"""
import pandas as pd
from sensortoolkit._reference.load_ref_data import Timeframe_Search


def Synoptic_Index(df_obj, averaging_suffix=True):
    """Create a timestamp index that spans the total duration of time during
    which sensors in an evaluation group were deployed.

    Searches for the eariest and latest timestamp in sensor datasets and
    creates a datetime index at the indicated averaging interval spanning the
    time period of testing.

    Args:
        df_obj (either pandas dataframe or list of dataframes):
            Sensor dataframe(s)
        averaging_suffix (bool):
            If true, a string suffix will be returned indicating the averaging
            interval of the passed dataframe object.

    Returns:
        timestamp_idx (pandas datetimeindex):
            Index at either 1-hour or 24-hour averaging intervals spanning
            the entire evaluation period.
        avg_suffix (str):
            If averaging_suffix is true, return suffix indicating the averaging
            interval of the timestamp index.
    """
    if type(df_obj) is list:
        df = df_obj[0]  # Use the first dataframe in the list as model
        df_list = df_obj

    if type(df_obj) is pd.core.frame.DataFrame:
        df = df_obj
        df_list = [df]

    # Compute timedelta between successive timestamps
    delta = (df.index[1:] - df.index[0:-1]).to_frame()

    idx_name = delta.index.name
    if idx_name is None:
        idx_name = 'Datetime_UTC'
        delta.index.name = idx_name

    # Use mode of timedelta to extrapolate # of datapoints recorded per hr
    time_delta = delta.index.to_series().mode()[0]

    # Check time interval (1hr or 24hr)
    deploy_begin, deploy_end = Timeframe_Search(df_list)

    if time_delta == pd.Timedelta('1 H'):
        timestamp_idx = pd.date_range(start=deploy_begin,
                                      end=deploy_end,
                                      freq='H')
        avg_suffix = '_1-hour'

    elif time_delta == pd.Timedelta('1 D'):
        timestamp_idx = pd.date_range(start=deploy_begin,
                                      end=deploy_end,
                                      freq='D')
        avg_suffix = '_24-hour'

    if averaging_suffix is True:
        return timestamp_idx, avg_suffix
    else:
        return timestamp_idx