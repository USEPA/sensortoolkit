# -*- coding: utf-8 -*-
"""
The ``sensortoolkit.plotting`` subpackage contains modules for creating various
plots, including timeseries figures displaying sensor and reference measurements,
scatter plotting functions for comparing measurement pairs such as sensor and
reference concentrations, figures for displaying the distribution of meteorological
conditions during the testing period, etc.

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
from ._performance_metrics import performance_metrics
from ._scatter import scatter_plotter, normalized_met_scatter
from ._timeseries import sensor_timeplot, deployment_timeline
