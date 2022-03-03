Conducting Analysis - The SensorEvaluation Class
================================================

.. role:: raw-html(raw)
   :format: html

sensortoolkit contains dozens of individual modules and functions for computing
statistical metrics and generating figures in accordance with U.S. EPA's recommended
`performance metrics and targets <https://www.epa.gov/air-sensor-toolbox/air-sensor-performance-targets-and-testing-protocols>`_.
The ``SensorEvaluation`` class packages many of `sensortoolkit`'s modules into
a user-friendly and efficient platform for evaluating sensor performance.

.. note::

  This section provides a brief overview of the ``SensorEvaluation`` class.
  For more detail on the class and its methods, see the
  `API Documentation for SensorEvaluation() <../../api/_autosummary/sensortoolkit.evaluation_objs._sensor_eval.SensorEvaluation.html#sensortoolkit.evaluation_objs._sensor_eval.SensorEvaluation>`_

.. important::

  While ``SensorEvaluation`` has been designed to calculate and utilize EPA's
  recommended performance metrics and target values for sensors measuring either :raw-html:`PM<sub>2.5</sub>`
  or :raw-html:`O<sub>3</sub>`, ``SensorEvaluation`` can be used to analyze data
  for any  `SDFS parameter <../../sdfs/index.html#id1>`_. For pollutants other than
  :raw-html:`PM<sub>2.5</sub>` or :raw-html:`O<sub>3</sub>`, users are encouraged
  to make use of the ``sensortoolkit.Parameter()``
  `methods for setting custom performance targets and metrics <../../testingattrib_objects/parameter.html#setting-performance-targets-and-metrics>`_.


A brief overview of ``SensorEvaluation``
----------------------------------------

- Computes various quantities and metrics recommended by U.S. EPA's performance targets reports
  including precision (SD - standard deviation, CV - coefficient of variation),
  error (root mean squared error - RMSE), linearity (:raw-html:`R<sup>2</sup>`),
  and bias (OLS regression slope and intercept).
- Contains numerous plotting methods for displaying and saving figures for
  time series, sensor vs. reference scatter, meteorological conditions, etc.
- Contains methods for printing summary statistics for evaluation conditions and
  performance evaluation results using U.S EPA's recommended performance metrics.

Below is an example of instantiating the ``SensorEvaluation`` class for the ``AirSensor``,
``ReferenceMonitor``, and ``Parameter`` objects discussed in the
`Testing Attribute Objects <../../testingattrib_objects/index.html>`_ section.

.. code-block:: python

  evaluation = sensortoolkit.SensorEvaluation(sensor,
                                              pollutant,
                                              reference,
                                              write_to_file=True)

.. note::
  ``evaluation`` is the name given to the ``SensorEvaluation`` class instance. Users are not required
  to refer to their class instances as ``evaluation`` and can instead assign whichever name suits best.

  Please note that subsequent reference to ``SensorEvaluation`` instance attributes and
  modules will use the name ``evaluation``.

Arguments passed to ``SensorEvaluation``
----------------------------------------

.. list-table:: ``sensortoolkit.SensorEvaluation()`` attributes
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
    - If true, evaluation statistics are saved to
      ``/data/eval_stats/[name of sensor]`` and figures are
      written to ``/figures/[name of sensor]``.

..
  Keyword Arguments passed to ``SensorEvaluation``
  """"""""""""""""""""""""""""""""""""""""""""""""

  Additional keyword arguments may be passed to the class. The current
  version of ``SensorEvaluation`` supports two additional keyword arguments for
  specifying information about the testing organization and evaluation location.

  ``testing_org``
  ^^^^^^^^^^^^^^^

  A dictionary containing the information about the testing organization.

  .. list-table:: ``testing_org`` Attributes
    :widths: 50 75
    :header-rows: 1

    * - Attribute name
      - Description
    * - ``Deployment name``
      - The descriptive name assigned to the sensor deployment.
    * - ``Org name``
      - The name of the testing organization.
    * - ``Website``
      - Website address for the testing organization.
    * - ``Contact email``
      - Contact email address responsible parties conducting testing.
    * - ``Contact phone``
      - Phone number for responsible parties conducting testing.

  **Example:**

  .. code-block:: python

    testing_org = {'Deployment name': '[Insert name of deployment]',
                   'Org name': ['[Insert organization name]'],
                   'Website': {'website name': '[Insert name of website]',
                               'website link': '[Insert website here]'},
                   'Contact email': '[Insert email here]',
                   'Contact phone': '[Insert phone number here]'}

  ``testing_loc``
  ^^^^^^^^^^^^^^^

  A dictionary containing information about the testing site. If the site is part
  of U.S. EPA's Air Quality System (AQS), the AQS Site ID should be specified.

  .. list-table:: ``testing_org`` Attributes
    :widths: 50 75
    :header-rows: 1

    * - Attribute name
      - Description
    * - ``Site name``
      - The name of the ambient monitoring site.
    * - ``Site address``
      - The street address of the monitoring site.
    * - ``Site lat``
      - The latitude coordinate of the site.
    * - ``Site lon``
      - The longitude coordinate of the site.

  **Example:**

  .. code-block:: python

    testing_loc = {'Site name': '[Insert name of site] ',
                   'Site address': '[Insert site address]',
                   'Site lat': '[Insert site latitude]',
                   'Site long': '[Insert site longitude]',
                   'Site AQS ID': '[If applicable, insert site AQS ID]'}

``SensorEvaluation`` Methods
----------------------------

``SensorEvaluation`` contain numerous methods for generating figures, calculating
statistical quantities, and displaying formatted summaries printed to the console
for either evaluation statistics or testing period site conditions.

Click on the categories below to learn more about these methods.

.. toctree::
  :maxdepth: 1

  plotting
  printing
  statistic
