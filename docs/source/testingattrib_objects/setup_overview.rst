Overview of Instantiating Testing Attributes
============================================

If you've been following the setup process outlined for creating local instances of
testing attribute objects including ``AirSensor``, ``ReferenceMonitor``, and ``Parameter``,
this section recaps the workflow for how to utilize these sensortoolkit testing attribute objects
in a python script.

Initial Instantiation
---------------------

If users are starting out with a new project directory or have not previously
created a setup configuration for the air sensor that the user intends to evaluate,
follow the script below for walking through the process of instantiating new
``AirSensor`` and ``ReferenceMonitor`` objects, including running the setup
module to create ``setup.json`` files for each of these objects.
**Highlighted lines indicate important differences to
specify when compared to subsequent instantiation of the sensor and reference
objects that require use of the setup.json configuration files created during
this initial use-case.**

.. code-block:: python
  :emphasize-lines: 34, 36, 40, 41, 42, 49, 50

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
      - reference datasets located at `/Data and Figures/reference_data/[data_type]/[site_name_site_id]`
          - raw (i.e., recorded, unmodified)
          - processed (i.e., converted to R-DFS)
          - reference_setup.json for importing, ingesting, and saving processed
            datasets in R-DFS format.

  """
  import sensortoolkit

  work_path = (r'C:\Users\...\Documents\sensortoolkit_testing')

  # AirSensor object instantiation
  sensor = sensortoolkit.AirSensor(make='Example_Make',
                                   model='Model',
                                   project_path=work_path)
  # Create Data and Figures directory, subdirectories
  sensor.create_directories()
  # Run setup configuration for sensor data, creates setup.json file
  sensor.sensor_setup()

  # Import and loading sensor data for the first time, shift ahead five hours
  # to UTC. Processed data files will be saved following ingestion.
  sensor.load_data(load_raw_data=True,
                   write_to_file=True,
                   tzone_shift=5)

  # Create Parameter attribute for pollutant (PM2.5) for which sensor evaluation
  # will be conducted
  pollutant = sensortoolkit.param.Parameter('PM25')

  # Loading reference object for the first time
  ref = sensortoolkit.ReferenceMonitor(project_path=work_path)
  ref.reference_setup()

  # Load reference data for the evaluation timeframe
  ref.load_data(bdate='2019-08-01',
                edate='2019-09-15',
                param_list=['PM25'],
                met_data=True)

  # Run SensorEvaluation or PeformanceReport here...

Instantiating from Previously Configured Objects
------------------------------------------------

Instantiating testing attributes from previously configured ``AirSensor`` and
``ReferenceMonitor`` objects. **highlighted lines indicate important differences to
specify when compared to an initial instantiation of the sensor and reference objects**.

.. code-block:: python
  :emphasize-lines: 27, 28, 37, 38, 39

  # -*- coding: utf-8 -*-
  """
  In the instance that users have previously run the sensor and reference
  setup configuration modules and wish to utilize these configurations for
  additional, follow-up analysis, users can save some time by loading processed
  versions of the sensor and reference datasets that are already configured in
  the `S-DFS` and `R-DFS` formatting schemes for sensor and reference data,
  respectively.

  Users should ensure that sensor processed datasets have been created and saved
  to the user's ``/Data and Figures/sensor_data/[sensor_name]/processed``
  directory during a previous run of the sensor_object.load_data() module, and
  that processed reference datasets corresponding to the reference data source
  the user intends to utilize are located at
  ``/Data and Figures/reference_data/[data_source]/processed/[site_name_site_aqs]``
  """
  import sensortoolkit

  work_path = (r'C:\Users\...\Documents\sensortoolkit_testing')

  # AirSensor object instantiation
  sensor_object = sensortoolkit.AirSensor(make='Example_Make',
                                 model='Model',
                                 project_path=work_path)

  # Load sensor data from processed datasets
  sensor_object.load_data(load_raw_data=False,
                          write_to_file=False)

  # Create Parameter attribute for pollutant (PM2.5) for which sensor evaluation
  # will be conducted
  pollutant = sensortoolkit.param.Parameter('PM25')

  # Loading a pre-configured reference object (must indicate source, site, site id
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
