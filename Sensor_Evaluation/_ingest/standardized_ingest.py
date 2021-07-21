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
    with open(setup_file_path) as file:
        setup = json.load(file)
        file.close()

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

    # Check whether the timestamp data are in Unix epoch
    if time_format == 'epoch':
        unit = 's'
        time_format = None
    else:
        unit = None

    # Since non-zero padded timestamp formatting depends on the platform, use
    # the strptime module to parse timestamps into standard formatting
    if '%-' or '%#' in time_format:
        print('..Non-zero padded formatting encountered in timeseries, '
              'attempting to conform')
        time_format = time_format.replace('%-', '%').replace('%#', '%')
        df['DateTime_UTC'] = df['DateTime_UTC'].apply(
                                lambda x: datetime.strptime(x, time_format))
        time_format = '%Y-%m-%d %H:%M:%S'

    # Convert the DateTime_UTC column to time-like data format and set as index
    # If errors encountered (timestamps cant be parsed), 'coerce' will set NaT
    df['DateTime_UTC'] = pd.to_datetime(df['DateTime_UTC'],
                                        format=time_format,
                                        unit=unit,
                                        errors='coerce')
    df = df.set_index(df['DateTime_UTC'])
    df = df.sort_index(ascending=True)
    df = df.drop(columns='DateTime_UTC')

    # Rename parameter header columns
    df = df.rename(columns=setup['col_rename_dict'])

    # Drop unused columns
    if len(setup['drop_cols']) > 0:
        # ignore errors if column not in df (may happen if DateTime_UTC in list
        # of all header columns, already dropped)
        df = df.drop(columns=setup['drop_cols'],
                     errors='ignore')

        # Force non numeric values to Nans
        #df = df.apply(lambda x: pd.to_numeric(x, errors='coerce'))

    return df


"""
import os
data_path = 'C:/Users/SFREDE01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/AIRS Project/AIRS Evaluation/Sensor_Raw_Data/Myriad_PocketLab/20210419 Data Collection/Data/E0/'
setup_path = "C:/Users/SFREDE01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Public_Sensor_Evaluation/User_Scripts/sensor setup files/Myriad_PocketLab_setup.json"
df_list = []
for filename in os.listdir(data_path):
    print(filename)
    df = Ingest(path=data_path + '/' + filename,
                name='Myriad_PocketLab', setup_file_path=setup_path)
    df_list.append(df)
"""
