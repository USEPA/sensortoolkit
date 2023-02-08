Analysis with sensortoolkit
===========================

This guide provides a brief overview of how to use the sensortoolkit library, including
primary functions and methods that are essential to making the most out of the library.
We will walk through the ``analysis.py`` script in evaluating data from a fictitious air sensor
named the ‘*Toco Toucan*’ explained in the `Quickstart Guide <./quickstart.html#id2>`_.

.. note::

  `Click here <./template.html#script-template>`__ to be brought to the full script template at the bottom of this page.

Create the Analysis Script
--------------------------

Open up your IDE and create a new python script. You can choose to name this
file anything you’d like, but we’ll go with ``analysis.py`` for this example.
This file should be saved in the project folder you created.

Copy and paste the script template provided at the bottom of this page
into ``analysis.py``. Text in brackets indicates where you should enter
information relevant to your evaluation. Don't forget to save afterward!

You can follow along the *Toco Toucan* example outlined below. In addition, other sections
in this documentation, including the `Testing Attribute Objects <./testingattrib_objects/index.html>`_
and `Evaluation Objects <./evaluation_objects/index.html>`_ sections, take a deeper dive into
importing and working with sensor and reference data and make use of the example datasets to
illustrate how sensortoolkit’s modules work.

Initial Setup
-------------

1 - Calling sensortoolkit from Scripts
""""""""""""""""""""""""""""""""""""""

Within your ``analysis.py`` script, import the sensortoolkit library

.. code-block:: python

  import sensortoolkit

2 - Setting the Project Path and Testing Attributes
"""""""""""""""""""""""""""""""""""""""""""""""""""

Next, you need to tell sensortoolkit where on your computer you are conducting your evaluation.
This is our ``toucan_evaluation`` folder, and the full path to that folder is referred to as the "project path".
Set the project path using the following function

.. code-block:: python

  # Configure the project directory where data, figures, etc. will be stored
  sensortoolkit.presets.set_project_path('[Insert project path]')

Once you've set the project path, add information about the testing organization and
location where the sensors were deployed. Inputting this information is optional
but is helpful in attributing the evaluation to the responsible party in meta data
files that are generated during analysis.

.. tip::

  It is strongly recommended to input information for the ``site_name`` and ``site_aqs_id``, if applicable, as these are used to name files and directories created by sensortoolkit in other functions.

.. code-block:: python

  # Add information about the testing organization that conducted the evaluation
  sensortoolkit.presets.test_org = {
      'testing_descrip': '[Insert name of deployment]',
      'org_name': '[Insert organization name]',
      'org_division': '[Insert organization division]',
      'org_type': '[Insert organization sector type]',
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

3 - Creating an AirSensor Object
""""""""""""""""""""""""""""""""

The next step is to create an object for our *Toco Toucan* sensor that will store all
the data sets and related attributes for our analysis. This is done by calling the
``sensortoolkit.AirSensor`` method:

.. code-block:: python

  # Create an AirSensor instance for the sensor you'd like to evaluate
  sensor = sensortoolkit.AirSensor(make='Toco',
                                   model='Toucan')

This creates an instance of ``sensortoolkit.AirSensor`` called ``sensor``.
Currently, the ``sensor`` object doesn't have many attributes since we've only specified
the make and model for the sensor, however, we will use ``sensor`` to continue the setup process
and eventually load sensor data.

.. note::

  More information about ``sensortoolkit.AirSensor`` is found `here <./testingattrib_objects/airsensor/index.html>`__

4 - Constructing Project Directories
""""""""""""""""""""""""""""""""""""

Next, we need to create a directory system of folders within our project path that
will house data sets, figures, reports, etc. To do so, use the ``create_directories()`` function
included alongside your ``sensor`` object. You will see a list of directories be printed to
the console that are created by the module.

.. code-block:: python

  # Construct sensor-specific directories in the project path for data, figures, etc.
  sensor.create_directories()

Below is the console output for ``create_directories()``:

.. code-block:: console

  Creating "data" subdirectory within C:\Users\...\Documents\toucan_evaluation
  ..\data\eval_stats
  ....\data\eval_stats\Toco_Toucan
  ..\data\reference_data
  ....\data\reference_data\airnow
  ......\data\reference_data\airnow\raw
  ......\data\reference_data\airnow\processed
  ....\data\reference_data\airnowtech
  ......\data\reference_data\airnowtech\raw
  ......\data\reference_data\airnowtech\processed
  ....\data\reference_data\aqs
  ......\data\reference_data\aqs\raw
  ......\data\reference_data\aqs\processed
  ..\data\sensor_data
  ....\data\sensor_data\Toco_Toucan
  ......\data\sensor_data\Toco_Toucan\processed_data
  ......\data\sensor_data\Toco_Toucan\raw_data

  Creating "figures" subdirectory within C:\Users\...\Documents\toucan_evaluation
  ..\figures\Toco_Toucan

  Creating "reports" subdirectory within C:\Users\...\Documents\toucan_evaluation

5 - Configuring the Sensor Setup
""""""""""""""""""""""""""""""""

Now we're ready to tell sensortoolkit how data from the *Toco Toucan* sensors should
be imported based on the formatting scheme for the recorded data sets. The ``sensor_setup()``
function included alongside your ``sensor`` object walks you through the process of transferring
data sets to the right location within the project path and asks you to indicate various attributes
regarding the recorded datasets in order to build a profile of the *Toco Toucan* sensor formatting.

.. code-block:: python

  # Run the interactive setup routine for specifying how to ingest sensor data
  sensor.sensor_setup()

6 - Importing Sensor Data
"""""""""""""""""""""""""

Following completion of the setup module, we can load the *Toco Toucan* data sets to the
``sensor`` object so that we have access to the data sets for analysis. The ``load_data()``
function included alongside your ``sensor`` object imports recorded datasets and processes
these into a standardized format for subsequent analysis:

.. code-block:: python

  # Import sensor data sets and save processed data sets to the data folder
  sensor.load_data(load_raw_data=True,
                   write_to_file=True)

We've now completed the setup procedure for the *Toco Toucan* sensors!

7 - Creating an ReferenceMonitor Object
"""""""""""""""""""""""""""""""""""""""

