# -*- coding: utf-8 -*-
"""
This module contains methods for applying downsampling methods to convert
timeseries datasets at unevenly spaced sampling intervals to a uniform, evenly
spaced interval (the downsampling interval).

The downsampling interval is determined based on the variation in the orginally
recorded dataset. If, for instance, a sensor was set to record at 60 second
intervals but the interval between consecutively recorded timestamps
varied from 60 +/- 20 seconds, data may be downsampled to 120 second averages.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Tue Aug 17 10:55:08 2021
Last Updated:
  Tue Aug 17 10:55:08 2021
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def sensor_timedelta(df_list, serials):
    """
    Create dataframe with time deltas (in seconds) between subsequent data
    entries.

    Args:
        df_list (list):
            List of sensor dataframes at original, recorded sampling frequency.
        serials (dict):
            A dictionary of sensor serial identifiers for each unit in a
            testing group.

    Returns:
        delta_df (pandas DataFrame):
            A dataset containing the intervals in seconds between consecutive
            timestamps in recorded datasets. Each column corresponds to the
            time delta intervals for datasets within the passed df_list.

    """
    delta_df = pd.DataFrame()
    for serial_id, df in zip(serials.values(), df_list):
        delta = pd.Series((df.index[1:] - df.index[0:-1]).seconds)
        delta_df[serial_id] = delta

        median = delta.median()
        total_len = delta.shape[0]
        delta_drift = delta[delta != median]
        delta_drift_len = delta_drift.shape[0]

        print('..Sensor median time delta:', median, 'seconds')
        print('....Percent of sensor dataset not recorded at median time '
              'delta:', '{:3.1f}'.format(100*(delta_drift_len/total_len))
              + '%')

    return delta_df


def plot_recording_interval(delta_df):
    """Create a plot of the time delta interval vs. row index for recorded
    datasets.

    This plot indicates whether the recording interval varied in datasets during
    the duration of measurements.

    Args:
        delta_df (pandas DataFrame):
            A dataset containing the intervals in seconds between consecutive
            timestamps in recorded datasets. Each column corresponds to the
            time delta intervals for datasets within the passed df_list.

    Returns:
        None.

    """
    fig, ax = plt.subplots(1,1, figsize=(10, 6))

    for col in delta_df:
        delta_df[col].plot(ax=ax)

    ax.set_xlabel('Row Index')
    ax.set_ylabel('Recording interval delta (s)')


def timedelta_quantiles(df_list, serials):
    """Create quantile dataframe of time deltas for each dataset the in passed
    list of datasets (``df_list``).

    Args:
        df_list (list):
            List of sensor dataframes at original, recorded sampling frequency.
        serials (dict):
            A dictionary of sensor serial identifiers for each unit in a
            testing group.

    Returns:
        quant_df (pandas DataFrame):
            Dataset containing the time delta interval for measurements
            (for each dataset in the passed df_list) listed by quantile, ranging
            from 0 to 1 in 0.001 (0.1%) increments. The 0.5 quantile (50th
            percentile) corresponds to the median of time delta intervals for
            each dataset.

    """
    delta_df = sensor_timedelta(df_list, serials)

    quant = lambda x, header: delta_df[header].quantile(x)
    quant_df = pd.DataFrame()
    for col in delta_df:
        quant_data = quant(np.arange(0, 1, 0.001), col)
        quant_df[col] = quant_data

    quant_df.index = quant_df.index.values.round(3)

    return quant_df


def downsampling_interval(quant_df, thres_quant=0.99, plot_quantiles=True):
    """Check if N times the median time delta is greater than the time delta at
    a threshold quantile (default is 99%) for each dataframe.

    Say we have the following scenario where a sensor was configured to record
    data at 60 second intervals but the recording interval occasionally drifted
    to shorter or longer intervals:

    - threshold quantile (``'thres_quant'``) = 0.99 (99th percentile)
    - threshold recording interval (recording interval at the 99th percentile)
      = 115 seconds
    - median recording interval (recording interval at the 50th percentile)
      = 60 seconds

    On the first iteration of the downsampling_interval() method, the function
    will check whether 1*60 seconds is greater than the threshold recording
    interval. Since 60 < 132 seconds, this is not true, so the method will step
    the multipliying factor up by 1. The second iteration will check whether
    2*60 seconds is greater than the theshold recording interval. Since this
    is true (120 > 115 seconds), the loop will exit and indicate that the
    dataset should be downsampled to 120 second intervals.

    Args:
        quant_df (pandas DataFrame):
            Dataset containing the time delta interval for measurements
            (for each dataset in the passed df_list) listed by quantile, ranging
            from 0 to 1 in 0.001 (0.1%) increments. The 0.5 quantile (50th
            percentile) corresponds to the median of time delta intervals for
            each dataset.
        thres_quant (float, optional):
            A threshold quantile (normalized between 0 and 1) for the
            distribution of time deltas in recorded datasets. Downsampling is
            applied for time delta intervals that are the first multiple of the
            median time delta that exceeds the time delta corresponding to the
            threshold quantile. Defaults to 0.99.
        plot_quantiles (bool):
            If True, create a figure displaying the distribution of time delta
            intervals in recorded datasets (relative frequency of recorded
            time deltas within each quantile interval vs. the time delta of
            consecutive recorded timestamps). Defaults to True.

    Returns:
        interval (int or float):
            The downsampling interval, in seconds.

    """
    mult = 1
    exceed = False
    median = quant_df.loc[.50, :]
    while exceed is False:

        exceed = all(mult*median > quant_df.loc[thres_quant, :])

        if all(mult*median == quant_df.loc[thres_quant, :]):
            exceed = True
        mult += 1

    mult -= 1
    interval = mult*median.mode()[0]

    if mult != 1:
        print('A downsampling interval of ' + str(interval) +
              ' seconds exceeds the ' + '{:3.2f}'.format(thres_quant) +
              ' percentile for sensor recording intervals.')
    else:
        print('The ' + '{:3.2f}'.format(thres_quant) + ' percentile for '
              'sensor recording intervals equals the median recording interval'
              '. Recommend proceeding with median recording interval.')

    if plot_quantiles:
        plot_timedelta_quantiles(quant_df, interval, thres_quant)

    return interval


def apply_downsampling(df_list, downsampling_interval):
    """Helper function for applying downsampled averaging to datasets for the
    passed downsampling interval.

    Args:
        df_list (list):
            List of sensor dataframes at original, recorded sampling frequency.
        downsampling_interval (int or float):
            The downsampling interval, in seconds.

    Returns:
        df_list (list):
            Modified list of sensor dataframes with downsampled, uniformly
            spaced timestamp intervals.

    """
    # Downsample to mean param values for every downsampled interval
    interval = pd.to_timedelta(downsampling_interval, unit='s')

    for i, df in enumerate(df_list):
        df = df[:].groupby([pd.Grouper(freq=interval)]).mean()

        df_list[i] = df

    return df_list


def plot_timedelta_quantiles(quant_df, interval, thres_quant=0.99):
    """
    Plot timedelta vs. quantile, indicate the threshold quantile and
    downsampling interval by gray dashed lines.

    Args:
        quant_df (pandas DataFrame):
            Dataset containing the time delta interval for measurements
            (for each dataset in the passed df_list) listed by quantile, ranging
            from 0 to 1 in 0.001 (0.1%) increments. The 0.5 quantile (50th
            percentile) corresponds to the median of time delta intervals for
            each dataset.
        interval (int or float):
            The downsampling interval, in seconds.
        thres_quant (float, optional):
            A threshold quantile (normalized between 0 and 1) for the
            distribution of time deltas in recorded datasets. Downsampling is
            applied for time delta intervals that are the first multiple of the
            median time delta that exceeds the time delta corresponding to the
            threshold quantile. Defaults to 0.99.

    Returns:
        None.

    """
    fig, ax = plt.subplots(1,1, figsize=(7, 7))
    quant_df.plot(ax=ax)
    quant_label = 'Quantile Threshold (' +str(thres_quant)+')'
    ax.axvline(x=thres_quant, label=quant_label, color='gray',
               linestyle='--', linewidth=2)
    downsample_label = 'Downsampling Interval (' + str(interval) + ' s)'
    ax.axhline(y=interval, label=downsample_label, color='k',
               linestyle=':', linewidth=3)

    ax.legend(fontsize=11)

    ax.set_xlabel('Quantile (%)', fontsize=12)
    ax.set_ylabel('Recording Interval Time Delta (s)', fontsize=12)
    ax.tick_params(axis='both', labelsize=11)
