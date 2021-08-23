===================================================
Configuring sensortoolkit for Analyzing Sensor Data
===================================================

Creating Sensor Directories
---------------------------
`sensortoolkit` organizes sensor data, resulting data structures, and figures
into several sub-directories in the …/Data and Figures/… folder.  Users can
create these folders during the setup process by running the ``Create_Sensor_Directories``
function. The function accepts two arguments: the sensor name ``name`` and the
parameters the user intends to evaluate ``eval_params``. Users are recommended to
include the name of the sensor make and model in the sensor name, separated by
an underscore. Below is an example for a sensor that will be evaluated for PM2.5
and O3:

.. code-block:: python

    SensorEvaluation.Create_Sensor_Directories(name='Sensor_Make_Model',
                             	                 eval_params=['PM25', 'O3'])

Running the code above will construct the sensor-specific directory structure
for subsequent analysis. The following is printed to the console indicating the
directories that are created by the ``Create_Sensor_Directories`` function.

.. code-block:: console

  Creating directories for sensor_make_model and evaluation parameters: PM25, O3
  ..Creating directory:
  ....\Data and Figures\eval_stats\sensor_make_model
  ..Creating directory:
  ....\Data and Figures\figures\sensor_make_model
  ....Creating sub-directory:
  ......\Data and Figures\figures\sensor_make_model\PM25
  ....Creating sub-directory:
  ......\Data and Figures\figures\sensor_make_model\O3
  ....Creating sub-directory:
  ......\Data and Figures\figures\sensor_make_model\Met
  ....Creating sub-directory:
  ......\Data and Figures\figures\sensor_make_model\deployment
  ..Creating directory:
  ....\Data and Figures\sensor_data\sensor_make_model
  ....Creating sub-directory:
  ......\Data and Figures\sensor_data\sensor_make_model\processed_data
  ....Creating sub-directory:
  ......\Data and Figures\sensor_data\sensor_make_model\raw_data

Adding Sensor datasets
----------------------
Once sensor directories have been established, users should place files for unprocessed data
recorded by the sensor make and model into the appropriate sub-directory. For the
example shown above, data files should be located at ``..\Data and Figures\sensor_data\sensor_make_model\raw_data``.

.. important::

    Data files pertaining to a particular sensor unit must include the unique
    serial identifier in each file name associated with the unit. The ingest
    module uses the IDs listed in the serials dictionary to locate, group, and
    import data for each unit.

*Example*
^^^^^^^^^
`sensortoolkit` comes with a set of example sensor datasets to help users familiarize
themselves with the structure of the library and its implementation. These data files
are organized under the sensor name ``Example_Make_Model``, and unprocessed sensor datasets
are located at ``..\Data and Figures\sensor_data\Example_Make_Model\raw_data``. Below is a
listing of .csv files at this directory location, where the name of the sensor, serial ID
(``SN01``, ``SN02``, and ``SN03``), and unprocessed data descriptor ``_raw`` are
indicated in each file name.

.. code-block:: console

    Example_Make_Model_SN01_raw.csv
    Example_Make_Model_SN02_raw.csv
    Example_Make_Model_SN03_raw.csv

Running the Setup Module
------------------------

Sensor data are recorded in a wide variety of formatting conventions and data types.
Data ingestion converts datasets recorded by sensors to a standardized formatting
scheme for data types, header names, and a sorted datetime index.

The ``Setup`` module included alongside the `sensortoolkit` library guides users
through an interactive process of entering in details regarding the formatting
of sensor datasets in recorded form. The Setup module creates a ``setup.json``
configuration file that contains details for describing and converting the recorded sensor
data format into the `sensortoolkit` Sensor Data Formatting Scheme (S-DFS). This file is
passed to a subroutine ``Ingest()`` to import the recorded dataset and convert
headers and date/time-like columns to S-DFS formatting.

To run the ``Setup`` module, import the `sensortoolkit` library (see Importing
the sensortoolkit Library for more detail) and run the following code:

