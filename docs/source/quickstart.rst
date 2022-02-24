****************
Quickstart Guide
****************

.. contents:: Table of Contents
  :depth: 3

Sensortoolkit allows rapid and reproducible evaluation of air sensor data regardless of
data formatting or encoding and facilitates comparison against reference data from a
variety of API services or locally maintained data files. Sensor performance is determined
using performance metrics and targets recommended by U.S. EPA's documents on the testing
and evaluation of sensors measuring either fine particular matter or ozone for use in non-regulatory,
supplemental, and informational monitoring applications.

This guide provides a brief overview of how to use the sensortoolkit library, including
primary functions and methods that are essential to making the most out of the library.
The guide walks you through a example scenario, evaluating data from a fictitious air sensor named the
*'Toco Toucan'* against reference data collected from a monitor collocated at the ambient monitoring
site where sensors were deployed in triplicate.

.. note::

  Script templates are provided at the end of this guide, recapping functions you
  will need for setting up analyses, conducting evaluations, and creating reports.
  `Click here <./quickstart.html#templates>`_ to jump to the templates section.


Installing and Updating sensortoolkit
=====================================

sensortoolkit can be easily downloaded with ``pip``, or if you wish to contribute to the
development of the package, you can clone the GitHub repository.

.. tip::

  `Click here <./install.html#installation>`_ for more info about installing sensortoolkit.

Sensortoolkit is actively maintained, and bug fixes and feature enhancements
are regularly added to the latest development build. **Users are strongly encouraged to update to
the latest version of sensortoolkit before using the library for analysis**. More information about
updating sensortoolkit can be found by following the link below.

.. tip::

  `Click here <./install.html#updating-sensortoolkit>`_ for more info about updating sensortoolkit.


Example Scenario - *Toco Toucan*
================================

.. sidebar:: A Real Toco Toucan

  .. image:: data/toco_toucan.jpg

Say that you have chosen to test a sensor from the manufacturer *'Toco'* called the
*'Toucan'*. Three Toco Toucans were deployed at an ambient air monitoring site alongside
reference instrumentation. Let's say that the Toucan air sensor measures both PM2.5 and O3 and that you have confirmed
with the agency overseeing the monitoring site that reference-grade monitors
designated either Federal Equivalent Methods (FEMs) or Federal Reference Methods (FRMs) are situated at the
monitoring site for the pollutants you plan to measure.
Following a sampling period of 30 days, you collect data from each Toucan sensor and acquire data
from the monitoring agency for collocated reference measurements.

Example Data Sets
-----------------

Example data sets for the Toco Toucan sensor and collocated reference monitor are included in the
GitHub repository under the ``/example_datasets`` folder. You can download these files
and follow along the example outlined here in the Quickstart guide. In addition, other sections in
this documentation, including the "Testing Attribute Objects" and "Evaluation Objects" sections,
take a deeper dive into importing and working with sensor and reference data and make use of the example
datasets to illustrate how sensortoolkit's modules work.

Initial Setup
-------------

1 - Create a Project Directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first decision you will need to make in using sensortoolkit is where to store scripts,
data, figures, and reports that are related to your current project. This could be any folder
location on your computer. I suggest creating a new folder in your documents directory. Let's
call this directory ``toucan_evaluation``.

2 - Calling sensortoolkit from Scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

sensortoolkit works best in development environments that allow you to simultaneously develop
scripts, view and explore variables, and execute code. These types of software utilities
are called integrated development environments (IDEs). One popular IDE for python included
alongside Anaconda distributions of the coding language is Spyder.

Open up your IDE and create a new python script. You can choose to name this file anything
you'd like, but we'll go with ``analysis.py`` for this example. This file should be saved
in the folder you created, so following from above, we now have a single file called ``analysis.py``
in the ``toucan_evaluation`` directory.

Next, within your ``analysis.py`` script, import the sensortoolkit library

.. code-block:: python

  import sensortoolkit

3 - Setting the Project Path and Testing Attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, you need to tell sensortoolkit where on your computer you are conducting your evaluation.
This is our ``toucan_evaluation`` folder, and the full path to that folder is referred to as the "project path".
Set the project path using the following function

