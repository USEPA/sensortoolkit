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

  For example, devices that record multiple datasets simulaneously will require
  custom ingestion methods. Datasets for the PurpleAir PA-II that are obtained
  from the ThingSpeak API may fall into this category, as the API service may
  provide separate datasets for each internal PM sensor (channels A and B).

  For these circumstances, users should create custom functions for importing
  sensor data. When attempting to load sensor data via the AirSensor.load_data()
  method, users should pass the custom ingestion function to load_data().

  Example:

  .. code-block:: python

    # Your custom ingestion function
    def custom_ingestion_method(path_to_data_file, sensor_serial_id):

        # Load data from the file path for the specified sensor unit
        data = pandas.read_csv(path_to_data_file)

        # Other steps you may need to take to convert the data into SDFS format
        # ...

        return data

    # Assuming you have created a AirSensor object named 'sensor'
    # Pass the custom ingest function to the ingest_method attribute
    sensor.load_data(load_raw_data=True,
                     write_to_file=True,
                     ingest_method=custom_ingestion_method)

  If users come across a circumstance where the ``standard_ingest()`` method is
  not successfully able to import sensor data, **users are recommended to create
  a custom ingestion method**.

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
    :param function object ingest_method:
        If not None, ``ingest_wrapper()`` will attempt to import sensor
        data using a passed custom written ingestion module instead of the
        ``standard_ingest()`` method.

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
    ingest_method = kwargs.get('ingest_method', None)
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
                        cwd = os.path.join(path, filename)
                        print('....' + filename)
                        df = ingest_wrapper(cwd, sensor_name, serial,
                                            data_path, ingest_method)

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

        data_dict = sensor_averaging(full_df_list,
                                     sensor_serials,
                                     sensor_name,
                                     write_to_file,
                                     path=processed_path,
                                     **kwargs)

    else:
        data_dict = processed_data_search(processed_path,
                                          sensor_serials,
                                          **kwargs)

    for interval in data_dict:
        for serial in data_dict[interval]:
            if not data_dict[interval][serial].empty:
               data_dict[interval][serial] =  concat_dataset(
                                                   data_dict[interval][serial],
                                                   start, end)

    return data_dict


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


def ingest_wrapper(cwd, sensor_name, serial, data_path, ingest_method):
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
        ingest_method (function object):
            If not None, ``ingest_wrapper()`` will attempt to import sensor
            data using a passed custom written ingestion module instead of the
            ``standard_ingest()`` method.

    Returns:
        pandas DataFrame object:
            Sensor dataframe imported and processed via the appropriate
            ingestion module.
    """
    # If setup json exists for particular sensor, use standard ingest module
    setup_path = os.path.abspath(os.path.join(data_path, '..',
                                              f'{sensor_name}_setup.json'))

    if os.path.exists(setup_path) and ingest_method is None:
        return standard_ingest(cwd, name=sensor_name,
                               setup_file_path=setup_path)
    else:
        return ingest_method(cwd, serial)