.. code-block:: python

  IngestionConfig = sensortoolkit.Setup()

Setting the Sensor Name
^^^^^^^^^^^^^^^^^^^^^^^

The user will then be prompted by the module to enter the name of the sensor.
Once the name is typed in the console, press enter. The user will be asked to
confirm the entry by typing ``y`` to confirm and continue or ``n`` to revise the entered name.
Below is an example of ``Setup`` module output and user entry for the `Example_Make_Model`
sensor dataset.

.. code-block:: console

  =============================== Set Sensor Name ==============================
  Options
  -------
   
  ==============================================================================
   
  Enter the name of the sensor: Example_Make_Model
   
  Sensor name: Example_Make_Model
   
  Confirm entry [y/n]: y

.. important::
  The name of the sensor should be the same name and format passed to the
  ``Create_Sensor_Directories`` module.

Setting the Column Header Index
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, users are prompted to enter the row index corresponding to the column headers.
If the column headers are included on the first row of each sensor dataset, the
user will enter ``0`` (row index starting at zero).

If column headers are not included in the sensor dataset, users should type ``None``.
As with sensor name entry, the user will be asked to confirm the entry with
``y`` or ``n`` to either continue or revise the entered value.

.. code-block:: console

  ============================= Column Header Index ============================
  Options
  -------
  ..type "None" if no header columns in recorded sensor dataset
  ===============================================================================
   
  Enter the row index number for column headers: 5
  Header row index: 5
   
  Confirm entry [y/n]: y


Setting the Column Header List
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, users enter the name of each column header in recorded sensor datasets.
Names must be entered as they appear in the datasets, and should include all
columns such as time-like columns and parameter related columns.

Once all the column headers in sensor datasets have been entered, press ``X`` to
exit column header name entry. A list of entered column names will appear, and
the user will be asked to confirm the entry with ``y`` or ``n`` to either continue
or revise the entered list.

.. code-block:: console

  ============================= Set Column Headers =============================
  Options
  -------
  ..press X to end adding entries
  ..press D to delete the previous entry
  ===============================================================================
   
  Enter column 1 header name: Time
   
  Enter column 2 header name: NO2 (ppb)
   
  Enter column 3 header name: O3 (ppb)
   
  Enter column 4 header name: PM2.5 (µg/m³)
   
  Enter column 5 header name: TEMP (°C)
   
  Enter column 6 header name: RH (%)
   
  Enter column 7 header name: DP (°C)
   
  Enter column 8 header name: Inlet
   
  Enter parameter column 9 header name: X
  ['Time', 'NO2 (ppb)', 'O3 (ppb)', 'PM2.5 (µg/m³)', 'TEMP (°C)', 'RH (%)', 'DP (°C)', 'Inlet']
   
  Confirm entry [y/n]: y


Configuring the Parameter Renaming Scheme
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, users are prompted to configure the parameter renaming scheme by entering
in the formatted parameter name (see list in options section) that corresponds
to each header name entered previously.

Column names that do not have a corresponding listed parameter should be dropped
from the dataset by pressing enter. In the example below, note that the columns
``Time`` and ``Inlet`` are dropped. Also note that  time-like columns are set as the
index via the ingestion module, and as a result, time-like columns duplicate the
index and are redundant. The user should always specify to drop time-like columns.

The user will be asked to confirm the entry with ``y`` or ``n`` to either continue or
revise the configured dictionary.

