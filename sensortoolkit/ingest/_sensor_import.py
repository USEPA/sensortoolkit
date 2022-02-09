# -*- coding: utf-8 -*-
"""
This module contains wrapper methods for importing and loading sensor data.
These methods call on other methods both within this module and in parallel
modules. For instance, recorded sensor datasets are located by the
``sensor_import()`` method, which subsequently calls methods in the
``_standard_ingest.py`` module for converting these datasets to SDFS format.
``sensor_import()`` can also be used to load previously processed (SDFS
formatted) sensor datasets by calling methods in the
``_processed_data_loader.py`` module.

.. important::

  The ``AirSensor.sensor_setup()`` method can be used to import sensor data from
  a wide range of formatting schemes. However, there may be circumstances in
  which the setup method and underlying generalized ingestion methodology is not
  able to handle certain sensor datasets.

  The PurpleAir PA-II and its datasets fall into this category, as the sensor
  produces two datasets, one for each internal plantower PMS5003 sensor
  (referred to as A and B). In order to import data from the PurpleAir sensor,
  a custom ingestion method named ``ingest_purpleair()`` is included in this
  module.

  When the user wishes to load sensor data, the ``sensor_import()`` method
  will call the ``ingestion_wrapper()`` which determines whether the general
  ingestion method ``sensortoolkit.ingest.standard_ingest()`` should be used, or
  whether a custom ingestion method should be called. For the case of the
  PurpleAir, the ``ingest_purpleair()`` method is called by the
  ``ingestion_wrapper()`` if the name of the sensor contains the phrase
  "purpleair".

  If users come across a circumstance where the ``standard_ingest()`` method is
  not successfully able to import sensor data, **users are recommended to create
  a custom ingestion method**, similar to how the ``ingest_purpleair()`` method
  is used to import PurpleAir data from multiple data channels. A reference to
  the **custom method will need to be added to the** ``ingest_wrapper()``
  **method** so that the ingestion method can be called if the name of the
  sensor matches the device associated with the custom method that was created.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Dec  4 08:57:18 2019
Last Updated:
  Wed Jul 14 10:22:15 2021
"""
import os
import sys
import pandas as pd
from sensortoolkit.datetime_utils import sensor_averaging
from sensortoolkit.ingest import standard_ingest, processed_data_search
from sensortoolkit.calculate import dewpoint, convert_temp


