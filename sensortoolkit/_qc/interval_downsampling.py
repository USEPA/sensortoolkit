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
  Tue Aug 17 10:55:08 2021
Last Updated:
  Tue Aug 17 10:55:08 2021
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def Sensor_TimeDelta(df_list, serials):
    """
    Create dataframe with time deltas (in seconds) between subsequent data
    entries.

    Args:
        df_list (TYPE): DESCRIPTION.
        serials (TYPE): DESCRIPTION.

    Returns:
        delta_df (TYPE): DESCRIPTION.

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


def Plot_RecordingInterval(delta_df):
    """


    Args:
        delta_df (TYPE): DESCRIPTION.

    Returns:
        None.

    """
    fig, ax = plt.subplots(1,1, figsize=(10, 6))

    for col in delta_df:
        delta_df[col].plot(ax=ax)

    ax.set_xlabel('Row Index')
    ax.set_ylabel('Recording interval delta (s)')


def TimeDelta_Quantiles(df_list, serials):
    """
    Create quantile dataframe for time deltas in the delta_df for each sensor

    Args:
        df_list (TYPE): DESCRIPTION.
        serials (TYPE): DESCRIPTION.

    Returns:
        quant_df (TYPE): DESCRIPTION.

    """
    delta_df = Sensor_TimeDelta(df_list, serials)

    quant = lambda x, header: delta_df[header].quantile(x)
    quant_df = pd.DataFrame()
    for col in delta_df:
        quant_data = quant(np.arange(0, 1, 0.001), col)
        quant_df[col] = quant_data

    quant_df.index = quant_df.index.values.round(3)

    return quant_df


def DownSampling_Interval(quant_df, thres_quant=0.99, plot_quantiles=True):
    """
    Check if N times the median time delta is greater than the time delta at
    the 99% quantile for each dataframe.

    E.g., if median recording interval is 60 seconds, on the first loop the
    code will check whether 2*60=120 seconds is greater than the 99th
    percentile of recording intervals within each dataset. If this is true
    for all dataframes, exit the loop. Otherwise step the value of 'mult'
    by one and repeat the loop.

    Args:
        quant_df (TYPE): DESCRIPTION.
        thres_quant (TYPE, optional): DESCRIPTION. Defaults to 0.99.
        plot_quantiles (TYPE): Defaults to True.

    Returns:
        interval (TYPE): DESCRIPTION.

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
        Plot_TimeDelta_Quantiles(quant_df, interval, thres_quant)

    return interval


def Apply_DownSampling(df_list, downsampling_interval):
    # Downsample to mean param values for every downsampled interval
    interval = pd.to_timedelta(downsampling_interval, unit='s')

    for i, df in enumerate(df_list):
        df = df[:].groupby([pd.Grouper(freq=interval)]).mean()

        df_list[i] = df

    return df_list


def Plot_TimeDelta_Quantiles(quant_df, interval, thres_quant=0.99):
    """
    Plot timedelta vs. qunatile, indicate the threshold quantile and
    downsampling interval by gray dashed lines.

    Args:
        quant_df (TYPE): DESCRIPTION.
        interval (TYPE): DESCRIPTION.
        thres_quant (TYPE, optional): DESCRIPTION. Defaults to 0.99.

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


if __name__ == '__main__':

    quant_df = TimeDelta_Quantiles(Eval.full_df_list, Eval.serials)
    interval = DownSampling_Interval(quant_df, thres_quant=0.95)

    # Consider adding a qc flag or something to the datasets that have been
    # downsampled

    #modified_df_list = Apply_DownSampling(Eval.full_df_list,
    #                                      downsampling_interval=interval)

