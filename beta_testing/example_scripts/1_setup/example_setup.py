# -*- coding: utf-8 -*-
"""
@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Tue Aug 24 15:46:29 2021
Last Updated:
  Tue Aug 24 15:46:29 2021
"""
import sensortoolkit

# full path to where you would like to place data, figures, reports, etc.
work_path = 'path/to/work-directory'

"""
  ----------------------------------------------------------------------------
   Construct file structure for sensor, specify ingestion formatting scheme
  ----------------------------------------------------------------------------
"""

sensor = sensortoolkit.AirSensor(make='Example_Make',
                                 model='Model',
                                 param_headers=['PM25', 'O3'],
                                 project_path=work_path)

# Run the next line of code to create sub-dirs for sensor data, figures, etc.
sensor.create_directories()

# Copy sensor data into the folder structure
sensor.copy_datasets()

# Run the next line of code to configure the formatting scheme for converting
# recorded sensor data to a standardized format utilized by SensorEvaluation
sensor.sensor_setup()

"""
  ----------------------------------------------------------------------------
   OPTIONAL: If working with AirNowTech datasets, uncomment the following
   lines of code to pre-process AirNowTech files, create separate monthly
   files for PM, gas, met
  ----------------------------------------------------------------------------
"""
# airnowtech_path = 'path/to/airnowtech-download.csv'
# sensortoolkit.reference.preprocess_airnowtech(path=airnowtech_path)
