Loading Sensor Data
===================

Following the use of the setup module for air sensor datasets, sensor data are
loaded to the ``AirSensor`` object via the ``AirSensor.load_data()`` method.
The procedure for loading sensor data depends slightly on whether the user is loading
datasets for the first time (i.e., the AirSensor.sensor_setup() module was run
immediately before this point and the ``/data/sensor_data/[sensor_name]/processed_data`` directory
containing SDFS formatted datasets is empty) or whether users have previously loaded sensor
datasets via the ``AirSensor.load_data()`` and wish to re-load these datasets for additional
analysis.

``AirSensor.load_data()`` accepts the following Boolean arguments:

.. list-table:: ``AirSensor.load_data()`` Arguments
  :widths: 50 75
  :header-rows: 1

  * - Argument
    - Description
  * - ``write_to_file``
    - If true, processed (SDFS formatted) sensor datasets will be saved as csv |br|
      files to the ``/data/sensor_data/[sensor_name]/processed_data`` |br|
      directory. If false, formatted datasets will not be saved to the user's hard drive.
  * - ``load_raw_data``
    - If true, raw data (datasets as originally recorded) in the appropriate |br|
      subdirectory will be loaded and 1-hour and 24-hour averages will be |br|
      computed. If false, processed data will be loaded.

Initial Import
^^^^^^^^^^^^^^

To load originally recorded datasets and save processed (SDFS formatted) versions
of sensor datasets to the appropriate directory location, select ``load_raw_data = True``
and ``write_to_file = True`` when calling the ``AirSensor.load_data()`` method.

Below, we follow with the example of the 'Toco Toucan' sensor discussed in the
`Quickstart Guide <../../quickstart.html#example-scenario-toco-toucan>`_. Recorded datasets are imported and ingested
into the sensortoolkit data formatting scheme followed by writing of processed csv
files to the ```.../processed_data`` directory.

.. code-block:: python

  # Loading sensor data for the first time
  sensor.load_data(load_raw_data=True,
                   write_to_file=True)

.. code-block:: console

  Importing Recorded Sensor Data:
  ..RT01
  ....Toco_Toucan_RT01_raw.csv
  ..RT02
  ....Toco_Toucan_RT02_raw.csv
  ..RT03
  ....Toco_Toucan_RT03_raw.csv
  ..RT01 recording interval mode: 0 days 00:01:00, 60.0 counts per hour
  ....writing full, hourly, and daily datasets to .csv files
  ..RT02 recording interval mode: 0 days 00:01:00, 60.0 counts per hour
  ....writing full, hourly, and daily datasets to .csv files
  ..RT03 recording interval mode: 0 days 00:01:00, 60.0 counts per hour
  ....writing full, hourly, and daily datasets to .csv files


Loading from Processed Data Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If users have previously loaded sensor datasets (i.e., processed sensor data files
have been created for the sensor), users can save a little bit of time by loading
the SDFS formatted processed datasets. This saves some time in that the processing
and averaging that occur on the first import of sensor datasets does not need to
take place.

To load processed datasets, ensure that the ``load_raw_data`` and ``write_to_file`` arguments
are both set to ``False``:

.. code-block:: python

  sensor.load_data(load_raw_data=False, write_to_file=False)

The following will be printed to the console, indicating that processed datasets recorded
at the original sampling frequency ('full'), 1-hour averaged datasets ('hourly')
and 24-hour averaged datasets ('daily') are loaded for each sensor in the evaluation.

.. code-block:: console

  Loading processed sensor data
  ..Toco_Toucan_RT01_daily.csv
  ..Toco_Toucan_RT01_full.csv
  ..Toco_Toucan_RT01_hourly.csv
  ..Toco_Toucan_RT02_daily.csv
  ..Toco_Toucan_RT02_full.csv
  ..Toco_Toucan_RT02_hourly.csv
  ..Toco_Toucan_RT03_daily.csv
  ..Toco_Toucan_RT03_full.csv
  ..Toco_Toucan_RT03_hourly.csv

-----

.. note::

  For details on accessing sensor datasets via the ``sensor_object.data`` attribute,
  please see `Accessing sensor data <../../data_structures/sensor_data.html#accessing-sensor-data>`_

  .. |br| raw:: html

     <br />
