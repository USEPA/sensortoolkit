# -*- coding: utf-8 -*-
"""Subpackage description.

===============================================================================

@Author:
    | Samuel Frederick, NSSC Contractor (ORAU)
    | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Sep  8 11:29:18 2021
Last Updated:
  Wed Sep  8 11:29:18 2021
"""

from ._duplicate_removal import remove_duplicates
from ._interval_downsampling import (timedelta_quantiles,
                                     downsampling_interval,
                                     apply_downsampling)
from ._invalidate import invalidate_period
from ._outlier_detection import cooks_outlier_detection
from ._persistent_values import persistent_values
from ._purpleair_abcleaning import purpleair_ab_averages
