Loading Reference Data
======================

Reference data are loaded either via the ``ReferenceMonitor.load_data()`` method,
or, if users wish to query the AirNow or AQS API, either the ``ReferenceMonitor.query_aqs()``
or the ``ReferenceMonitor.query_aqs()`` method should be used.

A description and example of each method is detailed below, where information has been
sorted by the reference data source or API service.

.. tabbed:: Local

  .. note::

    This section provides a brief overview of loading reference data with the ``ReferenceMonitor.load_data()`` method.
    For more detailed documentation, please see
    `API documentation for sensortoolkit.ReferenceMonitor.load_data() <../../api/_autosummary/sensortoolkit.testing_attrib_objs._referencemonitor.ReferenceMonitor.html#sensortoolkit.testing_attrib_objs._referencemonitor.ReferenceMonitor.load_data>`_.

  To load reference data from locally acquired files, users should call the
  ``ReferenceMonitor.load_data()`` method.

  ``ReferenceMonitor.load_data()`` accepts the following arguments:

  .. list-table:: ``ReferenceMonitor.load_data()`` Arguments
    :widths: 50 75
    :header-rows: 1

    * - Argument
      - Description
    * - ``bdate``
      - The beginning date ("YYYY-MM-DD" format) for the sensor testing period.
    * - ``edate``
      - The ending date ("YYYY-MM-DD" format) for the sensor testing period.
    * - ``param_list``
      - A list of SDFS parameters measured by reference monitors at the |br|
        monitoring site for which data will be loaded.
    * - ``met_data``
      - Optional, if true, meteorological data will be loaded in addition to |br|
        datasets corresponding to parameters passed to ``param_list``. Defaults |br|
        to true (U.S. EPA's documents for recommended performance testing |br|
        protocols, metrics, and target values encourage users to report |br|
        meteorological conditions for sensor performance evaluations and |br|
        reports).

  .. note::

    The ``ReferenceMonitor.reference_setup()`` method saves SDFS formatted reference
    datasets in month-long segments (e.g.,
    ``/data/reference_data/local/processed/Burdens_Creek_370630099/H_201909_PM.csv``
    corresponds to 1-hour averaged reference data for instruments at the Burdens
    Creek monitoring site that measured particulate matter during the month of
    September 2019).

    ``ReferenceMonitor.load_data()`` will load monthly datasets corresponding to
    the set of months spanning the ``bdate`` and ``edate`` arguments.

  .. code-block:: python

    """
    Example - Loading local reference data for the Burdens Creek Monitoring site
    ----------------------------------------------------------------------------

    Prior to loading local datasets, a new ``ReferenceMonitor`` instance was
    created and a setup configuration was specified with 'local' as the
    reference data source. Site information was provided for the Burdens Creek
    Monitoring site:

    >>> reference = sensortoolkit.ReferenceMonitor(project_path=WORK_PATH)
    >>> reference.reference_setup()

    See ReferenceMonitor Setup for more information on running the ``reference_setup()``
    method.

    """
    reference.load_data(bdate=sensor.bdate,
                        edate=sensor.edate,
                        param_list=sensor.param_headers)

  .. code-block:: console

    Loading reference dataframes
    ..2019-08
    ....H_201908_PM.csv
    ....H_201908_Met.csv
    Computing 24-hour averaged reference datasets

