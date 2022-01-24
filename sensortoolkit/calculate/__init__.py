# -*- coding: utf-8 -*-
"""
Analysis modules supporting the calculation of parameter quantities and
statistical metrics that are either recommended by U.S. EPA's Performance
Targets Reports, or may be used to compliment performance evaluation efforts.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Sep  8 09:51:09 2021
Last Updated:
  Wed Sep  8 09:51:09 2021
"""

from ._aqi import aqi
from ._convert_temp import convert_temp
from ._cv import cv
from ._rmse import rmse
from ._dewpoint import dewpoint
from ._normalize import normalize
from ._nowcast_pm25 import nowcast_pm25
from ._uptime import uptime
from ._regression_stats import regression_stats, join_stats
from ._intersensor_mean import intersensor_mean
