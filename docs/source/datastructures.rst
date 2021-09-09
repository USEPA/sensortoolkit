
******************************
Data Structures and Formatting
******************************
The ``SensorEvaluation`` class contains a number of data structures that store
sensor and reference data, and related statistical metrics. Below is a discussion
of these data structures, as well as the Sensor Data Formattting Scheme (S-DFS) and
Reference Data Formatting Scheme (R-DFS) in which sensor and reference data are formatted.

More detail regarding the ``SensorEvaluation`` class, including its methods and
arguments are included in the `API documentation for SensorEvaluation <../html/_autosummary/sensortoolkit._evaluation.sensor_eval.SensorEvaluation.html>`_

``SensorEvaluation`` Data Structures
====================================

.. note::
  We remind readers that the ``SensorEvaluation`` class can be instantiated with
  whichever name suits the user's needs best, however, below we refer to an instance
  of ``SensorEvaluation`` as ``Eval`` when referencing instance attributes (including data structures).

  See `Conducting Analysis with the SensorEvaluation Class <sensoreval.html>`_ for more information regarding instantiation of the ``SensorEvaluation`` class.


Sensor Data List Containers
---------------------------

Sensor data files that have been imported and processed into the S-DFS scheme are
sorted based on the interval between consecutive timestamps. Data sets at the
original recorded sampling frequency of the sensor are placed in a list named ``Eval.full_df_list``.
Data sets that have been averaged to 1-hour and 24-hour averages are placed in
``Eval.hourly_df_list`` and ``Eval.daily_df_list``, respectively. These lists contain data sets
for all sensors in the evaluation cohort, and are referred to here as list containers
for pandas Dataframes as these lists hold or `contain` data sets in the `pandas.DataFrame object <https://pandas.pydata.org/docs/reference/frame.html>`_
format.

 .. note::
   Data sets for sensor units within each list container are organized by the order
   each unit serial ID appears in the ``Eval.serials`` dictionary.

   For example, if the ``Eval.serials`` dictionary lists three sensors as

   .. code-block:: python

      Eval.serials = {'1': 'SN01',
                      '2': 'SN02',
                      '3': 'SN03'}

   and the associated ``Eval.hourly_df_list`` (or
   ``Eval.full_df_list`` or ``Eval.daily_df_list``) lists three data sets as

   .. code-block:: python

      Eval.hourly_df_list = [pandas.DataFrame,
                             pandas.DataFrame,
                             pandas.DataFrame]

   then the pandas DataFrame object corresponding to sensor ``SN01`` is found at
   the first position within the ``Eval.hourly_df_list``, i.e., index position zero:

   .. code-block:: python

      sn01_dataset =  Eval.hourly_df_list[0]


Example dataset within ``Eval.full_df_list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. note::
      DataFrame object at list position zero shown (``dataset = Eval.full_df_list[0]``). Only the first ten rows are
      displayed.

    .. csv-table:: `Example_Make_Model_SN01_full.csv`
       :file: data/Example_Make_Model_SN01_full.csv
       :header-rows: 1
       :widths: auto

Example dataset within ``Eval.hourly_df_list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  .. note::
    DataFrame object at list position zero shown (``dataset = Eval.hourly_df_list[0]``). Only the first ten rows are
    displayed.

  .. csv-table:: `Example_Make_Model_SN01_hourly.csv`
     :file: data/Example_Make_Model_SN01_hourly.csv
     :header-rows: 1
     :widths: auto

Example dataset within ``Eval.daily_df_list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  .. note::
    DataFrame object at list position zero shown (``dataset = Eval.daily_df_list[0]``). Only the first ten rows are
    displayed.

  .. csv-table:: `Example_Make_Model_SN01_daily.csv`
     :file: data/Example_Make_Model_SN01_daily.csv
     :header-rows: 1
     :widths: auto

Reference Dataframes
--------------------
Both 1-hour and 24-hour averaged data sets are computed for FRM/FEM reference data,
and data sets are organized by parameter classification and adhere to the following
naming convention for the prefix of each DataFrame:

* ``pm_``: Instruments measuring particulate matter (:math:`PM_{1}`, :math:`PM_{2.5}`, :math:`PM_{10}`)

  * ``pm_hourly_ref_df``
  * ``pm_daily_ref_df``

