# -*- coding: utf-8 -*-
"""
The ``sensortoolkit.model`` subpackage contains modules for applying or creating
correction methods for sensor data. Methods include the U.S.-Wide Correction
Equation developed by Barkjohn et al. 2021 [#f1]_ for the PurpleAir PA-II and
modules for calculating or applying a general linear correction equation based
on the ordinary least-squares regression between sensor (dependent variable) and
reference (independent variable) measurements.

===============================================================================

@Author:
    | Samuel Frederick, NSSC Contractor (ORAU)
    | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Sep  8 10:49:38 2021
Last Updated:
  Wed Sep  8 10:49:38 2021
"""

from ._apply_correction import individual_corr
from ._purpleair_uscorrection import purpleair_us_corr
from ._sensor_ols import sensor_ols
