==================
Evaluation Objects
==================
sensortoolkit contains several class objects to aid users in various data
analysis tasks. **These objects can be roughly divided into two categories:
testing attribute objects and evaluation objects.**

Since users may wish to evaluate multiple sensor types and numerous pollutants,
the intent in organizing the evaluation workflow into a set of recognizable and
consistent class objects is to provide an easy-to-navigate platform for conducting
evaluations and data analysis, while also allowing a high degree of customization.

-------

Conducting performance evaluations of air sensors with ``sensortoolkit`` is
accomplished via the library's evaluation objects, ``sensortoolkit.SensorEvaluation``
and ``sensortoolkit.PerformanceReport``. ``sensortoolkit.SensorEvaluation`` can be used
to conduct performance evaluations for air sensors with EPA's recommended performance
metrics and targets for either fine particulate matter or ozone sensors, and figures
and summary statistics can be generating for reviewing sensor performance. Testing
reports utilizing EPA's reporting templates for base testing of air sensors
under NSIM applications are created via the ``sensortoolkit.PerformanceReport`` class.

.. toctree::
    :caption: Overview of sensortoolkit Evaluation Objects
    :titlesonly:

    sensoreval/index
    performancereport
