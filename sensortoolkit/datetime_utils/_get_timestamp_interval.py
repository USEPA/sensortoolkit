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
  Wed Sep  8 11:12:46 2021
Last Updated:
  Wed Sep  8 11:12:46 2021
"""
import pandas as pd


def get_timestamp_interval(df, warning=False):
    """Compute recording interval for dataframe.

    Compute time delta between successive timestamps and take the mode of
    recorded time deltas to be the device recording interval.

    Args:
        df (pandas dataframe):
            A dataframe with time-like index.

    Returns:
        interval_str:
            A string describing the most common (mode) recording interval
            in the dataframe.
    """
    delta = (df.index[1:] - df.index[0:-1]).to_frame()
    idx_name = delta.index.name
    t_delta = delta[idx_name].mode()[0]

    delta_std = delta.std()[0].seconds

    t_delta_comps = ['days', 'hours', 'minutes', 'seconds',
                     'milliseconds', 'microseconds', 'nanoseconds']

    delta_df = pd.DataFrame(t_delta.components, columns=['value'],
                            index=t_delta_comps)

    delta_df = delta_df.where(delta_df != 0).dropna()

    interval_str = ''
    for i, (index, row) in enumerate(delta_df.iterrows(), 1):
        # If the interval has a value of one, remove the plural 's'
        if row.value == 1:
            index = index[:-1]
        interval_str += str(row.value) + ' ' + str(index)
        if i < delta_df.size:
            interval_str += ', '

    if warning and delta_std > 0:
        print('Warning, variation in sampling frequency for passed dataframe')
        #interval_str += ' +/- ' + str(delta_std) + ' seconds'

    return interval_str