# -*- coding: utf-8 -*-
"""
Testing attribute setup process for an air sensor and reference monitor in a
new project directory called 'work_path'. At the start of using this script,
users should have an empty directory at the work_path folder, except for a
version of this script that should be housed within the work_path folder.

Following the use of this script, the following should be contained within
the user's project directory:

    - `/Data and Figures` and `/Reports` directories (as well as the subfolder
      structure within the directories)
    - sensor datasets located at `/Data and Figures/sensor_data/[sensor_name]`
        - raw (i.e., recorded, unmodified)
        - processed (i.e., converted to S-DFS)
        - [sensor_name]_setup.json for importing, ingesting, and saving processed
          datasets in S-DFS format.
    - reference datasets located at ``/Data and Figures/reference_data/[data_type]/[site_name_site_id]``
        - raw (i.e., recorded, unmodified)
        - processed (i.e., converted to R-DFS)
        - reference_setup.json for importing, ingesting, and saving processed
          datasets in R-DFS format.

"""
import sensortoolkit

work_path = (r'C:\Users\SFREDE01\OneDrive - Environmental Protection Agency '
             '(EPA)\Profile\Documents\sensortoolkit_testing')

# AirSensor object instantiation
sensor = sensortoolkit.AirSensor(make='Example_Make',
                                 model='Model',
                                 project_path=work_path)
# Create Data and Figures directory, subdirectories
sensor.create_directories()
# Run setup configuration for sensor data, creates setup.json file
sensor.sensor_setup()

# Import and loading sensor data for the first time, processed data files will
# be saved following ingestion.
sensor.load_data(load_raw_data=True,
                 write_to_file=True)

# Create Parameter attribute for pollutant (PM2.5) for which sensor evaluation
# will be conducted
pollutant = sensortoolkit.Parameter('PM25')

# Loading reference object for the first time
ref = sensortoolkit.ReferenceMonitor(project_path=work_path)
ref.reference_setup()

# Load reference data for the evaluation timeframe
ref.load_data(bdate='2019-08-01',
              edate='2019-09-15',
              param_list=['PM25'],
              met_data=True)

# Run SensorEvaluation or PeformanceReport here...
