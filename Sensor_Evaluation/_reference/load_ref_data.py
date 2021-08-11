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
  Tue Jan 28 14:23:44 2020
Last Updated:
  Wed Jul 14 12:44:57 2021
"""
import pandas as pd


def Load_Ref_DataFrames(sensor_df_list, path=None, sensor_params=None):
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

    overall_begin, overall_end = Timeframe_Search(sensor_df_list)

    pm_list = ['PM1', 'PM25', 'PM10']
    gas_list = ['O3', 'NO2', 'SO2', 'CO', 'NOx']
    met_list = ['Temp', 'RH', 'Press', 'DP', 'WS', 'WD']

    pm_ref_data, gas_ref_data, met_ref_data = False, False, False

    if any(i in sensor_params for i in pm_list):
        pm_ref_data = True
    if any(i in sensor_params for i in gas_list):
        gas_ref_data = True
    if any(i in sensor_params for i in met_list):
        met_ref_data = True

    if pm_ref_data is True:
        pm_ref_df = pd.DataFrame()
    if gas_ref_data is True:
        gas_ref_df = pd.DataFrame()
    if met_ref_data is True:
        met_ref_df = pd.DataFrame()

    (pm_ref_df, gas_ref_df, met_ref_df) = (pd.DataFrame(),
                                           pd.DataFrame(),
                                           pd.DataFrame())

    if not path.endswith('/'):
        path += '/'

    for date in pd.date_range(start=overall_begin,
                              end=overall_end).to_period('M').unique():
        month = str(date.month).zfill(2)
        year = str(date.year)

        print('..{0:s}-{1:s}'.format(year, month))

        if pm_ref_data is True:
            pm_ref_df = Import_Ref_DataFrame(pm_ref_df, path,
                                             year, month,
                                             suffix='_PM')

        if met_ref_data is True:
            met_ref_df = Import_Ref_DataFrame(met_ref_df, path,
                                              year, month,
                                              suffix='_Met')

        if gas_ref_data is True:
            gas_ref_df = Import_Ref_DataFrame(gas_ref_df, path,
                                              year, month,
                                              suffix='_Gases')

    ref_dict = {'PM': pm_ref_df, 'Gases': gas_ref_df, 'Met': met_ref_df}

    return ref_dict


def Import_Ref_DataFrame(df, path, year, month, suffix=None):
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


def Timeframe_Search(sensor_df_list):
    """Determines the timeframe for which reference data should be loaded.

    Locates the beginning and end date of each hourly averaged sensor dataframe
    and subsequently determines the eariest and latest date within all recorded
    sensor datasets

    Args:
        sensor_df_list (list):
            List of sensor dataframes

    Returns:
        overall_begin (datetime.date):
            Earliest recorded date in the passed sensor dataframe list.
        overall_end (datetime.date):
            Latest recorded date in the passed sensor dataframe list.
    """
    # Determine reference data to load via begin and end timestamp for sensor
    # datasets. Choose earliest begin and latest end timestamp.
    begin_times = []
    end_times = []

    for df in sensor_df_list:

        begin_time = df.index.min().date()
        end_time = df.index.max().date()

        begin_times.append(begin_time)
        end_times.append(end_time)

    overall_begin = min(begin_times)
    overall_end = max(end_times)

    return overall_begin, overall_end