We will now follow a similar process for the reference monitor collocated alongside
the *Toco Toucan* sensors at the monitoring site. First, create an object for the
reference monitor by calling the ``sensortoolkit.ReferenceMonitor`` method:

.. code-block:: python

  # Create a ReferenceMonitor instance for FRM/FEM monitor collocated alongside sensors
  reference = sensortoolkit.ReferenceMonitor()

This creates an instance of ``sensortoolkit.ReferenceMonitor`` called ``reference``.

.. note::

  More information about ``sensortoolkit.ReferenceMonitor`` is found `here <./testingattrib_objects/referencemonitor/index.html>`__

8 - Configuring the Reference Setup
"""""""""""""""""""""""""""""""""""

As with the *Toco Toucan* sensor data sets, we need to give sensortoolkit an indication of the
location of reference monitor datasets and data formatting in order to import and utilize
these data sets. This is accomplished via the ``reference_setup()`` function which is included
alongside your ``reference`` object.

.. code-block:: python

  # Run the interactive setup routine for specifying how to ingest reference data
  reference.reference_setup()

9 - Importing Reference Data
""""""""""""""""""""""""""""

Reference data are imported via the ``load_data()`` function included alongside your ``reference``
object. If you intend to query data from either the AirNow or AQS API, please see
`Loading Reference Data <./testingattrib_objects/referencemonitor/load_data.html>`__ for more information.

.. code-block:: python

  # Import reference data for parameter types measured by the air sensor, also
  # import meteorological data if instruments collocated at monitoring site
  reference.load_data(bdate=sensor.bdate,
                      edate=sensor.edate,
                      param_list=sensor.param_headers,
                      met_data=True)

10 - Creating a Parameter Object
""""""""""""""""""""""""""""""""

The final component we need to specify is which environmental parameter or pollutant
measured by the *Toco Toucan* air sensor that we wish to evaluate against collocated reference
measurements. We will evaluate the performance of the Toucan sensor for measuring PM2.5. Like the
``sensortoolkit.AirSensor`` and ``sensortoolkit.ReferenceMonitor`` methods that we used to create
objects for the sensor and reference monitor included in our evaluation, we will create an object
for the evaluation parameter PM2.5 via the ``sensortoolkit.Parameter`` method.

.. code-block:: python

  # Create a Parameter instance for the pollutant you wish to evaluate
  # Select pollutant name from list of SDFS labels
  pollutant = sensortoolkit.Parameter('PM25')

.. note::

  More information about ``sensortoolkit.Parameter`` is found `here <./testingattrib_objects/parameter.html>`__

.. caution::

  Note that the label ``PM25`` that we've passed to ``sensortoolkit.Parameter`` is not arbitrary! This label
  is included in a list of parameter labels recognized by sensortoolkit as potential evaluation parameters. A
  full list is available under the `sensortoolkit Data Formatting Scheme Page <./sdfs/index.html#id1>`_.

----

Evaluating Air Sensor Data
--------------------------

