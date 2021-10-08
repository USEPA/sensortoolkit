==============================
Data Structures and Formatting
==============================

The ``SensorEvaluation`` class contains a number of data structures that store
sensor and reference data, and related statistical metrics. Below is a discussion
of these data structures, as well as the Sensor Data Formattting Scheme (S-DFS) and
Reference Data Formatting Scheme (R-DFS) in which sensor and reference data are formatted.

More detail regarding the ``SensorEvaluation`` class, including its methods and
arguments are included in the `API documentation for SensorEvaluation <../html/_autosummary/sensortoolkit._evaluation.sensor_eval.SensorEvaluation.html>`_

.. toctree::
    :maxdepth: 3

    sensor_data
    sdfs
    reference_data
    rdfs
    config_structs
    eval_structs

.. note::
  We remind readers that the ``SensorEvaluation`` class can be instantiated with
  whichever name suits the user's needs best, however, below we refer to an instance
  of ``SensorEvaluation`` as ``Eval`` when referencing instance attributes (including data structures).

  See `Conducting Analysis with the SensorEvaluation Class <sensoreval.html>`_ for more information regarding instantiation of the ``SensorEvaluation`` class.
