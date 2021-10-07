AirSensor Setup
===============

Sensor data are recorded in a wide variety of formatting conventions and data types.
Data ingestion converts datasets recorded by sensors to a standardized formatting
scheme for data types, header names, and a sorted datetime index.

The ``sensortoolkit.AirSensor.sensor_setup()`` module guides users
through an interactive process of entering in details regarding the formatting
of raw sensor datasets. The Setup module creates a ``setup.json``
configuration file that contains details for describing and converting the recorded sensor
data format into the `sensortoolkit` Sensor Data Formatting Scheme (S-DFS). This file is
passed to a subroutine ``sensortoolkit.sensor_ingest.standard_ingest()`` to import the recorded dataset and convert
headers and date/time-like columns to S-DFS formatting.


To run the ``sensor_setup()`` module, users should first ensure that they have created an
``AirSensor`` object via the directions above and have run the ``create_directories()`` method if
the folder structure listed above does not exist in the user's project directory.

Continuing with the above example for an ``AirSensor`` instance named ``sensor_object``,
the setup module is called via the following line of code:

.. code-block:: python

  sensor_object.sensor_setup()

Running this code, users should notice a number of printed statements in the console
that are waiting on user input. ``sensor_setup()`` is an interactive module, where the
user inputs information via the console. The following steps below walk through the
setup process:

1. Selecting File Data Type
^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, users specify the data type for recorded sensor data. Accepted data
types include .csv, .txt, and .xlsx. Future updates to sensortoolkit may
expand this list to include additional supported data types. Users should enter
one of the data types listed in the section banner.

.. code-block:: console

  ============================== Select Data Type ==============================
  Options
  -------
  ['.csv', '.txt', '.xlsx']
  ==============================================================================

  Enter the sensor data type from the list of supported data types: .csv

  Selected data type: .csv

  Confirm entry [y/n]: y

2. Selecting Data Files
^^^^^^^^^^^^^^^^^^^^^^^

Next, the user is asked to select how sensor datasets will be selected for copying
to the project path that the user specified. Users are presented with three options:
``directory``, which will locate and copy all of the data files in the specified directory for the
indicated data type, ``recursive directory``, which will locate and copy all data files within the
specified directory and any subdirectories contained within the indicated folder path, and ``files`` which
copies over files that the user manually selects within a directory.

.. code-block:: console

  ======================= Select Data Files or Directory =======================
  Options
  -------
  ['directory', 'recursive directory', 'files']
  ==============================================================================

  Enter how to select sensor datasets from the list of options above: files

  Select data sets by files

  Confirm entry [y/n]: y

3. Copying Data files
^^^^^^^^^^^^^^^^^^^^^
Once the user selects an option for indicating how data files should be located
and confirms the entry, a subsequent section in the console will prompt the user to
select the files for the recorded sensor datasets corresponding to the indicated file type.

Users should see a file explorer window open up, asking the user to select either a directory
or file(s) depending on the users' selection in the preceding step.

Users will be prompted to press enter to continue with the file transfer after
reviewing the filenames for the datasets that will be transferred and the location
where the copied datasets will be saved.

.. code-block:: console

  ================== Copy Data Files to the Project Directory ==================
  ==============================================================================

  [File Browser: Select the files for recorded sensor datasets with file type ".csv"]
  Source Files:
  ['C:/Users/.../Documents/Public_Sensor_Evaluation/beta_testing/data/sensor/Example_Make_Model_SN01_raw.csv',
  'C:/Users/.../Documents/Public_Sensor_Evaluation/beta_testing/data/sensor/Example_Make_Model_SN02_raw.csv',
  'C:/Users/.../Documents/Public_Sensor_Evaluation/beta_testing/data/sensor/Example_Make_Model_SN03_raw.csv']

  Destination Directory:
  ..C:\Users\SFREDE01\OneDrive - Environmental Protection Agency
  (EPA)\Profile\Documents\sensortoolkit_testing\Data and
  Figures\sensor_data\Example_Make_Model\raw_data

  Press enter to continue.

  Copying the following files:
  ..C:/Users/SFREDE01/OneDrive - Environmental Protection Agency (EPA)/Profile/Docu
  ments/Public_Sensor_Evaluation/beta_testing/data/sensor/Example_Make_Model_SN01
  _raw.csv
  ..C:/Users/SFREDE01/OneDrive - Environmental Protection Agency (EPA)/Profile/Docu
  ments/Public_Sensor_Evaluation/beta_testing/data/sensor/Example_Make_Model_SN02
  _raw.csv
  ..C:/Users/SFREDE01/OneDrive - Environmental Protection Agency (EPA)/Profile/Docu
  ments/Public_Sensor_Evaluation/beta_testing/data/sensor/Example_Make_Model_SN03
  _raw.csv

  Press enter to continue.

