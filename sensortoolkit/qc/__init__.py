# -*- coding: utf-8 -*-
"""
The ``sensortoolkit.qc`` subpackage contains various modules for quality control
(QC) methods, including the identification and removal of duplicated timestamp
entries, downsampling of irregularly spaced data, invalidation of data points,
detection and removal of persistent or constant values, and the method of cleaning
A and B channel data for PurpleAir PA-II measurements developed by Barkjohn et
al. 2021.

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
