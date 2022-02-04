AirSensor Setup
===============

Sensor data are recorded in a wide variety of formatting conventions and data types.
Data ingestion converts datasets recorded by sensors to a standardized formatting
scheme for data types, header names, and a sorted datetime index.

The ``sensortoolkit.AirSensor.sensor_setup()`` module guides users
through an interactive process of entering in details regarding the formatting
of raw sensor datasets. The Setup module creates a ``setup.json``
configuration file that contains details for describing and converting the recorded sensor
data format into the `sensortoolkit Data Formatting Scheme (SDFS) <../../sdfs/index.html>`_. This file is
passed to a subroutine ``sensortoolkit.sensor_ingest.standard_ingest()`` to import the recorded dataset and convert
headers and date/time-like columns to SDFS formatting.

To run the ``sensor_setup()`` module, users should first ensure that they have created an
``AirSensor`` object via the directions above and have run the ``create_directories()`` method if
the folder structure listed above does not exist in the user's project directory.

Continuing with the `Quickstart Guide <../../quickstart.html#example-scenario-toco-toucan>`_  example for the 'Toco Toucan' sensor,
following the creation of an ``AirSensor`` instance called ``sensor``,
the setup module is called via the following line of code:

.. code-block:: python

  sensor.sensor_setup()

Running this code, users should notice a number of printed statements in the console
that are waiting on user input. ``sensor_setup()`` is an interactive module, where the
user inputs information via the console. The following steps below walk through the
setup process:

.. important::

  A console width of at least 80 characters is recommended to properly format
  printed statements, banners, and tables within this setup method.

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
or file(s) depending on the users' selection in the preceding step. In the example below,
we assume that the datasets for the 'Toco Toucan' sensor have been placed directly within
the ``/Documents`` directory.

Users will be prompted to press enter to continue with the file transfer after
reviewing the filenames for the datasets that will be transferred and the location
where the copied datasets will be saved.

.. code-block:: console

  ================== Copy Data Files to the Project Directory ==================
  ==============================================================================

  [File Browser: Select the files for recorded sensor datasets with file type ".csv"]
  Source Files:
  ['C:/Users/.../Documents/toco_toucan_RT01_raw.csv',
  'C:/Users/.../Documents/toco_toucan_RT02_raw.csv',
  'C:/Users/.../Documents/toco_toucan_RT03_raw.csv']

  Destination Directory:
  ..C:\Users\...\Documents\toucan_evaluation\data\sensor_data\Toco_Toucan\raw_data

  Press enter to continue.

  Copying the following files:
  ..C:/Users/.../Documents/toco_toucan_RT01_raw.csv
  ..C:/Users/.../Documents/toco_toucan_RT02_raw.csv
  ..C:/Users/.../Documents/toco_toucan_RT03_raw.csv

  Press enter to continue.

4. Selecting the Column Header Index
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Next, users are prompted to enter the row index corresponding to the column headers.
Sensor datasets may place the header information at the top of the file, and in this
case, the header row index would be ``0``. Occasionally, data sets do not include any
column headers, and users should type ``None`` for the header row index under such circumstances.

To help the user in selecting the row index number corresponding to the header information,
the first ten rows of one of the sensor datasets are printed to the console. The row index
is indicated on the left hand side of the console statement.

Below are a few examples for various sensor datasets, each displaying a different formatting
scheme regarding where the header row is located in recorded datasets.

.. tabbed:: Header Row Index = 0

  .. code-block:: console
    :emphasize-lines: 11

    ============================= Column Header Index ============================
    Options
    -------
    ..type "None" if no header columns in recorded sensor dataset
    ==============================================================================

    The first ten unformatted rows of C:\Users\...\Documents\sensortoolkit_testing
    \data\sensor_data\Northern_Cardinal\raw_data\Northern_Cardinal_CC01.csv
    are displayed below:
                                                       0
    0  serialId,timeUtc,aqi,pm1MassConcCalib[ug/m3],p...
    1  cardinalis_01,2019-07-09T11:59:00.000Z,54,,10,...
    2  cardinalis_01,2019-07-09T11:56:00.000Z,55,,9.8...
    3  cardinalis_01,2019-07-09T11:53:00.000Z,57,,10....
    4  cardinalis_01,2019-07-09T11:51:00.000Z,53,,10....
    5  cardinalis_01,2019-07-09T11:48:00.000Z,56,,10....
    6  cardinalis_01,2019-07-09T11:46:00.000Z,54,,9.9...
    7  cardinalis_01,2019-07-09T11:43:00.000Z,56,,11....
    8  cardinalis_01,2019-07-09T11:40:00.000Z,58,,9.7...
    9  cardinalis_01,2019-07-09T11:38:00.000Z,57,,10,...

    Enter the row index number for column headers: 0

    Header row index: 0

    Confirm entry [y/n]: y

