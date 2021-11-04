``sensortoolkit.datetime_utils``
--------------------------------

The ``sensortoolkit.datetime_utils`` subpackage contains various modules for
working with pandas DataFrame objects with timeseries index of type ``pandas.DatetimeIndex``.
Modules are included for setting the timestamp index, averaging recorded datasets to
longer averaging intervals (e.g., 1-hour, 24-hours), etc.

Clicking on each module below will open a page with a detailed description and 
list of functions included within the module.

.. autosummary::
   :toctree: _autosummary
   :template: custom-module-template.rst
   :recursive:

   sensortoolkit.datetime_utils._format_date
   sensortoolkit.datetime_utils._get_timestamp_interval
   sensortoolkit.datetime_utils._set_datetime_index
   sensortoolkit.datetime_utils._time_averaging
   sensortoolkit.datetime_utils._timeframe_utils
