====================
The Parameter Object
====================

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

    sensortoolkit.param.Parameter.__param_dict__.keys()

For example, a Parameter instance called ``pollutant`` can be created for the pollutant :raw-html:`PM<sub>2.5</sub>`
by specifying the SDFS parameter name ``PM25``:

.. code-block:: python

  pollutant = sensortoolkit.param.Parameter('PM25')

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
    - A formatted version of the parameter name (used for figures and reports)
    - ``'PM$_{2.5}$'``
  * - ``format_baseline``
    - For ``format_name``, contains the baseline component of the parameter name.
    - ``'PM'``
  * - ``format_subscript``
    - For ``format_name``, contains the subscripted component of the parameter name (e.g., '2.5' in PM2.5)
    - ``'2.5'``
  * - ``units``
    - The units of measure for the parameter. Formatted in LateX syntax for figures.
    - ``'($\\mu g/m^3$)'``
  * - ``criteria_pollutant``
    - Boolean, describes whether the parameter is a criteria pollutant (``True``) or non-criteria (``False``)
    - ``True``
  * - ``aqs_parameter_code``
    - The AQS Parameter code, useful for AQS queries [#f1]_.
    - ``88101``
  * - ``averaging``
    - The FRM/FEM averaging intervals commonly utilized for analyzing parameter data [#f2]_.
    - ``['1-hour', '24-hour']``

.. rubric:: Footnotes

.. [#f1] A list of parameter codes is located at https://aqs.epa.gov/aqsweb/documents/codetables/parameters.html
.. [#f2] Reference data for particulate matter are commonly analyzed at either 1-hour or 24-hour intervals, but other pollutants that are strongly correlated with diurnal variability such as ozone are typically analyzed at high time resolution such as 1-hour intervals)


Performance Targets and Metrics
-------------------------------

Each parameter object comes with a subclass ``PerformanceTargets`` that contains
metric descriptions, target ranges, and target values for conducting performance
evaluations for sensor data corresponding to the parameter of interest.

For ``PM25`` and ``O3``, U.S. EPA's recommended performance metrics and target
values are included in the pre-configured scheme for these parameters. A full description
of all metric names and target values/ranges can be accessed for a parameter
instance via:

.. code-block:: python

  all_metrics = pollutant.PerformanceTargets.get_AllMetrics()

Continuing with the example for ``PM25``, the ``all_metrics`` variable should
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


Individual metric target values and ranges can be accessed via the ``get_PerformanceMetric``
method. The example below is for accessing the description of the ``Slope`` metric contained within
the ``Bias`` category:

.. code-block:: python

  metric = pollutant.PerformanceTargets.get_PerformanceMetric(metric_category='Bias',
                                                              metric_name='Slope')

Continuing with the example for ``PM25``, the ``metric`` variable should
contain the following information:

.. code-block:: python

  {'description': 'Ordinary least squares regression slope',
   'bounds': (0.65, 1.35),
   'goal': 1.0,
   'metric_units': None}


Setting Performance Targets and Metrics
---------------------------------------

.. code-block:: python

  pollutant.PerformanceTargets.set_MetricCategory(metric_category, metric_names)
  pollutant.PerformanceTargets.set_PerformanceMetric(metric_category, metric_name)
