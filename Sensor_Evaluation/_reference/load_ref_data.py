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
  Mon Sep 4 10:52:00 2020
"""
import pandas as pd


def Load_Ref_DataFrames(sensor_df_list, path=None, namespace=None):
    """
    Definition
    ----------
    Locates reference data via 'path' variable for PM and meteorological
    parameters. Data are combined into reference dataframes (..._ref_df) and
    timestamp is set to index. Strings in data files, such as "NoData" are
    forced to NaN. Subsequently, dataframes (...ref_df with minute resolution
    data) are averaged to hourly data (..._hourly_ref_df), and these dataframes
    are time-shifted by 5 hours to set timestamps to UTC.
    """

    print("Loading reference dataframes")

    overall_begin, overall_end = Timeframe_Search(sensor_df_list)

    pm_list = ['PM1', 'PM25', 'PM10']
    gas_list = ['O3', 'NO2', 'SO2', 'CO', 'NOx']
    met_list = ['Temp', 'RH', 'Press', 'DP', 'WS', 'WD']

    pm_ref_data, gas_ref_data, met_ref_data = False, False, False

    if any(i in namespace for i in pm_list):
        pm_ref_data = True
    if any(i in namespace for i in gas_list):
        gas_ref_data = True
    if any(i in namespace for i in met_list):
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

    try:
        filename = 'H_' + year + month + suffix + '.csv'
        load_df = pd.read_csv(path + filename, parse_dates=['DateTime_UTC'],
                              index_col='DateTime_UTC')

        df = df.append(load_df)

        print('....' + filename)

    except FileNotFoundError:
        print("Warning, file not found:", filename)
        pass

    return df


def Timeframe_Search(sensor_df_list):
    """
    Definition
    ----------
    Determines the timeframe for which reference data should be loaded by
    locating the beginning and end time of each hourly averaged dataframe and
    subsequently determining the extrema of begin/end times.
    """
    # Determine reference data to load via begin and end timestamp for sensor
    # datasets. Choose earliest begin and latest end timestamp.
    begin_times = []
    end_times = []

    for df in sensor_df_list:

        begin_time = df.index[0].date()
        end_time = df.index[-1].date()

        begin_times.append(begin_time)
        end_times.append(end_time)

    overall_begin = min(begin_times)
    overall_end = max(end_times)

    return overall_begin, overall_end
