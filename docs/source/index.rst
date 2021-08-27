=============
sensortoolkit
=============

.. important::

    This documentation is currently under development. Please check for
    updates to the BitBucket repository before referencing the documentation.

`sensortoolkit` is a Python library for evaluating air sensor data. The library
is intended for use with sensors collocated at ambient air monitoring sites
alongside FRM/FEM monitors for comparison and analysis of sensor data against
reference-grade data.

`sensortoolkit` can be used to evaluate sensor data for a single or multiple
sensors measuring one of the following pollutants:
:math:`PM_1, PM_{2.5}, PM_{10}, CO, CO_2, NO, NO_2, NO_x, O_3, SO_2, SO_x`.

U.S. EPA's Performance Targets Reports
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In February 2021, U.S. EPA released two reports outlining recommended performance
testing protocols, metrics, and target values for fine particulate matter (:math:`PM_{2.5}`)
and ozone (:math:`O_3`) air sensors used in
non-regulatory, supplemental, and informational monitoring (NSIM) applications.

.. sidebar:: Links to U.S. EPA's Reports

  * `Fine Particulate Matter Report <https://cfpub.epa.gov/si/si_public_record_Report.cfm?dirEntryId=350785&Lab=CEMM>`_
  * `Ozone Report <https://cfpub.epa.gov/si/si_public_record_Report.cfm?dirEntryId=350784&Lab=CEMM>`_

The sensortoolkit library includes numerous modules for computing performance metrics recommended by
U.S. EPA for evaluating  :math:`PM_{2.5}` and ozone (:math:`O_3`) sensors. Additionally,
plotting functions are included for visualizing performance evaluation results, including
visualization of sensor performance metric values against U.S. EPA's performance targets,
sensor time series, scatter plots comparing collocated sensor and reference measurements,
distribution plots for displaying the range of meteorlogical conditions during the
deployment, etc. Tabular statistics and figures can be automatically compiled into
testing reports recommended by U.S. EPA's performance targets documents for testing
conducting at ambient air monitoring sites.

.. note::

    Presently, evaluation of sensor performance with sensortoolkit using
    U.S. EPA’s recommended performance metrics and target values is limited to
    :math:`PM_{2.5}` and :math:`O_3`.

FRM/FEM data may not be available at all testing sites for non-criteria
pollutants (PM1, CO2, NO, NOx, SOx). Testers should ensure that sensors are
collocated alongside reference instrumentation capable of reporting 1-hour and/or
24-hour concentration values for evaluation parameters of interest.

.. toctree::
    :caption: User Guide
    :titlesonly:

    install
    import_sensortoolkit
    setup
    sensoreval
    datastructures
    performancereport

.. toctree::
    :hidden:
    :caption: API Documentation
    :titlesonly:

    api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
