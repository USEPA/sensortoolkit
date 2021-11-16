# -*- coding: utf-8 -*-
"""
In the instance that users have previously run the sensor and reference
setup configuration modules and wish to utilize these configurations for
additional, follow-up analysis, users can save some time by loading processed
versions of the sensor and reference datasets that are already configured in
the `S-DFS` and `R-DFS` formatting schemes for sensor and reference data,
respectively.

Users should ensurenthat sensor processed datasets have been created and saved
to the user's ``/Data and Figures/sensor_data/[sensor_name]/processed``
directory during a previous run of the sensor_object.load_data() module, and
that processed reference datasets corresponding to the reference data source
the user intends to utilize are located at
``/Data and Figures/reference_data/[data_source]/processed/[site_name_site_aqs]``
"""
import sensortoolkit

work_path = (r'C:\Users\SFREDE01\OneDrive - Environmental Protection Agency '
             '(EPA)\Profile\Documents\sensortoolkit_testing')

# AirSensor object instantiation
sensor_object = sensortoolkit.AirSensor(make='Example_Make',
                                        model='Model',
                                        project_path=work_path)

# Load sensor data from processed datasets
sensor_object.load_data(load_raw_data=False,
                        write_to_file=False)

# Create Parameter attribute for pollutant (PM2.5) for which sensor evaluation
# will be conducted
pollutant = sensortoolkit.Parameter('PM25')

# Loading a pre-configured reference object (indicate source, site, site id
# if applicable)
ref = sensortoolkit.ReferenceMonitor(project_path=work_path,
                                     data_source='airnowtech',
                                     site_name='Burdens Creek',
                                     site_id='370630099')

# Load reference data for the evaluation timeframe
ref.load_data(bdate='2019-08-01',
              edate='2019-09-15',
              param_list=['PM25'],
              met_data=True)

# Run SensorEvaluation or PeformanceReport here...
