# -*- coding: utf-8 -*-
"""
This module contains methods for importing reference datasets (i.e., datasets
containing reference measurements that have been processed into the SDFS format
following use of the ``sensortoolkit.lib_utils.ReferenceSetup()`` method).

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Tue Jan 28 14:23:44 2020
Last Updated:
  Wed Jul 14 12:44:57 2021
"""
import os
import pandas as pd
from sensortoolkit.datetime_utils import interval_averaging

def load_ref_dataframes(bdate, edate, path, classes):
    """Load reference data for the parameters measured by the sensors in the
    passed sensor dataframe list and for the timeframe indicated by sensor
    dataset timestamps.

    Args:
        sensor_df_list (list):
            List of sensor dataframes.
        path (str):
            Full directory path to reference data.
        sensor_params (set):
            A unique listing of parameters measured by the
            sensor make and model being evaluated.

    Returns:
        ref_dict (dict):
            Dictionary containing reference datasets organized by parameter
            classification (keys).

    """
    print("Loading reference dataframes")

    pm_ref_data, gas_ref_data, met_ref_data = False, False, False

    if 'PM' in classes:
        pm_ref_data = True
    if 'Gases' in classes:
        gas_ref_data = True
    if 'Met' in classes:
        met_ref_data = True

    (pm_h_ref_df, gas_h_ref_df, met_h_ref_df) = (pd.DataFrame(),
                                                 pd.DataFrame(),
                                                 pd.DataFrame())

    (pm_d_ref_df, gas_d_ref_df, met_d_ref_df) = (pd.DataFrame(),
                                                 pd.DataFrame(),
                                                 pd.DataFrame())

    for date in pd.date_range(start=bdate, end=edate).to_period('M').unique():
        month = str(date.month).zfill(2)
        year = str(date.year)

        print('..{0:s}-{1:s}'.format(year, month))

        if pm_ref_data is True:
            # Import 1-hr averaged data
            pm_h_ref_df = import_ref_dataframe(pm_h_ref_df, path,
                                               year, month,
                                               suffix='_PM')
        if met_ref_data is True:
            # Import 1-hr averaged data
            met_h_ref_df = import_ref_dataframe(met_h_ref_df, path,
                                                year, month,
                                                suffix='_Met')
        if gas_ref_data is True:
            # Import 1-hr averaged data
            gas_h_ref_df = import_ref_dataframe(gas_h_ref_df, path,
                                                year, month,
                                                suffix='_Gases')

    # Compute 24-hr averaged data
    print('Computing 24-hour averaged reference datasets')
    if pm_ref_data is True:
        pm_d_ref_df = interval_averaging(pm_h_ref_df,
                                         freq='D',
                                         interval_count=24,
                                         thres=0.75)
    if met_ref_data is True:
        met_d_ref_df = interval_averaging(met_h_ref_df,
                                          freq='D',
                                          interval_count=24,
                                          thres=0.75)
    if gas_ref_data is True:
        gas_d_ref_df = interval_averaging(gas_h_ref_df,
                                          freq='D',
                                          interval_count=24,
                                          thres=0.75)

    ref_dict = {'PM': {'1-hour': pm_h_ref_df,
                       '24-hour':  pm_d_ref_df},
                'Gases': {'1-hour': gas_h_ref_df,
                          '24-hour':  gas_d_ref_df},
                'Met': {'1-hour': met_h_ref_df,
                        '24-hour':  met_d_ref_df}
                }

    return ref_dict


def import_ref_dataframe(df, path, year, month, suffix=None):
    """Import reference data for the specified monthly period and parameter
    classification.

    Args:
        df (pandas dataframe):
            Constructor dataframe containing reference data (FRM/FEM) at 1-hour
            averaged intervals. Data loaded by this module are appended to the
            constructor dataframe and returned.
        path (str):
            Full path to reference data directory where files are located.
        year (str):
            The year (YYYY) for which data will be loaded.
        month (str):
            The month (MM) for which data will be loaded.
        suffix (str):
            The parameter classification ('PM', 'Gases', or 'Met') indicating
            the type of reference data to be imported.

    Returns:
        df (pandas dataframe):
            Modified dataframe with imported data appended to the passed
            dataset. Contains reference data (FRM/FEM) at 1-hour averaged
            intervals.

    """
    try:
        filename = f'H_{year}{month}{suffix}.csv'
        load_df = pd.read_csv(os.path.join(path, filename),
                              parse_dates=['DateTime'], index_col='DateTime')

        # Append loaded dataframe based on the first instance of a timestamp
        # index value (i.e., avoid duplicate index values by combining only
        # new timestamp indecies with the primary dataframe 'df')
        df = df.combine_first(load_df)

        print('....' + filename)

    except FileNotFoundError:
        print("Warning, file not found:", filename)
        pass

    return df
