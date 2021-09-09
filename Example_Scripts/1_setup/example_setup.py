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
sensor_name = 'Example_Make_Model'

"""
  ----------------------------------------------------------------------------
   Construct file structure for sensor, specify ingestion formatting scheme
  ----------------------------------------------------------------------------
"""

# Run the next line of code to create sub-dirs for sensor data, figures, etc.
sensortoolkit.lib_utils.create_sensor_directories(name=sensor_name,
                                                  eval_params=['PM25', 'O3'],
                                                  path=work_path,
                                                  )

# Copy sensor data into the folder structure
sensortoolkit.lib_utils.copy_datasets(name=sensor_name,
                                      path=work_path
                                      )

# Run the next line of code to configure the formatting scheme for converting
# recorded sensor data to a standardized format utilized by SensorEvaluation
IngestionConfig = sensortoolkit.lib_utils.Setup(name=sensor_name,
                                                path=work_path)

"""
  ----------------------------------------------------------------------------
   OPTIONAL: If working with AirNowTech datasets, uncomment the following
   lines of code to pre-process AirNowTech files, create separate monthly
   files for PM, gas, met
  ----------------------------------------------------------------------------
"""
# airnowtech_path = 'path/to/airnowtech-download.csv'
# sensortoolkit.reference.preprocess_airnowtech(airnowtech_path)
