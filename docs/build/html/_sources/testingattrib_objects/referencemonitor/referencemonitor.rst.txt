===========================
The ReferenceMonitor Object
===========================
After creating an ``AirSensor`` object, users follow a similar procedure for
configuring the `ReferenceMonitor` object for importing and accessing FRM/FEM
data.

Continuing with the `evaluation.py` example, an instance of the ``ReferenceMonitor``
object is created via the following code:

.. code-block:: python

  # Loading reference object for the first time
  reference_object = sensortoolkit.ReferenceMonitor(project_path=work_path)

.. note::
  The above code snippet assumes that the user named their instance of the ``sensortoolkit.ReferenceMonitor``
  object ``reference_object``. If a different name was chosen, replace instances of ``reference_object.`` with ``[custom_name].``
  to access the instance attributes.

.. note::
  The above code snippet assumes that the user hasn't set up reference data for
  the testing site that were retrieved from a reference data service or source,
  such as the `AQS API`, `AirNow API`, `AirNowTech`, or a locally acquired data set.

  For users that have already gone through the setup process during past evaluations
  for reference data corresponding to a particular site and source and intend to use
  the same data source for subsequent evaluations at the monitoring site, a ``reference_setup.json``
  should have been created during the original setup process. In order to point to the
  particular ``reference_setup.json`` file, the user will need to specify additional parameters
  during the ``sensortoolkit.ReferenceMonitor()`` object instantiation. Please see [X]
  for more detail about instantiating ``ReferenceMonitor`` objects for
  previously-configured reference data sources.
  ..
  # Loading a pre-configured reference object (indicate source, site, site id
  # if applicable)
  reference_object = sensortoolkit.ReferenceMonitor(project_path=work_path,
                                              data_source='airnowtech',
                                              site_name='Burdens Creek',
                                              site_id='370630099')

When running the above code, the following message will be printed to the console
indicating that the user should continue the setup process by running the ``reference_setup()``
method:

.. code-block:: console

  ..reference data source and monitoring site information not specified, run
   ReferenceMonitor.reference_setup() to continue

Running the Setup Module
------------------------
Continuing with the example above, the ``ReferenceMonitor.reference_setup()``
method provides an interactive utility for specifying reference data attributes
and data ingestion. The module can be called via the following line of code:

.. code-block:: python

  reference_object.reference_setup()

Running the above code, the user is greeted with a number of printed statements in
the console that prompt the user's input. ``reference_setup()`` is an interactive
module, where the user inputs information via the console. The following steps
below walk through the setup process:

1. Selecting the Reference Data Service/Source
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
First, the user is asked to specify the service or source for reference data.
The user's entry must correspond to one of the options listed in the table shown
in the banner for the section: users must choose from ``airnow`` (user plans to
query the AirNow API), ``aqs`` (user plans to query the AQS API), ``airnowtech`` (user
has downloaded files from the AirNowTech system and has saved files locally to the user's
system), or ``local`` (a catchall for reference data files the user may have stored
locally on their system that were not acquired from any of the services previously mentioned).

The example below will walk through the setup process for a data file acquired locally for
EPA's sensor testing site:

.. code-block:: console

  =================== Select Name of Service for Data Source ===================
  Options
  -------
  ['airnow', 'aqs', 'airnowtech', 'local']
  ==============================================================================

  Enter the name of the service from the list of options above: local


2. Adding Monitoring Site Information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Next, the user should enter in information about the ambient monitoring site
at which the collocation study was conducted. If certain details are unknown or
don't apply to the site (e.g. Non-AQS sites will not have an AQS Site ID), entries
can be skipped by pressing the 'Enter' key.

.. important::
  Users are strongly recommended to provide a site name and, if applicable, a site AQS ID.
  These attributes are used to organize reference data within the ``/Data and Figures/reference_data/[data source]/[raw or processed]``
  subdirectories.

  This is particularly important if users are working with data from numerous sites yet share the same data source.
  For instance, if one is using AirNowTech for reference data at two sites, Site A and Site B,
  the folder structure for processed reference datasets should look something like:

  .. code-block:: console

    my_evaluation
    |
    └───Data and Figures
       └───reference_data
            └───airnowtech
               ├───raw
               └───processed
                  ├SiteNameA_AAAAAAAAA
                  └SiteNameB_BBBBBBBBB

  where AAAAAAAAA is the AQS site ID for site A and BBBBBBBBB is the AQS site ID
  for site B.

  If the site name is unspecified, datasets will be placed in a subfolder named ``UnspecifiedSite_XXXXXXXXX``
  where ``XXXXXXXXX`` is the AQS site ID if specified. If both the site name and AQS Site ID
  are not specified, data sets will be placed in a folder named ``UnspecifiedSite_UnspecifiedSiteID``.
  For this reason, specifying the site name and site ID where applicable is strongly advised to avoid
  data being stored in an ambiguous ``UnspecifiedSite_UnspecifiedSiteID``.

