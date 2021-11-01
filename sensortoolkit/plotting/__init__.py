# -*- coding: utf-8 -*-
"""Subpackage description.

===============================================================================

@Author:
    | Samuel Frederick, NSSC Contractor (ORAU)
    | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Sep  8 12:00:24 2021
Last Updated:
  Wed Sep  8 12:00:24 2021
"""

from ._plot_formatting import (get_colormap_range, met_scatter_lims,
                               sensor_subplot_formatting, set_fontsize,
                               subplot_dims, wrap_text)
from ._distribution import met_distrib, ref_distrib
from ._errorbars import error_bars
from ._intrasensor_comparison import compare_sensors
from ._performance_metrics import performance_metrics
from ._scatter import scatter_plotter, normalized_met_scatter
from ._timeseries import sensor_timeplot, deployment_timeline
