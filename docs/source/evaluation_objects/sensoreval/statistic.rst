Statistical Methods
-------------------

.. role:: raw-html(raw)
   :format: html

The statistical methods discussed below populate various `performance evaluation data structures <../../data_structures/eval_structs.html#performance-evaluation-data-structures>`_
accessed via the user's ``SensorEvaluation`` instance. Simultaneously, data files (both .csv and .json format)
are written to the user's ``/data/eval_stats/[sensor_name]`` directory (where ``[sensor_name]``
is the name of the air sensor make and model) if the ``write_to_file``
argument specified during instantiation of the ``SensorEvaluation`` object is set to ``True``.

.. note::

 This section provides a brief overview of the statistical methods accessed via
 instances of the ``SensorEvaluation`` class. For more detail on calling these
 methods, click on the link to the API documentation indicated below each
 method header.

-----

``SensorEvaluation.add_deploy_dict_stats()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`API Documentation for add_deploy_dict_stats() <../../api/_autosummary/sensortoolkit.evaluation_objs._sensor_eval.SensorEvaluation.html#sensortoolkit.evaluation_objs._sensor_eval.SensorEvaluation.add_deploy_dict_stats>`_

Description
"""""""""""

**Calculates:**

- CV for 1-hour averaged sensor datasets
- CV for 24-hour averaged sensor datasets
- RMSE for 1-hour averaged sensor datasets
- RMSE for 24-hour averaged sensor datasets
- Reference monitor concentration range, mean concentration during testing period for 1-hour averaged measurements
- Reference monitor concentration range, mean concentration during testing period for 24-hour averaged measurements
- Meteorological monitor measurement range, mean value for temperature and/or relative humidity measurements at 1-hour intervals
- Meteorological monitor measurement range, mean value for temperature and/or relative humidity measurements at 24-hour intervals

**Populates:**

- ``SensorEvaluation.deploy_dict``

**Writes Files:**

- `Deployment dictionary <../../data_structures/eval_structs.html#deployment-dictionary-evaluation-deploy-dict>`_

Example
"""""""

>>> evaluation.add_deploy_dict_stats()
Computing CV for 1-Hour averaged PM25
..N excluded: 20 out of 756 total
..N concurrent: 736
..Concurrent measurement timeframe: 2019-08-01 13:00:00+00:00 - 2019-09-02 00:00:00+00:00
Computing CV for 24-Hour averaged PM25
..N excluded: 2 out of 32 total
..N concurrent: 30
..Concurrent measurement timeframe: 2019-08-02 00:00:00+00:00 - 2019-09-01 00:00:00+00:00

------

``SensorEvaluation.calculate_metrics()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`API Documentation for calculate_metrics() <../../api/_autosummary/sensortoolkit.evaluation_objs._sensor_eval.SensorEvaluation.html#sensortoolkit.evaluation_objs._sensor_eval.SensorEvaluation.calculate_metrics>`_

Description
"""""""""""

.. note::

  ``calculate_metrics()`` will check whether ``SensorEvaluation.deploy_dict`` has
  been populated with statistics via the ``add_deploy_dict_stats()`` method and
  will call this method if the dictionary has not been populated yet.

**Calculates:**

- 1-hour averaged sensor vs. reference regression statistics for each sensor
- 24-hour averaged sensor vs. reference regression statistics for each sensor
- 1-hour averaged sensor vs. intersensor average regression statistics for each sensor
- 24-hour averaged sensor vs. intersensor average regression statistics for each sensor

**Populates:**

- ``SensorEvaluation.stats_df``
- ``SensorEvaluation.avg_stats_df``

**Writes Files:**

- `Statistics DataFrame - Sensor vs. FRM/FEM <../../data_structures/eval_structs.html#sensor-vs-frm-fem-statistics-evaluation-stats-df>`_
- `Statistics DataFrame - Sensor vs. Intersensor Average <../../data_structures/eval_structs.html#sensor-vs-intersensor-average-statistics-evaluation-avg-stats-df>`_

Example
"""""""

Below is an example for the `Toco Toucan Quickstart Guide example <../../quickstart.html#example-scenario-toco-toucan>`_

>>> evaluation.calculate_metrics()
Computing 1-hour regression statistics for Toco_Toucan vs. T-API T640X at 16.67 LPM
..RT01
..RT02
..RT03
Computing 24-hour regression statistics for Toco_Toucan vs. T-API T640X at 16.67 LPM
..RT01
..RT02
..RT03
Computing 1-hour regression statistics for Toco_Toucan vs. T-API T640X at 16.67 LPM
..RT01
..RT02
..RT03
Computing 24-hour regression statistics for Toco_Toucan vs. T-API T640X at 16.67 LPM
..RT01
..RT02
..RT03