.. code-block:: console

  ================ Enter Ambient Air Monitoring Site Information ===============
  Options
  -------
  ..press enter to skip entries

  Notes
  -----
  Site AQS ID required for AQS queries
  Site Latitude and Longitude required for AirNow queries
  ==============================================================================

  Enter the name of the monitoring site: Burdens Creek

  Confirm entry [y/n]: y


  Enter the name of the Agency overseeing the monitoring site: OAQPS

  Confirm entry [y/n]: y


  Enter the AQS site ID (if applicable) [format XX-XXX-XXXX]:37-063-0099

  Confirm entry [y/n]: y


  Enter the site latitude (in decimal coordinates):35.889

  Confirm entry [y/n]: y


  Enter the site longitude (in decimal coordinates):-78.874

  Confirm entry [y/n]: y

3. Selecting File Data Type
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Next, users specify the data type for recorded reference data. Accepted data
types include .csv, .txt, and .xlsx. Future updates to sensortoolkit may
expand this list to include additional supported data types. Users should enter
one of the data types listed in the section banner.

.. code-block:: console

  ============================== Select Data Type ==============================
  Options
  -------
  ['.csv', '.txt', '.xlsx']
  ==============================================================================

  Enter the reference data type from the list of supported data types:.csv

  Selected data type: .csv

  Confirm entry [y/n]: y

4. Selecting Data Files
^^^^^^^^^^^^^^^^^^^^^^^
Next, the user is asked to select how reference datasets will be selected for copying
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

  Enter how to select reference datasets from the list of options above:files

  Select data sets by files

  Confirm entry [y/n]: y


5. Copying Data files
^^^^^^^^^^^^^^^^^^^^^
Once the user selects an option for indicating how data files should be located
and confirms the entry, a subsequent section in the console will prompt the user to
select the files for the recorded reference datasets corresponding to the indicated file type.

Users should see a file explorer window open up, asking the user to select either a directory
or file(s) depending on the users' selection in the preceding step.

Users will be prompted to press enter to continue with the file transfer after
reviewing the filenames for the datasets that will be transferred and the location
where the copied datasets will be saved.

.. code-block:: console

  ================== Copy Data Files to the Project Directory ==================
  ==============================================================================

  [File Browser: Select the files for recorded reference datasets with file type ".csv"]

  Source Files:
  ['C:/Users/.../Documents/AIRS Project/AIRS\nEvaluation/AIRS_Ref_Data/min_201908_PM.csv',
   'C:/Users/.../Documents/AIRS Project/AIRS\nEvaluation/AIRS_Ref_Data/min_201909_PM.csv']

  Destination Directory:
  ..C:\Users\SFREDE01\OneDrive - Environmental Protection Agency
  (EPA)\Profile\Documents\sensortoolkit_testing\Data and
  Figures\reference_data\local\raw\Burdens_Creek_370630099

  Press enter to continue.

  Copying the following files:
  ..C:/Users/SFREDE01/OneDrive - Environmental Protection Agency
  (EPA)/Profile/Documents/AIRS Project/AIRS
  Evaluation/AIRS_Ref_Data/min_201908_PM.csv
  ..C:/Users/SFREDE01/OneDrive - Environmental Protection Agency
  (EPA)/Profile/Documents/AIRS Project/AIRS
  Evaluation/AIRS_Ref_Data/min_201909_PM.csv

  Press enter to continue.

6. Selecting the Column Header Index
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Next, users are prompted to enter the row index corresponding to the column headers.
Reference datasets may place the header information at the top of the file, and in this
case, the header row index would be ``0``. Occasionally, data sets do not include any
column headers, and users should type ``None`` for the header row index under such circumstances.

To help the user in selecting the row index number corresponding to the header information,
the first ten rows of one of the reference datasets are printed to the console. The row index
is indicated on the left hand side of the console statement. Below, the example dataset contains
a number of rows of metadata, so the header index containing descriptors for the time column and
pollutant measurement columns is found on row index #2.

