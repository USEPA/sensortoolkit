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
  Wed Dec  4 08:57:18 2019
Last Updated:
  Wed Jul 14 10:22:15 2021
"""
import pandas as pd
import os
import sys
from sensortoolkit.datetime_utils import sensor_averaging
from sensortoolkit.sensor_ingest import standard_ingest, processed_data_search
from sensortoolkit.calculate import dewpoint

# Sensor-specific modules
from sensortoolkit.model import purpleair_us_corr
from sensortoolkit.qc import purpleair_ab_averages


def sensor_import(sensor_name=None, sensor_serials=None, tzone_shift=0,
                  load_raw_data=False, data_path=None, processed_path=None,
                  write_to_file=False, **kwargs):
    """Import recorded or processed sensor data.

    If loading recorded datasets (i.e., load_raw_data is True), the method will
    walk through the directory path where recorded sensor datasets should be
    located (..//Data and Figures//sensor_data//Sensor_Name//raw_data). Users
    must follow the expected naming scheme for files in this location,
    specifying the sensor name and sensor serial identifier for each dataset.
    If multiple files were recorded for each sensor unit, files must be
    chronologically ordered, and the naming scheme specifying sensor serial id
    and sensor make and model must also be adopted. Files must be type '.csv'
    or '.txt'.

    Here are two example cases that follow the expected naming scheme:

        Example 1)
        Import recorded data from one file per sensor
        ---------------------------------------------
        Say the sensor name is 'Example_Make_Model' and three sensor units were
        tested with the following serial identifiers:

            sensor_serials = {'1': 'SN01', '2': 'SN02', '3': 'SN03'}

        Let's also assume that the three units each record separate '.csv'
        files. The recorded sensor datasets should be placed at the following
        folder location:

            '..//Data and Figures//sensor_data//Example_Make_Model//raw_data'

        The folder structure should look something like:

            path//to//raw_data//
                Example_Make_Model_SN01.csv
                Example_Make_Model_SN02.csv
                Example_Make_Model_SN03.csv

        These files adhere to the expected file naming scheme and data file
        formatting and will be loaded without issue by the Import method.


        Example 2)
        Import data from multiple files per sensor within nested subdirectories
        -----------------------------------------------------------------
        For simplicity, let's use the same serial identifiers as before. The
        data will also be located at the same folder path. However, now let's
        say that instead of one file per sensor, datasets are recorded at daily
        intervals over the evaluation period and were collected at weekly
        intervals and organized by unit ID into sub-directories. Let's also say
        that the data files are recorded as .txt files instead of .csv files.
        The data sets can be placed into the ..//raw_data folder path, and
        might look something like:

            path//to//raw_data//
                //2021_01_08_data_collection
                    //SN01//
                        Example_Make_Model_SN01_20210101.txt
                        Example_Make_Model_SN01_20210102.txt
                        ...
                        Example_Make_Model_SN01_20210108.txt
                    //SN02//
                        Example_Make_Model_SN02_20210101.txt
                        Example_Make_Model_SN02_20210102.txt
                        ...
                        Example_Make_Model_SN02_20210108.txt
                    //SN03//
                        Example_Make_Model_SN03_20210101.txt
                        Example_Make_Model_SN03_20210102.txt
                        ...
                        Example_Make_Model_SN03_20210108.txt
                //2021_01_15_data_collection
                    //SN01//
                        Example_Make_Model_SN01_20210109.txt
                        Example_Make_Model_SN01_20210110.txt
                        ...
                        Example_Make_Model_SN01_20210115.txt
                    //SN02//
                        Example_Make_Model_SN02_20210109.txt
                        Example_Make_Model_SN02_20210110.txt
                        ...
                        Example_Make_Model_SN02_20210115.txt
                    //SN03//
                        Example_Make_Model_SN03_20210109.txt
                        Example_Make_Model_SN03_20210110.txt
                        ...
                        Example_Make_Model_SN03_20210115.txt
                ...

        (Note: if all the files have unique names, one could place all of
        the .txt files in the //raw_data// directory. This example is simply
        meant to illustrate that the import method can handle these types of
        nested folder structures if the appropriate naming scheme is followed).

    Args:
        sensor_name (str): The make and model of the sensor being evaluated.
        serials (dict): A dictionary of sensor serial identifiers for each unit
            in a testing group
        tzone_shift (int): ) An integer value by which to shift the sensor data
            to UTC. Specifying 0 will not shift the data.
        load_raw_data (bool): If true, raw data in the appropriate subdirectory
            will be loaded and 1-hr and 24-hr averages will be computed and
            saved to a processed data subdirectory for the specified sensor.
            If false, processed data will be loaded.
        data_path (str): The full directory path to raw sensor data for a given
            sensor make and model.
        processed_path (str): The full directory path to processed sensor data
            for a given sensor make and model.
        write_to_file (bool): If true and load_raw_data true, processed files
            will be written to folder location. In addition, subsequent
            evaluation statistics will be written to the Data and Figures and
            eval_stats sensor subdirectory. Figures will also be written to the
            appropriate figures subdirectory.

    Returns:
        full_df_list (list):
          List of pandas dataframe objects, one for each sensor dataset
          containing processed full time-resolution data.
        hourly_df_list (list):
          List of pandas dataframe objects, one for each sensor dataset
          containing processed hourly averaged time-resolution data.
        daily_df_list (list):
          List of pandas dataframe objects, one for each sensor dataset
          containing processed daily (24-hr) averaged time-resolution data.
    Raises:
        System exit: If searching for recorded sensor datasets and no files
        found with the expected naming scheme or file formatting (files must
        be ordered chronologically, contain the unique serial identifier
        corresponding to the sensor unit that recorded the sensor data file,
        and must be in either .csv or .txt format).
    """
    valid_extensions = ['.csv', '.txt', '.xlsx']

    if load_raw_data is True:
        full_df_list = []
        print('Importing Recorded Sensor Data:')

        for serial in sensor_serials.values():
            sensor_df = pd.DataFrame()
            print('..' + serial)

            file_list = []
            for path, folders, files in os.walk(data_path):
                for filename in files:
                    filename_l = filename.lower()
                    # check the file has one of the listed valid extensions
                    valid_file = any(filename_l.endswith(extension) for
                                     extension in valid_extensions)
                    if serial in filename and valid_file:
                        # Load sensor data and append file datasets
                        cwd = '//'.join([path, filename])
                        print('....' + filename)
                        df = ingest_wrapper(cwd, sensor_name, serial,
                                            data_path)
                        sensor_df = sensor_df.append(df)
                file_list.extend(files)

            # Check if serial ID not found in any file names.
            if not any(serial in file for file in file_list):
                console_out = ('Serial ID ' + serial + ' not found in data '
                               'files:\n' + '\n'.join(files))
                print(console_out)

            if sensor_df.empty:
                console_out = ('No sensor data files found with the expected'
                               ' naming scheme. Files for each sensor must be '
                               'ordered chronologically and contain the sensor'
                               ' serial ID. Files must be either .csv or .txt')
                sys.exit(console_out)

            # any concatenation would happen here
            start = kwargs.get('deploy_bdate', None)
            end = kwargs.get('deploy_edate', None)
            if start is not None:
                sensor_df = sensor_df.loc[start:, :]
            if end is not None:
                sensor_df = sensor_df.loc[:end, :]

            sensor_df = sensor_df.shift(tzone_shift, freq='H')

            full_df_list.append(sensor_df)

        hourly_df_list, daily_df_list = sensor_averaging(full_df_list,
                                                         sensor_serials,
                                                         sensor_name,
                                                         write_to_file,
                                                         path=processed_path)

    else:
        df_tuple = processed_data_search(processed_path,
                                         sensor_serials,
                                         **kwargs)
        full_df_list, hourly_df_list, daily_df_list = df_tuple

    # Compute dewpoint
    full_df_list = dewpoint(full_df_list)
    hourly_df_list = dewpoint(hourly_df_list)

    return full_df_list, hourly_df_list, daily_df_list


def ingest_wrapper(cwd, sensor_name, serial, data_path):
    """Wrapper for ingestion modules. Selects the ingestion module to convert
    sensor-specific data formatting to standardized format for analysis.

    Args:
        cwd (str):
            full path to recorded sensor dataset including the file name.
        sensor_name (str):
            The make and model of the sensor.
        serial (dict):
            The serial identifier unique to each sensor unit
        data_path (str):
            full path to sensor data top directory (contains subdirs for
            processed and raw data, and the setup.json if configured)

    Returns:
        pandas dataframe object:
            Sensor dataframe imported and processed via the appropriate
            ingestion module.
    """
    # If setup json exists for particular sensor, use standard ingest module
    setup_path = os.path.abspath(data_path + '../' + sensor_name
                                 + '_setup.json')

    if os.path.exists(setup_path):
        return standard_ingest(cwd, name=sensor_name,
                               setup_file_path=setup_path)

    # Otherwise, use sensor-specific ingestion modules
#    elif sensor_name == 'Example_Make_Model':
#        return Ingest_Example_Make_Model(cwd)

    elif sensor_name == 'Sensit_RAMP':
        return ingest_sensit_ramp(cwd)

    elif sensor_name == 'PurpleAir_PAII':
        # assuming Thingspeak API dataset
        return ingest_purpleair(cwd, serial)

#    if sensor_name == 'Your_Sensor_Model_Here':
#        return Custom_Ingest_Module_For_Your_Sensor(cwd)

    else:
        sys.exit('No sensor specific import module specified for '
                 + sensor_name)


"""Sensor specific ingestion modules-------------------------------------------
"""


def ingest_example_make_model(cwd):
    """Ingestion module for an example sensor dataset.

    Recorded sensor data are imported and headers are converted into a
    standard format for analysis.

    Args:
        cwd (str): The full path to the sensor data file

    Returns:
        df (Pandas DataFrame object): A dataframe containing sensor data that
            has been converted into standardized syntax
    """
    idx_name = 'Time'

    try:
        df = pd.read_csv(cwd, header=5, index_col=idx_name,
                         parse_dates=[idx_name])
    except FileNotFoundError as e:
        sys.exit(e)

    df.index.name = 'DateTime_UTC'

    # Force non numeric values to Nans
    df = df.apply(lambda x: pd.to_numeric(x, errors='coerce'))

    # Drop unsed columns and rename others to consistent naming scheme
    df = df.drop('Inlet', axis=1)
    df = df.rename(columns={'NO2 (ppb)': 'NO2',
                            'O3 (ppb)': 'O3',
                            'PM2.5 (µg/m³)': 'PM25',
                            'TEMP (°C)': 'Temp',
                            'RH (%)': 'RH',
                            'DP (°C)': 'DP'})
    return df


def ingest_sensit_ramp(cwd):
    """Ingestion module for the Sensit RAMP.

    Args:
        cwd (str): The full path to the sensor data file

    Returns:
        df (Pandas DataFrame object): A dataframe containing sensor data that
            has been converted into standardized syntax
    """

    # List of column names
    col_list = ['Serial_ID', 'DateTime', 'CO_Header', 'CO',
                'NO_Header', 'NO', 'NO2_Header', 'NO2',
                'O3_Header', 'O3', 'CO2_Header', 'CO2',
                'Temp_Header', 'Temp', 'RH_Header', 'RH',
                'PM1_Header', 'PM1', 'PM25_Header', 'PM25',
                'PM10_Header', 'PM10', 'WD_Header', 'WD',
                'WS_Header', 'WS', 'BATT_Header', 'BATT',
                'CHRG_Header', 'CHRG', 'RUN_Header', 'RUN',
                'SD_Header', 'SD', 'RAW_Header', 'RAW_1',
                'RAW_2', 'RAW_3', 'RAW_4', 'RAW_5', 'RAW_6',
                'RAW_7', 'RAW_8', 'STAT_Header', 'STAT_1',
                'STAT_2', 'STAT_3']

    # Load sensor datasets, column names not specified in files (header==None)
    try:
        df = pd.read_csv(cwd, header=None, names=col_list)
    except FileNotFoundError as e:
        sys.exit(e)


    # drop the header columns for RAMP datasets
    drop_headers = [col for col in df.columns if col.endswith('_Header')]
    df = df.drop(columns=drop_headers)

    df.Serial_ID = df.Serial_ID.str.replace('XDATE', '')

    # Set the DateTime columns as the timelike index
    df = df.set_index(pd.to_datetime(df['DateTime']))
    df.index.name = 'DateTime_UTC'

    # Limit dataset to parameter data (exclude columns not used in analysis)
    df = df[['Serial_ID', 'CO', 'NO', 'NO2', 'O3', 'CO2',
             'PM1', 'PM25', 'PM10', 'Temp', 'RH', 'WD', 'WS']]

    return df


def ingest_purpleair(cwd, serial):
    """Ingestion module for the PurpleAir PA-II (and PA-II-SD).

    Args:
        cwd (str):
            The full path to the sensor data file.
        serial (str):
            The serial identifier unique to each sensor unit.

    Returns:
        df (Pandas DataFrame object):
            A dataframe containing sensor data that has been converted into
            standardized syntax.

    NOTE:
        PurpleAir data formatting vary depending on the source of acquisition
    and this module is intended *ONLY* for data downloaded from the Thingspeak
    API.

    The Import() module expects a single data frame for each sensor (sensor_df)
    for use in analysis. Because the PurpleAir PAII contains two internal PM
    sensors corresponding to data channels 'A' and 'B', this ingestion module
    expects data for these seperate channels to be in two unique files.

    Data files for each sensor channel MUST contain the sensor serial ID
    followed immediately by an upper-case 'A' or 'B' depending on the channel
    (e.g., PurpleAir sensor with serial ID de90 must have two associated .csv
    files that contain the phrases 'de90A' for channel A data or 'de90B' for
    channel B data).

    Data for channels A and B are loaded in tandem based on the naming scheme
    for the channel A file (note file names can differ only by the distinction
    of 'A' or 'B' channel data). These data sets are then merged and the
    QC criteria of Barkjohn et al. 2021 are used to computing AB averages.
    Finally, the US-wide correction equation developed by Barkjohn et al. 2021
    is computed for the AB averages and added as an additional column to the
    merged dataset.
    """
    if serial+'A' in cwd:
        # Load data for both channels A and B
        for channel in ['A', 'B']:
            if channel == 'B':
                cwd = cwd.replace(serial+'A', serial+'B')

            try:
                df = pd.read_csv(cwd, encoding='utf-16')
            except FileNotFoundError as e:
                sys.exit(e)

            df = df.rename(columns={'monitor-id': 'Sensor_id',
                                    ' channel-id': 'Channel',
                                    ' created-at': 'DateTime_UTC',
                                    ' entry-id': 'Entry',
                                    ' PM1.0 (ATM)': 'PM1_ATM',
                                    ' PM2.5 (ATM)': 'PM25_ATM',
                                    ' PM10.0 (ATM)': 'PM10_ATM',
                                    ' Uptime': 'Uptime',
                                    ' RSSI': 'RSSI',
                                    ' Temperature': 'Temp',
                                    ' Humidity': 'RH',
                                    ' PM2.5 (CF=1)': 'PM25_CF1',
                                    ' Mem': 'Mem',
                                    ' Adc': 'Adc',
                                    ' Pressure': 'Press',
                                    ' Unused': 'Unused'})

            df.DateTime_UTC = df.DateTime_UTC.str.replace(
                                'T', ' ').str.replace('Z', '').str.lstrip(' ')

            timestamp_fmt = '%Y-%m-%d %H:%M:%S'
            df = df.set_index(pd.to_datetime(df['DateTime_UTC'],
                                             format=timestamp_fmt)
                              ).sort_index()

            df = df.drop(['Sensor_id',
                          'Channel',
                          'DateTime_UTC',
                          'Entry'], axis=1)

            if channel == 'A':
                df_A = df.drop(['RSSI', 'Uptime'], axis=1)
            if channel == 'B':
                df_B = df.drop(['Mem', 'Adc', 'Unused'], axis=1)

        # Merge the channel dataframes
        df = pd.merge_asof(df_A, df_B, on='DateTime_UTC',
                           suffixes=['_a', '_b'], #left_index=True,
                           tolerance=pd.Timedelta('5s'),
                           direction='nearest')
        df = df.set_index('DateTime_UTC', drop=True)

        # Convert Temp from F to C
        df['Temp'] = (df['Temp'] - 32) / 1.8

        # Merge concentrations for A and B channels
        df = purpleair_ab_averages(df, cleaning=True,
                                   a_col_name='PM25_ATM_a',
                                   b_col_name='PM25_ATM_b')

        # US Correction
        df = purpleair_us_corr(df, param='PM25')

        return df

    elif serial + 'B' in cwd:
        return None


#def custom_ingest_module_for_your_sensor(cwd):
#    """Ingestion module for converting your sensor data to standard format.
#    Below are some useful guidelines for setting up your sensor's data
#    ingestion module.
#    """
#    # The name of the column you'd like to set as the time-like index
#    idx_name = 'Timestamp_column'
#
#    # Read in csv files at the current working directory 'cwd'
#    df = pd.read_csv(cwd,
#                     header=0, # Modify if data don't start on the first row
#
#                     # These last two columns are useful if you know there is
#                     # a particular column with timestamps to set as the index
#                     index_col=idx_name,
#                     parse_dates=[idx_name])
#
#    # If the time-like index should to be a combination of columns, (e.g., if
#    # one column has date information and another has time information) this
#    # can be accomplished via some code that looks something like:
#    # df['timestamp_column'] = df['column_A'] + df['column_B']
#
#    # Reset the index name to datetime_UTC. If the timestamp is not in UTC,
#    # you can use something like df.shift(N, freq='H') where N is the number of
#    # hours you want to shift by.
#    df.index.name = 'DateTime_UTC'  # Don't change this line
#
#    # Force non numeric values to Nans
#    # Optional, however this may remove some useful data like QC flags or
#    # status codes. Sometimes this is helpful for setting a consistent numeric
#    # data type for the data in each column to avoid type/value error.
#    df = df.apply(lambda x: pd.to_numeric(x, errors='coerce'))
#
#    # Drop unsed columns and rename others to consistent naming scheme
#    df = df.drop(['Columns', 'you', 'want', 'to', 'drop'] , axis=1)
#    df = df.rename(
#        # Below are some examples of sensor data columns to rename
#        # The list and number of parameters will change depending on your sensor
#        columns={'The label for NO2 in your sensor data files': 'NO2',
#                 'The label for O3 in your sensor data files': 'O3',
#                 'The label for PM2.5 in your sensor data files': 'PM25',
#                 'The label for temperature in your sensor data files': 'Temp',
#                 'The label for relative humidity in your sensor data files': 'RH',
#                 'The label for dewpoint in your sensor data files': 'DP'})
#    return df