def sensor_import(sensor_name=None, sensor_serials=None,
                  load_raw_data=False, data_path=None, processed_path=None,
                  write_to_file=False, **kwargs):
    """Import recorded or processed sensor data.

    If loading recorded datasets (i.e., load_raw_data is True), the method will
    walk through the directory path where recorded sensor datasets should be
    located (``..//data//sensor_data//Sensor_Name//raw_data``). Users
    must follow the expected naming scheme for files in this location,
    specifying the sensor name and sensor serial identifier for each dataset.
    If multiple files were recorded for each sensor unit, files must be
    chronologically ordered, and the naming scheme specifying sensor serial id
    and sensor make and model must also be adopted. Files must be type '.csv'
    or '.txt'.

    Here are two example cases that follow the expected naming scheme:

    - **Example 1**:

      *Import recorded data from one file per sensor*:

      Say the sensor name is 'Example_Make_Model' and three sensor units were
      tested with the following serial identifiers:

      .. code-block:: python

        sensor_serials = {'1': 'SN01', '2': 'SN02', '3': 'SN03'}

      Let's also assume that the three units each record separate '.csv'
      files. The recorded sensor datasets should be placed at the following
      folder location:

      .. code-block:: console

        '..//data//sensor_data//Example_Make_Model//raw_data'

      The folder structure should look something like:

      .. code-block:: console

        path//to//raw_data//
            Example_Make_Model_SN01.csv
            Example_Make_Model_SN02.csv
            Example_Make_Model_SN03.csv

      These files adhere to the expected file naming scheme and data file
      formatting and will be loaded without issue by the Import method.


    - **Example 2**:

      *Import data from multiple files per sensor within nested subdirectories:*

      For simplicity, let's use the same serial identifiers as before. The
      data will also be located at the same folder path. However, now let's
      say that instead of one file per sensor, datasets are recorded at daily
      intervals over the evaluation period and were collected at weekly
      intervals and organized by unit ID into sub-directories. Let's also say
      that the data files are recorded as .txt files instead of .csv files.
      The data sets can be placed into the ``..//raw_data`` folder path, and
      might look something like:

      .. code-block:: console

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

      .. note::

        If all the files have unique names, one could place all of
        the .txt files in the ``//raw_data//`` directory. This example is simply
        meant to illustrate that the import method can handle these types of
        nested folder structures if the appropriate naming scheme is followed).

    Args:
        sensor_name (str): The make and model of the sensor being evaluated.
        serials (dict): A dictionary of sensor serial identifiers for each unit
            in a testing group
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
            evaluation statistics will be written to the 'data' and
            'eval_stats' sensor subdirectory. Figures will also be written to
            the appropriate figures subdirectory.

    **Keyword Arguments**

    :param str bdate:
        The timestamp (date) marking the beginning of the sensor testing period,
        formatted as ``'YYYY-MM-DD HH:MM:SS'``. Sensor datasets will be
        concatenated to begin at this timestamp.
    :param str edate:
        The timestamp (date) marking the end of the sensor testing period,
        formatted as ``'YYYY-MM-DD HH:MM:SS'``. Sensor datasets will be
        concatenated to end at this timestamp.
    :param bool custom_ingest_module:
        If True, ``ingest_wrapper()`` will attempt to import sensor data using
        a custom written ingestion module instead of the ``standard_ingest()``
        method.

    Returns:
        (tuple): Three-element tuple containing:

            - **full_df_list** (*list*): List of pandas dataframe objects, one
              for each sensor dataset containing processed full time-resolution
              data.
            - **hourly_df_list** (*list*): List of pandas dataframe objects, one
              for each sensor dataset containing processed hourly averaged
              time-resolution data.
            - **daily_df_list** (*list*): List of pandas dataframe objects, one
              for each sensor dataset containing processed daily (24-hr)
              averaged time-resolution data.

    Raises:
        AttributeError: If searching for recorded sensor datasets and no files
            found with the expected naming scheme or file formatting (files must
            be ordered chronologically, contain the unique serial identifier
            corresponding to the sensor unit that recorded the sensor data file,
            and must be in either .csv or .txt format).

    """
    valid_extensions = ['.csv', '.txt', '.xlsx']
    custom_ingest = kwargs.get('custom_ingest_module', None)
    start = kwargs.get('bdate', None)
    end = kwargs.get('edate', None)

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
                                            data_path, custom_ingest)

                        sensor_df = sensor_df.append(df)

                        if df.attrs != {} and sensor_df.attrs == {}:
                            sensor_df.attrs = df.attrs

                file_list.extend(files)

            # Check if serial ID not found in any file names.
            if not any(serial in file for file in file_list):
                console_out = ('Serial ID ' + serial + ' not found in data '
                               'files:\n' + '\n'.join(file_list))
                print(console_out)

            if sensor_df.empty:
                console_out = ('No sensor data files found with the expected'
                               ' naming scheme. Files for each sensor must be '
                               'ordered chronologically and contain the sensor'
                               ' serial ID. Files must be either .csv or .txt')
                raise AttributeError(console_out)

            sensor_df = sensor_df.sort_index()
            sensor_df = concat_dataset(data=sensor_df, bdate=start, edate=end)

            full_df_list.append(sensor_df)

        hourly_df_list, daily_df_list = sensor_averaging(full_df_list,
                                                         sensor_serials,
                                                         sensor_name,
                                                         write_to_file,
                                                         path=processed_path,
                                                         **kwargs)

    else:
        df_tuple = processed_data_search(processed_path,
                                         sensor_serials,
                                         **kwargs)
        full_df_list, hourly_df_list, daily_df_list = df_tuple

        full_df_list = [concat_dataset(df, start, end)
                        for df in full_df_list]
        hourly_df_list = [concat_dataset(df, start, end)
                          for df in hourly_df_list]
        daily_df_list = [concat_dataset(df, start, end)
                         for df in daily_df_list]

    # Compute dewpoint
    full_df_list = dewpoint(full_df_list)
    hourly_df_list = dewpoint(hourly_df_list)

    return full_df_list, hourly_df_list, daily_df_list


def concat_dataset(data, bdate, edate):
    """Concatenate pandas DataFrame with DateTimeIndex to the specified time
    period (bdate, edate).

    Args:
        data (pandas DataFrame): Air sensor dataset to concatenate.
        bdate (str): The beginning timestamp for the concatenated dataset.
        edate (str): The ending timestamp for the concatenated dataset.

    Returns:
        data (pandas DataFrame): The concatenated sensor dataset.

    """
    if bdate is not None:
        data = data.loc[bdate:, :]
    if edate is not None:
        data = data.loc[:edate, :]
    return data

