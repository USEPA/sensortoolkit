Creating Testing Reports - The PerformanceReport Class
======================================================

.. role:: raw-html(raw)
  :format: html

Creating testing reports with ``sensortoolkit.PerformanceReport`` is very similar to using
the ``sensortoolkit.SensorEvaluation`` class. Users pass the same attributes to the
``PerformanceReport`` class as they do to conduct analysis with ``SensorEvaluation``
(``PerformanceReport`` is an inherited class of ``SensorEvaluation``, which means that
its initialization creates a ``SensorEvaluation`` instance and is used to construct reports).

Note that information about the testing organization and testing location can be
populated in reports via the respective ``sensortoolkit.presets`` attributes:

.. code-block:: python

  # Fill in bracketed placeholder text with your information
  # Add information about the testing organization that conducted the evaluation
  sensortoolkit.presets.test_org = {
      'testing_descrip': '[Insert name of deployment]',
      'org_name': '[Insert organization name]',
      'org_division': '[Insert organization division]',
      'org_type': '', #not needed
      'org_website': {'title': '[Insert title of website]',
                      'link': '[Insert website link]'},
      'org_contact_email': '[Insert email]',
      'org_contact_phone': '[Insert phone number]'}

  # Add information about the testing location where sensors were sited
  sensortoolkit.presets.test_loc = {
      'site_name': '[Insert name of site] ', #strongly recommended
      'site_address': '[Insert site address]',
      'site_lat': '[Insert site latitude]',
      'site_lon': '[Insert site longitude]',
      'site_aqs_id': '[If applicable, insert site AQS ID]'} #strongly recommended, if applicable

These dictionaries house information about the testing organization, contact information,
and site details including the address, coordinates, and site AQS ID if applicable.

``testing_org``
~~~~~~~~~~~~~~~

A dictionary containing the information about the testing organization.

.. list-table:: ``testing_org`` Attributes
  :widths: 50 75
  :header-rows: 1

  * - Attribute name
    - Description
  * - ``testing_descrip``
    - The descriptive name assigned to the sensor deployment.
  * - ``org_name``
    - The name of the testing organization.
  * - ``org_division``
    - The organization testing division.
  * - ``org_type``
    - The organization sector type.
  * - ``org_website``
    - Website title and address for the testing organization.
  * - ``org_contact_email``
    - Contact email address responsible parties conducting testing.
  * - ``org_contact_phone``
    - Phone number for responsible parties conducting testing.

``testing_loc``
~~~~~~~~~~~~~~~

A dictionary containing information about the testing site. If the site is part
of U.S. EPA's Air Quality System (AQS), the AQS Site ID should be specified.

.. list-table:: ``testing_org`` Attributes
  :widths: 50 75
  :header-rows: 1

  * - Attribute name
    - Description
  * - ``site_name``
    - The name of the ambient monitoring site.
  * - ``site_address``
    - The street address of the monitoring site.
  * - ``site_lat``
    - The latitude coordinate of the site.
  * - ``site_lon``
    - The longitude coordinate of the site.
  * - ``site_aqs_id``
    - [AQS Sites Only] The AQS site code assigned to the ambient monitoring site.


Below is an example of running the `PerformanceReport` class to create a testing
report for the ``Toco_Toucan`` sensor evaluating its :raw-html:`PM<sub>2.5</sub>` performance.

.. code-block:: python

  # Instantiate the PerformanceReport class for the example sensor dataset
  report = sensortoolkit.PerformanceReport(sensor,
                                           pollutant,
                                           reference,
                                           write_to_file=True,
                                           figure_search=False)

  # Compile the report and save the file to the reports subfolder
  report.CreateReport()

Arguments passed to ``PerformanceReport``
-----------------------------------------

