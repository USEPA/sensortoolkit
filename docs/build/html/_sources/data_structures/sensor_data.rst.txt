Sensor Data Structures
----------------------

Sensor data are accessed via the ``AirSensor`` object instance. Following
the `Toco Toucan Quickstart Guide example <../quickstart.html#example-scenario-toco-toucan>`_,
mention of ``sensor`` variable below refers to the ``AirSensor``
object instantiated under the `Testing Attribute Objects - The AirSensor Object` section.

Accessing Sensor Data
^^^^^^^^^^^^^^^^^^^^^
Sensor datasets are access via the ``sensor.data`` attribute, which stores `pandas DataFrames <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
in a dictionary structure at recorded sampling frequency, 1-hour averaged intervals, and 24-hour averaged intervals for each
parameter classification:

.. code-block:: python

  {'[serial identifier 1]': # Key will differ depending on choice of serial identifiers
       {'1-minute': pandas DataFrame object, # Key may differ depending on sensor sampling freq.
        '1-hour': pandas DataFrame object,
        '24-hour': pandas DataFrame object},
   '[serial identifier 2]': # Key will differ depending on choice of serial identifiers
       {'1-minute': pandas DataFrame object, # Key may differ depending on sensor sampling freq.
        '1-hour': pandas DataFrame object,
        '24-hour': pandas DataFrame object},
   '[serial identifier 3]': # Key will differ depending on choice of serial identifiers
       {'1-minute': pandas DataFrame object, # Key may differ depending on sensor sampling freq.
        '1-hour': pandas DataFrame object,
        '24-hour': pandas DataFrame object}
  }

.. note::

  The keys for accessing sensor datasets are dependent on the user's configured
  choice for serial identifiers. Additionally, the first key within
  each unit data sub-dictionary will depend on the configured sampling frequency
  for the sensor. For the example above, the sampling frequency was set to
  1-minute intervals, so the key for the first dataset entry is ``1-minute``.

Dataset Example
^^^^^^^^^^^^^^^

The first five rows of data for the Toco Toucan sensor unit ``RT01`` that have been averaged to 1-hour intervals
and formatted as an SDFS dataset (accessed as ``sensor['RT01']['1-hour']``) are shown at the following link:
`Example Sensor Dataset <../sdfs/index.html#example-sdfs-datasets>`_


..
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
         :file: ../data/Example_Make_Model_SN01_full.csv
         :header-rows: 1
         :widths: auto

  Example dataset within ``Eval.hourly_df_list``
  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. note::
      DataFrame object at list position zero shown (``dataset = Eval.hourly_df_list[0]``). Only the first ten rows are
      displayed.

    .. csv-table:: `Example_Make_Model_SN01_hourly.csv`
       :file: ../data/Example_Make_Model_SN01_hourly.csv
       :header-rows: 1
       :widths: auto

  Example dataset within ``Eval.daily_df_list``
  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. note::
      DataFrame object at list position zero shown (``dataset = Eval.daily_df_list[0]``). Only the first ten rows are
      displayed.

    .. csv-table:: `Example_Make_Model_SN01_daily.csv`
       :file: ../data/Example_Make_Model_SN01_daily.csv
       :header-rows: 1
       :widths: auto
