# -*- coding: utf-8 -*-
"""
@Author:
  Samuel Frederick, NSSC Contractor (ORAU)
  U.S. EPA, Office of Research and Development
  Center for Environmental Measurement and Modeling
  Air Methods and Characterization Division, Source and Fine Scale Branch
  109 T.W Alexander Drive, Research Triangle Park, NC 27711
  Office: 919-541-4086 | Email: frederick.samuel@epa.gov

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