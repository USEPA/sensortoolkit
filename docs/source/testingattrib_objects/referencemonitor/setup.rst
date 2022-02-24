ReferenceMonitor Setup
======================

.. role:: raw-html(raw)
   :format: html

The ``sensortoolkit.ReferenceMonitor.reference_setup()`` module guides users through
an interactive process of entering in details regarding the reference data configuration
the user plans to make use of for conducting evaluations.

For reference datasets that users have downloaded locally, the setup process walks users through entering in details
necessary for constructing a data ingestion configuration. This configuration is saved
to a setup.json configuration file that contains details for describing and converting
the recorded sensor data format into the `sensortoolkit Data Formatting Scheme (SDFS) <../../sdfs/index.html>`_.

If users plan to query either the AirNow or AQS API (user accounts required for either service),
the setup module will walk users through an abbreviated process in order to indicate various site
parameters that are required for querying these API services.

Continuing with the `Toco Toucan Quickstart example <../../quickstart.html#example-scenario-toco-toucan>`_,
following the creation of our ``reference`` object, the setup module can be called via the following line of code:

.. code-block:: python

  reference.reference_setup()

Running the above code, the user is greeted with a number of printed statements in
the console that prompt the user's input. ``reference_setup()`` is an interactive
module, where the user inputs information via the console.

.. note::

  If you're following along with the `Toco Toucan Quickstart example <../../quickstart.html#example-scenario-toco-toucan>`_,
  please note that example reference data sets included in the GitHub repository under the ``/example_datasets``
  folder were downloaded from AirNow-Tech. To use the ``"airnowtech_example_reference_data.csv"``
  data file, **follow the setup directions below under the "AirNow-Tech" tab.**

.. tip::

  Because the setup process is slightly different depending on the service selected,
  use the tabs below to select the reference data service or source corresponding
  to your use case. This will display the setup process corresponding to the selected
  service or data source.

.. important::

  A console width of at least 80 characters is recommended to properly format
  printed statements, banners, and tables within this setup method.