.. list-table:: ``sensortoolkit.PerformanceReport()`` attributes
  :widths: 50 75
  :header-rows: 1

  * - Attribute name
    - Description
  * - ``sensor``
    - A ``sensortoolkit.AirSensor`` object.
  * - ``param``
    - A ``sensortoolkit.Parameter`` object.
  * - ``reference``
    - A ``sensortoolkit.ReferenceMonitor`` object.
  * - ``write_to_file``
    - If true, evaluation statistics are saved to ``/data/eval_stats/[name of sensor]`` |br|
      and figures are written to ``/figures/[name of sensor]``.
  * - ``figure_search``
    - If true, PerformanceReport will search for figures in the ``/figures`` |br|
      directory before attempting to create new figures. If false, |br|
      PerformanceReport will create all new figures (may risk overwriting |br|
      existing figures). Defaults to False.

Console Output
~~~~~~~~~~~~~~

When the above code block is run (including both instantiation of the ``PerformanceReport``
object ``report`` and running the ``PerformanceReport.create_report()`` method),
the following will be printed to the console.

.. code-block:: console

  Computing normalized PM25 values (by Teledyne Advanced Pollution Instrumentation T640X)
  Computing normalized PM25 values (by Teledyne Advanced Pollution Instrumentation T640X)
  Computing mean parameter values across concurrent sensor datasets
  Computing mean parameter values across concurrent sensor datasets
  Populating deployment dataframe with evaluation statistics
  Computing CV for 1-Hour averaged PM25
  ..N excluded: 20 out of 733 total
  ..N concurrent: 713
  ..Concurrent measurement timeframe: 2019-08-01 12:00:00+00:00 - 2019-09-01 00:00:00+00:00
  Computing CV for 24-Hour averaged PM25
  ..N excluded: 3 out of 32 total
  ..N concurrent: 29
  ..Concurrent measurement timeframe: 2019-08-02 00:00:00+00:00 - 2019-08-31 00:00:00+00:00
  Computing 1-hour regression statistics for Toco_Toucan vs. Teledyne Advanced Pollution Instrumentation T640X
  ..RT01
  ..RT02
  ..RT03
  Computing 1-hour regression statistics for Toco_Toucan vs. Teledyne Advanced Pollution Instrumentation T640X
  ..RT01
  ..RT02
  ..RT03
  Computing 24-hour regression statistics for Toco_Toucan vs. Teledyne Advanced Pollution Instrumentation T640X
  ..RT01
  ..RT02
  ..RT03
  Computing 24-hour regression statistics for Toco_Toucan vs. Teledyne Advanced Pollution Instrumentation T640X
  ..RT01
  ..RT02
  ..RT03
  ..Saving dataset to the following path: C:/Users/.../Documents/toucan_evaluation\data\eval_stats\Toco_Toucan\Toco_Toucan_PM25_vs_Teledyne_Advanced_Pollution_Instrumentation_T640X_stats_df_230209.csv
  ..Saving dataset to the following path: C:/Users/.../Documents/toucan_evaluation\data\eval_stats\Toco_Toucan\Toco_Toucan_PM25_vs_Teledyne_Advanced_Pollution_Instrumentation_T640X_avg_stats_df_230209.csv
  Creating Testing Report for Toco_Toucan
  ..Adding figures to report
  ..creating subplot for 1 sensor with 1 row and 1 column
  ..creating subplot for 1 sensor with 1 row and 1 column
  ..Adding tabular data
  [Note]: PM25 values below the Federal MDL (0.1 Micrograms per Cubic Meter) are not shown
    Computing normalized PM25 values (by FEM)
  [Note]: PM25 values below the Federal MDL (0.1 Micrograms per Cubic Meter) are not shown
    Computing normalized PM25 values (by FEM)
  ..creating subplot for 3 sensors with 1 row and 3 columns
  ..creating subplot for 3 sensors with 1 row and 3 columns
  ..Saving report
  ....\reports\Toco_Toucan\PM25\Base_Testing_Report_PM25_Toco_Toucan_230209.pptx

