***************************************************
Conducting Analysis with the SensorEvaluation Class
***************************************************

`sensortoolkit` contains dozens of individual modules and functions for computing
statistical metrics and generating figures in accordance with U.S. EPA's recommended
`performance metrics and targets <https://www.epa.gov/air-sensor-toolbox/air-sensor-performance-targets-and-testing-protocols>`_.
The ``SensorEvaluation`` class packages many of `sensortoolkit`'s modules into
a user-friendly and efficient platform for evaluating sensor performance.

=========================================
A brief overview of ``SensorEvaluation``:
=========================================

* Loads unprocessed, recorded sensor data and converts datasets to `sensortoolkit`'s
  Sensor Data Formatting Scheme (S-DFS).
* Saves processed S-DFS datasets at recorded sampling frequnecy, and 1-hour and 24-hour averages
* Retreival of reference data from reference data repositories (AQS, AirNow) or local
  import of reference datasets, including support for downloaded datasets from AirNowTech.
  Reference data from any of the sources listed are translated into `sensortoolkit`'s
  Reference Data Formatting Standard (R-DFS) and are saved locally as .csv files.
* Time alignment of sensor and reference data to UTC timestamps.
* Computes various quantitites and metrics recommended by U.S. EPA's performance targets reports
  including precision (standard deviation, coefficient of variation), error (RMSE),
  linarity (:math:`R^2`), and bias (OLS regression slope and intercept).
* Contains numerous plotting methods for displaying and saving figures for
  time series, sensor vs. reference scatter, meteorological conditions, etc.
* Contains methods for printing summary statistics for evaluation conditions and
  performance evaluation results using U.S EPA's recommended performance metrics.

Below is an example instantiating the `SensorEvaluation` class for the `Example_Make_Model`
sensor datasets included alongside `sensortoolkit`. This example is for an evaluation of
PM2.5 sensor data against reference data retieved from AirNowTech (*further discussion of
reference data sources follows below*).

.. code-block:: python

  Eval = SensorEvaluation(sensor_name='Example_Make_Model',
                          eval_param='PM25',
                          work_path=work_path,
                          reference_data=ref_path,
                          serials={'1': 'SN01',
                                   '2': 'SN02',
                                   '3': 'SN03'},
                          tzone_shift=5,
                          load_raw_data=False,
                          write_to_file=True)

.. note::
  ``Eval`` is the name given to the ``SensorEvaluation`` class instance. Users are not required
  to refer to their class instances as ``Eval`` and can instead assign whichever name suits best.

  Please note that subsequent reference to ``SensorEvaluation`` instance attributes and
  modules will use the name ``Eval``.

Console Output:

.. code-block:: console

  Loading processed sensor data
  ..Example_Make_Model_SN01_daily.csv
  ..Example_Make_Model_SN01_full.csv
  ..Example_Make_Model_SN01_hourly.csv
  ..Example_Make_Model_SN02_daily.csv
  ..Example_Make_Model_SN02_full.csv
  ..Example_Make_Model_SN02_hourly.csv
  ..Example_Make_Model_SN03_daily.csv
  ..Example_Make_Model_SN03_full.csv
  ..Example_Make_Model_SN03_hourly.csv
  Loading reference dataframes
  ..2019-08
  ....H_201908_PM.csv
  ....H_201908_Met.csv
  ....H_201908_Gases.csv
  ..2019-09
  ....H_201909_PM.csv
  ....H_201909_Met.csv
  ....H_201909_Gases.csv
  Computing normalized PM25 values (by T-API T640X at 16.67 LPM)
  Computing normalized PM25 values (by T-API T640X at 16.67 LPM)
  Computing mean parameter values across concurrent sensor datasets
  Computing mean parameter values across concurrent sensor datasets

Arguments passed to ``SensorEvaluation``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``sensor_name``: The name of the sensor, should be the same name passed to the
  ``Create_Sensor_Directories()`` and ``Setup()`` methods.
* ``eval_param``: The parameter to evaluate, should be one of the parameters
  listed in the eval_params list passed to the ``Create_Sensor_Directories()`` method.
