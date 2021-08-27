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
  Mon Jul 19 14:03:36 2021
Last Updated:
  Mon Jul 19 14:03:36 2021
"""
import json
import pandas as pd
import sys
from datetime import datetime
import os


def Ingest(path, name=None, setup_file_path=None):
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
    # with open(setup_file_path) as file:
    #     setup = json.load(file)
    #     file.close()

    setup = ParseSetup(setup_file_path, data_path=path)

    idx_list = setup['timestamp_col_headers']
    idx_format_dict = setup['time_format_dict']

    if setup['dtype'] in ('.csv', '.txt'):
        try:
            names = None
            if setup['header_iloc'] is None:
                names = setup['all_col_headers']
            df = pd.read_csv(path, header=setup['header_iloc'], names=names)
        except FileNotFoundError as e:
            sys.exit(e)
    else:
        # Put other pandas read functions here
        sys.exit()

    # If the header row loads on a row of data (may be intentional if
    # formatting for first row is unusual and doesnt follow delimited format).
    if df.columns.all() != setup['all_col_headers']:
        df.columns = setup['all_col_headers']

    # Set Datetime Index
    df['DateTime_UTC'] = df[idx_list].astype(str).apply(''.join, axis=1)
    time_format = ''.join(idx_format_dict.values())

    # Since non-zero padded timestamp formatting depends on the platform, use
    # the strptime module to parse timestamps into standard formatting
    if '%-' in time_format or '%#' in time_format:
        print('..Non-zero padded formatting encountered in timeseries, '
              'attempting to conform')
        time_format = time_format.replace('%-', '%').replace('%#', '%')
        df['DateTime_UTC'] = df['DateTime_UTC'].apply(
                                lambda x: datetime.strptime(x, time_format))
        time_format = '%Y-%m-%d %H:%M:%S'

    # Check whether the timestamp data are in Unix epoch
    if time_format == 'epoch':
        unit = 's'
        time_format = None
    else:
        unit = None

    # Convert the DateTime_UTC column to time-like data format and set as index
    # If errors encountered (timestamps cant be parsed), 'coerce' will set NaT
    df['DateTime_UTC'] = pd.to_datetime(df['DateTime_UTC'],
                                        format=time_format,
                                        unit=unit,
                                        errors='coerce')

    df = df.set_index(df['DateTime_UTC'])
    df = df.sort_index(ascending=True)
    df = df.drop(columns=['DateTime_UTC'])
    df = df.drop(columns=setup['timestamp_col_headers'])

    # Rename parameter header columns
    df = df.rename(columns=setup['col_rename_dict'])

    # Drop unused columns
    if len(setup['drop_cols']) > 0:
        # ignore errors if column not in df (may happen if DateTime_UTC in list
        # of all header columns, already dropped)
        df = df.drop(columns=setup['drop_cols'], errors='ignore')

        # Force non numeric values to Nans
        #df = df.apply(lambda x: pd.to_numeric(x, errors='coerce'))

    return df


def ParseSetup(setup_file_path, data_path):
    """Construct file-specific setup file from the setup.json generated by the
    Setup() module.
    """
    # Ensure norm path
    data_path = os.path.normpath(data_path)

    with open(setup_file_path) as file:
        setup = json.load(file)
        file.close()

    file_setup = {}
    file_col_list = []
    file_col_renaming_dict = {}
    file_drop_cols = []

    # Parse setup.json for data file specific header names
    for row_entry in setup['col_headers']:
        row_config = setup['col_headers'][row_entry]
        row_headers = list(row_config.keys())

        for header in row_headers:
            file_list = row_config[header]['files']
            file_list = [os.path.normpath(path) for path in file_list]
            if data_path in file_list:
                file_col_list.append(header)

                sdfs_param_header = row_config[header]['SDFS_param']
                if sdfs_param_header != '':
                    file_col_renaming_dict[header] = sdfs_param_header
                else:
                    file_drop_cols.append(header)

    # Create a list/dict of timestamp columns specific to loaded dataset
    file_idx_list = [col for col in setup['timestamp_col_headers']
                     if col in file_col_list]
    file_idx_format = {col: setup['time_format_dict'][col] for col
                       in setup['time_format_dict'] if col in file_col_list}

    file_setup['name'] = setup['name']
    file_setup['work_path'] = setup['work_path']
    file_setup['dtype'] = setup['dtype']
    file_setup['header_iloc'] = setup['header_iloc']
    file_setup['all_col_headers'] = file_col_list
    file_setup['col_rename_dict'] = file_col_renaming_dict
    file_setup['drop_cols'] = file_drop_cols
    file_setup['timestamp_col_headers'] = file_idx_list
    file_setup['time_format_dict'] = file_idx_format

    return file_setup
