Loading Reference Data
======================

.. tabbed:: Local

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

.. tabbed:: AirNowTech

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

.. tabbed:: Querying the AQS API

  .. code-block:: python

    aqs_username = 'usernam@email.com'
    aqs_key = 'NOT-A-REAL-KEY'

    ref.query_aqs(username=aqs_username,
                key=aqs_key,
                param_list=['PM25'],
                bdate='2019-08-01',
                edate='2019-09-15')

  .. code-block:: console

    Querying AQS API
    ..Parameter(s): PM25
    ..Query start: 2019-08-01
    ..Query end: 2019-08-31
    ..Response status: Success
    ..Query start: 2019-08-01
    ..Query end: 2019-08-31
    ..Response status: Success
    ..Query site(s):
    ....Site name: Triple Oak
    ......AQS ID: 37-183-0021
    ......Latitude: 35.8652
    ......Longitude: -78.8197
    Querying AQS API
    ..Parameter(s): PM25
    ..Query start: 2019-09-01
    ..Query end: 2019-09-30
    ..Response status: Success
    ..Query start: 2019-09-01
    ..Query end: 2019-09-30
    ..Response status: Success
    ..Query site(s):
    ....Site name: Triple Oak
    ......AQS ID: 37-183-0021
    ......Latitude: 35.8652
    ......Longitude: -78.8197
    Querying AQS API
    ..Parameter(s): Temp, RH
    ..Query start: 2019-08-01
    ..Query end: 2019-08-31
    ..Response status: No data matched your selection
    Querying AQS API
    ..Parameter(s): Temp, RH
    ..Query start: 2019-09-01
    ..Query end: 2019-09-30
    ..Response status: No data matched your selection

.. tabbed:: Querying the AirNow API

  .. code-block:: python

    airnow_key = 'NOT-A-REAL-KEY'
    ref.query_airnow(key=airnow_key,
                     param_list=['PM25'],
                     bdate='2019-08-01',
                     edate='2019-09-15')

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
    Querying AirNow API
    ..Parameter(s): PM25
    ..Query start: 2019-09-01
    ..Query end: 2019-09-30
    ..Query site(s):
    ....Site name: Burdens Creek
    ......AQS ID: 37-063-0099
    ......Latitude: 35.8894
    ......Longitude: -78.8747
    ..Query Status: Success

-----

.. note::

  For details on accessing reference datasets via the ``reference_object.data`` attribute,
  please see [X]