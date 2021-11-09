# -*- coding: utf-8 -*-
"""
Description.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Mon Aug  9 09:30:03 2021
Last Updated:
  Mon Aug  9 09:30:03 2021
"""
import io
import os
import pathlib
import datetime
import pandas as pd
import numpy as np
from sensortoolkit.datetime_utils import interval_averaging, get_timestamp_interval
from sensortoolkit.qc import remove_duplicates

def process_oaqps(data_path, lib_path, formatting='envista',
                  interval='min'):
    """Loop through list of raw datasets, convert to standard format, save
    processed datasets to file at recorded and 1-hour averaged intervals.


    Args:
        data_path (str): DESCRIPTION.

    Returns:
        None.

    """

    for item in os.listdir(data_path):
        if item.endswith('.csv') and item.startswith(interval):
            print(item)

            file = pathlib.Path(str(data_path) + '//' + item)
            df = ingest_oaqps(str(file), formatting=formatting)

            # Modify time
            mtime = datetime.datetime.fromtimestamp(file.stat().st_mtime)
            df['Data_Acquisition_Date_Time'] = mtime

            # Shift dataframes to UTC (ahead five hours)
            df = df.shift(5, freq='H')

            h_df = interval_averaging(df, freq='H', interval_count=60, thres=0.75)

            processed_m_path = (lib_path + '/data/reference_Data/'
                                'oaqps/processed_data/' + item)
            processed_h_path = (lib_path + '/data/reference_Data/'
                                'oaqps/processed_data/' + item.replace('min', 'H'))
            df.to_csv(processed_m_path)
            h_df.to_csv(processed_h_path)


def ingest_oaqps(file_path, formatting=None):
    """Read raw csv data and format timestamps, column headers.


    Args:
        file_path (str): DESCRIPTION.

    Returns:
        df (pandas DataFrame): DESCRIPTION.

    """
    if formatting == 'envista':
        df = from_envista(file_path)
    if formatting == 'envidas':
        df = from_envidas(file_path)

    df = format_headers(df, formatting=formatting)

    return df


def from_envidas(file_path):
    """Ingestion scheme for AIRS data provided in Envidas format.

    Example:
        Head and tail of 1-hour averaged PM data
                                                   Site:PM
    0    Date,Time,UV_370nm_AE33 LC : Value,UV_370nm_AE...
    1    11/1/2020,1:00 AM,1842.83333333333,1,1006.1,1,...
    2    11/1/2020,2:00 AM,1666.41666666667,1,919.5,1,5...
    3    11/1/2020,3:00 AM,1546.43333333333,1,856.06666...
    4    11/1/2020,4:00 AM,1676.45,1,871.583333333333,1...
    ..                                                 ...
    716  11/30/2020,8:00 PM,124.397222222222,1,92.84722...
    717  11/30/2020,9:00 PM,80.2805555555556,1,56.31666...
    718  11/30/2020,10:00 PM,100.486111111111,1,62.5888...
    719  11/30/2020,11:00 PM,84.5194444444444,1,52.0944...
    720  12/1/2020,12:00 AM,78.5888888888889,1,51.00555...

    Returns:
        None.

    """
    # Some lines end with comma delim, others do not. Solution recommended by
    # Scott Boston (https://stackoverflow.com/questions/47519294/pandas-dataframe-read-csv-with-rows-that-have-not-have-comma-at-the-end)
    with open(file_path) as f:
        data = f.read() + '\n'  # Add newline str to each line
        f.close()
    df = pd.read_csv(io.StringIO(data.replace(',\n', '\n')), header=1)

    rename = {col: col.replace(' : ',
                                '_').replace(' ',
                                            '_').replace('Status',
                                                          'QAQC_Code')
              for col in df.columns}
    df = df.rename(columns=rename)

    df['DateTime'] = pd.to_datetime(df.Date + ' ' + df.Time,
                                    format = '%m/%d/%Y %I:%M %p')
    df = df.set_index(df.DateTime)

    df = df.drop(columns=['Date', 'Time', 'DateTime'])

    keep = ['UV_370nm_AE33_LC_Value',           # <-- PM Headers
            'UV_370nm_AE33_LC_QAQC_Code',
            'BC_880nm_AE33_LC_Value',
            'BC_880nm_AE33_LC_QAQC_Code',
            'T640_2_PM25_Value',
            'T640_2_PM25_QAQC_Code',
            'T640_2_PM10_Value',
            'T640_2_PM10_QAQC_Code',
            '10M_Wind_Speed_Value',             # <-- Met Headers
            '10M_Wind_Speed_QAQC_Code',
            '10M_Wind_Direction_Value',
            '10M_Wind_Direction_QAQC_Code',
            '3M_Temp_Value',
            '3M_Temp_QAQC_Code',
            '3M_RH_Value',
            '3M_RH_QAQC_Code',
            'CO_Value',                         # <-- Gas Headers
            'CO_QAQC_Code',
            #'NO_Value',
            #'NO_QAQC_Code'
            'CAPS_NO2_Value',
            'CAPS_NO2_QAQC_Code',
            'T265_O3_Value',
            'T265_O3_QAQC_Code']

    df = df.drop(columns=[col for col in df.columns if col not in keep])

    # Use Envista naming convention for instrument header names
    rename_instruments = {'UV_370nm_AE33_LC_Value': 'UV_633_370nm',
                          'UV_370nm_AE33_LC_QAQC_Code': 'UV_633_370nm_QAQC_Code',
                          'BC_880nm_AE33_LC_Value': 'BC AE33 880nm',
                          'BC_880nm_AE33_LC_QAQC_Code': 'BC AE33 880nm_QAQC_Code',
                          'T640_2_PM25_Value': 'T640_2_PM25',
                          'T640_2_PM10_Value': 'T640_2_PM10',
                          '10M_Wind_Speed_Value': 'WS Ultra 10m',
                          '10M_Wind_Speed_QAQC_Code': 'WS Ultra 10m_QAQC_Code',
                          '10M_Wind_Direction_Value': 'WD Ultra 10m',
                          '10M_Wind_Direction_QAQC_Code': 'WD Ultra 10m_QAQC_Code',
                          '3M_Temp_Value': '3m Temp',
                          '3M_Temp_QAQC_Code': '3m Temp_QAQC_Code',
                          '3M_RH_Value': '3m RH',
                          '3M_RH_QAQC_Code': '3m RH_QAQC_Code',
                          'CO_Value': 'CO',
                          'CO_QAQC_Code': 'CO_QAQC_Code',
                          'CAPS_NO2_Value': 'CAPS NO2',
                          'CAPS_NO2_QAQC_Code': 'CAPS NO2_QAQC_Code',
                          'T265_O3_Value': 'O3-API T265',
                          'T265_O3_QAQC_Code': 'O3-API T265_QAQC_Code'
                           }

    df = df.rename(columns=rename_instruments)

    b_timestamp, e_timestamp = df.index.min(), df.index.max()
    interval = get_timestamp_interval(df, as_timedelta=True)

    new_idx = pd.date_range(start=b_timestamp, end=e_timestamp, freq=interval)
    new_df = pd.DataFrame(index=new_idx)
    df = new_df.combine_first(df)

    return df


