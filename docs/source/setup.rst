===================================================
Configuring sensortoolkit for Analyzing Sensor Data
===================================================

Creating Sensor Directories
---------------------------
`sensortoolkit` organizes sensor data, resulting data structures, and figures
into several sub-directories in the ``/Data and Figures`` folder.

.. important::
  Users have the option of working from within the folder location where the `sensortoolkit`
  repository was downloaded, storing sensor and reference data in the provided ``/Data and Figures`` directory,
  or users may wish to organize their work in a separate directory. In either case, various
  subdirectories and folders will need to be created so users can store data, figures, and evaluation
  statistics.

Users can create these folders during the setup process by running the ``Create_Sensor_Directories``
function. The function accepts the following arguments

* ``name``: The sensor name. Users are recommended to include the name of the
  sensor make and model in the sensor name, separated by an underscore.
* ``eval_params``: A list of parameters the user intends to evaluate
* ``work_path``: The path to the directory where the user intends to store data, figures,
  and reports

Below is an example for a sensor that will be evaluated for PM2.5 and O3 at the
folder location ``C:/Users/.../Documents/my_evaluation``:

.. code-block:: python

    sensor_name = 'Sensor_Make_Model'
    work_path = 'C:/Users/.../Documents/my_evaluation'

    sensortoolkit.Create_Sensor_Directories(name=sensor_name,
                             	              eval_params=['PM25', 'O3'],
                                            work_path=work_path)

Running the code above will construct the sensor-specific directory structure
for subsequent analysis. Here, we're assuming that the folder``my_evaluation``
only has the python file with the code written above. The ``Data and Figures``
and ``Reports`` folders, along with all relevant subdirectories, will be constructed.

The following is printed to the console indicating the directories that are created
by the ``Create_Sensor_Directories`` function.

.. code-block:: console

  Creating "Data and Figures" subdirectory within C:/Users/.../Documents/my_evaluation
  ....\Data and Figures\eval_stats
  ....\Data and Figures\figures
  ....\Data and Figures\reference_data
  ......\Data and Figures\reference_data\airnow
  ........\Data and Figures\reference_data\airnow\raw_api_datasets
  ........\Data and Figures\reference_data\airnow\processed
  ......\Data and Figures\reference_data\airnowtech
  ........\Data and Figures\reference_data\airnowtech\downloaded_datasets
  ........\Data and Figures\reference_data\airnowtech\processed
  ......\Data and Figures\reference_data\aqs
  ........\Data and Figures\reference_data\aqs\raw_api_datasets
  ........\Data and Figures\reference_data\aqs\processed
  ......\Data and Figures\reference_data\oaqps
  ........\Data and Figures\reference_data\oaqps\raw_data
  ........\Data and Figures\reference_data\oaqps\processed_data
  ....\Data and Figures\sensor_data

  Creating "Reports" subdirectory within C:/Users/.../Documents/my_evaluation

  Creating directories for sensor_make_model and evaluation parameters: PM25, O3
  ....\Data and Figures\eval_stats\sensor_make_model
  ....\Data and Figures\figures\sensor_make_model
  ......\Data and Figures\figures\sensor_make_model\PM25
  ......\Data and Figures\figures\sensor_make_model\O3
  ......\Data and Figures\figures\sensor_make_model\Met
  ......\Data and Figures\figures\sensor_make_model\deployment
  ....\Data and Figures\sensor_data\sensor_make_model
  ......\Data and Figures\sensor_data\sensor_make_model\processed_data
  ......\Data and Figures\sensor_data\sensor_make_model\raw_data

Adding Sensor datasets
----------------------
Once sensor directories have been established, users should place files for unprocessed data
recorded by the sensor make and model into the appropriate sub-directory. For the
example shown above, data files should be located at ``\Data and Figures\sensor_data\sensor_make_model\raw_data``.

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
are located at ``\Data and Figures\sensor_data\Example_Make_Model\raw_data``. Below is a
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

  sensor_name = 'Example_Make_Model'
  work_path = 'C:/Users/.../Documents/my_evaluation'

  IngestionConfig = sensortoolkit.Setup(name=sensor_name,
                                        work_path)


1. Setting the Column Header Index
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
  ==============================================================================

  Enter the row index number for column headers: 5

  Header row index: 5

  Confirm entry [y/n]: y

2. Selecting File Data Type
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, users specify the data type for recorded sensor data. Accepted data
types include .csv, .txt, and .xlsx. Future updates to sensortoolkit may
expand this list to include additional supported data types. Users should enter
the number associated with the data types listed in the section banner.

.. code-block:: console

  ============================== Select Data Type ==============================
  Options
  -------
  ['.csv', '.txt', '.xlsx']
  ==============================================================================

  Enter the sensor data type from the list of supported data types: .csv

  Selected data type: .csv

  Confirm entry [y/n]: y

3. Specifying Column Headers and Parsing Sensor Datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If column headers are not included in the sensor datasets (i.e., the column
header index in step 1 was set to ``None``), users will need to manually enter
the names of column headers for sensor datasets. This will prompt a section labeled
`Manually Set Column Headers` and the user will be asked to enter in columns until
the user indicates to the console to end header entry model by pressing ``X``.

.. note::

  Manual configuration of column headers is not required if an integer header row index
  value is set in step 1 of the ``Setup()`` module.

Next, the module will automatically search for datafiles corresponding to the
file type and header index (if previously specified). A list of unique headers for
each column index are displayed.