.. tabbed:: AirNowTech

  .. note::

    This section provides a brief overview of loading reference data with the ``ReferenceMonitor.load_data()`` method.
    For more detailed documentation, please see
    `API documentation for sensortoolkit.ReferenceMonitor.load_data() <../../api/_autosummary/sensortoolkit.testing_attrib_objs._referencemonitor.ReferenceMonitor.html#sensortoolkit.testing_attrib_objs._referencemonitor.ReferenceMonitor.load_data>`_.

  To load processed (SDFS formatted) airnowtech datasets, users should call the
  ``ReferenceMonitor.load_data()`` method.

  ``ReferenceMonitor.load_data()`` accepts the following arguments:

  .. list-table:: ``ReferenceMonitor.load_data()`` Arguments
    :widths: 50 75
    :header-rows: 1

    * - Argument
      - Description
    * - ``bdate``
      - The beginning date ("YYYY-MM-DD" format) for the sensor testing period.
    * - ``edate``
      - The ending date ("YYYY-MM-DD" format) for the sensor testing period.
    * - ``param_list``
      - A list of SDFS parameters measured by reference monitors at the |br|
        monitoring site for which data will be loaded.
    * - ``met_data``
      - Optional, if true, meteorological data will be loaded in addition to |br|
        datasets corresponding to parameters passed to ``param_list``. Defaults |br|
        to true (U.S. EPA's documents for recommended performance testing |br|
        protocols, metrics, and target values encourage users to report |br|
        meteorological conditions for sensor performance evaluations and |br|
        reports).

  .. note::

    The ``ReferenceMonitor.reference_setup()`` method saves SDFS formatted reference
    datasets in month-long segments (e.g.,
    ``/data/reference_data/airnowtech/processed/Burdens_Creek_370630099/H_201909_PM.csv``
    corresponds to 1-hour averaged reference data for instruments at the Burdens
    Creek monitoring site that measured particulate matter during the month of
    September 2019).

    ``ReferenceMonitor.load_data()`` will load monthly datasets corresponding to
    the set of months spanning the ``bdate`` and ``edate`` arguments.

  .. code-block:: python

    """
    Example - Loading AirNowTech reference data for the Burdens Creek Monitoring site
    ---------------------------------------------------------------------------------

    Prior to loading AirNowTech datasets, a new ``ReferenceMonitor`` instance was
    created and a setup configuration was specified with 'airnowtech' as the
    reference data source. Site information was provided for the Burdens Creek
    Monitoring site:

    >>> reference = sensortoolkit.ReferenceMonitor(project_path=WORK_PATH)
    >>> reference.reference_setup()

    See the 'ReferenceMonitor Setup' section for more information on running
    the ``reference_setup()`` method.

    """

    reference.load_data(bdate=sensor.bdate,
                        edate=sensor.edate,
                        param_list=sensor.param_headers)

  .. code-block:: console

    Loading reference dataframes
    ..2019-08
    ....H_201908_PM.csv
    ....H_201908_Met.csv
    Computing 24-hour averaged reference datasets

.. tabbed:: Querying the AQS API

  .. note::

    This section provides a brief overview of querying EPA's Air Quality System (AQS)
    API for reference data. For more detailed documentation, please see
    `API documentation for sensortoolkit.ReferenceMonitor.query_aqs() <../../api/_autosummary/sensortoolkit.testing_attrib_objs._referencemonitor.ReferenceMonitor.html#sensortoolkit.testing_attrib_objs._referencemonitor.ReferenceMonitor.query_aqs>`_.

  The ``ReferenceMonitor.query_aqs()`` method accepts the following arguments:

  .. list-table:: ``ReferenceMonitor.query_aqs()`` Arguments
    :widths: 50 75
    :header-rows: 1

    * - Argument
      - Description
    * - ``username``
      - The email account registered with the API service.
    * - ``key``
      - The API authentication key code.
    * - ``param_list``
      - A list of SDFS parameters measured by reference monitors at the monitoring |br|
        site for which data will be loaded.
    * - ``bdate``
      - The beginning date ("YYYY-MM-DD" format) for the sensor testing period.
    * - ``edate``
      - The ending date ("YYYY-MM-DD" format) for the sensor testing period.
    * - ``site_id``
      - The AQS site ID for the air monitoring site from which reference |br|
        measurements will be returned by the API.
    * - ``met_data``
      - Optional, if true, meteorological data for temperature and relative |br|
        humidity measurements will be queried in addition to parameters passed |br|
        to ``param_list``. Defaults to true (U.S. EPA's documents for |br|
        recommended performance testing protocols, metrics, and target values |br|
        encourage users to report meteorological conditions for sensor |br|
        performance evaluations and reports).

  .. code-block:: python

    """
    Example - Querying the AQS API for data collected at the Millbrook School Monitoring site
    -----------------------------------------------------------------------------------------

    Prior to querying the AQS API, a new ``ReferenceMonitor`` instance was
    created and a setup configuration was specified with 'aqs' as the
    reference data source. Site information was provided for the Millbrook School
    Monitoring site:

    >>> reference = sensortoolkit.ReferenceMonitor(project_path=WORK_PATH)
    >>> reference.reference_setup()

    See the 'ReferenceMonitor Setup' section for more information on running
    the ``reference_setup()`` method.

    """

    aqs_username = 'username@email.com'
    aqs_key = 'NOT-A-REAL-KEY'

    reference.query_aqs(username=aqs_username,
                        key=aqs_key,
                        bdate=sensor.bdate,
                        edate=sensor.edate,
                        param_list=sensor.param_headers)

  When the above code block is run, a dialog indicating the status of the API
  query will be printed to the console. Below is the console output for an example
  query to the Millbrook Elementary School Monitoring Site in Raleigh, NC (**note that prior
  to running the code block above, the** ``ReferenceMonitor.reference_setup()`` **method
  was configured for an AQS query to the Millbrook School monitoring site**).

  During the example API query below, ``PM25`` data for multiple reference
  instruments were returned. A 'parameter occurrence code' (POC) is assigned to each
  reference instrument measuring the same parameter quantity at a monitoring site,
  and if multiple POCs are detected, the console will prompt the user to enter the POC
  corresponding to the instrument measurements they intend to use (highlighted rows
  in the console output below).

  .. tip::

    EPA's `AirData Air Quality Monitors Map <https://epa.maps.arcgis.com/apps/webappviewer/index.html?id=5f239fd3e72f424f98ef3d5def547eb5&extent=-146.2334,13.1913,-46.3896,56.5319>`_
    can be used to locate monitoring sites, reference instrumentation for
    various parameters, and instrument POCs.

  .. code-block:: console
    :emphasize-lines: 17

    Querying AQS API
    ..Parameter(s): PM25
    ..Query start: 2019-08-01
    ..Query end: 2019-08-31
    ..Response status: Success
    ..Query start: 2019-08-01
    ..Query end: 2019-08-31
    ..Response status: Success
    ..Query site(s):
    ....Site name: Millbrook School
    ......AQS ID: 37-183-0014
    ......Latitude: 35.8561
    ......Longitude: -78.5742

    The following parameter occurrence codes (POCs) for PM25 were found:
    ..POC: 3, number of entries: 744
    ..POC: 5, number of entries: 744

    Enter the POC for data entries you wish to keep: 5

    Querying AQS API
    ..Parameter(s): Temp, RH
    ..Query start: 2019-08-01
    ..Query end: 2019-08-31
    ..Response status: Success
    ..Query start: 2019-08-01
    ..Query end: 2019-08-31
    ..Response status: Success
    ..Query site(s):
    ....Site name: Millbrook School
    ......AQS ID: 37-183-0014
    ......Latitude: 35.8561
    ......Longitude: -78.5742