* ``gas_``: Instruments measuring gaseous pollutants (:math:`O_3`, :math:`CO`, :math:`CO_2`, :math:`NO`, :math:`NO_2`, :math:`NO_x`, :math:`SO_2`, :math:`SO_x`)

  * ``gas_hourly_ref_df``
  * ``gas_daily_ref_df``

* ``met_``: Instruments measuring meteorlogical parameters (temperature, relative humidity, pressure, dewpoint, wind speed, wind direction)

  * ``met_hourly_ref_df``
  * ``met_daily_ref_df``

.. tip::

  Since working with six reference dataframes can be challenging to track and retreive
  reference data for the selected ``Eval.param``, the dataframes ``Eval.hourly_ref_df`` and
  ``Eval.daily_ref_df`` are aliases of the reference dataframes corresponding to the parameter
  classification of the ``Eval.param``.

  For instance, if ``Eval.param.name = 'PM25'``, ``Eval.hourly_ref_df`` corresponds to
  ``Eval.pm_hourly_ref_df`` and ``Eval.daily_ref_df`` corresponds
  to  ``Eval.pm_daily_ref_df``. Note that corresponding dataframes point to the same object
  in memory, and as a result, modifications to one dataframe will be reflected in the corresponding
  dataframe.

Performance Evaluation Data Structures
--------------------------------------

Various data structures containing tabular statistics and information about
evaluation conditions can also be constructed. These data structures can be
constructed by running the following line of code:

.. code-block:: python

  Eval.calculate_metrics()

This will constuct the statistics dataframes ``Eval.stats_df`` and ``Eval.avg_stats_df`` and
populate the deployment dictionary ``Eval.deploy_dict`` with details about the evaluation.
More detail about each of these data structures is provided below.

Statistics Dataframes: ``Eval.stats_df`` and ``Eval.avg_stats_df``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sensor vs. FRM/FEM Statisitcs: ``Eval.stats_df``
""""""""""""""""""""""""""""""""""""""""""""""""

DataFrame containing statisitics relating the **sensor vs. FRM/FEM** linearity (:math:`R^2`),
bias (`slope` and `intercept`), `RMSE`, N (Number of sensor-FRM/FEM data point pairs), as well
as the minimum, maximum, and the mean sensor concentration. Data are presented for all
averaging intervals specified by ``Eval.eval_param_averaging``.

``Eval.stats_df`` is saved as a comma-separated value file at ...

Below is an example of ``Eval.stats_df`` for the ``Example_Make_Model`` sensor dataset:

.. csv-table:: `stats_df.csv`
   :file: data/stats_df.csv
   :header-rows: 1
   :widths: auto

Sensor vs. Intersensor Average Statistics: ``Eval.avg_stats_df``
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

DataFrame containing statisitics relating the **sensor vs. intersensor average**
linearity (:math:`R^2`), bias (`slope` and `intercept`), RMSE, N (Number of concurrent
sensor measurements during which all sensors in the testing group reported values), as well as the
minimum, maximum, and the mean sensor concentration. Data are presented for all
averaging intervals specified by ``Eval.eval_param_averaging``.

``Eval.avg_stats_df`` is saved as a comma-separated value file at ...

Below is an example of ``Eval.stats_df`` for the ``Example_Make_Model`` sensor dataset:

.. csv-table:: `avg_stats_df.csv`
   :file: data/avg_stats_df.csv
   :header-rows: 1
   :widths: auto

Deployment Dictionary: ``Eval.deploy_dict``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The deployment dictionary ``Eval.deploy_dict`` contains descriptive statistics and textual information about
the deployment, including details about the testing agency, deployment site,
sensors tested, and site conditions during the evaluation.

The top level organizes details by deployment group, testing information, and
testing location. A deployment group is defined as a collection of sensors that are
collocated and concurrently recording data during a consecutive timeframe.

Expanding the deployment group field, three subfields are listed detailing sensor
descriptions (‘sensors’), statistics pertaining to the evaluation parameter (‘PM25’),
and statistics describing the meteorological site conditions during the deployment
(‘Meteorological Conditions’). Timestamps for the start, end, and duration of the
evaluation are also listed (derived from sensor dataset timestamps).

The parameter statistics subfield contains categories for sensor-sensor (inter-sensor)
precision, error relative to FRM/FEM, and reference (FRM/FEM) measurement statistics.
The example shown below is for a scenario where the evaluation parameter is ‘PM25’
(PM2.5). Statistics are presented at sampling frequencies indicated for the
evaluation parameter via the  eval_param_averaging instance attribute.

