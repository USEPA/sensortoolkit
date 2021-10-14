# -*- coding: utf-8 -*-
"""
Description.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Mon Jul 19 14:03:36 2021
Last Updated:
  Mon Jul 19 14:03:36 2021
"""
import json
import pandas as pd
import sys
from datetime import datetime
import os
import pytz


def standard_ingest(path, name=None, setup_file_path=None):
    """Ingestion module for sensor data using setup.json configuration file
    via the Setup class.

    Sensor data file data type must be .csv, .txt, or .xlsx.

    Args:
        path (str):
            The full path to the recorded sensor data file
        name (str):
            The make and model of the sensor
        setup_file_path (str):
            The full path to the setup.json file

    Returns:
        df (pandas dataframe):
            Dataframe containing sensor data in standardized formatting for
            datetime index and header naming scheme.
    """
    setup = ParseSetup(setup_file_path, data_path=path)

    idx_list = setup['timestamp_col_headers']
    idx_format_dict = setup['time_format_dict']

    if setup['file_extension'] in ('.csv', '.txt', '.xlsx'):
        try:
            names = None
            row_idx = None
            if setup['header_iloc'] is None:
                names = setup['all_col_headers']
            if setup['data_row_idx'] is not None:
                row_idx = setup['data_row_idx']

            if setup['file_extension'] in ('.csv', '.txt'):
                df = pd.read_csv(path, header=setup['header_iloc'],
                                 names=names, skiprows=row_idx)
            if setup['file_extension'] == '.xlsx':
                df = pd.read_excel(path, header=setup['header_iloc'],
                                   names=names, skiprows=row_idx)

        except FileNotFoundError as e:
            sys.exit(e)
    else:
        # Put other pandas read functions here
        sys.exit('Invalid data type. Must be either .csv, .txt, or .xlsx')

    # If the header row loads on a row of data (may be intentional if
    # formatting for first row is unusual and doesnt follow delimited format).
    if df.columns.all() != setup['all_col_headers']:
        df.columns = setup['all_col_headers']

    # Drop rows where nans in time stamp entries
    df = df.loc[df[idx_list].dropna().index, :]

    # Set Datetime Index
    df['DateTime'] = df[idx_list].astype(str).apply(''.join, axis=1)
    time_format = ''.join([val for key, val in idx_format_dict.items()
                           if not key.endswith('_tz')])
    time_zone_list = [val for key, val in idx_format_dict.items()
                      if key.endswith('_tz') and val is not None]
    if len(time_zone_list) > 1:
        raise ValueError(f'Too many time zones specified for datetime index:'
                         f' {", ".join(time_zone_list)}. Only one time zone '
                         'should be specified.')
    elif len(time_zone_list) == 0:
       print('No time zone specified for datetime index. '
             'Continuing with tz-naive datetime index.')
       time_zone = None
    else:
        time_zone = time_zone_list[0]

    # Since non-zero padded timestamp formatting depends on the platform, use
    # the strptime module to parse timestamps into standard formatting
    if '%-' in time_format or '%#' in time_format:
        print('..Non-zero padded formatting encountered in timeseries, '
              'attempting to conform')
        time_format = time_format.replace('%-', '%').replace('%#', '%')
        df['DateTime'] = df['DateTime'].apply(
                                    lambda x: apply_strptime(x, time_format))

        time_format = '%Y-%m-%d %H:%M:%S'

    # Check whether the timestamp data are in Unix epoch
    if time_format == 'epoch':
        unit = 's'
        time_format = None
    else:
        unit = None

    # Convert the DateTime column to time-like data format and set as index
    # If errors encountered (timestamps cant be parsed), 'coerce' will set NaT
    df['DateTime'] = pd.to_datetime(df['DateTime'],
                                    format=time_format,
                                    unit=unit,
                                    errors='coerce')

    df = df.set_index(df['DateTime'])
    df = df.sort_index(ascending=True)

    if time_zone is not None:
        tz = pytz.timezone(time_zone)
        offset = tz.utcoffset(tz.zone) / pd.to_timedelta('1 hour')
        print(f'....converting datetime index from {time_zone} (UTC {offset} '
              'hours) to UTC.')
        df = df.tz_localize(time_zone).tz_convert('UTC')

    # Remove rows where coerced errors resulted in NaT values for index
    null_idx = df.loc[df.index.isna(), :]
    if null_idx.empty is False:
        print('\nThe following rows contain invalid timestamp data, dropping'
              ' from dataset:\n')
        print(null_idx)
        df = df.loc[df.index.dropna(), :]

    setup['timestamp_col_headers'].append('DateTime')
    timestamp_cols = set(setup['timestamp_col_headers'])
    df = df.drop(columns=timestamp_cols)

    # Rename parameter header columns
    df = df.rename(columns=setup['col_rename_dict'])

    # Drop unused columns
    if len(setup['drop_cols']) > 0:
        # ignore errors if column not in df
        df = df.drop(columns=setup['drop_cols'], errors='ignore')

    # Reference data columns
    for param in setup['sdfs_header_names']:
        param_cols = ['_Unit', '_Param_Code', '_Method_Code', '_Method',
                      '_Method_POC']

        for col in param_cols:
            header = param + col
            if header in setup:
                df[header] = setup[header]

    site_cols = ['site_name', 'agency', 'site_aqs', 'site_lat', 'site_lon']
    for col in site_cols:
        if col in setup:
            col_name = col.title()
            if col_name == 'Site_Aqs':
                col_name = 'Site_AQS'
            df[col_name] = setup[col]

    return df