.. code-block:: python

  # Configure the project directory where data, figures, etc. will be stored
  sensortoolkit.presets.set_project_path()

Once you've set the project path, add information about the testing organization and
location where the sensors were deployed. Inputting this information is optional
but is helpful in attributing the evaluation to the responsible party in meta data
files that are generated during analysis.

.. code-block:: python

  # Add information about the testing organization that conducted the evaluation
  sensortoolkit.presets.test_org = {
      'Deployment name': '[Insert name of deployment]',
      'Org name': ['[Insert organization name line 1]',
                   '[Insert organization name line 2]'],
      'Website': {'website name': '[Insert name of website]',
                  'website link': '[Insert website here]'},
      'Contact email': '[Insert email here]',
      'Contact phone': '[Insert phone number here]'}

  # Add information about the testing location where sensors were sited
  sensortoolkit.presets.test_loc = {
      'Site name': '[Insert name of site] ',
      'Site address': '[Insert site address]',
      'Site lat': '[Insert site latitude]',
      'Site long': '[Insert site longitude]',
      'Site AQS ID': '[If applicable, insert site AQS ID]'}

4 - Creating an AirSensor Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The next step is to create an object for our Toco Toucan sensor that will store all
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

.. tip::

  More information about ``sensortoolkit.AirSensor`` is found `here <./testingattrib_objects/airsensor/index.html>`_


5 - Constructing Project Directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

6 - Configuring the Sensor Setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now we're ready to tell sensortoolkit how data from the Toco Toucan sensors should
be imported based on the formatting scheme for the recorded data sets. The ``sensor_setup()``
function included alongside your ``sensor`` object walks you through the process of transferring
data sets to the right location within the project path and asks you to indicate various attributes
regarding the recorded datasets in order to build a profile of the Toco Toucan sensor formatting.

.. code-block:: python

  # Run the interative setup routine for specifying how to ingest sensor data
  sensor.sensor_setup()

7 - Importing Sensor Data
^^^^^^^^^^^^^^^^^^^^^^^^^

Following completion of the setup module, we can load the Toco Toucan data sets to the
``sensor`` object so that we have access to the data sets for analysis. The ``load_data()``
function included alongside your ``sensor`` object imports recorded datasets and processes
these into a standardized format for subsequent analysis:

.. code-block:: python

  # Import sensor data sets and save processed data sets to the data folder
  sensor.load_data(load_raw_data=True,
                   write_to_file=True)

We've now completed the setup procedure for the Toco Toucan sensors!

8 - Creating an ReferenceMonitor Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We will now follow a similar process for the reference monitor collocated alongside
the Toco Toucan sensors at the monitoring site. First, create an object for the
reference monitor by calling the ``sensortoolkit.ReferenceMonitor`` method:

.. code-block:: python

  # Create a ReferenceMonitor instance for FRM/FEM monitor collocated alongside sensors
  reference = sensortoolkit.ReferenceMonitor()

This creates an instance of ``sensortoolkit.ReferenceMonitor`` called ``reference``.

.. tip::

  More information about ``sensortoolkit.ReferenceMonitor`` is found `here <./testingattrib_objects/referencemonitor/index.html>`_

9 - Configuring the Reference Setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As with the Toco Toucan sensor data sets, we need to give sensortoolkit an indication of the
location of reference monitor datasets and data formatting in order to import and utilize
these data sets. This is accomplished via the ``reference_setup()`` function which is included
alongside your ``reference`` object.

.. code-block:: python

  # Run the interactive setup routine for specifying how to ingest reference data
  reference.reference_setup()

10 - Importing Reference Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Reference data are imported via the ``load_data()`` function included alongside your ``reference``
object. If you intend to query data from either the AirNow or AQS API, please see
`Loading Reference Data <./testingattrib_objects/referencemonitor/load_data.html>`_ for more information.

.. code-block:: python

  # Import reference data for parameter types measured by the air sensor, also
  # import meteorological data if instruments collocated at monitoring site
  reference.load_data(bdate=sensor.bdate,
                      edate=sensor.edate,
                      param_list=sensor.param_headers,
                      met_data=True)