.. code-block:: console

  ============================= Column Header Index ============================
  Options
  -------
  ..type "None" if no header columns in recorded sensor dataset
  ==============================================================================

  The first ten unformatted rows of C:\Users\...\Documents\sensortoolkit_testing
  \Data and Figures\reference_data\local\raw\Burdens_Creek_370630099\min_201908_PM.csv
  are displayed below:
                                             0
  0  Station: BURDENS CREEK PM  Periodically: 8/1/2...
  1                                            ,,,,,,,
  2  Date & Time,UV_633_370nm,BC AE33 880nm,Grimm P...
  3        ,ng/m3,ng/m3,ug/m3L,ug/m3,ug/m3,ug/m3,ug/m3
  4      8/1/2019 7:00 AM,875,726,12,17.5,9.4,9.5,19.8
  5    8/1/2019 7:01 AM,958,785,11.5,16.6,9.4,9.5,18.1
  6    8/1/2019 7:02 AM,999,800,11.3,16.1,9.4,9.5,18.3
  7    8/1/2019 7:03 AM,936,787,11.6,16.5,9.4,9.4,17.7
  8    8/1/2019 7:04 AM,935,768,12.4,18.1,9.4,9.4,16.3
  9      8/1/2019 7:05 AM,908,752,11,14.9,9.2,9.5,15.7

  Enter the row index number for column headers: 2

  Header row index: 2

  Confirm entry [y/n]: y

7. Parsing Sensor Datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If column headers are not included in the reference datasets (i.e., the column
header index in step 1 was set to ``None``), users will need to manually enter
the names of column headers for datasets. This will prompt a section labeled
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

  Parsing datasets at "../Data and Figures/reference_data/local/raw/Burdens_Creek_370630099/"
  ..Header(s) at column index 0: ['Date & Time']
  ..Header(s) at column index 1: ['UV_633_370nm']
  ..Header(s) at column index 2: ['BC AE33 880nm']
  ..Header(s) at column index 3: ['Grimm PM2.5']
  ..Header(s) at column index 4: ['Grimm PM10']
  ..Header(s) at column index 5: ['GRIMM PM1']
  ..Header(s) at column index 6: ['T640_2_PM25']
  ..Header(s) at column index 7: ['T640_2_PM10']

  Press enter to continue.

8. Specifying Timestamp Columns
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

  Enter Timestamp column name #1: Date & Time

  Enter Timestamp column name #2: X

  Timestamp column list: ['Date & Time']

  Press enter to continue.

