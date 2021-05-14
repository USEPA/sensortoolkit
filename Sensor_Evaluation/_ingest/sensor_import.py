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
#    """
