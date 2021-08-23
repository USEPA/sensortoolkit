
***************
Data Structures
***************
The ``SensorEvaluation`` class contains a number of data structures that store
sensor and reference data, and related statistical metrics. Below is a discussion
of these data structures, as well as the Sensor Data Formattting Scheme (S-DFS) and
Reference Data Formatting Scheme (R-DFS) in which sensor and reference data are formatted.

More detail regarding the ``SensorEvaluation`` class, including its methods and
arguments are included in the `API documentation for SensorEvaluation <../html/_autosummary/sensortoolkit.sensor_eval.SensorEvaluation.html>`_

``SensorEvaluation`` Data Structures
====================================

Sensor Data List Containers
--------------------------------

Sensor data files that have been imported and processed into the S-DFS scheme are
sorted based on the interval between consecutive timestamps. Data sets at the
original recorded sampling frequency of the sensor are placed in a list named ``full_df_list``.
Data sets that have been averaged to 1-hour and 24-hour averages are placed in
``hourly_df_list`` and ``daily_df_list``, respectively. These lists contain data sets
for all sensors in the evaluation cohort, and are referred to here as list containers
for pandas Dataframes as these lists hold or `contain` data sets in the `pandas.DataFrame object <https://pandas.pydata.org/docs/reference/frame.html>`_
format.

 .. note::
   Data sets for sensor units within each list container are organized by the order
   each unit serial ID appears in the ``SensorEvaluation.serials`` dictionary.

   For example, if the ``serials`` dictionary lists three sensors as

   .. code-block:: python

      SensorEvaluation.serials = {'1': 'SN01',
                                  '2': 'SN02',
                                  '3': 'SN03'}

   and the associated ``SensorEvaluation.hourly_df_list`` (or
   ``SensorEvaluation.full_df_list`` or ``SensorEvaluation.daily_df_list``) lists three data sets as

   .. code-block:: python

      SensorEvaluation.hourly_df_list = [pandas.DataFrame,
                                         pandas.DataFrame,
                                         pandas.DataFrame]

   then the pandas DataFrame object corresponding to sensor ``SN01`` is found at
   the first position within the ``hourly_df_list``, i.e., index position zero:

   .. code-block:: python

      sn01_dataset =  SensorEvaluation.hourly_df_list[0]


Example dataset within ``full_df_list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. note::
      DataFrame object at list position zero shown (``dataset = full_df_list[0]``). Only the first ten rows are
      displayed.

    .. csv-table:: `Example_Make_Model_SN01_full.csv`
       :file: data/Example_Make_Model_SN01_full.csv
       :header-rows: 1
       :widths: auto

Example dataset within ``hourly_df_list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  .. note::
    DataFrame object at list position zero shown (``dataset = hourly_df_list[0]``). Only the first ten rows are
    displayed.

  .. csv-table:: `Example_Make_Model_SN01_hourly.csv`
     :file: data/Example_Make_Model_SN01_hourly.csv
     :header-rows: 1
     :widths: auto

Example dataset within ``daily_df_list``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  .. note::
    DataFrame object at list position zero shown (``dataset = daily_df_list[0]``). Only the first ten rows are
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
  reference data for the selected ``eval_param``, the dataframes ``hourly_ref_df`` and
  ``daily_ref_df`` are aliases of the reference dataframes corresponding to the parameter
  classification of the ``eval_param``.

  For instance, if ``eval_param = 'PM25'``, ``hourly_ref_df`` corresponds to  ``pm_hourly_ref_df`` and ``daily_ref_df`` corresponds
  to  ``pm_daily_ref_df``. Note that corresponding dataframes point to the same object
  in memory, and as a result, modifications to one dataframe will be reflected in the corresponding
  dataframe.


Data Formatting
===============

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
