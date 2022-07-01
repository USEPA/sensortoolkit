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


    n_warmups = len(data.value_grp.dropna().unique())
    print(f'{n_warmups} warmup events detected')

    invalidate_duration = pd.to_timedelta(warmup_duration)
    data = data.groupby('value_grp').apply(lambda x:
                                            write_warmup_code(x, param,
                                                              invalidate_duration))

    data = data.drop(columns=['DateTime', 'value_grp'])

    if invalidate:
        invalid_idx = data[data[f'{param}_QAQC_Code']=='WarmUp'].index
        data.loc[invalid_idx, f'{param}_Value'] = np.nan

    passed_dataframe[[f'{param}_Value', f'{param}_QAQC_Code']] = data

    return passed_dataframe


def write_warmup_code(series, param, invalidate_duration):
    i = series.value_grp.unique()[0]

    if i % 1000 == 0:
        print(f'..{i}')

    idx_min = series.index.min()
    idx_max = idx_min + invalidate_duration
    series.loc[idx_min:idx_max, f'{param}_QAQC_Code'] = 'WarmUp'

    return series