9. Specifying the Parameter Renaming Scheme and Monitor Information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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
  Choose from the following list of SDFS parameter names
  ['PM1', 'PM25', 'PM10', 'O3', 'NO2', 'NO', 'NOx', 'SO2', 'SOx', 'CO', 'CO2',
  'Temp', 'RH', 'Press', 'DP', 'WS', 'WD']
  ==============================================================================

  [1/7] Enter SDFS parameter associated with UV_633_370nm:
  ..UV_633_370nm will be dropped

  [2/7] Enter SDFS parameter associated with BC AE33 880nm:
  ..BC AE33 880nm will be dropped

  [3/7] Enter SDFS parameter associated with Grimm PM2.5:
  ..Grimm PM2.5 will be dropped

  [4/7] Enter SDFS parameter associated with Grimm PM10:
  ..Grimm PM10 will be dropped

  [5/7] Enter SDFS parameter associated with GRIMM PM1:
  ..GRIMM PM1 will be dropped

  [6/7] Enter SDFS parameter associated with T640_2_PM25: PM25

  Enter the units of measure for T640_2_PM25:ug/m^3

  Confirm entry [y/n]: y

  Is the parameter code for reference measurements 88101?

  Confirm entry [y/n]: y
  Method Code                             Collection Description Method Type
  0           116               BGI Model PQ200 PM2.5 Sampler w/WINS         FRM
  1           117              R & P Model 2000 PM2.5 Sampler w/WINS         FRM
  2           118           R & P Model 2025 PM2.5 Sequential w/WINS         FRM
  3           119              Andersen RAAS2.5-100 PM2.5 SAM w/WINS         FRM
  4           120              Andersen RAAS2.5-300 PM2.5 SEQ w/WINS         FRM
  5           123                          Thermo Env Model 605 CAPS         FRM
  6           128              Andersen RAAS2.5-2000PM2.5 Aud w/WINS         FRM
  7           129               R & P Model 2000 PM-2.5 Audit w/WINS         FRM
  8           135                   URG-MASS100 Single PM2.5 Sampler         FRM
  9           136               URG-MASS300 Sequential PM2.5 Sampler         FRM
  10          142               BGI Models PQ200-VSCC or PQ200A-VSCC         FRM
  11          143         R & P Model 2000 PM-2.5 Air Sampler w/VSCC         FRM
  12          144       R & P Model 2000 PM-2.5 Audit Sampler w/VSCC         FRM
  13          145  R & P Model 2025 PM-2.5 Sequential Air Sampler...         FRM
  14          153           Thermo Electron Model RAAS2.5-100 w/VSCC         FRM
  15          154     Thermo Electron Model RAAS2.5-200 Audit w/VSCC         FRM
  16          155  Thermo Electron Model RAAS2.5-300 Sequential w...         FRM
  17          170               Met One BAM-1020 Mass Monitor w/VSCC         FEM
  18          177          Thermo Scientific Partisol 2000-D Dichot.         FEM
  19          179  Thermo Scientific Dichot. Partisol-Plus Model ...         FEM
  20          181  Thermo Scientific TEOM 1400 FDMS or 1405 8500C...         FEM
  21          182    Thermo Scientific TEOM 1405-DF Dichotomous FDMS         FEM
  22          183      Thermo Scientific 5014i or FH62C14-DHS w/VSCC         FEM
  23          184          Thermo Scientific Model 5030 SHARP w/VSCC         FEM
  24          195             GRIMM EDM Model 180 with naphion dryer         FEM
  25          203                    Opsis SM200-Dust Monitor w/VSCC         FEM
  26          204                Teledyne Model 602 Beta plus w/VSCC         FEM
  27          209  Met One BAM-1022 Mass Monitor w/ VSCC or TE-PM...         FEM
  28          219        Tisch Model TE-Wilbur2.5 Low-Volume Sampler         FRM
  29          221                      Met One E-FRM PM2.5 with WINS         FRM
  30          235    Met One E-FRM PM2.5 with URG-2000-30EGN cyclone         FEM
  31          236                           Teledyne T640 at 5.0 LPM         FEM
  32          238                        Teledyne T640X at 16.67 LPM         FEM
  33          245                  Met One E-SEQ-FRM PM2.5 with WINS         FRM
  34          521                      Met One E-FRM PM2.5 with VSCC         FRM
  35          545                  Met One E-SEQ-FRM PM2.5 with VSCC         FRM
  36          581               Thermo Scientific 1405-F FDMS w/VSCC         FEM

  Enter the method code corresponding to the reference method for T640_2_PM25:238

  Confirm entry [y/n]: y

  Enter the parameter occurance code for the above reference method:1

  Confirm entry [y/n]: y

  [7/7] Enter SDFS parameter associated with T640_2_PM10: PM10

  Enter the units of measure for T640_2_PM10:ug/m^3

  Confirm entry [y/n]: y

  Is the parameter code for reference measurements 81102?

  Confirm entry [y/n]: y
  Method Code                           Collection Description Method Type
  0             1                                    LO-VOL-SA244E         NaN
  1             2                                   LO-VOL-GMW9200         NaN
  2             3                               LO-VOL-WA10-DICHOT         NaN
  3             4                             LO-VOL-SA246B-DICHOT         NaN
  4            11                                    DUSTTRAK 8530         NaN
  5            12                                    DUSTTRAK 8533         NaN
  6            25                                    MED-VOL-SA254         NaN
  7            26                                  MED-VOL-GMW9100         NaN
  8            40                   WEDDING-AUTOMATED-PM10 SAMPLER         NaN
  9            41                       BAM-102-CONTINUOUS MONITOR         NaN
  10           51                                     HI-VOL-SA321         NaN
  11           52                                    HI-VOL-SA321A         NaN
  12           53                                   HI-VOL-GMW9000         NaN
  13           54                                       HI-VOL-W10         NaN
  14           55                     HI-VOL-W10-(W/MAINT.AC.PORT)         NaN
  15           56                    HI-VOL-SA321G-(321-W/OILSHIM)         NaN
  16           57                   HI-VOL-SA321AG(321A-W/OILSHIM)         NaN
  17           58                                    HI-VOL-SA321B         NaN
  18           59                                    HI-VOL-SA1200         NaN
  19           62                             HI-VOL-WEDDING-INLET         FRM
  20           63                               HI-VOL SA/GMW-1200         FRM
  21           64                              HI-VOL-SA/GMW-321-B         FRM
  22           65                              HI-VOL-SA/GMW-321-C         FRM
  23           71                               OREGON-DEQ-MED-VOL         FRM
  24           73                   LO-VOL-DICHOTOMOUS-SA246B-INLT         FRM
  25           76                   INSTRMENTL-ANDRSEN-SA246B-INLT         FEM
  26           79                    INSTRUMENTAL-R&P SA246B-INLET         FEM
  27           81                   INSTRUMENTAL-WEDDING-AUTOMATIC         FEM
  28           98                          R&P Model 2000 Partisol         FRM
  29          122                      INSTRUMENT MET ONE 4 MODELS         FEM
  30          124                        BGI Inc. Model PQ100 PM10         FRM
  31          125                        BGI Inc. Model PQ200 PM10         FRM
  32          126                     R - P Co Partisol Model 2000         FRM
  33          127                     R - P Co Partisol Model 2025         FRM
  34          130               Andersen RAAS10-100 Single channel         FRM
  35          131                    Andersen RAAS10-200 S-Channel         FRM
  36          132                    Andersen RAAS10-300 M-channel         FRM
  37          141             Tisch Environ Model-6070 PM10 Hi-Vol         FRM
  38          150                  T A Series FH 62 C14 Continuous         FEM
  39          151                  Environnement S.A. Model MP101M         FEM
  40          156                               Instrument DKK_TOA         FEM
  41          162                    Hi Vol SSI Ecotech Model 3000         FRM
  42          193                   OPSIS Model SM200 PM10 Monitor         FEM
  43          197              Thermo Partisol Model 2000-D Dichot         FEM
  44          198              Thermo Partisol Model 2025-D Dichot         FEM
  45          205                                       AP 602 BAM         FEM
  46          208  Thermo Scientific 1405-DF Dichotomous TEOM FDMS         FEM
  47          216       Tisch Model TE-Wilbur10 Low-Volume Sampler         FRM
  48          226                               Met One E-BAM PLUS         FEM
  49          231                               Met One E-FRM PM10         FRM
  50          239                  Teledyne API T640X at 16.67 LPM         FEM
  51          246                                Met One E-SEQ-FRM         FRM
  52          702                                     INTERIM PM10         NaN
  53          771                                     INTERIM PM10         NaN
  54          772                                     INTERIM PM10         NaN
  55          773                            LO-VOL-DICHOT-INTERIM         NaN
  56          774                         HI-VOL INTERIM 15 MICRON         NaN
  57          790                                 Virtual Impactor         NaN
  58          792                                 Virtual Impactor         NaN
  59          879  INSTRUMENTAL-R&P SA246B-Inlet (Tx Modification)         NaN
  60          900                        BGI Inc. frmOMNI at 5 lpm         NaN

  Enter the method code corresponding to the reference method for T640_2_PM10:239

  Confirm entry [y/n]: y

  Enter the parameter occurance code for the above reference method:1

  Confirm entry [y/n]: y

  Configured renaming scheme:
  {'BC AE33 880nm': '',
  'GRIMM PM1': '',
  'Grimm PM10': '',
  'Grimm PM2.5': '',
  'T640_2_PM10': 'PM10',
  'T640_2_PM25': 'PM25',
  'UV_633_370nm': ''}

  Press enter to continue.

