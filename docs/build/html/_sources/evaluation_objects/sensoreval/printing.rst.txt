Descriptive Summary Methods
---------------------------

.. role:: raw-html(raw)
   :format: html

Below is a discussion of descriptive summary methods included alongside ``SensorEvaluation``.
These methods print formatted summaries in the console for testing conditions and
evaluation statistics, printed to the console. Example outputs are shown for each summary method.

.. note::

  This section provides a brief overview of the descriptive summary methods accessed via
  instances of the ``SensorEvaluation`` class. For more detail on calling these
  methods, click on the link to the API documentation indicated below each
  method header.

.. important::

  A console width of at least 86 characters is recommended to properly format
  printed statements resulting from these methods.

-----

``SensorEvaluation.print_eval_metrics()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`API Documentation for print_eval_metrics() <../../api/_autosummary/sensortoolkit.evaluation_objs._sensor_eval.SensorEvaluation.html#sensortoolkit.evaluation_objs._sensor_eval.SensorEvaluation.print_eval_metrics>`_

Description
"""""""""""

Display a summary of performance evaluation results using EPA’s recommended
performance metrics (:raw-html:`PM<sub>2.5</sub>` and :raw-html:`O<sub>3</sub>`).

The coefficient of variation, sensor vs FRM/FEM OLS regression slope,
intercept, and :raw-html:`R<sup>2</sup>`,, and RMSE are displayed. Regression statistics
are computed for each sensor, and the mean metric value is
presented alongside the range (min to max).

Example
"""""""

Below is an example for the `Toco Toucan Quickstart Guide example <../../quickstart.html#example-scenario-toco-toucan>`_

.. code-block:: console

  ----------------------------------------------------------------------------------------
                     Toco_Toucan 24-hour Performance Evaluation Results
                         Reference Method: T-API T640X at 16.67 LPM
  ----------------------------------------------------------------------------------------
    CV  |         Slope          |       Intercept        |          R^2           | RMSE
  ----------------------------------------------------------------------------------------
   7.1  |          0.87          |         -2.38          |          0.59          | 3.6
        |     (0.84 to 0.92)     |    (-2.56 to -2.12)    |     (0.54 to 0.63)     |

-----

``SensorEvaluation.print_eval_conditions()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`API Documentation for print_eval_conditions() <../../api/_autosummary/sensortoolkit.evaluation_objs._sensor_eval.SensorEvaluation.html#sensortoolkit.evaluation_objs._sensor_eval.SensorEvaluation.print_eval_conditions>`_

Description
"""""""""""

Display conditions for the evaluation parameter and meteorological conditions
during the testing period.

Values for the evaluation parameter recorded by the sensor, FRM/FEM
instrument, and temperature and relative humidity values are
displayed by the mean of 1-hour or 24-hour averages during the
testing period. The range (min to max) of each parameter is listed
below the mean in parentheses.

Example
"""""""

Below is an example for the `Toco Toucan Quickstart Guide example <../../quickstart.html#example-scenario-toco-toucan>`_


.. code-block:: console

  ----------------------------------------------------------------------------------------
                       Toco_Toucan (3) 24-hour Evaluation Conditions
  ----------------------------------------------------------------------------------------
   Eval period  |   Duration   | Sensor PM25  |   Ref PM25   |     Temp     |      RH
  ----------------------------------------------------------------------------------------
    08-01-19-   |   32 days    |     4.4      |     7.7      |      26      |      71
     09-02-19   |              | (1.2 to 8.1) |(4.9 to 11.0) |  (21 to 29)  |  (60 to 88)
