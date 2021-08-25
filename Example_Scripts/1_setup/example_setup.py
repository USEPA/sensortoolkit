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
  Tue Aug 24 15:46:29 2021
Last Updated:
  Tue Aug 24 15:46:29 2021
"""
import sensortoolkit

# full path to where you would like to place data, figures, reports, etc.
work_path = 'path/to/work-directory'

# If the work directory is different than the library folder, change the
# line below with the path to the library: e.g., user/documents/sensor-evaluation
lib_path = None

"""
  ----------------------------------------------------------------------------
   Construct file structure for sensor, specify ingestion formatting scheme
  ----------------------------------------------------------------------------
"""
# Run the next line of code to create sub-dirs for sensor data, figures, etc.
sensortoolkit.Create_Sensor_Directories(name='Example_Make_Model',
                                        eval_params=['PM25', 'O3'],
                                        work_path=work_path,
                                        lib_path=lib_path,
                                        )

# Code for copying sensor data into the folder structure?

# Run the next line of code to configure the formatting scheme for converting
# recorded sensor data to a standardized format utilized by SensorEvaluation
IngestionConfig = sensortoolkit.Setup(work_path)

"""
  ----------------------------------------------------------------------------
   OPTIONAL: If working with AirNowTech datasets, uncomment the following
   lines of code to pre-process AirNowTech files, create separate monthly
   files for PM, gas, met
  ----------------------------------------------------------------------------
"""
# airnowtech_path = 'path/to/airnowtech-download.csv'
# sensortoolkit.PreProcess_AirNowTech(airnowtech_path)