* ``work_path``: The path to the directory where the user intends to store data, figures,
  and reports
* ``reference_data``: The service or folder directory from which reference data
  are acquired. More detail about the different options for reference data acquisition below...
* ``serials``: A dictionary of sensor serial identifiers for each unit in a testing group.
* ``tzone_shift``: An integer value by which to shift the sensor data to UTC.
  Specifying ``0`` will not shift the data.
* ``load_raw_data``: If true, raw data in the appropriate subdirectory will be
  loaded and 1-hour and 24-hour averages will be computed and saved to a processed
  data subdirectory for the specified sensor. If false, processed data will be loaded.
* ``write_to_file``: If true and load_raw_data true, processed files will be
  written to folder location. In addition, subsequent evaluation statistics will
  be written to the Data and Figures/eval_stats sensor subdirectory. Figures will
  also be written to the appropriate figures subdirectory.
* kwargs (tip about for evaluation dates (other kwargs?))

==============
Reference Data
==============

Upon creation of a class instance, the user must indicate what reference data
to use. Users can either specify that reference data should be retrieved by API
query (AirNow or AQS) or imported from a local destination (e.g., .csv files
downloaded from AirNowTech). Note that both the AirNow and AQS APIs require
users have an account and key to complete successful queries. AirNowTech also
requires a user account to access its online data portal. Accounts for these
services are free and can created via the following links
(`AirNowTech account request <https://www.airnowtech.org/requestAccnt.cfm>`_,
`AirNow API account request <https://docs.airnowapi.org/account/request/>`_,
`AQS API sign up <https://aqs.epa.gov/aqsweb/documents/data_api.html#signup>`_).

The use of each service involves a slightly difference process for data retreival,
and arguments that must be passed to ``SensorEvaluation`` at the time of instantiation.
The use of each service with ``SensorEvaluation`` is detailed below:

AirNowTech
^^^^^^^^^^

If users have an AirNowTech account, data files downloaded from https://www.airnowtech.org/data/index.cfm
can be imported for use by the ``SensorEvaluation`` class and `sensortoolkit` modules.

.. important::
  When downloading data from AirNowTech's online data query tool, users should check 'Table' and
  select 'Unpivoted' under the Display Settings box.

`sensortoolkit`'s ``PreProcess_AirNowTech()`` function parses the downloaded dataset
in monthly intervals and creates three separate datasets for particulate matter
(:math:`PM_{2.5}` and :math:`PM_{10}`), gaseous pollutants (:math:`O3`, :math:`NO_2`, :math:`CO`, etc.),
and meteorological parameters (temperature, relative humidity, etc.). These data sets
are processed with `sensortoolkit`'s Reference Data Formatting Standard (R-DFS) and are
saved to ``../Data and Figures/reference_data/airnowtech/processed``.

.. code-block:: python

  import sensortoolkit

  airnowtech_path = 'path/to/airnowtech-download.csv'
  sensortoolkit.PreProcess_AirNowTech(airnowtech_path)


Once AirNowTech datasets have been formatted, the ``SensorEvaluation`` class can
be instantiated, where the ``reference_data`` argument is set to the full directory
path for the processed AirNowTech datasets:

.. code-block:: python

  from sensortoolkit import SensorEvaluation

  work_path = 'C:/Users/.../Documents/my_evaluation'
  ref_path = work_path + '/Data and Figures/reference_data/airnowtech/processed'

  # Mock evaluation using AIRS reference data downloaded from AirNowTech
  Eval = SensorEvaluation(sensor_name='Example_Make_Model',
                          eval_param='PM25',
                          work_path=work_path,
                          reference_data=ref_path,
                          bbox=AIRS_bbox,
                          serials={'1': 'SN01',
                                   '2': 'SN02',
                                   '3': 'SN03'},
                          tzone_shift=5,
                          load_raw_data=False,
                          write_to_file=False)


.. note::

  The sensor name, evaluation parameter, serials, timezone shift, load raw data
  option, and write to file option should be configured by the user for their
  unique use case and may differ from those shown above.

