=====================
sensortoolkit Modules
=====================

.. note::

    The API documentation is currently under development. Please check for
    updates to the BitBucket repository before referencing this section.

Below is listing of subpackages (in red) contained within `sensortoolkit`. Each subpackage
contains a number of modules (python files containing various functions) listed in a
table for each subpackage. Click on module names to view functions within each file.

``sensortoolkit.calculate``
---------------------------

.. autosummary::
   :toctree: _autosummary
   :template: custom-module-template.rst
   :recursive:

   sensortoolkit.calculate._aqi
   sensortoolkit.calculate._cv
   sensortoolkit.calculate._dewpoint
   sensortoolkit.calculate._intersensor_mean
   sensortoolkit.calculate._normalize
   sensortoolkit.calculate._nowcast_pm25
   sensortoolkit.calculate._regression_stats
   sensortoolkit.calculate._rmse
   sensortoolkit.calculate._uptime

``sensortoolkit.datetime_utils``
--------------------------------

.. autosummary::
   :toctree: _autosummary
   :template: custom-module-template.rst
   :recursive:

   sensortoolkit.datetime_utils._format_date
   sensortoolkit.datetime_utils._get_timestamp_interval
   sensortoolkit.datetime_utils._set_datetime_index
   sensortoolkit.datetime_utils._time_averaging
   sensortoolkit.datetime_utils._timeframe_utils

``sensortoolkit.deploy``
------------------------

.. autosummary::
  :toctree: _autosummary
  :template: custom-module-template.rst
  :recursive:

  sensortoolkit.deploy._create_deploy_dict
  sensortoolkit.deploy._deployment_period
  sensortoolkit.deploy._get_max_conc

``sensortoolkit.evaluation``
----------------------------

.. autosummary::
  :toctree: _autosummary
  :template: custom-module-template.rst
  :recursive:

  sensortoolkit.evaluation._sensor_eval
  sensortoolkit.evaluation._airsensor

``sensortoolkit.lib_utils``
---------------------------

.. autosummary::
  :toctree: _autosummary
  :template: custom-module-template.rst
  :recursive:

  sensortoolkit.lib_utils._copy_datasets
  sensortoolkit.lib_utils._flatten_list
  sensortoolkit.lib_utils._sensor_subfolders

``sensortoolkit.model``
-----------------------

.. autosummary::
  :toctree: _autosummary
  :template: custom-module-template.rst
  :recursive:

  sensortoolkit.model._apply_correction
  sensortoolkit.model._purpleair_uscorrection
  sensortoolkit.model._sensor_ols

``sensortoolkit.param``
-----------------------

.. autosummary::
  :toctree: _autosummary
  :template: custom-module-template.rst
  :recursive:

  sensortoolkit.param._parameter
  sensortoolkit.param._targets

``sensortoolkit.performancereport``
-----------------------------------

.. autosummary::
  :toctree: _autosummary
  :template: custom-module-template.rst
  :recursive:

  sensortoolkit.performancereport._performance_report

``sensortoolkit.plotting``
--------------------------

.. autosummary::
  :toctree: _autosummary
  :template: custom-module-template.rst
  :recursive:

  sensortoolkit.plotting._distribution
  sensortoolkit.plotting._errorbars
  sensortoolkit.plotting._intrasensor_comparison
  sensortoolkit.plotting._performance_metrics
  sensortoolkit.plotting._plot_formatting
  sensortoolkit.plotting._scatter
  sensortoolkit.plotting._timeseries

``sensortoolkit.qc``
--------------------

.. autosummary::
  :toctree: _autosummary
  :template: custom-module-template.rst
  :recursive:

  sensortoolkit.qc._duplicate_removal
  sensortoolkit.qc._interval_downsampling
  sensortoolkit.qc._invalidate
  sensortoolkit.qc._outlier_detection
  sensortoolkit.qc._persistent_values
  sensortoolkit.qc._purpleair_abcleaning

``sensortoolkit.reference``
---------------------------

.. autosummary::
  :toctree: _autosummary
  :template: custom-module-template.rst
  :recursive:

  sensortoolkit.reference._import_airnowtech
  sensortoolkit.reference._import_oaqps
  sensortoolkit.reference._load_ref_data
  sensortoolkit.reference._ref_api_query

``sensortoolkit.sensor_ingest``
-------------------------------

.. autosummary::
  :toctree: _autosummary
  :template: custom-module-template.rst
  :recursive:

  sensortoolkit.sensor_ingest._processed_data_loader
  sensortoolkit.sensor_ingest._sensor_import
  sensortoolkit.sensor_ingest._standard_ingest