Now that we've completed the initial setup process for the *Toco Toucan* sensor and
collocated reference monitor, we are ready to test out sensortoolkit's evaluation
modules. Use of these modules can be divided into one of two categories, allowing either
data analysis within an IDE or the generation of performance evaluation reports.

Data Analysis with SensorEvaluation
"""""""""""""""""""""""""""""""""""

``SensorEvaluation`` provides a platform for analyzing air sensor data against
regulatory grade measurements. With ``SensorEvaluation``, users can compute
various quantities and metrics recommended by U.S. EPA’s performance
targets reports including precision, error, linearity, and bias. ``SensorEvaluation`` also
contains numerous plotting methods for displaying and saving figures for
time series, sensor vs. reference scatter, meteorological conditions, etc.

.. code-block:: python

  # Run the evaluation
  evaluation = sensortoolkit.SensorEvaluation(sensor,
                                              pollutant,
                                              reference,
                                              write_to_file=True)

.. note::

  More information about ``sensortoolkit.SensorEvaluation`` is found `here <./evaluation_objects/sensoreval/index.html>`__

Creating Reports with PerformanceReport
"""""""""""""""""""""""""""""""""""""""

``PerformanceReport`` leverages many of the functions included in ``SensorEvaluation``
to automate the process of creating and compiling testing reports. These reports
provide a detailed overview of the testing site and conditions, summarize sensor performance
via EPA's recommended performance metrics and target values, and display results by way of time series
figures, scatter plots, and tabular statistics.

.. code-block:: python

  # Create a performance evaluation report for the sensor
  report = sensortoolkit.PerformanceReport(sensor,
                                           pollutant,
                                           reference,
                                           write_to_file=True)

  # Generate report
  report.CreateReport()

.. note::

  More information about ``sensortoolkit.PerformanceReport`` is found `here <./evaluation_objects/performancereport.html>`__

------

Script Template
================

Below is the template that you can use to get started with sensortoolkit. This
can be copied directly from the documentation into your IDE of choice.

.. note::

  Text in brackets indicates where you should enter information relevant to your evaluation.

.. code-block:: python

  ## ---------------------------- INITIAL SETUP ---------------------------- ##

  # Ensure the latest version of sensortoolkit is downloaded
  import sensortoolkit

  # Configure the project directory where data, figures, etc. will be stored
  sensortoolkit.presets.set_project_path('[Insert project path]')

  # Add information about the testing organization that conducted the evaluation
  sensortoolkit.presets.test_org = {
      'testing_descrip': '[Insert name of deployment]',
      'org_name': '[Insert organization name]',
      'org_division': '[Insert organization division]',
      'org_type': '[Insert organization sector type]',
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

  # --------------------------------- SENSOR --------------------------------- #

  # Create an AirSensor instance for the sensor you'd like to evaluate
  sensor = sensortoolkit.AirSensor(make='[Insert sensor manufacturer]',
                                   model='[Insert sensor model]')

  # Construct sensor-specific directories in the project path for data, figures, etc.
  sensor.create_directories()

  # Run the interactive setup routine for specifying how to ingest sensor data
  sensor.sensor_setup()

  # Import sensor datasets and save processed datasets to the data folder
  sensor.load_data(load_raw_data=True,
                   write_to_file=True)

  # ------------------------------- REFERENCE ------------------------------- #

  # Create a ReferenceMonitor instance for FRM/FEM monitor collocated alongside sensors
  reference = sensortoolkit.ReferenceMonitor()

  # Run the interactive setup routine for specifying how to ingest reference data
  reference.reference_setup()

  # Import reference data for parameter types measured by the air sensor, also
  # import meteorological data if instruments collocated at monitoring site
  reference.load_data(bdate=sensor.bdate,
                      edate=sensor.edate,
                      param_list=sensor.param_headers,
                      met_data=True)

  # ------------------------------- PARAMETER ------------------------------- #

  # Create a Parameter instance for the pollutant you wish to evaluate
  pollutant = sensortoolkit.Parameter('[Insert pollutant from list of SDFS labels]')

  ## -------------------------- EVALUATION OBJECTS -------------------------- ##
  # ------------------------------- EVALUATION ------------------------------- #

  # Run the evaluation
  evaluation = sensortoolkit.SensorEvaluation(sensor,
                                              pollutant,
                                              reference,
                                              write_to_file=True)

  # --------------------------------- REPORT --------------------------------- #

  # Create a performance evaluation report for the sensor
  report = sensortoolkit.PerformanceReport(sensor,
                                          pollutant,
                                          reference,
                                          write_to_file=True)

  # Generate report
  report.CreateReport()