def from_envista(file_path):
    """Ingestion scheme for AIRS data provided in Envista ARM format.


    Returns:
        None.

    """
    df = pd.read_csv(file_path, header=2)
    df = df[1:-8]

    df = format_ref_timestamp(df)

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

    df = df.set_index(df.DateTime).drop(columns=['DateTime'])


    return df



def format_ref_timestamp(df):
    """


    Args:
        df (pandas DataFrame): DESCRIPTION.

    Returns:
        df (pandas DataFrame): DESCRIPTION.

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

    df['DateTime'] = pd.to_datetime(datetime, format=datetime_fmt)
    df.drop(columns=['Date & Time'], inplace=True)
    if split_timestamp:
        df.drop(columns=['DateTime', 'Time'], inplace=True)

    return df


def format_headers(df, formatting='envista'):

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

            if formatting == 'envidas':
                df = df.rename(columns={col_name + '_qaqc_code':
                                            param + '_QAQC_Code'})

            df = format_qaqc(param, data, df, formatting=formatting)
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

                    if formatting == 'envidas':
                        df = df.rename(columns={col_name + '_qaqc_code':
                                                param + '_QAQC_Code'})


                    df = format_qaqc(param, data, df, formatting=formatting)
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
    df['Data_Source'] = 'OAQPS/AQAD/AAMG (via {0})'.format(formatting)
    df['Data_Acquisition_Date_Time'] = 'Unspecified'

    return df


def format_qaqc(param, series=None, df=None, formatting='envista'):
    if formatting == 'envista':
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

    if formatting == 'envidas':
        invalid_idx = df[df[param + '_QAQC_Code'] == 0].index
        valid_idx = df[df[param + '_QAQC_Code'] == 1].index

        df.loc[invalid_idx, param + '_QAQC_Code'] = -1
        df.loc[valid_idx, param + '_QAQC_Code'] = 0
        df.loc[invalid_idx, param + '_QAQC_Code'] = 1


    return df



if __name__ == '__main__':
       lib_path = os.path.abspath(__file__ + '../../../..')
       data_path = r'C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Public_Sensor_Evaluation\Data and Figures\reference_data\oaqps\raw_data\AIRS - 1120 - 0721\GASES'
       df = process_oaqps(data_path, lib_path, formatting='envidas',
                                interval='min')

    # file = r"C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Public_Sensor_Evaluation\Data and Figures\reference_data\oaqps\raw_data\AIRS - 1120 - 0721\PM\min_202011_PM.csv"
    # df = ingest_oaqps(file, formatting='envidas')
