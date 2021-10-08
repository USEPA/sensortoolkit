************************************************
Conducting Analysis - The SensorEvaluation Class
************************************************

`sensortoolkit` contains dozens of individual modules and functions for computing
statistical metrics and generating figures in accordance with U.S. EPA's recommended
`performance metrics and targets <https://www.epa.gov/air-sensor-toolbox/air-sensor-performance-targets-and-testing-protocols>`_.
The ``SensorEvaluation`` class packages many of `sensortoolkit`'s modules into
a user-friendly and efficient platform for evaluating sensor performance.

========================================
A brief overview of ``SensorEvaluation``
========================================

- Computes various quantitites and metrics recommended by U.S. EPA's performance targets reports
  including precision (standard deviation, coefficient of variation), error (RMSE),
  linarity (:math:`R^2`), and bias (OLS regression slope and intercept).
- Contains numerous plotting methods for displaying and saving figures for
  time series, sensor vs. reference scatter, meteorological conditions, etc.
- Contains methods for printing summary statistics for evaluation conditions and
  performance evaluation results using U.S EPA's recommended performance metrics.

Below is an example of instantiating the `SensorEvaluation` class for the ``AirSensor``,
``ReferenceMonitor``, and ``Parameter`` objects discussed in the `sensortoolkit Objects` section.

.. code-block:: python

  evaluation = sensortoolkit.SensorEvaluation(sensor=sensor_object,
                                              param=pollutant,
                                              reference=reference_object,
                                              write_to_file=True)

.. note::
  ``evaluation`` is the name given to the ``SensorEvaluation`` class instance. Users are not required
  to refer to their class instances as ``evaluation`` and can instead assign whichever name suits best.

  Please note that subsequent reference to ``SensorEvaluation`` instance attributes and
  modules will use the name ``evaluation``.

Arguments passed to ``SensorEvaluation``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
    - If true, evaluation statistics will be written to the
      Data and Figures/eval_stats sensor subdirectory and figures will
      also be written to the appropriate figures subdirectory.

Keyword Arguments passed to ``SensorEvaluation``
""""""""""""""""""""""""""""""""""""""""""""""""

Additional keyword arguments may be passed to the class. The current
version of ``SensorEvaluation`` supports two additional keyword arguments for
specifying information about the testing organization and evaluation location.

``testing_org``
"""""""""""""""

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

# Add note that contact info appear in header and first table

``testing_loc``
"""""""""""""""

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

.. toctree::
  :maxdepth: 1

  plotting