AQS API
^^^^^^^
To query AQS for reference data corresponding to the specified evaluation parameter,
the AQS site ID corresponding to the ambient monitoring site of interest must be specified.
The example below specifies the AQS Site ID for the Triple Oaks monitoring
site in Raleigh NC, nearby EPA’s testing site for sensor evaluations.
To determine the AQS ID for sites nearby a testing location, please visit `EPA's AirData
Air Quality Monitor Map <https://epa.maps.arcgis.com/apps/webappviewer/index.html?id=5f239fd3e72f424f98ef3d5def547eb5&extent=-146.2334,13.1913,-46.3896,56.5319>`_.
Additionally, the reference_data parameter should be set to ``AQS``

.. code-block:: python

  from sensortoolkit import SensorEvaluation

  work_path = 'C:/Users/.../Documents/my_evaluation'

  # Mock evaluation using Triple Oak AQS site (nearby AIRS) reference data
  # obtained from the AQS API
  triple_oaks_ID = {"state": "37",
                    "county": "183",
                    "site": "0021"}

  SensorEvaluation.aqs_username = 'username_address@email.com'
  SensorEvaluation.aqs_key = 'Your-AQS-Key-Here'

  Eval = SensorEvaluation(sensor_name='Example_Make_Model',
                          eval_param='PM25',
                          work_path=work_path,
                          reference_data='AQS',
                          aqs_id=triple_oaks_ID,
                          serials={'1': 'SN01',
                                   '2': 'SN02',
                                   '3': 'SN03’},
  		                    tzone_shift=5,
                          load_raw_data=True,
                          write_to_file=True)

.. note::

  The sensor name, evaluation parameter, serials, timezone shift, load raw data
  option, and write to file option should be configured by the user for their
  unique use case and may differ from those shown above.

Console Output:

.. code-block:: console

    Loading processed sensor data
    ..Example_Make_Model_SN01_daily.csv
    ..Example_Make_Model_SN01_full.csv
    ..Example_Make_Model_SN01_hourly.csv
    ..Example_Make_Model_SN02_daily.csv
    ..Example_Make_Model_SN02_full.csv
    ..Example_Make_Model_SN02_hourly.csv
    ..Example_Make_Model_SN03_daily.csv
    ..Example_Make_Model_SN03_full.csv
    ..Example_Make_Model_SN03_hourly.csv
    Querying AQS API
    ..Query start: 2019-08-01
    ..Query end: 2019-08-31
    ..Query site(s):
    ....Site name: Triple Oak
    ......AQS ID: 37-183-0021
    ......Latitude: 35.8652
    ......Longitude: -78.8197
    ..Query Status: Success
    Querying AQS API
    ..Query start: 2019-09-01
    ..Query end: 2019-09-30
    ..Query site(s):
    ....Site name: Triple Oak
    ......AQS ID: 37-183-0021
    ......Latitude: 35.8652
    ......Longitude: -78.8197
    ..Query Status: Success
    Writing AQS query dataframes to csv files
    ../reference_data/aqs/processed/AQS_37-183-0021_PM25_B190801_E190902.csv
    ../reference_data/aqs/raw_api_datasets/AQS_raw_37-183-0021_PM25_B190801_E190902.csv
    Computing normalized PM25 values (by Met One BAM-1022 PM2.5 w/ VSCC or TE-PM2.5C FEM)
    Computing normalized PM25 values (by Met One BAM-1022 PM2.5 w/ VSCC or TE-PM2.5C FEM)
    Computing mean parameter values across concurrent sensor datasets
    Computing mean parameter values across concurrent sensor datasets


* The AQS API is queried in monthly intervals for PM25 reference data recorded at
  the Triple Oaks air monitoring site, which was selected based on its proximity
  to the site where the air sensor was deployed. AQS returns a successful query,
  and the console indicates data were retrieved from the Triple Oaks monitoring
  site for the months of August and September 2019. AQS data are then parsed
  into the reference data format described in the parameter naming scheme data
  dictionary. Both raw (unmodified datasets as returned by the API) and
  processed datasets are written to .csv files at the folder path printed to the
  console.
* Sensor PM25 concentrations are normalized against reference measurements (this
  particular AQS query indicates that the reference monitor is a Met One BAM-1022).
* The mean across sensor measurements is also calculated.
* Processed sensor data are loaded

AirNow API
^^^^^^^^^^

To query AirNow for reference data corresponding to the specified evaluation
parameter, the parameter bbox  must be specified. AirNow returns all relevant
data within a bounding box region. The example on the right specifies a small
bounding box surrounding EPA’s testing site (AIRS) located at the Agency’s RTP
campus. Users are encouraged to set narrow margins for the bounding box surrounding
the air monitoring site of interest. Additionally, the reference_data parameter
should be set to ``AirNow``.

.. code-block:: python

  from sensortoolkit import SensorEvaluation

  work_path = 'C:/Users/.../Documents/my_evaluation'

  # bbox for AIRS [set narrow margins (+/- 0.01 deg) around known coordinates]
  AIRS_bbox = {"minLat": "35.88",
               "maxLat": "35.89",
               "minLong": "-78.88",
               "maxLong": "-78.87"}

  SensorEvaluation.airnow_key = 'Your-AirNow-Key-Here'

  # Mock evaluation using AIRS reference data obtained from the AirNow API
  Eval = SensorEvaluation(sensor_name='Example_Make_Model',
                          eval_param='PM25',
                          work_path=work_path,
                          reference_data='AirNow',
                          bbox=AIRS_bbox,
                          serials={'1': 'SN01',
                                   '2': 'SN02',
                                   '3': 'SN03'},
                          tzone_shift=5,
                          load_raw_data=False,
                          write_to_file=False)


.. note::

  The sensor name, evaluation parameter, serials, timezone shift, load raw data
  option, and write to file option should be configured by the user for their
  unique use case and may differ from those shown above.

Console Output:

.. code-block:: console

  Loading processed sensor data
  ..Example_Make_Model_SN01_daily.csv
  ..Example_Make_Model_SN01_full.csv
  ..Example_Make_Model_SN01_hourly.csv
  ..Example_Make_Model_SN02_daily.csv
  ..Example_Make_Model_SN02_full.csv
  ..Example_Make_Model_SN02_hourly.csv
  ..Example_Make_Model_SN03_daily.csv
  ..Example_Make_Model_SN03_full.csv
  ..Example_Make_Model_SN03_hourly.csv
  Querying AirNow API
  ..Query start: 2019-08-01
  ..Query end: 2019-08-31
  ..Query site(s):
  ....Site name: Burdens Creek
  ......AQS ID: 37-063-0099
  ......Latitude: 35.8894
  ......Longitude: -78.8747
  ..Query Status: Success
  Querying AirNow API
  ..Query start: 2019-09-01
  ..Query end: 2019-09-30
  ..Query site(s):
  ....Site name: Burdens Creek
  ......AQS ID: 37-063-0099
  ......Latitude: 35.8894
  ......Longitude: -78.8747
  ..Query Status: Success
  Writing AirNow query dataframes to csv files
  ../reference_data/airnow/processed/AirNow_37-063-0099_PM25_B190801_E190902.csv
  ../reference_data/airnow/raw_api_datasets/AirNow_raw_37-063-0099_PM25_B190801_E190902.csv
  Computing normalized PM25 values (by Unknown Reference)
  Computing normalized PM25 values (by Unknown Reference)
  Computing mean parameter values across concurrent sensor datasets
  Computing mean parameter values across concurrent sensor datasets


* The AirNow API is queried in monthly intervals for PM25 reference data recorded
  at monitoring sites within the specified bounding box. AirNow returns a successful
  query, and the console indicates data were retrieved from the Burdens Creek
  monitoring site. AirNow data are then parsed into the reference data format described
  in the parameter naming scheme data dictionary. Both raw (datasets as returned by
  the API) and processed datasets are written to .csv files at the folder path indicated.
* Sensor PM25 concentrations are normalized against reference measurements (AirNow
  does not indicate the name of the reference instrument for the evaluation parameter,
  so the reference is referred to as ’Unknown Reference’).
* The mean across sensor measurements is also calculated.
* Processed sensor data are loaded