.. code-block:: console

  ===================== Configure Parameter Column Renaming ====================
  Options
  -------
  ..press enter to skip columns that will be dropped
  Note, timestamp columns should be skipped by pressing enter. These columns are
  assigned as the index during ingestion, and as a result, timestamp columns are
  redundant and should be dropped.
  Choose from the following list
  ['PM1', 'PM25', 'PM10', 'O3', 'NO2', 'NO', 'NOx', 'SO2', 'SOx', 'CO', 'CO2',
  'Temp', 'RH', 'Press', 'DP', 'WS', 'WD']
  ===============================================================================
   
  Enter parameter associated with "Time":
  .."Time" will be dropped
   
  Enter parameter associated with "NO2 (ppb)": NO2
   
  Enter parameter associated with "O3 (ppb)": O3
   
  Enter parameter associated with "PM2.5 (µg/m³)": PM25
   
  Enter parameter associated with "TEMP (°C)": Temp
   
  Enter parameter associated with "RH (%)": RH
   
  Enter parameter associated with "DP (°C)": DP
   
  Enter parameter associated with "Inlet":
  .."Inlet" will be dropped
  Configured renaming scheme: {'NO2 (ppb)': 'NO2', 'O3 (ppb)': 'O3', 'PM2.5 (µg/m³)': 'PM25', 'TEMP (°C)': 'Temp', 'RH (%)': 'RH', 'DP (°C)': 'DP'}
   
  Confirm entry [y/n]: y

Setting Timestamp Column Headers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Similar to the process of specifying all column header names, users must list
all time-like columns that will be used for the DateTime_UTC index. Typically,
this either includes one column as is the case for the example, or two columns;
one column for the date and another for the time.

Once entry is complete, the user should press ``X`` to exit column header entry mode.
The user will be asked to confirm the entry with ``y`` or ``n`` to either continue
or revise the entered list of time line column headers.

.. code-block:: console

  ======================== Set Timestamp Column Headers ========================
  Options
  -------
  ..press X to end adding entries
  ..press D to delete the previous entry
  ===============================================================================
   
  Enter timestamp column 1 header name: Time
   
  Enter timestamp column 2 header name: X
  ['Time']
   
  Confirm entry [y/n]: y


Configuring Timestamp Column Formatting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, the timestamp column formatting should be specified. Users are encouraged
to reference https://strftime.org/ for a table of formatting codes. Additional
info is available in the Python documentation: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes.

A formatting scheme must be specified for each time-like column indicated in
the previous section.

The user will be asked to confirm the entry with `y` or `n` to either continue
or revise the entered formatting scheme.

.. code-block:: console

  ==================== Configure Timestamp Column Formatting ===================
  Options
  -------
  ..format code list: https://docs.python.org/3/library/datetime.html#strftime-
  and-strptime-format-codes
  ..If a timestamp column is formatted as the number of seconds since the Unix
  epoch (1 Jan. 1970), enter "epoch"
  ..press enter to skip columns that will be dropped
  ===============================================================================
   
  Enter date/time formatting for "Time": %Y/%m/%d %H:%M:%S
   
  Confirm entry [y/n]: y
  Configured formatting scheme: {'Time': '%Y/%m/%d %H:%M:%S'}

.. tip::

    Non-zero padded values (e.g., specifying January as ``1`` rather than
    zero-padded ``01``) should be indicated by either ``%-`` or ``%#`` (e.g.,
    non-zero padded month will be ``%-m`` or ``%#m``).


Selecting File Data Type
^^^^^^^^^^^^^^^^^^^^^^^^
Lastly, users specify the data type for recorded sensor data. Accepted data
types include .csv, .txt, and .xlsx. Future updates to sensortoolkit may
expand this list to include additional supported data types. Users should enter
the number associated with the data types listed in the section banner.

.. code-block:: console

  ============================== Select Data Type ==============================
  Options
  -------
  {'1': '.csv', '2': '.txt', '3': '.xlsx'}
  ===============================================================================
   
  Enter the number associated with the data type: 1
  Selected data type: .csv

Once a data type is selected, the setup configuration will be written to a
setup.json file located at ``..\Data and Figures\sensor_data\Sensor_Make_Model\``
where ``Sensor_Make_Model`` is replaced by the name given to the sensor.

.. code-block:: console

  ============================= Setup Configuration ============================
  Options
  -------
  ===============================================================================
  ..writing setup configuration to Example_Make_Model_setup.json
   
