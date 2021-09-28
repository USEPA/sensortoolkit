# -*- coding: utf-8 -*-
"""
@Author:
    | Samuel Frederick, NSSC Contractor (ORAU)
    | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Tue Jan 28 14:23:44 2020
Last Updated:
  Wed Jul 14 12:44:57 2021
"""
import pandas as pd
#from sensortoolkit.datetime_utils import timeframe_search
#from sensortoolkit.param import Parameter

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

    #overall_begin, overall_end = timeframe_search(sensor_df_list)

    # pm_list = [param for param in Parameter.__param_dict__
    #            if Parameter(param).classifier == 'PM']
    # gas_list = [param for param in Parameter.__param_dict__
    #             if Parameter(param).classifier == 'Gases']
    # met_list = [param for param in Parameter.__param_dict__
    #             if Parameter(param).classifier == 'Met']

    pm_ref_data, gas_ref_data, met_ref_data = False, False, False

    if 'PM' in classes:
        pm_ref_data = True
    if 'Gases' in classes:
        gas_ref_data = True
    if 'Met' in classes:
        met_ref_data = True

    (pm_ref_df, gas_ref_df, met_ref_df) = (pd.DataFrame(), pd.DataFrame(),
                                           pd.DataFrame())

    if not path.endswith('/'):
        path += '/'

    for date in pd.date_range(start=bdate, end=edate).to_period('M').unique():
        month = str(date.month).zfill(2)
        year = str(date.year)

        print('..{0:s}-{1:s}'.format(year, month))

        if pm_ref_data is True:
            pm_ref_df = import_ref_dataframe(pm_ref_df, path,
                                             year, month,
                                             suffix='_PM')

        if met_ref_data is True:
            met_ref_df = import_ref_dataframe(met_ref_df, path,
                                              year, month,
                                              suffix='_Met')

        if gas_ref_data is True:
            gas_ref_df = import_ref_dataframe(gas_ref_df, path,
                                              year, month,
                                              suffix='_Gases')

    ref_dict = {'PM': {'1-hour': pm_ref_df,
                       '24-hour':  pd.DataFrame()},
                'Gases': {'1-hour': gas_ref_df,
                          '24-hour':  pd.DataFrame()},
                'Met': {'1-hour': met_ref_df,
                        '24-hour':  pd.DataFrame()}
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
        filename = 'H_' + year + month + suffix + '.csv'
        load_df = pd.read_csv(path + filename, parse_dates=['DateTime_UTC'],
                              index_col='DateTime_UTC')

        # Append loaded dataframe based on the first instance of a timestamp
        # index value (i.e., avoid duplicate index values by combining only
        # new timestamp indecies with the primary dataframe 'df')
        df = df.combine_first(load_df)

        print('....' + filename)

    except FileNotFoundError:
        print("Warning, file not found:", filename)
        pass

    return df