def ingest_wrapper(cwd, sensor_name, serial, data_path, custom_ingest):
    """Wrapper for ingestion modules. Selects the ingestion module to convert
    sensor-specific data formatting to SDFS format for analysis.

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
        custom_ingest_module (bool):
            If True, ``ingest_wrapper()`` will attempt to import sensor data
            using a custom written ingestion module instead of the
            ``standard_ingest()`` method.

    Returns:
        pandas DataFrame object:
            Sensor dataframe imported and processed via the appropriate
            ingestion module.
    """
    # If setup json exists for particular sensor, use standard ingest module
    setup_path = os.path.abspath(data_path + '../' + sensor_name
                                 + '_setup.json')

    if os.path.exists(setup_path) and custom_ingest is None:
        return standard_ingest(cwd, name=sensor_name,
                               setup_file_path=setup_path)
    else:
        return globals()[custom_ingest](cwd, serial)
        # Otherwise, use sensor-specific ingestion modules
        # if 'purpleair' in sensor_name.lower():
        #     # assuming Thingspeak API dataset
        #     return ingest_purpleair(cwd, serial)

    #    if sensor_name == 'Your_Sensor_Model_Here':
    #        return Custom_Ingest_Module_For_Your_Sensor(cwd)

        # else:
        #     sys.exit('No sensor specific import module specified for '
        #              + sensor_name)


# Sensor specific ingestion modules

# Depreciate custom ingestion module for example dataset
# def ingest_example_make_model(cwd):
#     """Ingestion module for an example sensor dataset.

#     Recorded sensor data are imported and headers are converted into a
#     standard format for analysis.

#     Args:
#         cwd (str): The full path to the sensor data file

#     Returns:
#         df (Pandas DataFrame object): A dataframe containing sensor data that
#             has been converted into standardized syntax
#     """
#     idx_name = 'Time'

#     try:
#         df = pd.read_csv(cwd, header=5, index_col=idx_name,
#                          parse_dates=[idx_name])
#     except FileNotFoundError as e:
#         sys.exit(e)

#     df.index.name = 'DateTime'

#     # Force non numeric values to Nans
#     df = df.apply(lambda x: pd.to_numeric(x, errors='coerce'))

#     # Drop unsed columns and rename others to consistent naming scheme
#     df = df.drop('Inlet', axis=1)
#     df = df.rename(columns={'NO2 (ppb)': 'NO2',
#                             'O3 (ppb)': 'O3',
#                             'PM2.5 (µg/m³)': 'PM25',
#                             'TEMP (°C)': 'Temp',
#                             'RH (%)': 'RH',
#                             'DP (°C)': 'DP'})
#     return df


# def ingest_sensit_ramp(cwd):
#     """Ingestion module for the Sensit RAMP.

#     Args:
#         cwd (str): The full path to the sensor data file

#     Returns:
#         df (Pandas DataFrame object): A dataframe containing sensor data that
#             has been converted into standardized syntax
#     """

#     # List of column names
#     col_list = ['Serial_ID', 'DateTime', 'CO_Header', 'CO',
#                 'NO_Header', 'NO', 'NO2_Header', 'NO2',
#                 'O3_Header', 'O3', 'CO2_Header', 'CO2',
#                 'Temp_Header', 'Temp', 'RH_Header', 'RH',
#                 'PM1_Header', 'PM1', 'PM25_Header', 'PM25',
#                 'PM10_Header', 'PM10', 'WD_Header', 'WD',
#                 'WS_Header', 'WS', 'BATT_Header', 'BATT',
#                 'CHRG_Header', 'CHRG', 'RUN_Header', 'RUN',
#                 'SD_Header', 'SD', 'RAW_Header', 'RAW_1',
#                 'RAW_2', 'RAW_3', 'RAW_4', 'RAW_5', 'RAW_6',
#                 'RAW_7', 'RAW_8', 'STAT_Header', 'STAT_1',
#                 'STAT_2', 'STAT_3']

#     # Load sensor datasets, column names not specified in files (header==None)
#     try:
#         df = pd.read_csv(cwd, header=None, names=col_list)
#     except FileNotFoundError as e:
#         sys.exit(e)


#     # drop the header columns for RAMP datasets
#     drop_headers = [col for col in df.columns if col.endswith('_Header')]
#     df = df.drop(columns=drop_headers)

#     df.Serial_ID = df.Serial_ID.str.replace('XDATE', '')

#     # Set the DateTime columns as the timelike index
#     df = df.set_index(pd.to_datetime(df['DateTime']))
#     df.index.name = 'DateTime'

#     # Limit dataset to parameter data (exclude columns not used in analysis)
#     df = df[['Serial_ID', 'CO', 'NO', 'NO2', 'O3', 'CO2',
#              'PM1', 'PM25', 'PM10', 'Temp', 'RH', 'WD', 'WS']]

