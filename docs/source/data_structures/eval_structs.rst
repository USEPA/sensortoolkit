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
   :file: ../data/stats_df.csv
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
   :file: ../data/avg_stats_df.csv
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
