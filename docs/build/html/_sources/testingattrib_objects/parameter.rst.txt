The Parameter Object
====================

.. role:: raw-html(raw)
   :format: html


This section provides a brief overview of the Parameter object. For more detailed documentation, please see
`API documentation for sensortoolkit.parameter <../api/_autosummary/sensortoolkit.param._parameter.Parameter.html>`_.

Overview
--------

The parameter object is used to keep track of attributes pertaining to the parameter or
pollutant for which sensor data are being evaluated. The table below describes in detail
the attributes contained within a parameter instance, and the Parameter class comes with
numerous pre-configured parameters (including all criteria pollutants).

.. tip::
  A full list of pre-configured parameters, including all criteria pollutants and
  meteorological parameters such as temperature, relative humidity, etc. can be
  accessed via:

  .. code-block:: python

    sensortoolkit.Parameter.__param_dict__.keys()

For example, a Parameter instance called ``pollutant`` can be created for the pollutant :raw-html:`PM<sub>2.5</sub>`
by specifying the SDFS parameter name ``PM25``:

.. code-block:: python

  pollutant = sensortoolkit.Parameter('PM25')

Attributes
----------

.. list-table:: ``sensortoolkit.Parameter()`` attributes
  :widths: 50 75 50
  :header-rows: 1

  * - Attribute name
    - Description
    - Example: ``PM25``
  * - ``name``
    - The SDFS name for the parameter
    - ``'PM25'``
  * - ``format_name``
    - A formatted expression for the parameter used |br|
      for displaying the name of the parameter on |br|
      plots.
    - ``'PM$_{2.5}$'``
  * - ``format_baseline``
    - For ``format_name``, contains the baseline |br|
      component of the parameter name.
    - ``'PM'``
  * - ``format_subscript``
    - For ``format_name``, contains the subscripted |br|
      component of the parameter name
    - ``'2.5'``
  * - ``classifier``
    - A term for sorting the parameter into one of |br|
      three environmental parameter classifications, |br|
      either 'PM' for particulate matter pollutants, |br|
      'Gases' for gaseous pollutants, or 'Met' for |br|
      meteorological environmental parameters.
    - ``'PM'``
  * - ``units``
    - The units of measure, expressed symbolically |br|
      in Unicode characters.
    - ``'µg/m³'``
  * - ``units_description``
    - A textual description of the units of measure.
    - ``'Micrograms per Cubic Meter'``
  * - ``units_aqs_code``
    - The AQS unit code, useful for AQS queries [#f1]_.
    - ``105``
  * - ``criteria_pollutant``
    - Boolean, describes whether the parameter is a |br|
      criteria pollutant (``True``) or non-criteria |br|
      (``False``).
    - ``True``
  * - ``aqs_parameter_code``
    - The AQS Parameter code, useful for AQS |br|
      queries [#f2]_.
    - ``88101``
  * - ``averaging``
    - The reference measurement averaging intervals |br|
      commonly utilized for analyzing parameter data. |br|
      Common averaging intervals are included |br|
      in a list [#f3]_.
    - ``['1-hour', '24-hour']``
  * - ``PerformanceTargets``
    - Performance metrics, target values and ranges |br|
      associated with the parameter. Preset values |br|
      are configured for PM25 and O3 using |br|
      U.S. EPA's recommended performance metrics |br|
      and targets.
    - See "Performance Metrics |br| and Target Values Section".

.. rubric:: Footnotes

.. [#f1] A list of AQS unit codes is located at https://aqs.epa.gov/aqsweb/documents/codetables/units.html
.. [#f2] A list of AQS parameter codes is located at https://aqs.epa.gov/aqsweb/documents/codetables/parameters.html
.. [#f3] Reference data for particulate matter are commonly analyzed at either 1-hour or 24-hour intervals, but other pollutants that are strongly correlated with diurnal variability such as ozone are typically analyzed exclusively at high time resolution such as 1-hour intervals)


Performance Metrics and Target Values
-------------------------------------

Each parameter object comes with a subclass ``PerformanceTargets`` that contains
metric descriptions, target ranges, and target values for conducting performance
evaluations for sensor data corresponding to the parameter of interest.

For :raw-html:`PM<sub>2.5</sub>` and :raw-html:`O<sub>3</sub>`, U.S. EPA's recommended performance metrics and target
values are included in the pre-configured scheme for these parameters. A full description
of all metric names and target values/ranges can be accessed for a parameter
instance via:

.. code-block:: python

  all_metrics = pollutant.PerformanceTargets.get_all_metrics()

Continuing with the example for :raw-html:`PM<sub>2.5</sub>`, the ``all_metrics`` variable should
contain the following information:

.. code-block:: python

  {'Bias':
            {'Slope':
              {'description': 'Ordinary least squares regression slope',
               'bounds': (0.65, 1.35),
               'goal': 1.0,
               'metric_units': None},
            'Intercept':
              {'description': 'Ordinary least squares regression intercept',
               'bounds': (-5.0, 5.0),
               'goal': 0.0,
               'metric_units': '$\\mu g/m^3$'}
             },
   'Linearity':
            {'R^2':
              {'description': 'Coefficient of determination',
               'bounds': (0.7, 1.0),
               'goal': 1.0,
               'metric_units': None}
               },
   'Error':
            {'RMSE':
              {'description': 'Root mean square error',
               'bounds': (0.0, 7.0),
               'goal': 0.0,
               'metric_units': '$\\mu g/m^3$'},
            'NRMSE':
              {'description': 'Normalized root mean square error',
               'bounds': (0.0, 30.0),
               'goal': 0.0,
               'metric_units': '%'}
               },
   'Precision':
            {'SD':
              {'description': 'Standard deviation',
               'bounds': (0.0, 5.0),
               'goal': 0.0,
               'metric_units': '$\\mu g/m^3$'},
            'CV':
              {'description': 'Coefficient of variation',
               'bounds': (0.0, 30.0),
               'goal': 0.0,
               'metric_units': '%'}
               }
   }


Individual metric target values and ranges can be accessed via the ``get_metric()``
method. The example below is for accessing the description of the ``Slope``
performance metric:

.. code-block:: python

  metric = pollutant.PerformanceTargets.get_metric(metric_name='Slope')

Continuing with the example for :raw-html:`PM<sub>2.5</sub>`, the ``metric`` variable should
contain the following information:

.. code-block:: python

  {'description': 'Ordinary least squares regression slope',
   'bounds': (0.65, 1.35),
   'goal': 1.0,
   'metric_units': None}


Setting Performance Targets and Metrics
---------------------------------------

For SDFS parameters that do not have preset performance targets or metrics, users
can configure custom metric categories via the ``pollutant.PerformanceTargets.set_metric_category()``
method and target values via the ``pollutant.PerformanceTargets.set_metric()`` method. A detailed description
and examples for both of these methods is included in the
`API documentation for sensortoolkit.parameter.PerformanceTargets <../api/_autosummary/sensortoolkit.param._targets.ParameterTargets.html>`_.

.. |br| raw:: html

   <br />