#     return df


def pa_thingspeak(cwd, serial):
    """Ingestion module for the PurpleAir PA-II (and PA-II-SD).

    Args:
        cwd (str):
            The full path to the sensor data file.
        serial (str):
            The serial identifier unique to each sensor unit.

    Returns:
        df (Pandas DataFrame object):
            A dataframe containing sensor data that has been converted into
            SDFS format.

    .. important::

      PurpleAir data formatting vary depending on the source of acquisition
      and this module is intended *ONLY* for data downloaded from the
      Thingspeak API.

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
                                    ' created-at': 'DateTime',
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

            df.DateTime = df.DateTime.str.replace(
                                'T', ' ').str.replace('Z', '').str.lstrip(' ')

            timestamp_fmt = '%Y-%m-%d %H:%M:%S'
            df = df.set_index(pd.to_datetime(df['DateTime'],
                                             format=timestamp_fmt)
                              ).sort_index()
            df = df.tz_localize('UTC')

            df = df.drop(['Sensor_id',
                          'Channel',
                          'DateTime',
                          'Entry'], axis=1)

            if channel == 'A':
                df_A = df.drop(['RSSI', 'Uptime'], axis=1)
            if channel == 'B':
                df_B = df.drop(['Mem', 'Adc', 'Unused'], axis=1)

        # Merge the channel dataframes
        df = pd.merge_asof(df_A, df_B, on='DateTime',
                           suffixes=['_a', '_b'], #left_index=True,
                           tolerance=pd.Timedelta('5s'),
                           direction='nearest')
        df = df.set_index('DateTime', drop=True)

        df = df.rename(columns={'Temp': 'Temp_Value',
                                'RH': 'RH_Value',
                                'Press': 'Press_Value'})
        # Convert Temp from F to C
        df['Temp_Value'] = (df['Temp_Value'] - 32) / 1.8

        return df

    if serial + 'B' in cwd:
        return None

def pa_sdcard(cwd, serial):
    """

    Note, this assume preprocessing of datasets:
    - Timestamp column has been changed from 'UTCDateTime' to 'DateTime'
    - Rows where an invalid timestamp entry was encountered (bad formatting)
      were dropped from the preprocessed dataset.

    Args:
        cwd (TYPE): DESCRIPTION.
        serial (TYPE): DESCRIPTION.

    Returns:
        df (TYPE): DESCRIPTION.

    """

    df = pd.read_csv(cwd, parse_dates=['DateTime'], index_col='DateTime')

    file_versions = list(df.firmware_ver.unique())

    if 4.02 in file_versions:
        print('......version 4.02 detected')

        firmware_df = df[df.firmware_ver==4.02]

        firmware_df = firmware_df.rename(
            columns={'hardwareversion,': 'pm1_0_atm,',
                     'pm1_0_atm,': 'pm2_5_atm,',
                     'pm2_5_atm,': 'pm10_0_atm,',
                     'pm10_0_atm,': 'pm1_0_cf_1,',
                     'pm1_0_cf_1,': 'pm2_5_cf_1,',
                     'pm2_5_cf_1,': 'pm10_0_cf_1,',
                     'pm10_0_cf_1,': 'pm2.5_aqi_atm,',
                     'pm2.5_aqi_atm,': 'pm2.5_aqi_cf_1,',
                     'pm2.5_aqi_cf_1,': 'p_0_3_um,',
                     'p_0_3_um,': 'p_0_5_um,',
                     'p_0_5_um,': 'p_1_0_um,',
                     'p_1_0_um,': 'p_2_5_um,',
                     'p_2_5_um,': 'p_5_0_um,',
                     'p_5_0_um,': 'p_10_0_um,',
                     'p_10_0_um,': 'pm1_0_atm_b,',
                     'pm1_0_atm_b,': 'pm2_5_atm_b,',
                     'pm2_5_atm_b,': 'pm10_0_atm_b,',
                     'pm10_0_atm_b,': 'pm1_0_cf_1_b,',
                     'pm1_0_cf_1_b,': 'pm2_5_cf_1_b,',
                     'pm2_5_cf_1_b,': 'pm10_0_cf_1_b,',
                     'pm10_0_cf_1_b,': 'pm2.5_aqi_atm_b,',
                     'pm2.5_aqi_atm_b,': 'pm2.5_aqi_cf_1_b,',
                     'pm2.5_aqi_cf_1_b,': 'p_0_3_um_b,',
                     'p_0_3_um_b,': 'p_0_5_um_b,',
                     'p_0_5_um_b,': 'p_1_0_um_b,',
                     'p_1_0_um_b,': 'p_2_5_um_b,',
                     'p_2_5_um_b,': 'p_5_0_um_b,',
                     'p_5_0_um_b,': 'p_10_0_um_b,',
                     'p_10_0_um_b,': 'gas'})
        firmware_df_idx = firmware_df.index
        firmware_df = firmware_df.drop(columns=['gas'])

        df.loc[firmware_df_idx, :] = firmware_df

    # Firmware prior to v5.00 had the CF=1 and CF=ATM labels swapped.
    version_label_swap = [version for version in file_versions if version < 5.00]

    # Correct labels for older firmware versions
    if version_label_swap != []:
        for version in version_label_swap:
            print('......swapping labels')
            firmware_df = df[df.firmware_ver==version]

            rename = {'pm1_0_atm': 'pm1_0_cf_1',
                     'pm2_5_atm': 'pm2_5_cf_1',
                     'pm10_0_atm': 'pm10_0_cf_1',
                     'pm1_0_cf_1': 'pm1_0_atm',
                     'pm2_5_cf_1': 'pm2_5_atm',
                     'pm10_0_cf_1': 'pm10_0_atm',
                     'pm2.5_aqi_atm': 'pm2.5_aqi_cf_1',
                     'pm2.5_aqi_cf_1': 'pm2.5_aqi_atm',
                     'pm1_0_atm_b': 'pm1_0_cf_1_b',
                     'pm2_5_atm_b': 'pm2_5_cf_1_b',
                     'pm10_0_atm_b': 'pm10_0_cf_1_b',
                     'pm1_0_cf_1_b': 'pm1_0_atm_b',
                     'pm2_5_cf_1_b': 'pm2_5_atm_b',
                     'pm10_0_cf_1_b': 'pm10_0_atm_b',
                     'pm2.5_aqi_atm_b': 'pm2.5_aqi_cf_1_b',
                     'pm2.5_aqi_cf_1_b': 'pm2.5_aqi_atm_b'}

            # Rename old column names with new names
            firmware_df = firmware_df.rename(
                columns={**rename, **{val:key for key, val in rename.items()}})


            firmware_df_idx = firmware_df.index

            df.loc[firmware_df_idx, :] = firmware_df

    drop_cols = ['mac_address',
                #'firmware_ver',  # Keeping firmware version in for time being
                'hardware',
                'adc',
                'mem',
                'rssi',
                'uptime',
                'p_0_3_um',
                'p_0_5_um',
                'p_1_0_um',
                'p_2_5_um',
                'p_5_0_um',
                'p_10_0_um',
                'p_0_3_um_b',
                'p_0_5_um_b',
                'p_1_0_um_b',
                'p_2_5_um_b',
                'p_5_0_um_b',
                'p_10_0_um_b',
                'hardwareversion',
                'pm2.5_aqi_atm',
                'pm2.5_aqi_cf_1',
                'pm2.5_aqi_atm_b',
                'pm2.5_aqi_cf_1_b',
                'gas']

    drop = [i for i in drop_cols if i in df.columns]

    df = df.drop(columns=drop)

    df = df.rename(columns={'current_temp_f': 'Temp_Value',
                            'current_humidity': 'RH_Value',
                            'current_dewpoint_f': 'DP_Value',
                            'pressure': 'Press_Value',
                            'pm1_0_atm': 'PM1_ATM_A_Value',
                            'pm2_5_atm': 'PM25_ATM_A_Value',
                            'pm10_0_atm': 'PM10_ATM_A_Value',
                            'pm1_0_cf_1': 'PM1_CF1_A_Value',
                            'pm2_5_cf_1': 'PM25_CF1_A_Value',
                            'pm10_0_cf_1': 'PM10_CF1_A_Value',
                            'pm1_0_atm_b': 'PM1_ATM_B_Value',
                            'pm2_5_atm_b': 'PM25_ATM_B_Value',
                            'pm10_0_atm_b': 'PM10_ATM_B_Value',
                            'pm1_0_cf_1_b': 'PM1_CF1_B_Value',
                            'pm2_5_cf_1_b': 'PM25_CF1_B_Value',
                            'pm10_0_cf_1_b': 'PM10_CF1_B_Value'
                            })

    # Convert F to C
    df.Temp_Value = convert_temp(df.Temp_Value, verbose=False)
    df.DP_Value = convert_temp(df.DP_Value, verbose=False)

    return df


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
#    # Reset the index name to DateTime. If the timestamp is not in UTC,
#    # you can use something like df.shift(N, freq='H') where N is the number of
#    # hours you want to shift by.
#    df.index.name = 'DateTime'  # Don't change this line
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
