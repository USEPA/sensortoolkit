Loading Sensor Data
===================

Initial Import
^^^^^^^^^^^^^^
..
  * - ``tzone_shift``
    - An integer value by which to shift the sensor data to UTC.
      Specifying ``0`` will not shift the data.
  * - ``load_raw_data``
    - If true, raw data in the appropriate subdirectory will be
      loaded and 1-hour and 24-hour averages will be computed and saved to a processed
      data subdirectory for the specified sensor. If false, processed data will be loaded.

.. code-block:: python

  # Loading sensor data for the first time, shift ahead five hours to UTC
  sensor_object.load_data(load_raw_data=True,
                          write_to_file=True,
                          tzone_shift=5)

.. code-block:: console

  Importing Recorded Sensor Data:
  ..SN01
  ....Example_Make_Model_SN01_raw.csv
  ..SN02
  ....Example_Make_Model_SN02_raw.csv
  ..SN03
  ....Example_Make_Model_SN03_raw.csv
  ..SN01 recording interval mode: 0 days 00:01:00, 60.0 counts per hour
  ....writing full, hourly, and daily datasets to .csv files
  ..SN02 recording interval mode: 0 days 00:01:00, 60.0 counts per hour
  ....writing full, hourly, and daily datasets to .csv files
  ..SN03 recording interval mode: 0 days 00:01:00, 60.0 counts per hour
  ....writing full, hourly, and daily datasets to .csv files


Loading from Processed Data Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If users have previously loaded sensor datasets (i.e., processed sensor data files
have been created for the sensor), users can save a little bit of time by loading
the S-DFS formatted processed datasets. This saves some time in that the processing
and averaging that occur on the first import of sensor datasets does not need to
take place.

.. note::

  If a time shift is specified during the initial import of sensor data, the shift
  is preserved in the processed datasets, as these files are written in UTC format,
  so users do not need to specify the ``time_shift`` parameter for loading processed
  datasets.

To load processed datasets, ensure that the ``load_raw_data`` and ``write_to_file`` arguments
are both set to ``False``:

.. code-block:: python

  sensor_object.load_data(load_raw_data=False, write_to_file=False)

The following will be printed to the console, indicating that processed datasets recorded
at the original sampling frequency ('full'), 1-hour averaged datasets ('hourly')
and 24-hour averaged datasets ('daily') are loaded for each sensor in the evaluation.

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

-----

.. note::

  For details on accessing sensor datasets via the ``sensor_object.data`` attribute,
  please see [X]