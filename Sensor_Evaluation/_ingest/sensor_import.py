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
  Wed Nov 13 16:35:00 2020
"""
import pandas as pd
import os
import sys
from Sensor_Evaluation._analysis.time_averaging import Sensor_Averaging
from Sensor_Evaluation._ingest.processed_data_loader import Processed_Data_Search
from Sensor_Evaluation._analysis.dewpoint import Dewpoint


def Import(sensor_name=None, sensor_serials=None, tzone_shift=0,
           load_raw_data=False, data_path=None, processed_path=None,
           write_to_file=False):
    """Data import module
    """
    if load_raw_data is True:
        full_df_list = []
        print('Importing Recorded Example Sensor Data:')

        # Could place sensor-specific pre-processing modules here for combining
        # data into format expected below (one csv file per sensor for data
        # collected during testing period)

        for item in os.listdir(data_path):
            if (any(serial in item for serial in list(sensor_serials.values()))
               and (item.startswith(sensor_name))):

                # Data import and cleanup
                cwd = data_path + item
                df = Ingest_Wrapper(cwd, sensor_name)

                df = df.shift(tzone_shift, freq='H')
                full_df_list.append(df)

        hourly_df_list, daily_df_list = Sensor_Averaging(full_df_list,
                                                         sensor_serials,
                                                         sensor_name,
                                                         write_to_file,
                                                         path=processed_path)

    else:
        df_tuple = Processed_Data_Search(processed_path, sensor_serials)
        full_df_list, hourly_df_list, daily_df_list = df_tuple

    # Compute dewpoint
    full_df_list = Dewpoint(full_df_list)
    hourly_df_list = Dewpoint(hourly_df_list)

    return full_df_list, hourly_df_list, daily_df_list


def Ingest_Wrapper(cwd, sensor_name):
    """Wrapper for ingestion modules. Selects the ingestion module to convert
    sensor-specific data formatting to standardized format for analysis.
    """

    if sensor_name == 'Example_Make_Model':
        return Ingest_Example_Make_Model(cwd)

#    if sensor_name == 'Your_Sensor_Model_Here':
#        return Custom_Ingest_Module_For_Your_Sensor(cwd)

    else:
        sys.exit('No sensor specific import module specified for', sensor_name)


"""Sensor specific ingestion modules-------------------------------------------
"""


def Ingest_Example_Make_Model(cwd):
    """Ingestion function for translating recorded sensor data into standard
    format for analysis.
    """
    idx_name = 'Time'

    df = pd.read_csv(cwd, header=5, index_col=idx_name,
                     parse_dates=[idx_name])

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

#def Custom_Ingest_Module_For_Your_Sensor(cwd):
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