.. tabbed:: Header Row Index > 0

  .. code-block:: console
    :emphasize-lines: 17

    ============================= Column Header Index ============================
    Options
    -------
    ..type "None" if no header columns in recorded sensor dataset
    ==============================================================================

    The first ten unformatted rows of C:\Users\...\Documents\sensortoolkit_testing
    \data\sensor_data\Toco_Toucan\raw_data\toco_toucan_RT01_raw.csv
    are displayed below:

                                                       0
    0                      Serial ID: Ramphastos Toco 01
    1                             Instrument Data Export
    2                              8/1/2019 to 8/31/2019
    3             (UTC-05:00) Eastern Time (US & Canada)
    4                         Averaging period: 1 minute
    5  Time,NO2 (ppb),O3 (ppb),PM2.5 (µg/m³),TEMP (°C...
    6  2019/08/01 07:11:00,,,5.4,24.80,95.3,24.0,Sample.
    7  2019/08/01 07:12:00,5.5,0.0,5.5,24.88,95.1,24....
    8  2019/08/01 07:13:00,2.0,4.4,5.3,25.00,95.1,24....
    9  2019/08/01 07:14:00,-0.9,8.8,5.4,25.14,95.2,24...

    Enter the row index number for column headers: 5

    Header row index: 5

    Confirm entry [y/n]: y

.. tabbed:: Header Row Index = None

  Select this option if the dataset does not contain a single row with header
  information. The example below indicates a log description followed immediately
  by rows with comma-delimited data.

  .. code-block:: console
    :emphasize-lines: 11-12

    ============================= Column Header Index ============================
    Options
    -------
    ..type "None" if no header columns in recorded sensor dataset
    ==============================================================================

    The first ten unformatted rows of C:\Users\...\Documents\sensortoolkit_testing
    \data\sensor_data\Scarlet_Macaw\raw_data\Scarlet_Macaw_AM01.txt
    are displayed below:
                                                       0
    0  =~=~=~=~=~=~=~=~=~=~=~= PuTTY log 2018.06.12 2...
    1  2018-06-13T01:23:26,23.0,36.9,1010.7,0.023,0.1...
    2  2018-06-13T01:24:27,23.0,37.9,1010.6,0.021,0.1...
    3  2018-06-13T01:25:28,23.0,39.3,1010.6,0.018,0.0...
    4  2018-06-13T01:26:29,23.0,38.5,1010.6,0.015,0.0...
    5  2018-06-13T01:27:30,23.0,38.0,1010.5,0.012,0.0...
    6  2018-06-13T01:28:31,23.1,37.7,1010.5,0.009,0.0...
    7  2018-06-13T01:29:32,23.1,37.3,1010.5,0.007,0.0...
    8  2018-06-13T01:30:33,23.1,37.2,1010.5,0.005,0.0...
    9  2018-06-13T01:31:34,23.1,36.9,1010.5,0.003,0.0...

    Enter the row index number for column headers: None

    Header row index: None

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

  Parsing datasets at "../data/sensor_data/Toco_Toucan/raw_data"
  ..header(s) at column index 0: ['Time']
  ..header(s) at column index 1: ['NO2 (ppb)']
  ..header(s) at column index 2: ['O3 (ppb)']
  ..header(s) at column index 3: ['PM2.5 (µg/m³)']
  ..header(s) at column index 4: ['TEMP (°C)']
  ..header(s) at column index 5: ['RH (%)']
  ..header(s) at column index 6: ['DP (°C)']
  ..header(s) at column index 7: ['Inlet']

  Press enter to continue.

.. tip::

  Occasionally, sensor datasets may have slightly different formatting if one
  sensor undergoes a firmware update that modifies the recorded format for sensor
  data.

  Say you have the following sensor datasets for sensors `a` and `b`, where both
  sensors are the same make and model, however sensor `b` underwent a firmware update
  that modified the data formatting:

  >>> sensor_dataset_a
  0                 Time  PM25
  1  2021/01/01 00:00:00   2.3
  2  2021/01/01 01:00:00   5.4
  3  2021/01/01 02:00:00   8.5
  4  2021/01/01 03:00:00   4.7
  5  2021/01/01 04:00:00   3.4

  >>> sensor_dataset_b
  0               time  PM25
  1  01-01-21 00:00:00   2.3
  2  01-01-21 01:00:00   5.4
  3  01-01-21 02:00:00   8.5
  4  01-01-21 03:00:00   4.7
  5  01-01-21 04:00:00   3.4

  The timestamp columns ``Time`` and ``time`` have different names (they also
  have different timestamp formatting, which we will come back to at step 6).

  In this instance, a user would see both timestamp headers indicated in column
  header position zero:

  .. code-block:: console

    ============================== Parsing Datasets ==============================
    ==============================================================================

    Parsing datasets at "../data/sensor_data/[sensor_name]/raw_data"
    ..header(s) at column index 0: ['Time', 'time']


6. Specifying Timestamp Columns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Users must list all time-like columns that will be used for the 'DateTime'
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

.. tip::

  Continuing with the illustrative example outlined in the tip for step #5 addressing
  instances with data formatting inconsistencies, users would need to specify all
  column header names corresponding to time-like data. For the example given for
  sensor datasets `a` and `b` with different formatting for the timestamp column
  name, both header names must be specified via the following:

  .. code-block:: console

    ========================== Specify Timestamp columns =========================
    Options
    -------
    ..press X to end adding entries
    ..press D to delete the previous entry
    ==============================================================================

    Enter Timestamp column #1: Time

    Enter Timestamp column #2: time

    Enter Timestamp column #3: X

    Timestamp column list: ['Time', 'time']

    Press enter to continue.

7. Specifying the Parameter Renaming Scheme
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, users are prompted to configure the parameter renaming scheme for converting
recorded datasets into sensortoolkit's Data Formatting Standard (SDFS), which
includes a `list of preset parameter names and associated attributes <../../sdfs/index.html>`_.

If parameters represented in the sensor datasets are included in the list of SDFS parameters,
select "S" when prompted to enter the type of parameter corresponding to the header name as
indicated in the recorded dataset.

If a header name does not correspond to one of the parameters in the list of preset SDFS parameter
names, you can create a new custom parameter attribute using the "N" character or "C" to associate
the header name with a custom parameter that you may have created previously. Otherwise, if you do
not choose to include the header and associated column in the processed datasets, you can enter an
empty character (by pressing the "Enter" key), which will skip over the header label and drop it
from datasets that are processed to the SDFS format.

.. code-block:: console

  ========================== Specify Parameter columns =========================
  Options
  -------
  ..press enter to skip columns that will be dropped

  Notes
  -----
  Choose from the following list of SDFS parameter names:
  ['CO', 'DP', 'NO', 'NO2', 'NOx', 'O3', 'PM1', 'PM10', 'PM25', 'SO2', 'SOx',
   'Temp', 'RH', 'Press', 'WD', 'WS']
  ==============================================================================

  [1/7]
  -----

  Enter the character indicating the type of parameter
  {'': '(enter key) Skip the current header and drop from SDFS datasets',
   'C': 'The header corresponds to an existing custom Parameter',
   'N': 'Create a new custom Parameter for the header',
   'S': 'The header corresponds to an SDFS Parameter'}

  Parameter type for header name "NO2 (ppb)": S

  SDFS Parameters:
  ['CO', 'DP', 'NO', 'NO2', 'NOx', 'O3', 'PM1', 'PM10', 'PM25', 'SO2', 'SOx',
   'Temp', 'RH', 'Press', 'WD', 'WS']

  From the list above, select the SDFS parameter associated with NO2 (ppb): NO2

    Are the units of measure [ppbv] for column header "NO2 (ppb)"?

    Confirm entry [y/n]: y

  [2/7]
  -----

  Enter the character indicating the type of parameter
  {'': '(enter key) Skip the current header and drop from SDFS datasets',
   'C': 'The header corresponds to an existing custom Parameter',
   'N': 'Create a new custom Parameter for the header',
   'S': 'The header corresponds to an SDFS Parameter'}

  Parameter type for header name "O3 (ppb)": S

  SDFS Parameters:
  ['CO', 'DP', 'NO', 'NO2', 'NOx', 'O3', 'PM1', 'PM10', 'PM25', 'SO2', 'SOx',
   'Temp', 'RH', 'Press', 'WD', 'WS']

  From the list above, select the SDFS parameter associated with O3 (ppb): O3

    Are the units of measure [ppbv] for column header "O3 (ppb)"?

    Confirm entry [y/n]: y

  [3/7]
  -----

  Enter the character indicating the type of parameter
  {'': '(enter key) Skip the current header and drop from SDFS datasets',
   'C': 'The header corresponds to an existing custom Parameter',
   'N': 'Create a new custom Parameter for the header',
   'S': 'The header corresponds to an SDFS Parameter'}

  Parameter type for header name "PM2.5 (µg/m³)": S

  SDFS Parameters:
  ['CO', 'DP', 'NO', 'NO2', 'NOx', 'O3', 'PM1', 'PM10', 'PM25', 'SO2', 'SOx',
   'Temp', 'RH', 'Press', 'WD', 'WS']

  From the list above, select the SDFS parameter associated with PM2.5 (µg/m³): PM25

    Are the units of measure [µg/m³] for column header "PM2.5 (µg/m³)"?

    Confirm entry [y/n]: y

  [4/7]
  -----

  Enter the character indicating the type of parameter
  {'': '(enter key) Skip the current header and drop from SDFS datasets',
   'C': 'The header corresponds to an existing custom Parameter',
   'N': 'Create a new custom Parameter for the header',
   'S': 'The header corresponds to an SDFS Parameter'}

  Parameter type for header name "TEMP (°C)": S

  SDFS Parameters:
  ['CO', 'DP', 'NO', 'NO2', 'NOx', 'O3', 'PM1', 'PM10', 'PM25', 'SO2', 'SOx',
   'Temp', 'RH', 'Press', 'WD', 'WS']

  From the list above, select the SDFS parameter associated with TEMP (°C): Temp

    Are the units of measure [°C] for column header "TEMP (°C)"?

    Confirm entry [y/n]: y

  [5/7]
  -----

  Enter the character indicating the type of parameter
  {'': '(enter key) Skip the current header and drop from SDFS datasets',
   'C': 'The header corresponds to an existing custom Parameter',
   'N': 'Create a new custom Parameter for the header',
   'S': 'The header corresponds to an SDFS Parameter'}

  Parameter type for header name "RH (%)": S

  SDFS Parameters:
  ['CO', 'DP', 'NO', 'NO2', 'NOx', 'O3', 'PM1', 'PM10', 'PM25', 'SO2', 'SOx',
   'Temp', 'RH', 'Press', 'WD', 'WS']

  From the list above, select the SDFS parameter associated with RH (%): RH

    Are the units of measure [%] for column header "RH (%)"?

    Confirm entry [y/n]: y

  [6/7]
  -----

  Enter the character indicating the type of parameter
  {'': '(enter key) Skip the current header and drop from SDFS datasets',
   'C': 'The header corresponds to an existing custom Parameter',
   'N': 'Create a new custom Parameter for the header',
   'S': 'The header corresponds to an SDFS Parameter'}

  Parameter type for header name "DP (°C)": S

  SDFS Parameters:
  ['CO', 'DP', 'NO', 'NO2', 'NOx', 'O3', 'PM1', 'PM10', 'PM25', 'SO2', 'SOx',
   'Temp', 'RH', 'Press', 'WD', 'WS']

  From the list above, select the SDFS parameter associated with DP (°C): DP

    Are the units of measure [°C] for column header "DP (°C)"?

    Confirm entry [y/n]: y

  [7/7]
  -----

  Enter the character indicating the type of parameter
  {'': '(enter key) Skip the current header and drop from SDFS datasets',
   'C': 'The header corresponds to an existing custom Parameter',
   'N': 'Create a new custom Parameter for the header',
   'S': 'The header corresponds to an SDFS Parameter'}

  Parameter type for header name "Inlet":
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

8. Configuring Timestamp Column Formatting
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


.. tip::

  Continuing with the illustrative example outlined in the tip for steps #5 and #6 that discuss
  instances with data formatting inconsistencies, users must specify the date/time
  formatting for each time-like column indicated in step #6. For the example given for
  sensor datasets `a` and `b` with different formatting for the timestamp column
  name, timestamp formatting for both the `Time` and `time` columns must be
  specified via the following:

  .. code-block:: console

    ========================== Specify Timestamp columns =========================
    Options
    -------
    ..press X to end adding entries
    ..press D to delete the previous entry
    ==============================================================================

    Enter date/time formatting for "Time": %Y/%m/%d %H:%M:%S

    Enter date/time formatting for "time": %m-%d-%y %H:%M:%S

    Confirm entry [y/n]: y

    Configured formatting scheme:
    {'Time': '%Y/%m/%d %H:%M:%S',
     'time': '%m-%d-%y %H:%M:%S'}

    Press enter to continue.


9. Specifying the DateTime Index Time Zone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, the time zone for the timestamp column should be indicated. `SDFS <../../sdfs/index.html>`_
formatted datasets indicate timestamps in Coordinated Universal Time (UTC), and during
dataset ingestion, timestamps are shifted by the UTC offset corresponding to the time zone
indicated at this step.

The ``pytz`` package is used for indicating time zone names
and corresponding UTC offsets, and users can type ``pytz.all_timezones`` to see a list of
all timezones in the ``pytz`` library (word of caution, there are a lot!). When the
console asks for the time zone corresponding to a particular column, the text you
enter is checked against the list of valid time zones in the ``pytz`` package and will
indicate an invalid entry if the user's input for the time zone was not a valid
time zone name.

.. code-block:: console

  ====================== Specify DateTime Index Time Zone ======================
  Options
  -------
  ..press enter to skip columns that will be dropped

  Notes
  -----
  For a list of all time zones, type "pytz.all_timezones"
  ==============================================================================

  Enter time zone for "Time": EST

  Confirm entry [y/n]: y

  Configured time zone formatting:
  {'Time': '%Y/%m/%d %H:%M:%S', 'Time_tz': 'EST'}

  Press enter to continue.


10. Configuring Sensor Serial identifiers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, users should indicate unique identifiers corresponding to each air sensor in
the testing group. It is common for sensors to be labeled by a unique serial identifier,
either indicated on the housing of the sensor or as a metadata entry for recorded datasets.

Assigning unique identifiers to sensors helps users to keep track of which sensor dataset
corresponds to which unit during analysis.

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

  ..C:\Users\...\Documents\toucan_evaluation\data\sensor_data\Toco_Toucan\raw_data\toco_toucan_RT01_raw.csv
  ..C:\Users\...\Documents\toucan_evaluation\data\sensor_data\Toco_Toucan\raw_data\toco_toucan_RT02_raw.csv
  ..C:\Users\...\Documents\toucan_evaluation\data\sensor_data\Toco_Toucan\raw_data\toco_toucan_RT03_raw.csv

  Enter the number of unique sensors corresponding to the datasets above: 3

  Confirm entry [y/n]: y
  Enter unique serial identifiers for each sensor associated with the datasets listed above:

  Enter serial identifier #1: RT01

  Confirm entry [y/n]: y

  Enter serial identifier #2: RT02

  Confirm entry [y/n]: y

  Enter serial identifier #3: RT03

  Confirm entry [y/n]: y

  Configured serial identifiers:
  {'1': 'RT01', '2': 'RT02', '3': 'RT03'}


  Press enter to continue.

11. Saving the Setup Configuration to ``setup.json``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lastly, the Setup module will automatically save the setup configuration
to a ``setup.json`` file.

This file is located at ``..\data\sensor_data\[sensor_name]\``
where ``[sensor_name]`` is replaced by the name given to the sensor.

.. code-block:: console

  ============================= Setup Configuration ============================
  ==============================================================================

  ..writing setup configuration to the following path:
    \data\sensor_data\Toco_Toucan\Toco_Toucan_setup.json
