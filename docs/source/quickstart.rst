Quickstart Guide
================

.. contents:: Table of Contents
  :depth: 2

Sensortoolkit allows rapid and reproducible evaluation of air sensor data regardless of
data formatting or encoding and facilitates comparison against reference data from a
variety of API services or locally maintained data files. Sensor performance is determined
using performance metrics and targets recommended by U.S. EPA's documents on the testing
and evaluation of sensors measuring either fine particular matter or ozone for use in non-regulatory,
supplemental, and informational monitoring applications.

This section walks you through an example scenario, evaluating data from a fictitious air
sensor named the *'Toco Toucan'* against reference data collected from a monitor collocated at
the ambient monitoring site where sensors were deployed in triplicate, and a quick summary of 
how to use sensortoolkit for the first time.

Example Scenario - Toco Toucan
------------------------------

.. sidebar:: A Real Toco Toucan

  .. image:: data/toco_toucan.jpg

Say that you have chosen to test a sensor from the manufacturer *'Toco'* called the
*'Toucan'*. Three *Toco Toucans* were deployed at an ambient air monitoring site alongside
reference instrumentation. Let's say that the Toucan air sensor measures both PM2.5
and O3 and that you have confirmed with the agency overseeing the monitoring site
that reference-grade monitors designated either Federal Equivalent Methods (FEMs)
or Federal Reference Methods (FRMs) are situated at the monitoring site for the
pollutants you plan to measure. Following a sampling period of 30 days, you
collect data from each Toucan sensor and acquire data from the monitoring
agency for collocated reference measurements.

1 - Setting Up for sensortoolkit
--------------------------------

Setting up for sensortoolkit requires downloading Python and an IDE, creating a project directory, and
downloading your sensor and reference data. A brief run through is given below, but more information
can be found in the next section.

Download Python and IDE
"""""""""""""""""""""""

As sensortoolkit is a Python package, users will need Python(v|min_python_version| or greater) to use it.
It's highly recommended that users download `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ or
`Anaconda <https://www.anaconda.com/products/individual>`_ as both are free installers
of a simple open source environment and package manager and Python.

.. note::

  `Click here <./setup.html#download-python-and-ide>`__ for more info about installing Python with Anaconda or Miniconda.

Sensortoolkit works best in development environments that allow you to simultaneously develop scripts, view and
explore variables, and, execute code. These types of software utilities are called integrated development
environments (IDEs). One popular IDE for Python included alongside Anaconda distributions of
the coding language is the `Spyder IDE <https://www.spyder-ide.org>`__.

Create Project Directory
""""""""""""""""""""""""

You will need to decide where to store scripts, data, figures, and reports that are related
to your current project. This could be any folder location on your computer. I suggest
creating a new folder in your documents directory. Let's call this directory ``toucan_evaluation``.

Example Data Sets
"""""""""""""""""

Example data sets for the *Toco Toucan* sensors and collocated reference monitor are included in the
GitHub repository under the ``/example_datasets`` folder. Download these files to your project directory.

.. note::

  `Click here <./setup.html>`__ for more info about setting up for sensortoolkit.

2 - Analysis with sensortoolkit
-------------------------------

Open up your IDE and create a new python script. You can choose to name this file
anything you’d like, but we’ll go with ``analysis.py`` for this example.
Copy and paste the script template given `here <./template.html#script-template>`__.

Follow along the *Toco Toucan* example outlined in the
`Analysis with sensortoolkit <./template.html#initial-setup>`__ section to understand the ``analysis.py`` script
and insert relevant information. Then, this file should be saved in the project directory you created.

.. note::

  `Click here <./template.html>`__ for more info about analysis with sensortoolkit and the script template.

3 - Installing and Updating sensortoolkit
-------------------------------------------

It's highly recommended to download sensortoolkit into a suitable environment, with all the packages and versions,
from the ``stk-environment.yml`` file included in the GitHub repository under the ``/environments`` folder.
Also, sensortoolkit can be easily downloaded with pip or, if you wish to contribute to the development of the package,
cloned from the GitHub repository.

.. note::

  `Click here <./install.html>`__ for more info about installing sensortoolkit.

Sensortoolkit is actively maintained, and bug fixes and feature enhancements
are regularly added to the latest development build. **Users are strongly encouraged to update to
the latest version of sensortoolkit before using the library for analysis**. More information about
updating sensortoolkit can be found by following the link below.

.. note::

  `Click here <./install.html#updating-sensortoolkit>`__ for more info about updating sensortoolkit.

4 - Running sensortoolkit
-------------------------

Run the ``analysis.py`` script from your IDE and follow the instructions in the console to create
and compile a testing report.

For more guidance when following sensortoolkit's interactive ingestion module, please see the
`Testing Attribute Objects <./testingattrib_objects/index.html>`_ and
`Evaluation Objects <./evaluation_objects/index.html>`_ sections which
describe in greater detail importing and working with sensor and reference
data while making use of the *Toco Toucan* example to illustrate how sensortoolkit’s modules work.