11 - Creating a Parameter Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The final component we need to specify is which environmental parameter or pollutant
measured by the Toco Toucan air sensor that we wish to evaluate against collocated reference
measurements. We will evaluate the performance of the Toucan sensor for measuring PM2.5. Like the
``sensortoolkit.AirSensor`` and ``sensortoolkit.ReferenceMonitor`` methods that we used to create
objects for the sensor and reference monitor included in our evaluation, we will create an object
for the evaluation parameter PM2.5 via the ``sensortoolkit.Parameter`` method.

.. code-block:: python

  # Create a Parameter instance for the pollutant you wish to evaluate
  # Select pollutant name from list of SDFS labels
  pollutant = sensortoolkit.Parameter('PM25')

.. tip::

  More information about ``sensortoolkit.Parameter`` is found `here <./testingattrib_objects/parameter.html>`_

.. caution::

  Note that the label ``PM25`` that we've passed to ``sensortoolkit.Parameter`` is not arbitrary! This label
  is included in a list of parameter labels recognized by sensortoolkit as potential evaluation parameters. A
  full list is available under the `sensortoolkit Data Formatting Scheme Page <./sdfs/index.html#id1>`_.

----

Evaluating Air Sensor Data
--------------------------

Now that we've completed the initial setup process for the Toco Toucan sensor and
collocated reference monitor, we are ready to test out sensortoolkit's evaluation
modules. Use of these modules can be divided into one of two categories, allowing either
data analysis within an IDE or the generation of performance evaluation reports.

Data Analysis with SensorEvaluation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

.. tip::

  More information about ``sensortoolkit.SensorEvaluation`` is found `here <./evaluation_objects/sensoreval/index.html>`_

Creating Reports with PerformanceReport
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

.. tip::

  More information about ``sensortoolkit.PerformanceReport`` is found `here <./evaluation_objects/performancereport.html>`_

------

Templates
=========

Below are templates that you can use to get started with sensortoolkit. These
can be copied directly from the documentation into your IDE of choice.

.. note::

  Text in brackets indicates where you should enter information relevant to your evaluation.


Initial Setup
-------------

This template summarizes the 'Initial Setup' process discussed above.

.. code-block:: python

  import sensortoolkit

  # Configure the project directory where data, figures, etc. will be stored
  sensortoolkit.presets.set_project_path()

  # Add information about the testing organization that conducted the evaluation
  sensortoolkit.presets.test_org = {
      'Deployment name': '[Insert name of deployment]',
      'Org name': ['[Insert organization name line 1]',
                   '[Insert organization name line 2]'],
      'Website': {'website name': '[Insert name of website]',
                  'website link': '[Insert website here]'},
      'Contact email': '[Insert email here]',
      'Contact phone': '[Insert phone number here]'}

  # Add information about the testing location where sensors were sited
  sensortoolkit.presets.test_loc = {
      'Site name': '[Insert name of site] ',
      'Site address': '[Insert site address]',
      'Site lat': '[Insert site latitude]',
      'Site long': '[Insert site longitude]',
      'Site AQS ID': '[If applicable, insert site AQS ID]'}

  # Create an AirSensor instance for the sensor you'd like to evaluate
  sensor = sensortoolkit.AirSensor(make='[Insert sensor manufacturer]',
                                   model='[Insert sensor model]')

  # Construct sensor-specific directories in the project path for data, figures, etc.
  sensor.create_directories()

  # Run the interative setup routine for specifying how to ingest sensor data
  sensor.sensor_setup()

  # Import sensor datasets and save processed datasets to the data folder
  sensor.load_data(load_raw_data=True,
                   write_to_file=True)

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

  # Create a Parameter instance for the pollutant you wish to evaluate
  pollutant = sensortoolkit.Parameter('[Insert pollutant from list of SDFS labels]')

Evaluation Objects
------------------

.. tabbed:: SensorEvaluation

  .. code-block:: python

    # Run the evaluation
    evaluation = sensortoolkit.SensorEvaluation(sensor,
                                                pollutant,
                                                reference,
                                                write_to_file=True)

.. tabbed:: PerformanceReport

  .. code-block:: python

    # Create a performance evaluation report for the sensor
    report = sensortoolkit.PerformanceReport(sensor,
                                             pollutant,
                                             reference,
                                             write_to_file=True)

    # Generate report
    report.CreateReport()