.. tabbed:: AirNow-Tech

  The following steps below walk through the setup process. The example below
  describes the setup process for a reference data file downloaded from AirNow-Tech
  for the EPA RTP monitoring site for sensor evaluations.

  **1. Selecting the Reference Data Service/Source**

    First, the user is asked to specify the service or source for reference data.
    The user's entry must correspond to one of the options listed in the table shown
    in the banner for the section: users must choose from ``airnow`` (user plans to
    query the AirNow API), ``aqs`` (user plans to query the AQS API), ``airnowtech`` (user
    has downloaded files from the AirNow-Tech system and has saved files locally to the user's
    system), or ``local`` (a catchall for reference data files the user may have stored
    locally on their system that were not acquired from any of the services previously mentioned).

    .. code-block:: console

      =================== Select Name of Service for Data Source ===================
      Options
      -------
      ['airnow', 'aqs', 'airnowtech', 'local']
      ==============================================================================

      Enter the name of the service from the list of options above: airnowtech

  **2. Adding Monitoring Site Information**

    Next, the user should enter in information about the ambient monitoring site
    at which the collocation study was conducted. If certain details are unknown or
    don't apply to the site (e.g. Non-AQS sites will not have an AQS Site ID), entries
    can be skipped by pressing the 'Enter' key.

    .. important::
      Users are strongly recommended to provide a site name and, if applicable, a site AQS ID.
      These attributes are used to organize reference data within the ``/data/reference_data/[data source]/[raw or processed]``
      subdirectories.

      This is particularly important if users are working with data from numerous sites yet share the same data source.
      For instance, if one is using AirNow-Tech for reference data at two sites, Site A and Site B,
      the folder structure for processed reference datasets should look something like:

      .. code-block:: console

        my_evaluation
        |
        └─data
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

  **3. Selecting File Data Type**

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

  **4. Selecting Data Files**

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

      Enter how to select reference datasets from the list of options above: files

      Select data sets by files

      Confirm entry [y/n]: y

  **5. Copying Data files**

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
      ['C:/Users/.../Documents/Public_Sensor_Evaluation/beta_testing/data/reference/20190901_20190930_PMGasMet.csv']

      Destination Directory:
      ..C:\Users\...\Documents\sensortoolkit_testing\data\reference_data\airnowtech\raw\Burdens_Creek_370630099

      Press enter to continue.

      Copying the following files:
      ..C:/Users/.../Documents/sensortoolkit/beta_testing/data/reference/20190901_20190930_PMGasMet.csv

      Press enter to continue.

  **6. Pre-processing AirNow-Tech Datasets**

    The local AirNow-Tech files that the user selected in the previous step are
    imported and processed versions of these datasets are ingested into the SDFS
    format via the ``sensortoolkit.reference.preprocess_airnowtech()`` method.
    Processed datasets are subsequently saved as comma-separated value files to
    ``/data/reference_data/airnowtech/processed/[site_name]_[site_id]``, where ``[site_name]``
    is the name of the site assigned by the user in step 2, and ``[site_id]`` is
    the AQS ID for the site assigned in step 2 (if applicable).

    .. code-block:: console

      ====================== Pre-process AirNow-Tech Datasets ======================
      ==============================================================================

      Writing AirNow-Tech data sets to csv files
      ../reference_data/airnowtech/processed/Burdens_Creek_370630099/H_201909_PM.csv
      Writing AirNow-Tech data sets to csv files
      ../reference_data/airnowtech/processed/Burdens_Creek_370630099/H_201909_Gases.csv
      Writing AirNow-Tech data sets to csv files
      ../reference_data/airnowtech/processed/Burdens_Creek_370630099/H_201909_Met.csv

  **7. Saving the Setup Configuration to** ``setup.json``

    The Setup module will automatically save the setup configuration
    to a ``reference_setup.json`` file at the indicated directory location:

    .. code-block:: console

      ============================= Setup Configuration ============================
      ==============================================================================

      ..writing setup configuration to the following path:
        \data\reference_data\airnowtech\raw\Burdens_Creek_370630099\reference_setup.json

.. tabbed:: AQS

  The following steps below walk through the setup process. The example below
  describes the setup process for a reference data file downloaded from AQS
  for the Triple Oak monitoring site nearby EPA's RTP monitoring site for sensor evaluations.

  **1. Selecting the Reference Data Service/Source**

    First, the user is asked to specify the service or source for reference data.
    The user's entry must correspond to one of the options listed in the table shown
    in the banner for the section: users must choose from ``airnow`` (user plans to
    query the AirNow API), ``aqs`` (user plans to query the AQS API), ``airnowtech`` (user
    has downloaded files from the AirNow-Tech system and has saved files locally to the user's
    system), or ``local`` (a catchall for reference data files the user may have stored
    locally on their system that were not acquired from any of the services previously mentioned).

    .. code-block:: console

      =================== Select Name of Service for Data Source ===================
      Options
      -------
      ['airnow', 'aqs', 'airnowtech', 'local']
      ==============================================================================

      Enter the name of the service from the list of options above: aqs

  **2. Adding Monitoring Site Information**

    Next, the user should enter in information about the ambient monitoring site
    at which the collocation study was conducted. If certain details are unknown or
    don't apply to the site (e.g. Non-AQS sites will not have an AQS Site ID), entries
    can be skipped by pressing the 'Enter' key.

    .. important::
      Users are strongly recommended to provide a site name and, if applicable, a site AQS ID.
      These attributes are used to organize reference data within the ``/data/reference_data/[data source]/[raw or processed]``
      subdirectories.

      This is particularly important if users are working with data from numerous sites yet share the same data source.
      For instance, if one is using AirNow-Tech for reference data at two sites, Site A and Site B,
      the folder structure for processed reference datasets should look something like:

      .. code-block:: console

        my_evaluation
        |
        └─data
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

      Enter the name of the monitoring site: Triple Oak

      Confirm entry [y/n]: y


      Enter the name of the Agency overseeing the monitoring site: NCDEQ

      Confirm entry [y/n]: y


      Enter the AQS site ID (if applicable) [format XX-XXX-XXXX]:37-183-0021

      Confirm entry [y/n]: y


      Enter the site latitude (in decimal coordinates):35.87

      Confirm entry [y/n]: y


      Enter the site longitude (in decimal coordinates):-78.82

      Confirm entry [y/n]: y

  **3. Saving the Setup Configuration to** ``setup.json``

    The Setup module will automatically save the setup configuration
    to a ``reference_setup.json`` file at the indicated directory location:

    .. code-block:: console

      ============================= Setup Configuration ============================
      ==============================================================================

      ..writing setup configuration to the following path:
        \data\reference_data\aqs\raw\Triple_Oak_371830021\reference_setup.json