4. Selecting the Column Header Index
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Next, users are prompted to enter the row index corresponding to the column headers.
Sensor datasets may place the header information at the top of the file, and in this
case, the header row index would be ``0``. Occasionally, data sets do not include any
column headers, and users should type ``None`` for the header row index under such circumstances.

To help the user in selecting the row index number corresponding to the header information,
the first ten rows of one of the sensor datasets are printed to the console. The row index
is indicated on the left hand side of the console statement. Below, the example dataset contains
a number of rows of metadata, so the header index containing descriptors for the time column and
pollutant measurement columns is found on row index #5.

.. code-block:: console

  ============================= Column Header Index ============================
  Options
  -------
  ..type "None" if no header columns in recorded sensor dataset
  ==============================================================================

  The first ten unformatted rows of C:\Users\...\Documents\sensortoolkit_testing
  \Data and Figures\sensor_data\Example_Make_Model\raw_data\Example_Make_Model_SN01_raw.csv
  are displayed below:

                                                     0
  0                   CRADA · AQY-BA-317 (AQY-BA-317A)
  1                             Instrument Data export
  2                               8/1/2019 to 9/1/2019
  3             (UTC-05:00) Eastern Time (US & Canada)
  4                         Averaging period: 1 minute
  5  Time,NO2 (ppb),O3 (ppb),PM2.5 (µg/m³),TEMP (°C...
  6   2019/08/01 07:11:00,,,5.4,24.80,95.3,24.0,Sample
  7  2019/08/01 07:12:00,5.5,0.0,5.5,24.88,95.1,24....
  8  2019/08/01 07:13:00,2.0,4.4,5.3,25.00,95.1,24....
  9  2019/08/01 07:14:00,-0.9,8.8,5.4,25.14,95.2,24...

  Enter the row index number for column headers: 5

  Header row index: 5

  Confirm entry [y/n]: y

5. Parsing Sensor Datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If column headers are not included in the sensor datasets (i.e., the column
header index in step 1 was set to ``None``), users will need to manually enter
the names of column headers for sensor datasets. This will prompt a section labeled
`Manually Set Column Headers` and the user will be asked to enter in columns until
the user indicates to the console to end header entry model by pressing ``X``.

.. note::

  Manual configuration of column headers is not required if an integer header row index
  value is set in the previous step.

Next, the module will automatically search for datafiles corresponding to the
file type and header index (if previously specified). A list of unique headers for
each column index are displayed.

.. code-block:: console

  ============================== Parsing Datasets ==============================
  ==============================================================================

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

6. Specifying Timestamp Columns
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

7. Configuring Sensor Serial identifiers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. important::

    Data files pertaining to a particular sensor unit must include the unique
    serial identifier in each file name associated with the unit. These serial IDs
    are used to locate, group, and import data for each unit.

.. code-block:: console

  ===================== Configure Sensor Serial Identifiers ====================
  Options
  -------
  ..press X to end adding entries
  ==============================================================================

  ..C:\Users\...\Documents\sensortoolkit_testing\Data and Figures\sensor_data\
  Example_Make_Model\raw_data\Example_Make_Model_SN01_raw.csv
  ..C:\Users\...\Documents\sensortoolkit_testing\Data and Figures\sensor_data\
  Example_Make_Model\raw_data\Example_Make_Model_SN02_raw.csv
  ..C:\Users\...\Documents\sensortoolkit_testing\Data and Figures\sensor_data\
  Example_Make_Model\raw_data\Example_Make_Model_SN03_raw.csv

  Enter the number of unique sensors corresponding to the datasets above: 3

  Confirm entry [y/n]: y
  Enter unique serial identifiers for each sensor associated with the datasets listed above:

  Enter serial identifier #1: SN01

  Confirm entry [y/n]: y

  Enter serial identifier #2: SN02

  Confirm entry [y/n]: y

  Enter serial identifier #3: SN03

  Confirm entry [y/n]: y

  Configured serial identifiers:
  {'1': 'SN01', '2': 'SN02', '3': 'SN03'}


  Press enter to continue.

8. Saving the Setup Configuration to ``setup.json``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lastly, the Setup module will automatically save the setup configuration
to a ``setup.json`` file.

This file is located at ``..\Data and Figures\sensor_data\Sensor_Make_Model\``
where ``Sensor_Make_Model`` is replaced by the name given to the sensor.

.. code-block:: console

  ============================= Setup Configuration ============================
  ==============================================================================

  ..writing setup configuration to the following path:
  \Data and Figures\sensor_data\Example_Make_Model\Example_Make_Model_setup.json
