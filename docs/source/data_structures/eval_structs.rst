Performance Evaluation Data Structures
--------------------------------------

.. role:: raw-html(raw)
   :format: html

Various data structures containing tabular statistics and information about
evaluation conditions can also be constructed. These data structures can be
constructed by running the following line of code:

.. code-block:: python

  evaluation.calculate_metrics()

This will construct the statistics dataframes ``evaluation.stats_df`` and ``evaluation.avg_stats_df`` and
populate the deployment dictionary ``evaluation.deploy_dict`` with details about the evaluation.
More detail about each of these data structures is provided below.

Statistics DataFrames
^^^^^^^^^^^^^^^^^^^^^

Sensor vs. FRM/FEM Statistics: ``evaluation.stats_df``
""""""""""""""""""""""""""""""""""""""""""""""""""""""

A pandas DataFrame containing statistics for the sensor vs. FRM/FEM linearity (:raw-html:`R<sup>2</sup>`),
bias (slope and intercept), RMSE, N (number of sensor-FRM/FEM data point pairs), as well
as the minimum, maximum, and the mean sensor concentration. Data are presented for all
averaging intervals specified by ``evaluation.eval_param_averaging``.

``evaluation.stats_df`` is saved as a comma-separated value file at
``/data/eval_stats/[sensor_name]/[sensor_name]_[parameter]_vs_[reference_name]_stats_df_YYMMDD.csv``

where ``[sensor_name]`` is the name of the sensor, ``[parameter]`` is the SDFS parameter name,
``[reference_name]`` is the name of the reference monitor, and ``YYMMDD`` is the date the figure was compiled.

Below is an example of ``evaluation.stats_df`` for the `Toco Toucan Quickstart Guide example <../quickstart.html#example-scenario-toco-toucan>`_:

.. csv-table:: `stats_df.csv`
   :file: ../data/stats_df_v2.csv
   :header-rows: 1
   :widths: auto

Sensor vs. Intersensor Average Statistics: ``evaluation.avg_stats_df``
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

A pandas DataFrame containing statistics relating the sensor vs. intersensor average
linearity (:raw-html:`R<sup>2</sup>`), bias (slope and intercept), RMSE, N (number of concurrent
sensor measurements during which all sensors in the testing group reported values), as well as the
minimum, maximum, and the mean sensor concentration. Data are presented for all
averaging intervals specified by ``evaluation.eval_param_averaging``.

``evaluation.avg_stats_df`` is saved as a comma-separated value file at
``/data/eval_stats/[sensor_name]/[sensor_name]_[parameter]_vs_[reference_name]_avg_stats_df_YYMMDD.csv``

where ``[sensor_name]`` is the name of the sensor, ``[parameter]`` is the SDFS parameter name,
``[reference_name]`` is the name of the reference monitor, and ``YYMMDD`` is the date the figure was compiled.

Below is an example of ``evaluation.stats_df`` for the `Toco Toucan Quickstart Guide example <../quickstart.html#example-scenario-toco-toucan>`_:

.. csv-table:: `avg_stats_df.csv`
   :file: ../data/avg_stats_df_v2.csv
   :header-rows: 1
   :widths: auto

Deployment Dictionary: ``evaluation.deploy_dict``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The deployment dictionary ``evaluation.deploy_dict`` contains descriptive statistics and textual information about
the deployment, including details about the testing agency, deployment site,
sensors tested, and site conditions during the evaluation.

The top level organizes details by deployment group, testing information, and
testing location. A deployment group is defined as a collection of sensors that are
collocated and concurrently recording data during a consecutive timeframe.

Expanding the deployment group field, three subfields are listed detailing sensor
descriptions (`sensors`), statistics pertaining to the evaluation parameter (`PM25`),
and statistics describing the meteorological site conditions during the deployment
(`Meteorological Conditions`). Timestamps for the start, end, and duration of the
evaluation are also listed (derived from sensor dataset timestamps).

The parameter statistics subfield contains categories for sensor-sensor (inter-sensor)
precision, error relative to FRM/FEM, and reference (FRM/FEM) measurement statistics.
The example shown below is for a scenario where the evaluation parameter is ``PM25``
(:raw-html:`PM<sub>2.5</sub>`). Statistics are presented at sampling frequencies indicated for the
evaluation parameter via the  eval_param_averaging instance attribute.

The Meteorological Conditions subfield contains statistics pertaining to
temperature, relative humidity, and other parameters measured by instruments
at the testing site. These measurements are independent of air sensor meteorological
measurements collected by internal sensing components.

The deployment dictionary ``evaluation.deploy_dict`` is saved as a JSON file to
``/data/eval_stats/[sensor_name]/[sensor_name]_[parameter]_Evaluation_YYMMDD.json``

where ``[sensor_name]`` is the name of the sensor, ``[parameter]`` is the SDFS parameter name,
``[reference_name]`` is the name of the reference monitor, and ``YYMMDD`` is the date the figure was compiled.

