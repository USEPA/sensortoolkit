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
  Mon Jan 27 08:49:12 2020
Last Updated:
  Wed Jul 28 14:18:59 2021
"""
from pandas.plotting import register_matplotlib_converters
import numpy as np
import math
register_matplotlib_converters()


def Plot_Error_Bars(xdata, ydata, ax, n_xbins=8, plot_yerror=True,
                    errorbar_c='k'):
    """

    Args:
        xdata
        ydata
        ax
        b_xbins
        plot_yerror
        errorbar_c

    Returns:
        None

    """
    combine = xdata.to_frame().join(ydata)

    xmin = xdata.min()
    xmax = xdata.max()
    xrange = xmax - xmin
    xbin_width = xrange / n_xbins
    xbin_centers = np.linspace(xmin + 0.5*xbin_width,
                               xmax - 0.5*xbin_width,
                               n_xbins)

    if plot_yerror is True:
        yerr_list = []
        yavg_list = []

        xdata = combine.loc[:, combine.columns[0]]
        ydata = combine.loc[:, combine.columns[1:]]

        for bin_center in xbin_centers:
            bin_min = bin_center - 0.5*xbin_width
            bin_max = bin_center + 0.5*xbin_width

            bin_idx = combine.where((xdata < bin_max) &
                                    (xdata > bin_min)).dropna(how='all').index

            bin_ydata = combine.loc[bin_idx, combine.columns[1:]]

            # Compute y-data std for xbin range
            bin_ystd = bin_ydata.stack().std()

            # Compute y-data avg for xbin range
            bin_yavg = bin_ydata.stack().mean()
            yavg_list.append(bin_yavg)

            # Number of sensor-reference data pairs per bin
            bin_n = bin_ydata.stack().count()

            # Compute standard error and append to yerror list
            try:
                std_err = bin_ystd / math.sqrt(bin_n)
                yerr_list.append(std_err)
            except ZeroDivisionError:
                yerr_list.append(0)
                print('Warning, divide by zero encountered, zero bin size')

    ax.errorbar(xbin_centers, yavg_list, yerr=yerr_list,
                fmt='D', mfc=errorbar_c, mec=errorbar_c, ecolor=errorbar_c,
                capsize=4, **{'markersize': 4}, alpha=.7)