.. important::
  In order to load sensor datasets, files must be placed in the proper subdirectory
  (e.g., ``/Data and Figures/sensor_data/Example_Make_Model/raw_data``).

.. code-block:: console

  ============================== Parsing Datasets ==============================
  ==============================================================================

  The following data files were found at "../Data and Figures/sensor_data/"Example_Make_Model/raw_data":
  ../Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN01_raw.csv
  ../Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN02_raw.csv
  ../Data and Figures/sensor_data/Example_Make_Model/raw_data/Example_Make_Model_SN03_raw.csv

  Parsing datasets at "../Data and Figures/sensor_data/"Example_Make_Model/raw_data"
  ..Column header(s) at row index 0: ['Time']
  ..Column header(s) at row index 1: ['NO2 (ppb)']
  ..Column header(s) at row index 2: ['O3 (ppb)']
  ..Column header(s) at row index 3: ['PM2.5 (µg/m³)']
  ..Column header(s) at row index 4: ['TEMP (°C)']
  ..Column header(s) at row index 5: ['RH (%)']
  ..Column header(s) at row index 6: ['DP (°C)']
  ..Column header(s) at row index 7: ['Inlet']

  Press enter to continue.

4. Specifying Timestamp Columns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Users must list all time-like columns that will be used for the DateTime_UTC
index. Typically, this either includes one column as is the case for the
example, or two columns (one column for the date and another for the time).

Once entry is complete, the user should press ``X`` to exit column header entry
mode.

.. code-block:: console

  ========================== Specify Timestamp columns =========================
  Options
  -------
  ..press X to end adding entries
  ..press D to delete the previous entry
  ==============================================================================

  Enter Timestamp column #1: Time

  Enter Timestamp column #2: X

  Timestamp column list: ['Time']

  Press enter to continue.

5. Specifying the Parameter Renaming Scheme
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, users are prompted to configure the parameter renaming scheme by entering
in `sensortoolkit`'s Sensor Data Formatting Standard (S-DFS) parameter name
that corresponds to each parameter header name.

.. tip::

  Column names that do not have a corresponding listed parameter should be dropped
  from the dataset by pressing enter.

.. code-block:: console

  ========================== Specify Parameter columns =========================
  Options
  -------
  ..press enter to skip columns that will be dropped

  Notes
  -----
  Choose from the following list of SDFS parameter names:
  ['PM1', 'PM25', 'PM10', 'O3', 'NO2', 'NO', 'NOx', 'SO2', 'SOx', 'CO', 'CO2',
  'Temp', 'RH', 'Press', 'DP', 'WS', 'WD']
  ==============================================================================

  [1/7] Enter SDFS parameter associated with NO2 (ppb): NO2

  [2/7] Enter SDFS parameter associated with O3 (ppb): O3

  [3/7] Enter SDFS parameter associated with PM2.5 (µg/m³): PM25

  [4/7] Enter SDFS parameter associated with TEMP (°C): Temp

  [5/7] Enter SDFS parameter associated with RH (%): RH

  [6/7] Enter SDFS parameter associated with DP (°C): DP

  [7/7] Enter SDFS parameter associated with Inlet:
  ..Inlet will be dropped

  Configured renaming scheme:
  {'DP (°C)': 'DP',
   'Inlet': '',
   'NO2 (ppb)': 'NO2',
   'O3 (ppb)': 'O3',
   'PM2.5 (µg/m³)': 'PM25',
   'RH (%)': 'RH',
   'TEMP (°C)': 'Temp'}

  Press enter to continue.

6. Configuring Timestamp Column Formatting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, the timestamp column formatting should be specified. Users are encouraged
to reference https://strftime.org/ for a table of formatting codes. Additional
info is available in the Python documentation: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes.

A formatting scheme must be specified for each time-like column indicated in
the previous section.

The user will be asked to confirm the entry with ``y`` or ``n`` to either continue
or revise the entered formatting scheme.

.. code-block:: console

  ==================== Configure Timestamp Column Formatting ===================
  Options
  -------
  ..If a timestamp column is formatted as the number of seconds since the Unix
  epoch (1 Jan. 1970), enter "epoch"
  ..press enter to skip columns that will be dropped

  Notes
  -----
  ..format code list: https://docs.python.org/3/library/datetime.html#strftime-
  and-strptime-format-codes
  ==============================================================================

  Enter date/time formatting for "Time": %Y/%m/%d %H:%M:%S

  Confirm entry [y/n]: y

  Configured formatting scheme:
  {'Time': '%Y/%m/%d %H:%M:%S'}

  Press enter to continue.

.. tip::

    Non-zero padded values (e.g., specifying January as ``1`` rather than
    zero-padded ``01``) should be indicated by either ``%-`` or ``%#`` (e.g.,
    non-zero padded month will be ``%-m`` or ``%#m``).

7. Saving the Setup Configuration to ``setup.json``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once the timestamp column formatting has been confirmed, the Setup module will
automatically save the setup configuration to a ``setup.json`` file.

This file is located at ``..\Data and Figures\sensor_data\Sensor_Make_Model\``
where ``Sensor_Make_Model`` is replaced by the name given to the sensor.

.. code-block:: console

  ============================= Setup Configuration ============================
  ==============================================================================

  ..writing setup configuration to the following path:
  \Data and Figures\sensor_data\Example_Make_Model\Example_Make_Model_setup.json
