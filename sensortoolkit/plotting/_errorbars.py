# -*- coding: utf-8 -*-
"""
This module contains a method ``error_bars()`` for displaying the y-error in
measured quantities at regularly spaced intervals (bins) along the x-axis. This
method can be used in conjunction with the ``normalized_met_scatter()`` plotting
method to display the standard error of normalized measurement pairs (dependent
variable) at regularly spaced intervals across the distribution of
measured temperature or relative humidity (independent variable).

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Mon Jan 27 08:49:12 2020
Last Updated:
  Wed Jul 28 14:18:59 2021
"""
from pandas.plotting import register_matplotlib_converters
import numpy as np
import math
register_matplotlib_converters()


def error_bars(xdata, ydata, ax, n_xbins=8, plot_yerror=True,
               errorbar_color='k'):
    """Display error bars on a passed matplotlib axes plot instance.

    Args:
        xdata (pandas Series):
            Data plotted along the x-axis of the passed axes instance 'ax'.
        ydata (pandas Series):
            Data plotted along the y-axis of the passed axes instance 'ax'.
        ax (matplotlib axes instance):
            A scatter plot displaying measurement pairs along x and y axes.
        n_xbins (int, optional):
            The number of bins along the range of the xdata from which the error
            bars will be computed. This also equals the number of errorbars.
            Defaults to 8.
        plot_yerror (bool, optional):
            Plot error along the y-axis. Defaults to True.
        errorbar_color (str, optional):
            The color of the error bars. Defaults to 'k' (black).

    Returns:
        None.

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
                fmt='D', mfc=errorbar_color, mec=errorbar_color,
                ecolor=errorbar_color, capsize=4, **{'markersize': 4},
                alpha=.7)
