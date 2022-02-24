===============
Data Structures
===============

sensortoolkit's objects, including the testing attribute objects ``AirSensor`` and
``ReferenceMonitor`` as well as the evaluation objects ``SensorEvaluation`` and ``PerformanceReport``,
each contain various data attributes (data structures).

The testing attribute objects store measurement
datasets within the ``AirSensor.data`` and ``ReferenceMonitor.data`` attributes
for sensor and reference data, respectively.

The evaluation objects ``SensorEvaluation`` and ``PerformanceReport`` construct numerous
performance evaluation data structures at time of object instantiation

Below is a discussion of data structures for both testing attribute objects and evaluation
objects.

More detail regarding the ``SensorEvaluation`` class, including its methods and
arguments are included in the `API documentation for SensorEvaluation <../_autosummary/sensortoolkit._evaluation.sensor_eval.SensorEvaluation.html>`_

.. toctree::
    :maxdepth: 3

    sensor_data
    reference_data
    config_structs
    eval_structs

.. note::
  A reminder that the ``SensorEvaluation`` class can be instantiated with
  whichever name suits the user's needs best. For illustrative purposes, instances of
  ``SensorEvaluation`` are referred to as ``Eval`` when referencing instance
  attributes (including data structures).