10. Configuring Timestamp Column Formatting
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

  Enter date/time formatting for "Date & Time": %-m/%-d/%Y %-I:%M %p

  Confirm entry [y/n]: y

  Configured formatting scheme:
  {'Date & Time': '%-m/%-d/%Y %-I:%M %p'}

  Press enter to continue.


11. Saving the Setup Configuration to ``setup.json``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Setup module will automatically save the setup configuration
to a ``reference_setup.json`` file at the indicated directory location:

.. code-block:: console

  ============================= Setup Configuration ============================
  ==============================================================================

  ..writing setup configuration to the following path:
  C:\Users\...\Documents\sensortoolkit_testing\Data and Figures\reference_data
  \local\raw\Burdens_Creek_370630099\reference_setup.json

12. Reference Data Ingestion and Saving Processed Datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: console

  ============================ Ingest Local Datasets ===========================
  ==============================================================================

  ..H_201909_PM.csv
  ..H_201910_PM.csv


Loading Reference Data
----------------------
.. code-block:: python

  reference_object.load_data(bdate='2019-08-01',
                             edate='2019-09-15',
                             param_list=['PM25'])

.. code-block:: console

  Loading reference dataframes
  ..2019-08
  ....H_201908_PM.csv
  ....H_201908_Met.csv
  ..2019-09
  ....H_201909_PM.csv
  ....H_201909_Met.csv