Below is an example of ``evaluation.deploy_dict`` for the `Toco Toucan Quickstart Guide example <../quickstart.html#example-scenario-toco-toucan>`_:

.. code-block:: json

  {
      "sensortoolkit Version": "0.9.0b2",
      "Date of Analysis": "2023-02-09 15:49:20 PM",
      "Sensor Name": "Toco_Toucan",
      "Sensor Firmware Version": "Unspecified",
      "Deployment Groups": {
          "Group 1": {
              "sensors": {
                  "1": {
                      "serial_id": "RT01",
                      "deploy_issues": "False",
                      "recording_interval": "1-minute",
                      "uptime_1-hour": 97.271,
                      "uptime_24-hour": 93.548
                  },
                  "2": {
                      "serial_id": "RT02",
                      "deploy_issues": "False",
                      "recording_interval": "1-minute",
                      "uptime_1-hour": 97.544,
                      "uptime_24-hour": 93.548
                  },
                  "3": {
                      "serial_id": "RT03",
                      "deploy_issues": "False",
                      "recording_interval": "1-minute",
                      "uptime_1-hour": 97.544,
                      "uptime_24-hour": 93.548
                  }
              },
              "eval_start": "2019-08-01T12:11:00+0000",
              "eval_end": "2019-09-01T00:59:00+0000",
              "eval_duration": "30 days 12:48:00",
              "PM25": {
                  "Precision": {
                      "cv_1-hour": 12.959,
                      "std_1-hour": 0.585,
                      "n_1-hour": 713,
                      "cv_24-hour": 6.874,
                      "std_24-hour": 0.308,
                      "n_24-hour": 29
                  },
                  "Error": {
                      "rmse_1-hour": 3.646,
                      "nrmse_1-hour": 46.871,
                      "rmse_24-hour": 3.478,
                      "nrmse_24-hour": 44.849
                  },
                  "Reference": {
                      "reference_name": "Teledyne Advanced Pollution Instrumentation T640X",
                      "conc_min_1-hour": 3.3,
                      "conc_max_1-hour": 15.3,
                      "conc_mean_1-hour": 7.779,
                      "n_exceed_conc_goal_1-hour": 0,
                      "conc_min_24-hour": 5.663,
                      "conc_max_24-hour": 11.046,
                      "conc_mean_24-hour": 7.754,
                      "n_exceed_conc_goal_24-hour": 0
                  }
              },
              "Meteorological Conditions": {
                  "Temperature": {
                      "instrument_name": "Instrumental-Electronic or Machine Average",
                      "min_1-hour": 14.3,
                      "max_1-hour": 37.7,
                      "n_exceed_target_criteria_1-hour": null,
                      "n_measurement_pairs_1-hour": 728.0,
                      "min_24-hour": 21.146,
                      "max_24-hour": 28.904,
                      "n_exceed_target_criteria_24-hour": null,
                      "n_measurement_pairs_24-hour": 30.0
                  },
                  "Relative Humidity": {
                      "instrument_name": "Instrumental-Hygrothermograph Electronic or Machine Average",
                      "min_1-hour": 24.0,
                      "max_1-hour": 97.0,
                      "n_exceed_target_criteria_1-hour": null,
                      "n_measurement_pairs_1-hour": 728.0,
                      "min_24-hour": 59.917,
                      "max_24-hour": 87.583,
                      "n_exceed_target_criteria_24-hour": null,
                      "n_measurement_pairs_24-hour": 30.0
                  }
              }
          }
      },
      "Testing Organization": {
          "testing_descrip": "Toco Toucan",
          "org_name": "U.S. Environmental Protection Agency",
          "org_division": "Office of Research and Development",
          "org_type": "",
          "org_website": {
              "title": "Air Sensor Toolbox | U.S. EPA Website",
              "link": "https://www.epa.gov/air-sensor-toolbox"
          },
          "org_contact_email": "Clements.Andrea@epa.gov",
          "org_contact_phone": "919-541-1364"
      },
      "Testing Location": {
          "site_name": "Burdens Creek",
          "site_address": "Research Triangle Park, NC",
          "site_lat": "35.889",
          "site_lon": "-78.874",
          "site_aqs_id": "37-063-0099"
      }
  }

.. note::
  ``n_exceed_conc_goal`` (1-hour/24-hour) for the evaluation parameter reference
  is the number of averaging intervals during which the reference concentration
  exceeds the EPA’s recommended elevated concentration value for either :raw-html:`PM<sub>2.5</sub>`
  (>25 :raw-html:`μg/m<sup>3</sup>`) or :raw-html:`O<sub>3</sub>` (> 60 ppbv) testing.

  This term as it relates to the ``Meteorological_Conditions`` subcategories for
  temperature and relative humidity indicate the number of intervals during which
  conditions exceeded the manufacturer's recommended operating range.
