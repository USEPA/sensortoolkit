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
  Mon Aug  9 09:30:03 2021
Last Updated:
  Mon Aug  9 09:30:03 2021
"""
import pandas as pd
import numpy as np
from Sensor_Evaluation._analysis.time_averaging import Interval_Averaging
import os
import pathlib
import datetime


def Ingest_OAQPS(file_path):
    """Read raw csv data and format timestamps, column headers.


    Args:
        file_path (TYPE): DESCRIPTION.

    Returns:
        df (TYPE): DESCRIPTION.

    """

    df = pd.read_csv(file_path, header=2)

    df = df[1:-8]
    df = Format_Ref_Timestamp(df)

    # Formatting changed in Feb 2020 for some headers, rename for consistency
    # with former column naming scheme
    rename_dict = {'10M_Wind_Direction': 'WD Ultra 10m',
                   '10M_Wind_Speed': 'WS Ultra 10m',
                   '3M_RH': '3m RH',
                   '3M_Temp': '3m Temp',
                   'BC_880nm_AE33 LC': 'BC AE33 880nm',
                   'GRIMM_PM1': 'GRIMM PM1',
                   'GRIMM_PM10': 'Grimm PM10',
                   'GRIMM_PM2.5': 'Grimm PM2.5',
                   'T265_O3': 'O3-API T265'}
    df = df.rename(columns=rename_dict)

    df = df.set_index(df.DateTime_UTC).drop(columns=['DateTime_UTC'])
    df = Format_Headers(df)

    return df


def Process_OAQPS(data_path, lib_path):
    """Loop through list of raw datasets, convert to standard format, save
    processed datasets to file at recorded and 1-hour averaged intervals.


    Args:
        data_path (TYPE): DESCRIPTION.

    Returns:
        None.

    """

    for item in os.listdir(data_path):
        if not item.endswith('.csv') and not item.startswith('min'):
            continue
        print(item)

        file = pathlib.Path(str(data_path) + '//' + item)
        df = Ingest_OAQPS(str(file))

        # Modify time
        mtime = datetime.datetime.fromtimestamp(file.stat().st_mtime)
        df['Data_Acquisition_Date_Time'] = mtime

        # Shift dataframes to UTC (ahead five hours)
        df = df.shift(5, freq='H')

        h_df = Interval_Averaging(df, freq='H', interval_count=60, thres=0.75)

        processed_m_path = (lib_path + '/Data and Figures/reference_Data/'
                            'oaqps/processed_data/' + item)
        processed_h_path = (lib_path + '/Data and Figures/reference_Data/'
                            'oaqps/processed_data/' + item.replace('min', 'H'))
        df.to_csv(processed_m_path)
        h_df.to_csv(processed_h_path)


def Format_Ref_Timestamp(df):
    """


    Args:
        df (TYPE): DESCRIPTION.

    Returns:
        df (TYPE): DESCRIPTION.

    """
    split_timestamp = False
    # Date and Time columns seperated after MM-YYYY
    if 'DateTime' and 'Time' in df:
        df['Date & Time'] = df.DateTime + ' ' + df.Time
        split_timestamp = True

    # Split the datetime column into separate date and time info
    split_datetime = df['Date & Time'].str.split(expand=True)

    # Assumes M/D/YYYY with no zero padding for M, D
    date = split_datetime[0].str.split('/', expand=True)

    date[0] = date[0].str.zfill(2)  # zfill month to MM
    date[1] = date[1].str.zfill(2)  # zfill day to DD

    # Reformat date to MM/DD/YYYY with zero padding
    date = date[0] + '/' + date[1] + '/' + date[2]

    # Assumes HH:MM with no zero padding (i.e. hr 1-9 as opposed to 01-09)
    time = split_datetime[1].str.split(':', expand=True)

    time[0] = time[0].str.zfill(2)  # zfill hour to HH

    # Some reference datasets include AM/PM, which is split into a third column
    dim_datetime = split_datetime.shape[1]

    if dim_datetime == 3:
        # If AM or PM info included
        time = time.join(split_datetime[2])
        time = time[0] + ':' + time[1] + ' ' + time[2]
    else:
        time = time[0] + ':' + time[1]

    # Rejoin date and time columns
    datetime = date + ' ' + time

    # Choose formatting based on whether AM/PM in datetime
    if datetime.str.split(expand=True).shape[1] == 3:
        datetime_fmt = '%m/%d/%Y %I:%M %p'  # MM/DD/YYYY HH:MM AM/PM (12hr fmt)
    if datetime.str.split(expand=True).shape[1] == 2:
        datetime_fmt = '%m/%d/%Y %H:%M'  # MM/DD/YYYY HH:MM (24hr fmt)

    df['DateTime_UTC'] = pd.to_datetime(datetime, format=datetime_fmt)
    df.drop(columns=['Date & Time'], inplace=True)
    if split_timestamp:
        df.drop(columns=['DateTime', 'Time'], inplace=True)

    return df


def Format_Headers(df):

    ref_dict = {'BC_UV': {'1': {'header_name': 'UV_633_370nm',
                                'method_name': 'Magee Scientific Aethalometer AE33',
                                'method_code': '894',
                                'param_code': '88314',
                                'method_poc': 1,
                                'unit': 'NG/M3'}},
                'BC_IR': {'1': {'header_name': 'BC AE33 880nm',
                                'method_name': 'Magee Scientific Aethalometer AE33',
                                'method_code': '894',
                                'param_code': '88313',
                                'method_poc': 1,
                                'unit': 'NG/M3'}},
                'PM1': {'1': {'header_name': 'GRIMM PM1',
                              'method_name': 'GRIMM EDM 180',
                              'method_code': '',
                              'param_code': '',
                              'method_poc': 1,
                              'unit': 'UG/M3'}},
                'PM25': {'1': {'header_name': 'T640_2_PM25',
                               'method_name': 'Teledyne API T640x',
                               'method_code': '238',
                               'param_code': '88101',
                               'method_poc': 1,
                               'unit': 'UG/M3'},
                         '2': {'header_name': 'Grimm PM2.5',
                               'method_name': 'GRIMM EDM 180',
                               'method_code': '195',
                               'param_code': '88101',
                               'method_poc': 2,
                               'unit': 'UG/M3'}},
                'PM10': {'1': {'header_name': 'T640_2_PM10',
                               'method_name': 'Teledyne API T640x',
                               'method_code': '239',
                               'param_code': '81102',
                               'method_poc': 1,
                               'unit': 'UG/M3'},
                         '2': {'header_name': 'Grimm PM10',
                               'method_name': 'GRIMM EDM 180',
                               'method_code': '85101', # not FEM for PM10
                               'param_code': '195',
                               'method_poc': 2,
                               'unit': 'UG/M3'}},
                'CO': {'1': {'header_name': 'CO',
                             'method_name': 'Teledyne API 300E', # Model 300 EU?
                             'method_code': '593', # If 300 EU
                             'param_code': '42101',
                             'method_poc': 1,
                             'unit': 'PPBV'}},
                'NO2': {'1': {'header_name': 'CAPS NO2', # Assuming N500
                              'method_name': 'Teledyne API 500',
                              'method_code': '256',
                              'param_code': '42602',
                              'method_poc': 1,
                              'unit': 'PPBV'}},
                'O3': {'1': {'header_name': 'O3-API T265',
                             'method_name': 'Teledyne API T265',
                             'method_code': '199',
                             'param_code': '44201',
                             'method_poc': 1,
                             'unit': 'PPBV'}},
                'SO2': {'1': {'header_name': 'SO2',
                             'method_name': 'Unknown Reference',
                             'method_code': '',
                             'param_code': '',
                             'method_poc': 1,
                             'unit': 'PPBV'}},
                'WS': {'1': {'header_name': 'WS Ultra 10m',
                             'method_name': 'Vaisala WXT520',
                             'method_code': '',
                             'param_code': '61101',
                             'method_poc': 1,
                             'unit': 'M/S'}},
                'WD': {'1': {'header_name': 'WD Ultra 10m',
                             'method_name': 'Vaisala WXT520',
                             'method_code': '',
                             'param_code': '61102',
                             'method_poc': 1,
                             'unit': 'DEG'}},
                'Temp': {'1': {'header_name': '3m Temp',
                               'method_name': 'RM Young 41382 VC',
                               'method_code': '',
                               'param_code': '62101',
                               'method_poc': 1,
                               'unit': 'CELSIUS'}},
                'RH': {'1': {'header_name': '3m RH',
                             'method_name': 'RM Young 41382 VC',
                             'method_code': '',
                             'param_code': '62201',
                             'method_poc': 1,
                             'unit': 'PERCENT'}}
                }

    # make all dataframe columns lower case
    df = df.rename(columns={col: col.lower() for col in df.columns})

    for param in ref_dict:
        principal_method = ref_dict[param]['1']

        col_name = principal_method['header_name'].lower()

        # ensure case match by lower case column header names

        if col_name in df.columns:
            data = df[col_name]

            df[param + '_Value'] = pd.to_numeric(data, errors='coerce')
            df[param + '_Unit'] = principal_method['unit']
            df = Format_QAQC(param, data, df)
            df[param + '_Param_Code'] = principal_method['param_code']
            df[param + '_Method'] = principal_method['method_name']
            df[param + '_Method_Code'] = principal_method['method_code']
            df = df.drop(columns=[col_name])

        else:
            try:
                secondary_method =  ref_dict[param]['2']
                col_name = secondary_method['header_name'].lower()

                # ensure case match by lower case column header names
                if col_name in df.columns:
                    data = df[col_name]
                    df[param + '_Value'] = pd.to_numeric(data, errors='coerce')
                    df[param + '_Unit'] = secondary_method['unit']
                    df = Format_QAQC(param, data, df)
                    df[param + '_Param_Code'] = secondary_method['param_code']
                    df[param + '_Method'] = secondary_method['method_name']
                    df[param + '_Method_Code'] = secondary_method['method_code']
                    df = df.drop(columns=[col_name])

                else:
                    #print(param + ' not in dataframe')
                    continue

            except KeyError:
                if col_name not in df.columns:
                    #print(param + ' not in dataframe')
                    continue
                else:
                    #print('No secondary instrument, ' + param + ' not in dataframe')
                    continue


    # Site info
    df['Agency'] = "U.S. EPA"
    df['Site_Name'] = 'Burdens Creek (AIRS)'
    df['Site_AQS'] = '37-063-0099'
    df['Site_Lat'] = 35.8895
    df['Site_Lon'] = -78.8746
    df['Data_Source'] = 'OAQPS/AQAD/AAMG'
    df['Data_Acquisition_Date_Time'] = ''

    return df


def Format_QAQC(param, series, df):
    # Calibration codes indicated in reference data
    codes = ['NoData',
             'Zero',    # Gas Calibration: Zero air generator
             'Span',    # Gas Calibration: Span (cylinder) gas
             'Spare',
             'Purge',   # Gas Calibration: Set ambient air, clear lines
             'Down',
             'InVld',
             'OffScan',
             '<Samp']

    for code in codes:

        code_idx = series[series==code].index
        if not code_idx.empty:
            df.loc[code_idx, param + '_QAQC_Code'] = code
        else:
            df[param + '_QAQC_Code'] = 0

        df[param + '_QAQC_Code'] = df[param + '_QAQC_Code'].fillna(0)

    return df



if __name__ == '__main__':
    lib_path = os.path.abspath(__file__ + '../../../..')
    data_path = os.path.abspath(lib_path + '/Data and Figures/reference_data/'
                                'oaqps/raw_data/1-minute')
    data_path = pathlib.PureWindowsPath(data_path)
    Process_OAQPS(data_path)