def apply_strptime(dt, time_format):
    """Wrapper for adding exception catching to datetime.strptime

    If datetime.strptime encounters a value it cannot encode into time-like
    form, the value is ignored.

    Args:
        dt (TYPE): An array of timestamp entries.
        time_format (TYPE): The expected format for timestamps.

    Returns:
        dt (TYPE): A time-casted timestamp value.

    """
    try:
        dt = datetime.strptime(dt, time_format)
    except ValueError:
        pass
    return dt

def ParseSetup(setup_path, data_path):
    """Construct file-specific setup file from the setup.json generated by the
    Setup() module.
    """
    # Ensure norm path
    data_path = os.path.normpath(data_path)

    with open(setup_path) as file:
        setup = json.load(file)
        file.close()

    file_col_list = []
    file_col_renaming_dict = {}
    file_drop_cols = []

    # Parse setup.json for data file specific header names
    for col_entry in setup['col_headers']:
        col_config = setup['col_headers'][col_entry]
        col_headers = list(col_config.keys())

        for header in col_headers:
            file_list = col_config[header]['files']
            file_list = [os.path.normpath(path) for path in file_list]
            if data_path in file_list:
                file_col_list.append(header)

                sdfs_param_header = col_config[header]['SDFS_param']
                if sdfs_param_header != '':
                    file_col_renaming_dict[header] = sdfs_param_header
                else:
                    file_drop_cols.append(header)

    # Create a list/dict of timestamp columns specific to loaded dataset
    file_idx_list = [col for col in setup['timestamp_col_headers']
                     if col in file_col_list]
    file_idx_format = {col: setup['time_format_dict'][col] for col
                       in setup['time_format_dict'] if col in file_col_list}
    file_tzone_info = {col +'_tz': setup['time_format_dict'][col + '_tz'] for
                       col in file_idx_format.keys()}
    file_idx_format.update(file_tzone_info)


    col_list = ['name', 'path', 'file_extension',
                'header_iloc', 'sdfs_header_names']
    file_setup = {col: setup[col] for col in col_list if col in setup}
    file_setup['all_col_headers'] = file_col_list
    file_setup['col_rename_dict'] = file_col_renaming_dict
    file_setup['drop_cols'] = file_drop_cols
    file_setup['timestamp_col_headers'] = file_idx_list
    file_setup['time_format_dict'] = file_idx_format

    for param in setup['sdfs_header_names']:
        param_cols = ['_Unit', '_Param_Code', '_Method_Code', '_Method',
                      '_Method_POC']

        for col in param_cols:
            header = param + col
            if header in setup:
                file_setup[header] = setup[header]

    site_cols = ['site_name', 'agency', 'site_aqs', 'site_lat', 'site_lon']
    for col in site_cols:
        if col in setup:
            file_setup[col] = setup[col]

    try:
        file_setup['data_row_idx'] = setup['data_row_idx']
    except KeyError:
        file_setup['data_row_idx'] = None

    return file_setup


if __name__ == '__main__':

    df = standard_ingest(path=r"C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\sensortoolkit_testing\Data and Figures\reference_data\local\raw\Burdens_Creek_370630099\min_201908_PM.csv", setup_file_path=r"C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\sensortoolkit_testing\Data and Figures\reference_data\local\raw\Burdens_Creek_370630099\reference_setup.json")