The Meteorological Conditions subfield contains statistics pertaining to
temperature, relative humidity, and other parameters measured by instruments
at the testing site. These measurements are independent of air sensor meteorological
measurements collected by internal sensing components.

The deployment dictionary ``Eval.deploy_dict`` is saved as a JSON file to ...

Below is an example of ``Eval.deploy_dict`` for the ``Example_Make_Model`` sensor dataset:

.. code-block:: json

  {
      "sensortoolkit Version": "1.0.0",
      "Date of Analysis": "2021-08-25 09:46:19 AM",
      "Testing Organization": {
          "Deployment number": "Deployment #1",
          "Org name": [
              "U.S. Environmental Protection Agency",
              "Office of Research and Development"
          ],
          "Website": {
              "website name": "Air Sensor Toolbox | U.S. EPA Website",
              "website link": "https://www.epa.gov/air-sensor-toolbox/evaluation-emerging-air-sensor-performance"
          },
          "Contact email": "PI: Clements.Andrea@epa.gov",
          "Contact phone": "919-541-1364"
      },
      "Testing Location": {
          "Site name": "Ambient Monitoring Innovative Research Station (AIRS) ",
          "Site address": "Research Triangle Park, NC",
          "Site lat": "35.889510N",
          "Site long": "-78.874572W",
          "Site AQS ID": "37 \u2013 063 \u2013 0099"
      },
      "Sensor Name": "Example_Make_Model",
      "Deployment Groups": {
          "Group 1": {
              "eval_start": "2019-08-01 12:11:00",
              "eval_end": "2019-09-02 04:59:00",
              "eval_duration": "31 days 16:48:00",
              "sensors": {
                  "1": {
                      "serial_id": "SN01",
                      "deploy_issues": "False",
                      "recording_interval": "1.0 minute",
                      "uptime_1-hour": 97.368,
                      "uptime_24-hour": 93.75
                  },
                  "2": {
                      "serial_id": "SN02",
                      "deploy_issues": "False",
                      "recording_interval": "1.0 minute",
                      "uptime_1-hour": 97.632,
                      "uptime_24-hour": 93.75
                  },
                  "3": {
                      "serial_id": "SN03",
                      "deploy_issues": "False",
                      "recording_interval": "1.0 minute",
                      "uptime_1-hour": 97.632,
                      "uptime_24-hour": 93.75
                  }
              },
              "PM25": {
                  "Precision": {
                      "cv_1-hour": 13.094,
                      "std_1-hour": 0.581,
                      "n_1-hour": 736,
                      "cv_24-hour": 7.091,
                      "std_24-hour": 0.313,
                      "n_24-hour": 30
                  },
                  "Error": {
                      "rmse_1-hour": 3.798,
                      "nrmse_1-hour": 48.561,
                      "rmse_24-hour": 3.615,
                      "nrmse_24-hour": 46.804
                  },
                  "Reference": {
                      "reference_name": "Teledyne API T640x",
                      "conc_min_1-hour": 3.352,
                      "conc_max_1-hour": 15.318,
                      "n_exceed_conc_goal_1-hour": 0,
                      "conc_min_24-hour": 4.999,
                      "conc_max_24-hour": 11.087,
                      "n_exceed_conc_goal_24-hour": 0
                  }
              },
              "Meteorological Conditions": {
                  "Temperature": {
                      "instrument_name": "RM Young 41382 VC",
                      "min_1-hour": 14.348,
                      "max_1-hour": 37.735,
                      "n_exceed_target_criteria_1-hour": 0,
                      "n_measurement_pairs_1-hour": 758.0,
                      "min_24-hour": 21.21,
                      "max_24-hour": 28.956,
                      "n_exceed_target_criteria_24-hour": 0,
                      "n_measurement_pairs_24-hour": 32.0
                  },
                  "Relative Humidity": {
                      "instrument_name": "RM Young 41382 VC",
                      "min_1-hour": 24.933,
                      "max_1-hour": 97.0,
                      "n_exceed_target_criteria_1-hour": 172,
                      "n_measurement_pairs_1-hour": 758.0,
                      "min_24-hour": 60.369,
                      "max_24-hour": 88.171,
                      "n_exceed_target_criteria_24-hour": 0,
                      "n_measurement_pairs_24-hour": 32.0
                  }
              }
          }
      }
  }

