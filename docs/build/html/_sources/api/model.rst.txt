``sensortoolkit.model``
-----------------------

The ``sensortoolkit.model`` subpackage contains modules for applying or creating
correction methods for sensor data. Methods include the U.S.-Wide Correction
Equation developed by Barkjohn et al. 2021 [#f1]_ for the PurpleAir PA-II and modules for
calculating or applying a general linear correction equation based on the ordinary
least-squares regression between sensor (dependent variable) and reference
(independent variable) measurements.

Clicking on each module below will open a page with a detailed description and
list of functions included within the module.

.. autosummary::
  :toctree: _autosummary
  :template: custom-module-template.rst
  :recursive:

  sensortoolkit.model._apply_correction
  sensortoolkit.model._purpleair_uscorrection
  sensortoolkit.model._sensor_ols

.. rubric:: Footnotes

.. [#f1] Barkjohn, K. K., Gantt, B., and Clements, A. L.: Development and application of a United States-wide correction for PM2.5 data collected with the PurpleAir sensor, Atmos. Meas. Tech., 14, 4617–4637, https://doi.org/10.5194/amt-14-4617-2021, 2021.