.. tabbed:: Querying the AirNow API

  .. note::

    This section provides a brief overview of querying EPA's AirNow API
    for reference data. For more detailed documentation, please see
    `API documentation for sensortoolkit.ReferenceMonitor.query_airnow() <../../api/_autosummary/sensortoolkit.testing_attrib_objs._referencemonitor.ReferenceMonitor.html#sensortoolkit.testing_attrib_objs._referencemonitor.ReferenceMonitor.query_airnow>`_.

  The ``ReferenceMonitor.query_airnow()`` method accepts the following arguments:

  .. list-table:: ``ReferenceMonitor.query_airnow()`` Arguments
    :widths: 50 75
    :header-rows: 1

    * - Argument
      - Description
    * - ``key``
      - The API authentication key code.
    * - ``param_list``
      - A list of SDFS parameters measured by reference monitors at the |br|
        monitoring site for which data will be loaded.
    * - ``bdate``
      - The beginning date ("YYYY-MM-DD" format) for the sensor testing period.
    * - ``edate``
      - The ending date ("YYYY-MM-DD" format) for the sensor testing period.
    * - ``bbox``
      - A bounding box of coordinates within which data will be queried. |br|
        Defaults to None.
    * - ``bbox_size``
      - Optional. Defaults to 0.01.

  .. code-block:: python

    """
    Example - Querying the AirNow API for data collected at the Millbrook School Monitoring site
    --------------------------------------------------------------------------------------------

    Prior to querying the AirNow API, a new ``ReferenceMonitor`` instance was
    created and a setup configuration was specified with 'airnow' as the
    reference data source. Site information was provided for the Burdens Creek
    Monitoring site:

    >>> reference = sensortoolkit.ReferenceMonitor(project_path=WORK_PATH)
    >>> reference.reference_setup()

    See the 'ReferenceMonitor Setup' section for more information on running
    the ``reference_setup()`` method.

    """
    airnow_key = 'NOT-A-REAL-KEY'
    reference.query_airnow(key=airnow_key,
                           bdate=sensor.bdate,
                           edate=sensor.edate,
                           param_list=sensor.param_headers)

  When the above code block is run, a dialog indicating the status of the API
  query will be printed to the console. Below is the console output for an example
  query to the Burdens Creek Monitoring Site in RTP, NC (**note that prior
  to running the code block above, the** ``ReferenceMonitor.reference_setup()`` **method
  was configured for an AirNow query to the Burdens Creek monitoring site**).

  .. code-block:: console

    Querying AirNow API
    ..Parameter(s): PM25
    ..Query start: 2019-08-01
    ..Query end: 2019-08-31
    ..Query site(s):
    ....Site name: Burdens Creek
    ......AQS ID: 37-063-0099
    ......Latitude: 35.8894
    ......Longitude: -78.8747
    ..Query Status: Success

-----

.. note::

  For details on accessing reference datasets via the ``reference_object.data`` attribute,
  please see `Accessing reference data <../../data_structures/reference_data.html#accessing-reference-data>`_.

.. |br| raw:: html

   <br />