.. note::
  ``n_exceed_conc_goal`` (1-hour/24-hour) for the evaluation parameter reference
  is the number of averaging intervals during which the reference concentration
  exceeds the EPA’s recommended elevated concentration value for either PM2.5
  (>25 μg/m3) or O3 (> 60 ppbv) testing.

  This term as it relates to the ``Meteorological_Conditions`` subcategories for
  temperature and relative humidity indicate the number of intervals during which
  conditions exceeded the manufacturer's recommended operating range.


Sensor and Reference Data Formatting
====================================

Sensor Data Formatting Standard (S-DFS)
---------------------------------------

.. csv-table:: `S-DFS`
   :file: data/S_DFS.csv
   :header-rows: 1
   :widths: auto

Reference Data Formatting Standard (R-DFS)
------------------------------------------

.. csv-table:: `R-DFS`
   :file: data/R_DFS.csv
   :header-rows: 1
   :widths: auto


Setup.JSON
----------

Setup.json files are generated by running the Setup module and contain information
about recorded sensor datasets that is used by the standard ingestion module
(``sensortoolkit.sensor_ingest.standard_ingest()``).

As sensors often record data with different formatting and header naming schemes,
these files assist in converting data recorded in their original format into S-DFS
scheme for parameter data names and date/time formatting.

.. code-block:: json

  {
      "name": "Example_Make_Model",
      "work_path": "C:/Users/.../Documents/my_evaluation",
      "dtype": ".csv",
      "all_col_headers": [
          "Time",
          "NO2 (ppb)",
          "O3 (ppb)",
          "PM2.5 (\u00b5g/m\u00b3)",
          "TEMP (\u00b0C)",
          "RH (%)",
          "DP (\u00b0C)",
          "Inlet"
      ],
      "timestamp_col_headers": [
          "Time"
      ],
      "drop_cols": [
          "Inlet"
      ],
      "header_iloc": 5,
      "file_list": [
          "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN01_raw.csv",
          "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN02_raw.csv",
          "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN03_raw.csv"
      ],
      "data_path": "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data",
      "col_headers": {
          "col_idx_0": {
              "Time": {
                  "SDFS_param": "DateTime_UTC",
                  "files": [
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN01_raw.csv"
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN02_raw.csv",
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN03_raw.csv"
                  ]
              }
          },
          "col_idx_1": {
              "NO2 (ppb)": {
                  "SDFS_param": "NO2",
                  "files": [
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN01_raw.csv",
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN02_raw.csv",
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN03_raw.csv"
                  ]
              }
          },
          "col_idx_2": {
              "O3 (ppb)": {
                  "SDFS_param": "O3",
                  "files": [
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN01_raw.csv",
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN02_raw.csv",
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN03_raw.csv"
                  ]
              }
          },
          "col_idx_3": {
              "PM2.5 (\u00b5g/m\u00b3)": {
                  "SDFS_param": "PM25",
                  "files": [
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN01_raw.csv",
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN02_raw.csv",
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN03_raw.csv"
                  ]
              }
          },
          "col_idx_4": {
              "TEMP (\u00b0C)": {
                  "SDFS_param": "Temp",
                  "files": [
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN01_raw.csv",
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN02_raw.csv",
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN03_raw.csv"
                  ]
              }
          },
          "col_idx_5": {
              "RH (%)": {
                  "SDFS_param": "RH",
                  "files": [
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN01_raw.csv",
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN02_raw.csv",
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN03_raw.csv"
                  ]
              }
          },
          "col_idx_6": {
              "DP (\u00b0C)": {
                  "SDFS_param": "DP",
                  "files": [
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN01_raw.csv",
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN02_raw.csv",
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN03_raw.csv"
                  ]
              }
          },
          "col_idx_7": {
              "Inlet": {
                  "SDFS_param": "",
                  "files": [
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN01_raw.csv",
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN02_raw.csv",
                      "C:/Users/.../Documents/test_dir/Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN03_raw.csv"
                  ]
              }
          }
      },
      "param_col_list": [
          "NO2 (ppb)",
          "O3 (ppb)",
          "PM2.5 (\u00b5g/m\u00b3)",
          "TEMP (\u00b0C)",
          "RH (%)",
          "DP (\u00b0C)",
          "Inlet"
      ],
      "time_format_dict": {
          "Time": "%Y/%m/%d %H:%M:%S"
      }
  }
