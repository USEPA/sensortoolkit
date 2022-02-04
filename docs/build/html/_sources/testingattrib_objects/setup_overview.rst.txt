Overview of Instantiating Testing Attributes
============================================

If you've been following the setup process outlined for creating local instances of
testing attribute objects including ``AirSensor``, ``ReferenceMonitor``, and ``Parameter``,
this section recaps the workflow for how to utilize these sensortoolkit testing attribute objects
in a python script.

This overview is divided into two sections describing the workflow for different
use cases. For users starting out fresh with an empty project directory and have
not run the setup modules for either sensor or reference data configurations,
please review the `'Initial Instantiation' <./setup_overview.html#id1>`_ section below. For users who may have
previously conducted an evaluation, walking through the initial workflow including
creating setup configurations for both sensor and reference datasets, individuals can
follow an abbreviated workflow, outlined in the
`'Instantiating from Previously Configured Objects' <./setup_overview.html#id2>`_
section.

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
  :emphasize-lines: 33, 35, 39, 40, 46, 47

  # -*- coding: utf-8 -*-
  """
  Testing attribute setup process for an air sensor and reference monitor in a
  new project directory (located at the project path). At the start of using
  this script, users should have an empty directory in the folder located at
  the project path, except for a python script that contains the commands below.

  Following the use of this script, the following should be contained within
  the user's project directory :

      - `/data`, `/figures`, and `/reports` directories (as well as the
        subfolder structure within the directories)
      - sensor datasets located at `/data/sensor_data/[sensor_name]`
          - raw (i.e., recorded, unmodified)
          - processed (i.e., converted to SDFS)
          - [sensor_name]_setup.json for importing, ingesting, and saving processed
            datasets in SDFS format.
      - reference datasets located at `/data/reference_data/[data_type]/[site_name_site_id]`
          - raw (i.e., recorded, unmodified)
          - processed (i.e., converted to SDFS)
          - reference_setup.json for importing, ingesting, and saving processed
            datasets in SDFS format.

  """
  import sensortoolkit

  sensortoolkit.presets.set_project_path('[path/to/the/evaluation]')

  # AirSensor object instantiation
  sensor = sensortoolkit.AirSensor(make='[Sensor Make]',
                                   model='[Sensor Model]')
  # Create Data and Figures directory, subdirectories
  sensor.create_directories()
  # Run setup configuration for sensor data, creates setup.json file
  sensor.sensor_setup()

  # Import and loading sensor data for the first time, processed data files will
  # be saved following ingestion.
  sensor.load_data(load_raw_data=True,
                   write_to_file=True)

  # Create a Parameter instance for the pollutant you wish to evaluate
  pollutant = sensortoolkit.Parameter('[Insert pollutant from list of SDFS labels]')

  # Loading reference object for the first time
  reference = sensortoolkit.ReferenceMonitor()
  reference.reference_setup()

  # Load reference data for the evaluation timeframe
  reference.load_data(bdate=sensor.bdate,
                      edate=sensor.edate,
                      param_list=sensor.param_headers,
                      met_data=True)

  # Run SensorEvaluation or PerformanceReport here...

Instantiating from Previously Configured Objects
------------------------------------------------

Users may have occasion to revise or reanalyze sensor datasets at a later date following
an initial round of analysis. If users have previously configured ``AirSensor`` and
``ReferenceMonitor`` objects for a testing scenario, these configurations will be saved to
the ``setup.json`` configuration files for both reference and sensor data. In addition,
processed versions of sensor and reference datasets that have been converted to SDFS
formatting will be have been saved during the initial analysis
to the user's ``/data`` folder within the project directory.

These previously created data structures allow users to reload previously configured
``AirSensor`` and ``ReferenceMonitor`` objects via an abbreviated workflow detailed below.
**Highlighted lines indicate important differences when compared
to an initial instantiation of the sensor and reference objects**.

.. code-block:: python
  :emphasize-lines: 25, 26, 32, 33, 34

  # -*- coding: utf-8 -*-
  """
  In the instance that users have previously run the sensor and reference
  setup configuration modules and wish to utilize these configurations for
  additional, follow-up analysis, users can save some time by loading processed
  versions of the sensor and reference datasets that are already configured in
  `SDFS` format.

  Users should ensure that sensor processed datasets have been created and saved
  to the user's ``/data/sensor_data/[sensor_name]/processed``
  directory during a previous run of the sensor.load_data() module, and
  that processed reference datasets corresponding to the reference data source
  the user intends to utilize are located at
  ``/data/reference_data/[data_source]/processed/[site_name_site_aqs]``
  """
  import sensortoolkit

  sensortoolkit.presets.set_project_path('[path/to/the/evaluation]')

  # AirSensor object instantiation
  sensor = sensortoolkit.AirSensor(make='[Sensor Make]',
                                   model='[Sensor Model]')

  # Load sensor data from processed datasets
  sensor.load_data(load_raw_data=False,
                   write_to_file=False)

  # Create a Parameter instance for the pollutant you wish to evaluate
  pollutant = sensortoolkit.Parameter('[Insert pollutant from list of SDFS labels]')

  # Loading a pre-configured reference object (must indicate source, site, site id if applicable)
  reference = sensortoolkit.ReferenceMonitor(data_source='[Enter the reference data source (lower case)]',
                                             site_name='[Enter the site name (replace spaces with underscores "_")]',
                                             site_id='[Enter the site AQS ID (no spaces)]')

  # Load reference data for the evaluation timeframe
  reference.load_data(bdate=sensor.bdate,
                      edate=sensor.edate,
                      param_list=sensor.param_headers,
                      met_data=True)

  # Run SensorEvaluation or PeformanceReport here...
