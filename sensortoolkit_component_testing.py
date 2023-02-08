#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 14:31:33 2022

@author: samfrederick
"""
import sensortoolkit

"""
On import, the following warnings were raised:

/Users/samfrederick/opt/anaconda3/lib/python3.8/site-packages/statsmodels/tsa/base/tsa_model.py:7: FutureWarning: pandas.Int64Index is deprecated and will be removed from pandas in a future version. Use pandas.Index with the appropriate dtype instead.
  from pandas import (to_datetime, Int64Index, DatetimeIndex, Period,
/Users/samfrederick/opt/anaconda3/lib/python3.8/site-packages/statsmodels/tsa/base/tsa_model.py:7: FutureWarning: pandas.Float64Index is deprecated and will be removed from pandas in a future version. Use pandas.Index with the appropriate dtype instead.
  from pandas import (to_datetime, Int64Index, DatetimeIndex, Period,
"""

# Configure the project directory where data, figures, etc. will be stored
sensortoolkit.presets.set_project_path('/Users/samfrederick/Documents/sensortoolkit_component_testing')

# Add information about the testing organization that conducted the evaluation
sensortoolkit.presets.test_org = {
    'Deployment name': '[Insert name of deployment]',
    'Org name': ['[Insert organization name line 1]',
                 '[Insert organization name line 2]'],
    'Website': {'website name': '[Insert name of website]',
                'website link': '[Insert website here]'},
    'Contact email': '[Insert email here]',
    'Contact phone': '[Insert phone number here]'}

# Add information about the testing location where sensors were sited
sensortoolkit.presets.test_loc = {
    'Site name': '[Insert name of site] ',
    'Site address': '[Insert site address]',
    'Site lat': '[Insert site latitude]',
    'Site long': '[Insert site longitude]',
    'Site AQS ID': '[If applicable, insert site AQS ID]'}

# Create an AirSensor instance for the sensor you'd like to evaluate
sensor = sensortoolkit.AirSensor(make='Toco',
                                 model='Toucan')

# Construct sensor-specific directories in the project path for data, figures, etc.
#sensor.create_directories()

# Run the interactive setup routine for specifying how to ingest sensor data
#sensor.sensor_setup()

# Import sensor datasets and save processed datasets to the data folder
sensor.load_data(load_raw_data=False,
                 write_to_file=False)

"""
Importing Recorded Sensor Data:
..RT01
....toco_toucan_RT01_raw.csv

..timestamp formatting inconsistent with specified format, 
proceeding by inferring timestamp format

....converting datetime index from EST (UTC -5.0 hours) to UTC.
..RT02
....toco_toucan_RT02_raw.csv
/Users/samfrederick/opt/anaconda3/lib/python3.8/site-packages/sensortoolkit/ingest/_sensor_import.py:259: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  sensor_df = sensor_df.append(df)

..timestamp formatting inconsistent with specified format, 
proceeding by inferring timestamp format

....converting datetime index from EST (UTC -5.0 hours) to UTC.
..RT03
....toco_toucan_RT03_raw.csv
/Users/samfrederick/opt/anaconda3/lib/python3.8/site-packages/sensortoolkit/ingest/_sensor_import.py:259: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  sensor_df = sensor_df.append(df)
  
..timestamp formatting inconsistent with specified format, 
proceeding by inferring timestamp format
"""

# Create a ReferenceMonitor instance for FRM/FEM monitor collocated alongside sensors
#reference = sensortoolkit.ReferenceMonitor()

reference = sensortoolkit.ReferenceMonitor(data_source='airnowtech',
                                           site_name='Burdens_Creek',
                                           site_id='370630099')

# Run the interactive setup routine for specifying how to ingest reference data
#reference.reference_setup()

# Import reference data for parameter types measured by the air sensor, also
# import meteorological data if instruments collocated at monitoring site
reference.load_data(bdate=sensor.bdate,
                    edate=sensor.edate,
                    param_list=sensor.param_headers,
                    met_data=True)
"""
Loading reference dataframes
..2019-08
/Users/samfrederick/opt/anaconda3/lib/python3.8/site-packages/pandas/core/arrays/datetimes.py:1162: UserWarning: Converting to PeriodArray/Index representation will drop timezone information.
  warnings.warn(
....H_201908_PM.csv
....H_201908_Met.csv
....H_201908_Gases.csv
Computing 24-hour averaged reference datasets
"""

# Create a Parameter instance for the pollutant you wish to evaluate
pollutant = sensortoolkit.Parameter('PM25')

# evaluation = sensortoolkit.SensorEvaluation(sensor,
#                                             pollutant,
#                                             reference,
#                                             write_to_file=True)

"""
/Users/samfrederick/opt/anaconda3/lib/python3.8/site-packages/sensortoolkit/calculate/_regression_stats.py:283: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  stats_df = hourly_stats.append(daily_stats)
/Users/samfrederick/opt/anaconda3/lib/python3.8/site-packages/sensortoolkit/calculate/_regression_stats.py:283: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.
  stats_df = hourly_stats.append(daily_stats)
"""

# Create a performance evaluation report for the sensor
report = sensortoolkit.PerformanceReport(sensor,
                                         pollutant,
                                         reference,
                                         write_to_file=True,
                                         figure_search=False
                                         )

"""
FileNotFoundError: [Errno 2] No such file or directory: '/Users/samfrederick/Documents/sensortoolkit_component_testing/figures/Toco_Toucan/PM25/Toco_Toucan_regression_boxplot_PM25_220301.png'
"""

# Generate report
report.CreateReport()