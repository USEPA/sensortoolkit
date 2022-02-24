The ReferenceMonitor Object
===========================

.. role:: gbg
.. role:: rbg

.. raw:: html

   <style>
      .gbg {background-color:#c4e5b4;}
      .rbg {background-color:#E5B4C4;}
   </style>


.. |br| raw:: html

  <br />

.. toctree::
  overview
  setup
  load_data

Choosing a Reference Data Source
--------------------------------

sensortoolkit allows users to work with reference data from one of four potential sources:

- **Local**: Reference datasets that are acquired locally from an air monitoring agency
  overseeing the site at which sensor are collocated alongside reference instrumentation.
  These data files should be located on the user's computer.
- `AQS <https://aqs.epa.gov/aqsweb/documents/data_api.html>`_: EPA's Air Quality System is the primary repository for acquiring reference datasets
  for monitors located at monitoring sites managed by state, local, tribal, and federal
  agencies. Datasets in AQS undergo rigorous quality control / quality assurance measures and this
  process may take up to 6 months. In turn, AQS does not contain real-time air quality data.
  Data are acquired via the ``sensortoolkit.ReferenceMonitor.query_aqs()`` method.
- `AirNow <https://docs.airnowapi.org/>`_: AirNow provides real-time air quality data (up to the most
  recent hour or day) from monitors managed by state, tribal, local, and federal agencies.
  Data from this service have not been validated and verified in the same manner as AQS data
  and should be considered preliminary. Official regulatory monitoring data are available from AQS.
  Data are acquired via the ``sensortoolkit.ReferenceMonitor.query_airnow()`` method.
- `AirNow-Tech <http://airnowtech.org/>`_: AirNow-Tech provides access to a greater pool of
  parameter data streams (including a wide range of meteorological parameters) and provides
  in-browser tools for visualizing and analyzing reference datasets. Unlike the AQS or AirNow
  API services, reference data from AirNow-Tech must be manually downloaded to the user's computer
  from the AirNow-Tech website prior to use with sensortoolkit.

If users are not acquiring reference data locally,
users should carefully consider which reference data service (AQS, AirNow, or AirNow-Tech)
is appropriate for their intended use. The list of valid query parameters for reference
measurements varies across services. The table below shows a list of SDFS parameters
alongside an indication of whether each reference data service provides data for each
parameter.

.. warning::

  **Meteorological parameters including temperature and relative humidity
  are not available from the AirNow API.**

  Numerous sensortoolkit methods including plotting functions and summary statistics
  require the availability of meteorological data (temperature and relative humidity).
  These methods are used by ``SensorEvaluation`` and ``PerformanceReport`` to indicate
  meteorological conditions at the testing site and meteorological influences on
  parameter measurements.

  If users choose to make use of the AirNow API for acquiring reference data, please
  note that functionality will be limited for methods requiring the use of meteorological
  datasets.

.. csv-table:: `Table of Reference Sources and Parameters`
  :file: ../../data/reference_sources.csv
  :align: center
  :header-rows: 1
  :widths: auto
