# -*- coding: utf-8 -*-
"""
This module contains methods for parsing setup.json configuration files and
their use in ingesting comma-separated datasets for both sensor and reference
data into sensortoolkit's SDFS format.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Mon Jul 19 14:03:36 2021
Last Updated:
  Mon Jul 19 14:03:36 2021
"""
import os
import sys
import json
from datetime import datetime
import pytz
import pandas as pd
from pandas.errors import EmptyDataError
from sensortoolkit.param import Parameter
from sensortoolkit.calculate import convert_temp
import charset_normalizer

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
        df (pandas DataFrame):
            Dataframe containing sensor data in standardized formatting for
            datetime index and header naming scheme.

    """
    setup = parse_setup(setup_file_path, data_path=path)

    time_fmt = setup['time_format_dict']
    idx_list = list(setup['time_format_dict'].keys())
    idx_format_dict = {col: time_fmt[col]['dt_format'] for col in idx_list}
    idx_tzone = [time_fmt[col]['dt_timezone'] for col in time_fmt if
                 time_fmt[col]['dt_timezone'] is not None]
    encoding_pred = setup['encoding_prediction']

    if setup['file_extension'] in ('.csv', '.txt', '.xlsx'):
        try:
            names = None
            row_idx = None
            if setup['header_iloc'] is None:
                names = setup['all_col_headers']
            if setup['data_row_idx'] is not None:
                row_idx = setup['data_row_idx']

            if setup['file_extension'] in ('.csv', '.txt'):
                try:
                    df = pd.read_csv(path, header=setup['header_iloc'],
                                     names=names, skiprows=row_idx,
                                     encoding=encoding_pred,
                                     on_bad_lines='warn')
                except UnicodeDecodeError:
                    print('\n[WARNING]: Reading the following dataset with uft-8 '
                          'encoding unsuccessful')
                    print(path)
                    print('..Attempting to guess encoding')

                    with open(path, 'rb') as f:
                        data = f.read(10000)
                    prediction = charset_normalizer.detect(data)
                    print('..encoding prediction:')
                    print(f'....{prediction}')
                    print('')

                    try:
                        df = pd.read_csv(path, header=setup['header_iloc'],
                                         names=names, skiprows=row_idx,
                                         encoding=prediction["encoding"],
                                         on_bad_lines='warn')
                    except UnicodeError as e:
                        print('Error encountered in file:', path)
                        print(e)
                        print(f'Encoding prediction {prediction["encoding"]} '
                              f'unsuccessful for {path}\n')
                        return pd.DataFrame()
                    except UnicodeDecodeError as e:
                        print('Error encountered in file:', path)
                        print(e)
                        print(f'Encoding prediction {prediction["encoding"]} '
                              f'unsuccessful for {path}\n')
                        return pd.DataFrame()

            if setup['file_extension'] == '.xlsx':
                df = pd.read_excel(path, header=setup['header_iloc'],
                                   names=names, skiprows=row_idx,
                                   encoding=encoding_pred, on_bad_lines='warn')

        except FileNotFoundError as e:
            sys.exit(e)
        except EmptyDataError as e:
            print(f'{e} (likely empty file)')
            print(path)
            return pd.DataFrame()
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
    time_format = ''.join([val for key, val in idx_format_dict.items()])
    time_zone_list = idx_tzone

    if len(idx_list) > 1 and len(time_zone_list) > 1:
        # Multiple time-like columns but the specified time zone for each does
        # not match
        if len(set(time_zone_list)) > 1:
            raise ValueError(f'Too many time zones specified for datetime index:'
                             f' {", ".join(time_zone_list)}. Only one time zone '
                             'should be specified.')
        else:
            time_zone = time_zone_list[0]

    if len(time_zone_list) == 0:
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
    # If errors encountered (timestamps cant be parsed), 'raise' will invoke
    # ValueError and prompt parsing with pandas inferring timestamp format
    try:
        df['DateTime'] = pd.to_datetime(df['DateTime'],
                                        format=time_format,
                                        unit=unit,
                                        errors='raise')
    except ValueError:
        print('\n..timestamp formatting inconsistent with specified format, \n'
              'proceeding by inferring timestamp format\n')
        df['DateTime'] = pd.to_datetime(df['DateTime'],
                                        infer_datetime_format=True,
                                        errors='coerce')


    df = df.set_index(df['DateTime'])
    df = df.sort_index(ascending=True)

    if time_zone is not None:
        dt = datetime.utcnow()
        tz = pytz.timezone(time_zone)
        offset = tz.utcoffset(dt) / pd.to_timedelta('1 hour')
        print(f'....converting datetime index from {time_zone} (UTC {offset} '
              'hours) to UTC.')
        # Check if the datetime index is already in UTC (can happen if format
        # was inferred and tzone set UTC)
        try:
            df = df.tz_localize(time_zone).tz_convert('UTC')
        except TypeError:
            pass
        # Experimental inclusion of metadata attributes dictionary
        df.attrs['local_tzone'] = time_zone

    # Remove rows where coerced errors resulted in NaT values for index
    null_idx = df.loc[df.index.isna(), :]
    if null_idx.empty is False:
        print('\nThe following rows contain invalid timestamp data, dropping'
              ' from dataset:\n')
        print(null_idx)
        df = df.loc[df.index.dropna(), :]

    idx_list.append('DateTime')
    timestamp_cols = set(idx_list)
    df = df.drop(columns=timestamp_cols)

    # Rename parameter header columns
    df = df.rename(columns=setup['col_rename_dict'])

    # Set numeric column types for parameter value columns
    for col in setup['col_rename_dict'].values():
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Unit scaling
    for header, conversion in setup['file_unit_scaling'].items():
        # Use a specific equation indicated by the conversion string
        if isinstance(conversion, str):

            if conversion == 'f_c':
                sdfs_header = setup['col_rename_dict'][header]
                converted_data = convert_temp(df[sdfs_header],
                                              from_unit='F',
                                              to_unit='C')
                df[sdfs_header] = converted_data

            # Other non-scalar conversions could go here

        # Use a scalar conversion factor
        if isinstance(conversion, (int, float)):

            scale_factor = conversion
            sdfs_header = setup['col_rename_dict'][header]
            print(f'....scaling {header} values by {scale_factor}')
            df[sdfs_header] = float(scale_factor) * df[sdfs_header]

    # Drop unused columns
    if len(setup['drop_cols']) > 0:
        # ignore errors if column not in df
        df = df.drop(columns=setup['drop_cols'], errors='ignore')

    # Reference data columns
    for param in setup['sdfs_header_names']:
        param_cols = {'_Unit': 'object',
                      '_Param_Code': 'int64',
                      '_Method_Code': 'int64',
                      '_Method': 'object',
                      '_Method_POC': 'int64'}
        for col, col_dtype in param_cols.items():
            header = param + col
            if header in setup:
                df[header] = setup[header]
                df[header] = df[header].astype(col_dtype, errors='ignore')
            # Add unit info based on sensortoolkit.Parameter if not specified
            else:
                param_obj = Parameter(param, set_units=False)
                if col == '_Unit' and param_obj.is_sdfs():
                    param_obj = Parameter(param, set_units=True)
                    df[header] = param_obj.units_description

    # Reorder parameter columns
    col_order = []
    for param in setup['sdfs_header_names']:
        col_order.extend([col for col in df.columns
                          if col.split('_')[0] == param])
    df = df[col_order]

    site_cols = {'site_name': 'object',
                 'agency': 'object',
                 'site_aqs': 'object',
                 'site_lat': 'float64',
                 'site_lon': 'float64',
                 'data_source': 'object'}
    # Site metadata columns
    for col, col_dtype in site_cols.items():
        if col in setup:
            col_name = col.title()
            if col_name == 'Site_Aqs':
                col_name = 'Site_AQS'
            df[col_name] = setup[col]
            df[col_name] = df[col_name].astype(col_dtype, errors='ignore')

    return df

def apply_strptime(dt, time_format):
    """Wrapper for adding exception catching to ``datetime.strptime``

    If ``datetime.strptime`` encounters a value it cannot encode into time-like
    form, the value is ignored.

    Args:
        dt (pandas Series): An array of timestamp entries.
        time_format (str): The expected format for timestamps.

    Returns:
        dt (pandas Series): A time-casted timestamp value.

    """
    try:
        dt = datetime.strptime(dt, time_format)
    except ValueError:
        pass
    return dt

def parse_setup(setup_path, data_path):
    """Construct file-specific setup file from the setup.json.

    Args:
        setup_path (str):
            Path to the setup.json file for ingesting datasets into SDFS format.
        data_path (str):
            Full path to the directory where recorded datasets are stored.

            - For sensor data, this path should look like:
              ``[project_path]/data/sensor_data/[sensor_name]/raw_data``
            - For reference data, this path should look like:
              ``[project_path]/data/reference_data/[ref_source]/raw/[sitename_siteid]``

    Returns:
        file_setup (dict):
            Data structure containing file-specific formatting configuration.
            Passed to ``standard_ingest()`` for ingestion of the dataset
            corresponding to the file into SDFS format.

    """
    # Ensure norm path
    data_path = os.path.normpath(data_path)

    with open(setup_path) as file:
        setup = json.load(file)
        file.close()

    file_col_list = []
    file_drop_cols = []
    file_col_headers = {}
    file_dt_headers = {}
    file_col_renaming = {}
    file_sdfs_headers = []
    file_unit_scaling = {}

    file_list = [os.path.normpath(file) for file in setup['file_list']]
    file_idx = file_list.index(os.path.normpath(data_path))
    # Either reference or sensor
    # data_type = setup['data_type']

    # Parse setup.json for data file specific header names
    for col_idx in setup['col_headers']:
        # config within the ith column index (i ranging from 0 to N-1 where
        # N is the number of columns in the dataset)
        col_idx_config = setup['col_headers'][col_idx]
        col_idx_headers = list(col_idx_config.keys())

        # Loop over header configs within the ith column index
        for header in col_idx_headers:
            # Create list of data files containing the current header
            header_file_list = [file_list[i] for i in
                                col_idx_config[header]['in_file_list_idx']]
            header_file_list = [os.path.normpath(path) for path in
                                header_file_list]

            # Add file dataset info if passed filename contains the current
            # header
            if data_path in header_file_list:
                file_col_list.append(header)

                header_config = col_idx_config[header]
                file_col_headers[header] = header_config

                if header_config['drop'] is True:
                    file_drop_cols.append(header)
                else:
                    # Add datetime index column info
                    if header_config['header_class'] == 'datetime':
                        file_dt_headers[header] = header_config
                    # Add parameter column info
                    if header_config['header_class'] == 'parameter':
                        sdfs_param = header_config['sdfs_param']

                        file_col_renaming[header] = header_config['sdfs_param'] + '_Value'

                        file_sdfs_headers.append(sdfs_param)

                        if ('unit_transform' in header_config and
                        header_config['unit_transform'] is not None):
                            file_unit_scaling[header] = header_config['unit_transform']

    col_list = ['name', 'path', 'file_extension', 'header_iloc']
    file_setup = {col: setup[col] for col in col_list if col in setup}
    file_setup['all_col_headers'] = file_col_list
    file_setup['col_rename_dict'] = file_col_renaming
    file_setup['drop_cols'] = file_drop_cols
    file_setup['time_format_dict'] = file_dt_headers
    file_setup['sdfs_header_names'] = file_sdfs_headers
    file_setup['file_unit_scaling'] = file_unit_scaling

    # Reference only: add parameter metadata columns
    for param in file_sdfs_headers:
        param_cols = ['_Unit', '_Param_Code', '_Method_Code', '_Method',
                      '_Method_POC']

        for col in param_cols:
            header = param + col
            if header in setup:
                file_setup[header] = setup[header]

    # Reference only: add site metadata columns
    site_cols = ['site_name', 'agency', 'site_aqs', 'site_lat', 'site_lon']
    for col in site_cols:
        if col in setup:
            file_setup[col] = setup[col]

    try:
        file_setup['data_row_idx'] = setup['data_row_idx']
    except KeyError:
        file_setup['data_row_idx'] = None

    try:
        file_setup['data_source'] = setup['dataset_kwargs']['ref_data_source']
    except KeyError:
        pass

    # default encoding prediction
    file_setup['encoding_prediction'] = 'utf-8'
    # pass on any predictions indicated by chardet in setup
    if 'encoding_predictions' in setup:
        if file_idx in list(int(key) for key in setup['encoding_predictions'].keys()):
            file_setup['encoding_prediction'] = setup['encoding_predictions'][str(file_idx)]

    return file_setup
