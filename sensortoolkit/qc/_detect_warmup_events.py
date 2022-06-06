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
  Thu May 26 11:16:32 2022
Last Updated:
  Thu May 26 11:16:32 2022
"""
import pandas as pd
import numpy as np

def warmup_incidents(data, param, interval=None, warmup_duration=None,
                     invalidate=False):
    """


    Args:
        data (pandas DataFrame object): DESCRIPTION.
        param (str): DESCRIPTION.
        interval (str, optional): DESCRIPTION. Defaults to None.
        warmup_duration (str, optional): DESCRIPTION. Defaults to None.
        invalidate (bool, optional): DESCRIPTION. Defaults to False.

    Raises:
        KeyError: DESCRIPTION.

    Returns:
        TYPE: DESCRIPTION.

    """
    passed_dataframe = data
    data = data[f'{param}_Value'].dropna()
    if data.dropna().empty:
        return {}

    if isinstance(data.index, pd.core.indexes.datetimes.DatetimeIndex):
        idx_name = data.index.name
        data = data.reset_index()
        if idx_name != 'DateTime':
            data = data.rename(columns={idx_name: 'DateTime'})

    if 'DateTime' not in data:
        raise KeyError('"DateTime" timestamp column not found in index')

    # Hyphens (like the hyphen in "1-minute") can cause pandas' to_timedelta()
    # function to interpret input as negative timedelta value. Remove hyphens
    # before passing to method.
    interval = interval.replace('-', ' ')
    interval = pd.to_timedelta(interval)

    data['value_grp'] = (data.DateTime.diff(1)!= interval
                              ).astype('int').cumsum()

    data = data.set_index(data.DateTime)

    invalidate_duration = warmup_duration
    for grp in data.value_grp.unique():

        grp_data = data[data.value_grp==grp]
        grp_data[f'{param}_QAQC_Flag'] = 0
        grp_start = grp_data.index.min()
        invalidate_end = grp_start + pd.to_timedelta(invalidate_duration)

        grp_data.loc[grp_start:invalidate_end, f'{param}_QAQC_Flag'] = 1
        data.loc[grp_data.index, f'{param}_Value'] = grp_data[f'{param}_Value']
        data.loc[grp_data.index, f'{param}_QAQC_Flag'] = grp_data[f'{param}_QAQC_Flag']

    data = data.drop(columns=['DateTime', 'value_grp'])

    if invalidate:
        invalid_idx = data[data[f'{param}_QAQC_Flag']==1].index
        data.loc[invalid_idx, f'{param}_Value'] = np.nan

    passed_dataframe[[f'{param}_Value', f'{param}_QAQC_Flag']] = data

    return passed_dataframe
