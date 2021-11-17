# -*- coding: utf-8 -*-
"""
The ``sensortoolkit.datetime_utils`` subpackage contains various modules for
working with pandas DataFrame objects with timeseries index of type
``pandas.DatetimeIndex``. Modules are included for setting the timestamp index,
averaging recorded datasets to longer averaging intervals (e.g., 1-hour,
24-hours), etc.

===============================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Sep  8 10:59:14 2021
Last Updated:
  Wed Sep  8 10:59:14 2021
"""

from ._format_date import get_todays_date
from ._timeframe_utils import timeframe_search, deploy_timestamp_index
from ._time_averaging import sensor_averaging, interval_averaging
from ._get_timestamp_interval import get_timestamp_interval
from ._set_datetime_index import set_datetime_index