.. tabbed:: AirNow


  The following steps below walk through the setup process. The example below
  describes the setup process for a reference data file downloaded from AirNow
  for the EPA RTP monitoring site for sensor evaluations.

  **1. Selecting the Reference Data Service/Source**

    First, the user is asked to specify the service or source for reference data.
    The user's entry must correspond to one of the options listed in the table shown
    in the banner for the section: users must choose from ``airnow`` (user plans to
    query the AirNow API), ``aqs`` (user plans to query the AQS API), ``airnowtech`` (user
    has downloaded files from the AirNow-Tech system and has saved files locally to the user's
    system), or ``local`` (a catchall for reference data files the user may have stored
    locally on their system that were not acquired from any of the services previously mentioned).

    .. code-block:: console

      =================== Select Name of Service for Data Source ===================
      Options
      -------
      ['airnow', 'aqs', 'airnowtech', 'local']
      ==============================================================================

      Enter the name of the service from the list of options above: airnow

  **2. Adding Monitoring Site Information**

    Next, the user should enter in information about the ambient monitoring site
    at which the collocation study was conducted. If certain details are unknown or
    don't apply to the site (e.g. Non-AQS sites will not have an AQS Site ID), entries
    can be skipped by pressing the 'Enter' key.

    .. important::
      Users are strongly recommended to provide a site name and, if applicable, a site AQS ID.
      These attributes are used to organize reference data within the ``/data/reference_data/[data source]/[raw or processed]``
      subdirectories.

      This is particularly important if users are working with data from numerous sites yet share the same data source.
      For instance, if one is using AirNow-Tech for reference data at two sites, Site A and Site B,
      the folder structure for processed reference datasets should look something like:

      .. code-block:: console

        my_evaluation
        |
        └─data
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

  **3. Saving the Setup Configuration to** ``setup.json``

    The Setup module will automatically save the setup configuration
    to a ``reference_setup.json`` file at the indicated directory location:

    .. code-block:: console

      ============================= Setup Configuration ============================
      ==============================================================================

      ..writing setup configuration to the following path:
        \data\reference_data\airnow\raw\Burdens_Creek_370630099\reference_setup.json
        .. tabbed:: Local

          The following steps below walk through the setup process. The example below
          describes the setup process for a reference data file acquired locally for
          EPA's sensor testing site:

.. tabbed:: Local

  **1. Selecting the Reference Data Service/Source**

    First, the user is asked to specify the service or source for reference data.
    The user's entry must correspond to one of the options listed in the table shown
    in the banner for the section: users must choose from ``airnow`` (user plans to
    query the AirNow API), ``aqs`` (user plans to query the AQS API), ``airnowtech`` (user
    has downloaded files from the AirNow-Tech system and has saved files locally to the user's
    system), or ``local`` (a catchall for reference data files the user may have stored
    locally on their system that were not acquired from any of the services previously mentioned).

    .. code-block:: console

      =================== Select Name of Service for Data Source ===================
      Options
      -------
      ['airnow', 'aqs', 'airnowtech', 'local']
      ==============================================================================

      Enter the name of the service from the list of options above: local

  **2. Adding Monitoring Site Information**

    Next, the user should enter in information about the ambient monitoring site
    at which the collocation study was conducted. If certain details are unknown or
    don't apply to the site (e.g. Non-AQS sites will not have an AQS Site ID), entries
    can be skipped by pressing the 'Enter' key.

    .. important::
      Users are strongly recommended to provide a site name and, if applicable, a site AQS ID.
      These attributes are used to organize reference data within the ``/data/reference_data/[data source]/[raw or processed]``
      subdirectories.

      This is particularly important if users are working with data from numerous sites yet share the same data source.
      For instance, if one is using AirNow-Tech for reference data at two sites, Site A and Site B,
      the folder structure for processed reference datasets should look something like:

      .. code-block:: console

        my_evaluation
        |
        └───data
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

  **3. Selecting File Data Type**

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

  **4. Selecting Data Files**

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

      Enter how to select reference datasets from the list of options above: files

      Select data sets by files

      Confirm entry [y/n]: y

  **5. Copying Data files**

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

  **6. Selecting the Column Header Index**

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
      \data\reference_data\local\raw\Burdens_Creek_370630099\min_201908_PM.csv
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

  **7. Parsing Reference Datasets**

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

      Parsing datasets at "../data/reference_data/local/raw/Burdens_Creek_370630099/"
      ..Header(s) at column index 0: ['Date & Time']
      ..Header(s) at column index 1: ['UV_633_370nm']
      ..Header(s) at column index 2: ['BC AE33 880nm']
      ..Header(s) at column index 3: ['Grimm PM2.5']
      ..Header(s) at column index 4: ['Grimm PM10']
      ..Header(s) at column index 5: ['GRIMM PM1']
      ..Header(s) at column index 6: ['T640_2_PM25']
      ..Header(s) at column index 7: ['T640_2_PM10']

      Press enter to continue.

  **8. Specifying Timestamp Columns**

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

      Enter Timestamp column name #1: Date & Time

      Enter Timestamp column name #2: X

      Timestamp column list: ['Date & Time']

      Press enter to continue.

  **9. Specifying the Parameter Renaming Scheme and Monitor Information**

    Next, users are prompted to configure the parameter renaming scheme by entering
    in the sensortoolkit Data Formatting Scheme (SDFS) parameter name
    that corresponds to each parameter header name.

    For each SDFS parameter specified, a set of queries will be prompted which
    ask the user to specify parameter-specific details. Based on the indicated
    SDFS parameter, a prompt will ask the user whether the reference
    measurements are associated with a standard `parameter code <https://aqs.epa.gov/aqsweb/documents/codetables/methods_all.html>`_
    EPA's Air Quality System (AQS) associates with the pollutant or environmental parameter.

    Parameter codes are assigned by AQS for classifying the
    type of parameter alongside a description of the reference method used to collect measurements.
    For instance, ``88101`` is the standard parameter code for :raw-html:`PM<sub>2.5</sub>` measurements collected at local
    conditions via an instrument designated a Federal Reference Method (FRM) or
    Federal Equivalent Method (FEM) for :raw-html:`PM<sub>2.5</sub>`.

    For the example below, measurements for :raw-html:`PM<sub>2.5</sub>` and :raw-html:`PM<sub>10</sub>` were collected by a
    Teledyne API T640x, which is designated an FEM for :raw-html:`PM<sub>2.5</sub>` and :raw-html:`PM<sub>10</sub>`. Measurements for these pollutants
    made with the T640x are categorized under the parameter codes ``88101`` for :raw-html:`PM<sub>2.5</sub>`
    measurements and ``88102`` for :raw-html:`PM<sub>10</sub>` measurements. A table of FRM/FEM methods
    is displayed if the user indicates that the parameter code corresponds to the
    standard AQS code indicated by the console. The user is asked to select the
    method code (which is AQS code associated with the reference instrument) for
    each parameter. Below, the highlighted lines indicate the table entries corresponding
    to the Teledyne API T640x used to collect :raw-html:`PM<sub>2.5</sub>` and :raw-html:`PM<sub>10</sub>` measurement data.

    .. tip::

      Column names that do not have a corresponding listed parameter should be dropped
      from the dataset by pressing enter.

    .. code-block:: console
      :emphasize-lines: 72, 152

      ========================== Specify Parameter columns =========================
      Options
      -------
      ..press enter to skip columns that will be dropped

      Notes
      -----
      Choose from the following list of SDFS parameter names
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

      Parameter type for header name "UV_633_370nm":
      ..UV_633_370nm will be dropped

      [2/7]
      -----

      Enter the character indicating the type of parameter
      {'': '(enter key) Skip the current header and drop from SDFS datasets',
       'C': 'The header corresponds to an existing custom Parameter',
       'N': 'Create a new custom Parameter for the header',
       'S': 'The header corresponds to an SDFS Parameter'}

      Parameter type for header name "BC AE33 880nm":
      ..BC AE33 880nm will be dropped

      [3/7]
      -----

      Enter the character indicating the type of parameter
      {'': '(enter key) Skip the current header and drop from SDFS datasets',
       'C': 'The header corresponds to an existing custom Parameter',
       'N': 'Create a new custom Parameter for the header',
       'S': 'The header corresponds to an SDFS Parameter'}

      Parameter type for header name "Grimm PM2.5":
      ..Grimm PM2.5 will be dropped

      [4/7]
      -----

      Enter the character indicating the type of parameter
      {'': '(enter key) Skip the current header and drop from SDFS datasets',
       'C': 'The header corresponds to an existing custom Parameter',
       'N': 'Create a new custom Parameter for the header',
       'S': 'The header corresponds to an SDFS Parameter'}

      Parameter type for header name "Grimm PM10":
      ..Grimm PM10 will be dropped

      [5/7]
      -----

      Enter the character indicating the type of parameter
      {'': '(enter key) Skip the current header and drop from SDFS datasets',
       'C': 'The header corresponds to an existing custom Parameter',
       'N': 'Create a new custom Parameter for the header',
       'S': 'The header corresponds to an SDFS Parameter'}

      Parameter type for header name "GRIMM PM1":
      ..GRIMM PM1 will be dropped

      [6/7]
      -----

      Enter the character indicating the type of parameter
      {'': '(enter key) Skip the current header and drop from SDFS datasets',
       'C': 'The header corresponds to an existing custom Parameter',
       'N': 'Create a new custom Parameter for the header',
       'S': 'The header corresponds to an SDFS Parameter'}

      Parameter type for header name "T640_2_PM25": S

      SDFS Parameters:
      ['CO', 'DP', 'NO', 'NO2', 'NOx', 'O3', 'PM1', 'PM10', 'PM25', 'SO2', 'SOx',
       'Temp', 'RH', 'Press', 'WD', 'WS']

      From the list above, select the SDFS parameter associated with T640_2_PM25: PM25

        Enter the units of measure for T640_2_PM25: Micrograms per cubic meter

        Confirm entry [y/n]: y

        Is the parameter code for reference measurements 88101?

        Confirm entry [y/n]: y

      |   Method Code | Collection Description                                     | Method Type   |
      |--------------:|:-----------------------------------------------------------|:--------------|
      |           116 | BGI Model PQ200 PM2.5 Sampler w/WINS                       | FRM           |
      |           117 | R & P Model 2000 PM2.5 Sampler w/WINS                      | FRM           |
      |           118 | R & P Model 2025 PM2.5 Sequential w/WINS                   | FRM           |
      |           119 | Andersen RAAS2.5-100 PM2.5 SAM w/WINS                      | FRM           |
      |           120 | Andersen RAAS2.5-300 PM2.5 SEQ w/WINS                      | FRM           |
      |           123 | Thermo Env Model 605 CAPS                                  | FRM           |
      |           128 | Andersen RAAS2.5-2000PM2.5 Aud w/WINS                      | FRM           |
      |           129 | R & P Model 2000 PM-2.5 Audit w/WINS                       | FRM           |
      |           135 | URG-MASS100 Single PM2.5 Sampler                           | FRM           |
      |           136 | URG-MASS300 Sequential PM2.5 Sampler                       | FRM           |
      |           142 | BGI Models PQ200-VSCC or PQ200A-VSCC                       | FRM           |
      |           143 | R & P Model 2000 PM-2.5 Air Sampler w/VSCC                 | FRM           |
      |           144 | R & P Model 2000 PM-2.5 Audit Sampler w/VSCC               | FRM           |
      |           145 | R & P Model 2025 PM-2.5 Sequential Air Sampler w/VSCC      | FRM           |
      |           153 | Thermo Electron Model RAAS2.5-100 w/VSCC                   | FRM           |
      |           154 | Thermo Electron Model RAAS2.5-200 Audit w/VSCC             | FRM           |
      |           155 | Thermo Electron Model RAAS2.5-300 Sequential w/VSCC        | FRM           |
      |           170 | Met One BAM-1020 Mass Monitor w/VSCC                       | FEM           |
      |           177 | Thermo Scientific Partisol 2000-D Dichot.                  | FEM           |
      |           179 | Thermo Scientific Dichot. Partisol-Plus Model 2025-D Seq   | FEM           |
      |           181 | Thermo Scientific TEOM 1400 FDMS or 1405 8500C FDMS w/VSCC | FEM           |
      |           182 | Thermo Scientific TEOM 1405-DF Dichotomous FDMS            | FEM           |
      |           183 | Thermo Scientific 5014i or FH62C14-DHS w/VSCC              | FEM           |
      |           184 | Thermo Scientific Model 5030 SHARP w/VSCC                  | FEM           |
      |           195 | GRIMM EDM Model 180 with naphion dryer                     | FEM           |
      |           203 | Opsis SM200-Dust Monitor w/VSCC                            | FEM           |
      |           204 | Teledyne Model 602 Beta plus w/VSCC                        | FEM           |
      |           209 | Met One BAM-1022 Mass Monitor w/ VSCC or TE-PM2.5C         | FEM           |
      |           219 | Tisch Model TE-Wilbur2.5 Low-Volume Sampler                | FRM           |
      |           221 | Met One E-FRM PM2.5 with WINS                              | FRM           |
      |           235 | Met One E-FRM PM2.5 with URG-2000-30EGN cyclone            | FEM           |
      |           236 | Teledyne T640 at 5.0 LPM                                   | FEM           |
      |           238 | Teledyne T640X at 16.67 LPM                                | FEM           |
      |           245 | Met One E-SEQ-FRM PM2.5 with WINS                          | FRM           |
      |           521 | Met One E-FRM PM2.5 with VSCC                              | FRM           |
      |           545 | Met One E-SEQ-FRM PM2.5 with VSCC                          | FRM           |
      |           581 | Thermo Scientific 1405-F FDMS w/VSCC                       | FEM           |

        Enter the method code corresponding to the reference method for T640_2_PM25:238

        Confirm entry [y/n]: y

        Enter the parameter occurrence code for the above reference method:1

        Confirm entry [y/n]: y

        Are the units of measure for T640_2_PM25 µg/m³?

        Confirm entry [y/n]: y

      [7/7]
      -----

      Enter the character indicating the type of parameter
      {'': '(enter key) Skip the current header and drop from SDFS datasets',
       'C': 'The header corresponds to an existing custom Parameter',
       'N': 'Create a new custom Parameter for the header',
       'S': 'The header corresponds to an SDFS Parameter'}

      Parameter type for header name "T640_2_PM10": S

      SDFS Parameters:
      ['CO', 'DP', 'NO', 'NO2', 'NOx', 'O3', 'PM1', 'PM10', 'PM25', 'SO2', 'SOx',
       'Temp', 'RH', 'Press', 'WD', 'WS']

      From the list above, select the SDFS parameter associated with T640_2_PM10: PM10

        Enter the units of measure for T640_2_PM10:Micrograms per cubic meter

        Confirm entry [y/n]: y

        Is the parameter code for reference measurements 81102?

        Confirm entry [y/n]: y

      |   Method Code | Collection Description                          | Method Type   |
      |--------------:|:------------------------------------------------|:--------------|
      |             1 | LO-VOL-SA244E                                   | nan           |
      |             2 | LO-VOL-GMW9200                                  | nan           |
      |             3 | LO-VOL-WA10-DICHOT                              | nan           |
      |             4 | LO-VOL-SA246B-DICHOT                            | nan           |
      |            11 | DUSTTRAK 8530                                   | nan           |
      |            12 | DUSTTRAK 8533                                   | nan           |
      |            25 | MED-VOL-SA254                                   | nan           |
      |            26 | MED-VOL-GMW9100                                 | nan           |
      |            40 | WEDDING-AUTOMATED-PM10 SAMPLER                  | nan           |
      |            41 | BAM-102-CONTINUOUS MONITOR                      | nan           |
      |            51 | HI-VOL-SA321                                    | nan           |
      |            52 | HI-VOL-SA321A                                   | nan           |
      |            53 | HI-VOL-GMW9000                                  | nan           |
      |            54 | HI-VOL-W10                                      | nan           |
      |            55 | HI-VOL-W10-(W/MAINT.AC.PORT)                    | nan           |
      |            56 | HI-VOL-SA321G-(321-W/OILSHIM)                   | nan           |
      |            57 | HI-VOL-SA321AG(321A-W/OILSHIM)                  | nan           |
      |            58 | HI-VOL-SA321B                                   | nan           |
      |            59 | HI-VOL-SA1200                                   | nan           |
      |            62 | HI-VOL-WEDDING-INLET                            | FRM           |
      |            63 | HI-VOL SA/GMW-1200                              | FRM           |
      |            64 | HI-VOL-SA/GMW-321-B                             | FRM           |
      |            65 | HI-VOL-SA/GMW-321-C                             | FRM           |
      |            71 | OREGON-DEQ-MED-VOL                              | FRM           |
      |            73 | LO-VOL-DICHOTOMOUS-SA246B-INLT                  | FRM           |
      |            76 | INSTRMENTL-ANDRSEN-SA246B-INLT                  | FEM           |
      |            79 | INSTRUMENTAL-R&P SA246B-INLET                   | FEM           |
      |            81 | INSTRUMENTAL-WEDDING-AUTOMATIC                  | FEM           |
      |            98 | R&P Model 2000 Partisol                         | FRM           |
      |           122 | INSTRUMENT MET ONE 4 MODELS                     | FEM           |
      |           124 | BGI Inc. Model PQ100 PM10                       | FRM           |
      |           125 | BGI Inc. Model PQ200 PM10                       | FRM           |
      |           126 | R - P Co Partisol Model 2000                    | FRM           |
      |           127 | R - P Co Partisol Model 2025                    | FRM           |
      |           130 | Andersen RAAS10-100 Single channel              | FRM           |
      |           131 | Andersen RAAS10-200 S-Channel                   | FRM           |
      |           132 | Andersen RAAS10-300 M-channel                   | FRM           |
      |           141 | Tisch Environ Model-6070 PM10 Hi-Vol            | FRM           |
      |           150 | T A Series FH 62 C14 Continuous                 | FEM           |
      |           151 | Environnement S.A. Model MP101M                 | FEM           |
      |           156 | Instrument DKK_TOA                              | FEM           |
      |           162 | Hi Vol SSI Ecotech Model 3000                   | FRM           |
      |           193 | OPSIS Model SM200 PM10 Monitor                  | FEM           |
      |           197 | Thermo Partisol Model 2000-D Dichot             | FEM           |
      |           198 | Thermo Partisol Model 2025-D Dichot             | FEM           |
      |           205 | AP 602 BAM                                      | FEM           |
      |           208 | Thermo Scientific 1405-DF Dichotomous TEOM FDMS | FEM           |
      |           216 | Tisch Model TE-Wilbur10 Low-Volume Sampler      | FRM           |
      |           226 | Met One E-BAM PLUS                              | FEM           |
      |           231 | Met One E-FRM PM10                              | FRM           |
      |           239 | Teledyne API T640X at 16.67 LPM                 | FEM           |
      |           246 | Met One E-SEQ-FRM                               | FRM           |
      |           702 | INTERIM PM10                                    | nan           |
      |           771 | INTERIM PM10                                    | nan           |
      |           772 | INTERIM PM10                                    | nan           |
      |           773 | LO-VOL-DICHOT-INTERIM                           | nan           |
      |           774 | HI-VOL INTERIM 15 MICRON                        | nan           |
      |           790 | Virtual Impactor                                | nan           |
      |           792 | Virtual Impactor                                | nan           |
      |           879 | INSTRUMENTAL-R&P SA246B-Inlet (Tx Modification) | nan           |
      |           900 | BGI Inc. frmOMNI at 5 lpm                       | nan           |

        Enter the method code corresponding to the reference method for T640_2_PM10:239

        Confirm entry [y/n]: y

        Enter the parameter occurrence code for the above reference method:1

        Confirm entry [y/n]:
        ..invalid entry, select [y/n]

        Confirm entry [y/n]: y

        Are the units of measure for T640_2_PM10 µg/m³?

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

  **10. Configuring Timestamp Column Formatting**

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

    **11. Specifying the DateTime Index Time Zone**

    Next, the time zone for the timestamp column should be indicated. `SDFS <../../sdfs/index.html>`_
    formatted datasets indicate timestamps in Coordinated Universal Time (UTC), and during
    dataset ingestion, timestamps are shifted by the UTC offset corresponding to the time zone
    indicated at this step.

    The ``pytz`` package is used for indicating time zone names
    and corresponding UTC offsets, and users can type ``pytz.all_timezones`` to see a list of
    all time zones in the ``pytz`` library (word of caution, there are a lot!). When the
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

      Enter time zone for "Date & Time": EST

      Confirm entry [y/n]: y

      Configured time zone formatting:
      {'Date & Time': '%-m/%-d/%Y %-I:%M %p', 'Date & Time_tz': 'EST'}

      Press enter to continue.

  **12. Saving the Setup Configuration to** ``setup.json``

    The Setup module will automatically save the setup configuration
    to a ``reference_setup.json`` file at the indicated directory location:

    .. code-block:: console

      ============================= Setup Configuration ============================
      ==============================================================================

      ..writing setup configuration to the following path:
        \data\reference_data\local\raw\Burdens_Creek_370630099\reference_setup.json

  **13. Reference Data Ingestion and Saving Processed Datasets**

    As a final step, recorded reference datasets are ingested via the configuration
    specified and processed version of these datasets that have been converted to
    SDFS format are saved as comma-separated value files to the
    ``/data/reference_data/[source]/processed/[site_name]_[site_id]`` directory, where
    ``[source]`` is the reference data source assigned in step 1, ``[site_name]``
    is the name of the site assigned by the user in step 2, and ``[site_id]`` is
    the AQS ID for the site assigned in step 2 (if applicable).

    .. code-block:: console

      ============================ Ingest Local Datasets ===========================
      ==============================================================================

      ..H_201909_PM.csv
      ..H_201910_PM.csv
