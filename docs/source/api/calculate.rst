``sensortoolkit.calculate``
---------------------------

The ``sensortoolkit.calculate`` subpackage contains various modules and methods
for calculating parameter quantities (e.g., U.S. EPA's Air Quality Index,
dewpoint as derived from temperature and relative humidity measurements, etc.)
and statistical performance evaluation metrics (e.g., CV, RMSE, Uptime, etc.).

Clicking on each module below will open a page with a detailed description and
list of functions included within the module.

.. autosummary::
   :toctree: _autosummary
   :template: custom-module-template.rst
   :recursive:

   sensortoolkit.calculate._aqi
   sensortoolkit.calculate._convert_temp
   sensortoolkit.calculate._cv
   sensortoolkit.calculate._dewpoint
   sensortoolkit.calculate._intersensor_mean
   sensortoolkit.calculate._normalize
   sensortoolkit.calculate._nowcast_pm25
   sensortoolkit.calculate._regression_stats
   sensortoolkit.calculate._rmse
   sensortoolkit.calculate._uptime