.. note::

   Reports are saved within the ``/reports`` folder, which is located inside the
   directory pointed to by the project path.

Example Report
--------------

Below is an example report for the ``Toco_Toucan`` sensor.

.. note::

   Sensortoolkit converts time to the UTC timezone. Graphs displayed in the report
   are in UTC.

Please note that at present, ``PerformanceReport`` does not populate the FRM/FEM
Instrumentation table with calibration dates, flowrate verification checks, and
any description of maintenance activities conducted on the reference instrumentation.
Users must either insert these details manually by placing information in the
provided table, or by appending documentation to the end of the report and noting on
the supplemental information page that addition documentation has been attached.

.. tabbed:: Page 1 - Testing Summary

  The first page of the testing report allows testers to insert information about their
  organization including contact information, and testers are also encouraged to
  provide details about the sensor and FRM/FEM instrumentation used for testing.

  Various plots generated via the ``PerformanceReport`` class are displayed below
  information about the deployment. These figures provide indication of the sensor's
  performance during the testing period, site conditions including temperature and
  relative humidity, and meteorological influences that may be present in sensor data.

  .. figure:: ../data/performance_report_example_pg1_v2.png
     :align: center
     :alt: The first page of the performance report. This page features tables for listing details about the testing organization, site information, sensor information, and FRM/FEM information. Below these tables are a number of figures, including timeseries and scatter plots at 1-hour and 24-hour averages indicating the agreement between the sensor and FRM/FEM. Below these plots is a figure displaying the results of the sensor against EPA's recommended performance metrics and target values for evaluating air sensor performance. Below this figure is a final row displaying the meteorological conditions during the deployment (temperature and relative humidity) and the influence of these meteorological parameters on sensor measurements.

     Toco Toucan Base Testing Report (Page 1)

.. tabbed:: Page 2 - Tabular Statistics

  The second page of the report includes tabular statistics, such as the performance
  metric values characterizing sensor vs. FRM/FEM accuracy (bias and linearity),
  error, and sensor-sensor (intersensor) precision.

  .. figure:: ../data/performance_report_example_pg2_v2.png
    :align: center
    :alt: The second page of the performance report. Tabular statistics are listed for the sensor vs. FRM/FEM correlation, indicating individual sensor unit regression statistics (coefficient of determination, slope, intercept) and data quality (the uptime percentage and number of paired sensor and FRM/FEM concentration pairs). Also in the sensor vs. FRM/FEM correlation section is a table containing error metric values (RMSE and NRMSE). Below is a section for inter-sensor precision (sensor vs. sensor). A table in this section indicates the precision metric values including CV and SD, and data quality (uptime and the number of paired hourly measurement periods that all sensors were concurrently recording alongside the reference monitor).

    Toco Toucan Base Testing Report (Page 2)

.. tabbed:: Page 3 - Sensor vs. FRM/FEM Scatter

  Scatter plots for each sensor unit vs. FRM/FEM measurement pairs are displayed
  on a third page of the report.

  .. figure:: ../data/performance_report_example_pg3_v2.png
     :align: center
     :alt: The third page of the performance report. This page includes sensor vs. FRM/FEM scatter plots for each sensor in the testing group at both 1-hour and 24-hour averages. Data pairs are colored by the relative humidity recorded by an independent monitor at the testing site to indicate whether humidity biases sensor measurements.

     Toco Toucan Base Testing Report (Page 3)

.. tabbed:: Page 4 - Supplemental Information

  .. figure:: ../data/performance_report_example_pg4_v2.png
     :align: center
     :alt: The fourth page of the performance report. This page includes a table listing various documents, reports, and observations that testers may wish to attached to the report. Entries are provided to indicate whether a particular type of documentation has been attached and a description of the URL or file path to the documentation.

     Toco Toucan Base Testing Report (Page 4)



.. |br| raw:: html

 <br />
