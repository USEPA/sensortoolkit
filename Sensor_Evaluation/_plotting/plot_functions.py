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
  Tue May 11 16:18:00 2021

Plot Color Palettes In Style of Seaborn:
    Good Red and Blue Combo:
        Red: #c3553aff
        Blue: #3f7f93ff
"""
import sys
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from matplotlib.patches import FancyBboxPatch
from matplotlib.collections import PatchCollection
from matplotlib.colors import rgb2hex
from matplotlib.patches import Rectangle
import seaborn as sns
from Sensor_Evaluation._analysis.model_analysis import Regression_Stats
from Sensor_Evaluation._format.format_names import Format_Param_Name
from Sensor_Evaluation._format.format_date import Get_Date
from Sensor_Evaluation._analysis.normalize_calculator import Normalize
from textwrap import wrap
import math
register_matplotlib_converters()
sns.set_style('darkgrid')


"""----------------------------------------------------------------------------
Figure formatting functions:
    Set_Fontsize
    Wrap_Text
    Subplot_Dims
    Sensor_Subpot_Formatting
----------------------------------------------------------------------------"""


def Set_Fontsize(serials):
    """Selects fontsize for figures based on the number of sensors present in
    the sensor serial ID dictionary.

    Args:
        serials (dict):
            A dictionary of serial identifiers unique to each sensor in the
            deployment testing group.
    Returns:
        fontsize (float):
            The fontsize for figures.
    """
    n_sensors = len(serials)

    if (n_sensors == 1):
        fontsize = 14
    if (n_sensors < 7 and n_sensors > 1):
        fontsize = 13
    else:
        fontsize = 11.7

    return fontsize


def Wrap_Text(labels, max_label_len=10):
    """Formats plotting text with line breaks based on specified text length.

    Code modified via Stack Overflow user DavidG code:
    https://stackoverflow.com/questions/47057789/matplotlib-wrap-text-in-legend

    Args:
        labels (list):
            list plotting labels (strings) such as header/title text
        max_label_len (int):
            The maximum number of characters on a single line. Labels longer
            than this will have a newline '\n' inserted at every max_label_len
            number of characters.

    Returns:
        labels (list):
            Modified list of labels with the newline character '\n' inserted
            for labels exceeding the max_label_len.

    """
    labels = ['\n'.join(wrap(l, max_label_len)) for l in labels]

    return labels


def Subplot_Dims(n_sensors):
    """Recommends subplot dimensions based on the nearest perfect square for
    number of sensors (except when n%10, n_cols in multiples of 5)

    Args:
        n_sensors (int):
            The number of sensors in the deployment group.
    Returns:
        n_rows (int):
            The number of subplot rows.
        n_cols (int):
            The number of subplot columns.
    """
    sqr = np.sqrt(n_sensors)
    n_rows = math.floor(sqr)
    if n_sensors % 10 == 0:
        n_rows = math.floor(n_sensors/5)
    n_cols = math.ceil(n_sensors / n_rows)

    return (n_rows, n_cols)


def Sensor_Subplot_Formatting(number_of_sensors, param, font_size,
                              RH_colormap, report_fmt=False):
    """Configure subplot parameters that control the spacing of subplots,
    number of subplots and dimensions of the Matplotliub axes object array,
    color bar formatting, etc.

    Args:

    Returns:

    """
    Nr, Nc = Subplot_Dims(number_of_sensors)

    sensor_plural, row_plural, column_plural = '', '', ''

    if number_of_sensors > 1:
        sensor_plural = 's'
    if Nr > 1:
        row_plural = 's'
    if Nc > 1:
        column_plural = 's'

    print('Creating subplot for', str(number_of_sensors),
          'sensor' + sensor_plural, 'with', str(Nr),
          'row' + row_plural,  'and', str(Nc), 'column' + column_plural)

    suptitle_xpos = 0.50
    if number_of_sensors == 1:  # 1x1 subplot
        suptitle_ypos = 0.98
        title_text_wrap = 35

        if RH_colormap is True:
            if param == 'O3':
                font_size = 12
                fig_size = (4.3, 3.91)
                wspace = .1
                hspace = .1
                left = 0.12
                right = 0.8
                top = 0.85
                bottom = 0.15
                suptitle_xpos = 0.46
                suptitle_ypos = 1.01
                title_text_wrap = 30
                suptitle_ypos = 0.95
            else:
                fig_size = (4.9, 5.5)
                wspace = .01
                hspace = .01
                left = 0.15
                right = 0.85
                top = 0.9
                bottom = 0.25
        else:
            fig_size = (4.9, 5.5)
            wspace = .01
            hspace = .01
            left = 0.15
            right = 0.85
            top = 0.95
            bottom = 0.1
        detail_fontsize = .85*font_size
        filename_suffix = '1_sensor'
        cbar_padding = .13
        cbar_aspect = 20

    elif number_of_sensors == 3:  # 3x1 subplot
        fig_size = (12.3, 5.12)
        suptitle_ypos = 0.99
        title_text_wrap = 70

        if RH_colormap is True:
            wspace = .38
            hspace = .05
            left = 0.06
            right = 0.94
            top = 0.97
            bottom = 0.22
        else:
            fig_size = (12, 4)
            wspace = .4
            hspace = .01
            left = 0.07
            right = 0.93
            top = 0.90
            bottom = 0.1
        detail_fontsize = .85*font_size
        filename_suffix = '3_sensors'
        cbar_padding = .16
        cbar_aspect = 20

    elif number_of_sensors in (5, 6):  # 2x3 subplot
        fig_size = (13, 9)
        suptitle_ypos = 0.97
        title_text_wrap = 70

        if RH_colormap is True:
            wspace = .1
            hspace = .34
            left = 0.03
            right = 0.97
            top = 0.90
            bottom = 0.17
        else:
            fig_size = (13, 8)
            wspace = .4
            hspace = .33
            left = 0.07
            right = 0.93
            top = 0.89
            bottom = 0.1
        detail_fontsize = .85*font_size
        filename_suffix = '6_sensors'
        cbar_padding = .08
        cbar_aspect = 20

    elif number_of_sensors in (7, 8):  # 2x4 subplot
        Nr = 2
        Nc = 4
        fig_size = (16, 9)
        suptitle_ypos = 0.97
        title_text_wrap = 70

        if RH_colormap is True:
            wspace = .1
            hspace = .34
            left = 0.03
            right = 0.97
            top = 0.90
            bottom = 0.17
        else:
            fig_size = (15, 8)
            wspace = .44
            hspace = .35
            left = 0.05
            right = 0.95
            top = 0.89
            bottom = 0.1
        detail_fontsize = .85*font_size
        filename_suffix = '8_sensors'
        cbar_padding = .08
        cbar_aspect = 20

    elif number_of_sensors == 9:  # 3x3 subplot
        Nr = 3
        Nc = 3
        fig_size = (12, 11)
        suptitle_ypos = 0.97
        title_text_wrap = 70

        if RH_colormap is True:
            wspace = .04
            hspace = .4
            left = 0.01
            right = 0.99
            top = 0.92
            bottom = 0.15
        else:
            fig_size = (12, 10)
            wspace = .4
            hspace = .35
            left = 0.07
            right = 0.93
            top = 0.89
            bottom = 0.1
        detail_fontsize = .85*font_size
        filename_suffix = '9_sensors'
        cbar_padding = .06
        cbar_aspect = 20
    else:
        print('No formatting presets configured for', str(number_of_sensors))

    if report_fmt is True:
        if param == 'PM25':
            wspace = .4
            hspace = .08
            left = 0.1
            right = 0.92
            top = 0.9
            bottom = 0.30
            cbar_padding = .0
            cbar_aspect = 20
        filename_suffix = 'report_fmt'

    return (Nr, Nc, fig_size, suptitle_xpos, suptitle_ypos, title_text_wrap,
            detail_fontsize, wspace, hspace, left, right, top, bottom,
            filename_suffix, cbar_padding, cbar_aspect, font_size)


"""----------------------------------------------------------------------------

Plotting subroutines

----------------------------------------------------------------------------"""


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


def Comparison_Plotter(ax, xdata, ydata, param_dict, stats_df=None,
                       sensor_index=None, text_position='upper_left',
                       xlim=(0, 40), ylim=(0, 40), fontsize=None,
                       detail_fontsize=None,
                       param=None, sensor_name=None, plot_one_to_one=True,
                       plot_regression=True, plot_trendline=True,
                       plot_rmse=True, plot_spearman=False, plot_n=True,
                       monocolor=None, colormap_vals=None, colormap_name=None,
                       empty_plot=False, **kwargs):
    """A helper function to create comparison scatterplots with linear
    regressions.

    Args:
        ax: Axes instance
            The axes attributes which are drawn
        xdata: array
            The x data
        ydata: array
            The y data
        param_dict: dict
            Dictionary of kwargs to pass to ax.plot
        text_pos:
            2x2 Tuple of float values ((a,b),(c,d)) specifying position
            of Linear regression equation (a,b) and R^2 value (c,d)
        plot_one_to_one: boolean
            True plots the one-to-one dashed line, setting false will not plot
            the line
        plot_regression: bool
            True plots linear regression, regression equation, R^2, and RMSE
        monocolor: string or none
            If monocolor is not None, scatterplots will be plotted in the
            specified color. Else, if colormap is selected, the color of the
            plots will conform to the colormap, otherwise, the default color
            scheme is selected.
        colormap_vals: Dataframe column or none
            Data that are used to set the colormap value.
        colormap_name: string or none
            The name of the colormap which the scatter plot will be assigned
        plot_text: boolean
            Defaults to true, text is drawn. Option to turn off text (false)
        spearman: boolean
            Conditional statement for plotting spearman correlation coefficient
            (rho)
        fontsize: int
            Selects the fontsize of regression statistics
        pointsize: float/int
            Determines the size of the points for the scatter plot, default
            is 2.
        xlim: tuple
          The domain of the graph. Default set to (0,40).
        ylim: tuple
          The range of the graph. Default set to (0,40).

    Returns:
        out:
            The scatterplot
        lregression_plt:
            Linear regression line
        if plot_one_to_one==True: one_to_one_plot
            Dashed line with slope equal to unity to illustrate one-to-one
            correlation

    """
    pointsize = kwargs.get('point_size', 20)
    alpha = kwargs.get('point_alpha', 0.5)

    if text_position == 'upper_left':
        text_x = 0.05
        text_y = 0.90
        text_xdisplacement = 0
        text_ydisplacement = .08
    elif text_position == 'bottom_right':
        if fontsize > 16:
            text_x = .45
        else:
            text_x = 0.5
        text_y = 0.3
        text_xdisplacement = 0
        text_ydisplacement = .08
    else:
        sys.exit('Invalid text position. Options: upper_left, bottom_right')

    text_x = kwargs.get('plottext_xloc', (text_x))
    text_y = kwargs.get('plottext_yloc', (text_y))
    text_xdisplacement = kwargs.get('plottext_xdisplacement',
                                    (text_xdisplacement))
    text_ydisplacement = kwargs.get('plottext_ydisplacement',
                                    (text_ydisplacement))

    axScatter = ax  # Redefine within internal scope of Comparison_Plotter fun.

    # Plot scatterplot with colormap or with monochrome
    # Colormap is based on the input parameter the user gives
    if isinstance(colormap_vals, pd.core.series.Series):
        norm = mpl.colors.Normalize(vmin=0, vmax=100)
        plotobj = axScatter.scatter(xdata, ydata, s=pointsize, alpha=alpha,
                                    c=colormap_vals, cmap=colormap_name,
                                    norm=norm)
    else:
        # If a particular color is specified, use that color, otherwise use
        # default color scheme
        if monocolor is not None:
            plotobj = axScatter.scatter(xdata, ydata, color=monocolor,
                                        s=pointsize, alpha=alpha)
        else:
            plotobj = axScatter.scatter(xdata, ydata, s=pointsize, alpha=alpha)

    axScatter.set_xlabel(param_dict['xlabel'], fontsize=fontsize)
    axScatter.set_ylabel(param_dict['ylabel'], fontsize=fontsize)
    axScatter.tick_params(labelsize=detail_fontsize)
    axScatter.set_aspect('equal')
    axScatter.set_xlim(xlim[0], xlim[1])
    axScatter.set_ylim(ylim[0], ylim[1])

    # Linear Regression
    # -----------------
    # Pearson Coefficient, Spearman Correlation, and RMSE dependent on regress.
    if stats_df is not None:
        intercept = stats_df.loc[0, 'Intercept']
        slope = stats_df.loc[0, 'Slope']

        if pd.isna(intercept) and pd.isna(slope):
            plot_regression = False
            plot_n = False

    if plot_regression is True:
        s1 = pd.Series(xdata)
        s2 = pd.Series(ydata)

        if plot_trendline:
            try:
                trend_data = np.linspace(s1.min(), 1.2*s1.max(), 2)
                trendline_color = kwargs.get('trendline_color', 'k')
                trendline_alpha = kwargs.get('trendline_alpha', 0.65)
                axScatter.plot(trend_data, slope*trend_data + intercept,
                               color=trendline_color, alpha=trendline_alpha)
            except TypeError as e:
                print(e)

                return plotobj

        if np.sign(intercept) == -1:
            intercept_sign = ''
        else:
            intercept_sign = '+'

        linear_reg_str = '$y={:.2f}x$' + intercept_sign + '{:.2f}'

        text_alpha = kwargs.get('plottext_alpha', 0.8)
        text_size = kwargs.get('plottext_size', 0.9*fontsize)
        text_color = kwargs.get('plottext_color', 'k')

        # Plot linear regression equation
        axScatter.text(text_x, text_y,
                       linear_reg_str.format(slope, intercept),
                       transform=axScatter.transAxes, color=text_color,
                       alpha=text_alpha, size=text_size)

        # Pearson Correlation Coefficient
        r_square = stats_df.loc[0, 'R$^2$']
        axScatter.text(text_x - text_xdisplacement,
                       text_y - text_ydisplacement,
                       '$R^2={:.2f}$'.format(r_square),
                       transform=axScatter.transAxes, color=text_color,
                       alpha=text_alpha, size=text_size)

        # Spearman Correlation
        if plot_spearman is True:
            spearman_corr = s1.corr(s2, method='spearman')
            axScatter.text(text_x - 2*text_xdisplacement,
                           text_y - 2*text_ydisplacement,
                           '$\rho={:.2f}$'.format(spearman_corr),
                           transform=axScatter.transAxes, color=text_color,
                           alpha=text_alpha, size=text_size)

        # Root Mean Square Error
        if plot_rmse is True:
            RMSE = stats_df.loc[0, 'Sensor RMSE']

        if plot_spearman is False and plot_rmse is True:
            axScatter.text(text_x - 2*text_xdisplacement,
                           text_y - 2*text_ydisplacement,
                           '$RMSE={:.2f}$'.format(RMSE),
                           transform=axScatter.transAxes, color=text_color,
                           alpha=text_alpha, size=text_size)

        # ---------------------------------------------------------------------

    # If text is enabled, print the number of scatterplot points graphed
    if plot_n is True:
        n_count = int(stats_df.loc[0, 'N'])
        # place the text below Rsqr text by same coord diff
        axScatter.text(text_x - 3*text_xdisplacement,
                       text_y - 3*text_ydisplacement,
                       '$N= $'+str(n_count),
                       transform=axScatter.transAxes, color=text_color,
                       alpha=text_alpha, size=text_size)

    # One-to-one dashed line for reference
    if plot_one_to_one is True:
        one_to_one = np.linspace(int(ylim[0]), int(ylim[1]), int(10*ylim[1]))
        axScatter.plot(one_to_one, one_to_one, linestyle='--', color='grey',
                       alpha=0.7)

    if empty_plot is True:
        plotobj.set_visible(False)

    return plotobj


"""----------------------------------------------------------------------------

Primary figure plotting functions

----------------------------------------------------------------------------"""


def Scatter_Plotter(df_list, ref_df, stats_df=None, plot_subset=None,
                    param=None, sensor_name=None, figure_path=None,
                    write_to_file=True, xlim=(0, 40),
                    ylim=(0, 40), time_interval=None, text_pos='upper_left',
                    font_size=10, point_size=10, met_ref_df=None,
                    RH_colormap=True, tight_layout=False, plot_title=True,
                    filename_suffix='', plot_regression=True,
                    plot_trendline=True, plot_rmse=True,
                    plot_spearman=False, plot_n=True, title_text=None,
                    mono_color=None, alpha=.5, sensor_serials=None,
                    tick_spacing=5, ref_name=None, deploy_dict=None,
                    ax=None, fig=None, report_fmt=False, return_axs=False,
                    empty_plot=False, param_class=None, **kwargs):
    """Front-end function for creating scatter plots.

    Calls Comparison_Plotter for lower-end tasks and sets formatting for plots
    based off passed parameters.

    Args:
        df_list: list
            A list containing the sensor dataframes from which data is plotted
        ref_df: Pandas Dataframe
            Reference dataframe
        stats_df: Pandas Dataframe
            Regression statistics dataframe for the sensor evaluation set
        plot_subset: Nonetype or list of strings
            To plot a subset of evaluated sensors, pass a list of the sensor
            numbers ('1', '2', '3', etc.) as assigned in the sensor serial
            dictionary. For example, plotting a subset for sensors '1', '3',
            and '5' in an evaluation is achieved by passing
            plot_subset=['1', '3', '5'].
        param: string
            Column header name for the pollutant values to be plotted
        sensor_name: string
            Unformatted sensor name, passed to Formatted_Sensor_Name() for
            including formatted version on plot
        figure_path: string
            Path to directory where the figure will be saved
        palette: string
            Color palette assigned to relative-humidity colormapped scatter
            plot points
        write_to_file: Boolean
            If true, writes to file and figure is closed. False skips file
            writing and does not close the figure
        xlim: tuple
            The x-limits of the scatter plot
        ylim: tuple
            The y-limits of the scatter plot
        time_interval: string
            Either '1-hour' or '24-hour', included in title of plot
        text_pos: string
            Determines position of text. Can either pass 'upper_left' or '
            bottom_right'
        font_size: int or float
            The font size for the xlabel, ylabel, and plot text. Passed on to
            Comparison_Plotter() which uses 0.85*font_size for tick labels.
            -- Recommend 15 for one sensor, 14 for three sensors, 14 for eight
            sensors, 13 for nine sensors
        point_size: int or float
            The size of the scatterpoint plots
            -- Recommend ~ 20
        met_ref_df: Nonetype or Pandas dataframe
            Reference dataframe for met data. Used as an alternative to sensor
            met data for plotting colormap of relative humidity on scatterplot
            points. If passed, the reference met data takes precedence over
            any existing sensor met data.
        RH_colormap: Boolean
            If true, relative humidity values will be used as a colormap on the
            scatterplot points.
        tight_layout: Boolean
            Optional plot with matplotlib's "fig.tight_layout()"
        plot_title: Boolean
            True generates a title at the top of the plot
        fontweight: string
            Passed on to matplotlib fontweight (accepts 'normal', 'bold', etc.)
        detection_limited: Boolean
            Passing true plots data with values below the lower detection limit
            masked
        filename_suffix: string
            Optional string added to end of filename. Defaults to empty string.
        plot_text: boolean
            Pass on to underlying Comparison_Plotter function. Defaults to
            True. If false, text on plots will not be generated.
        plot_regression: boolean
            Pass on to underlying Comparison_Plotter function. Defaults to
            True. If false, regression lines on plots will not be generated.
        monocolor: string
            A single color (specified in hex) for scatter plots.
            Recommend #2251D0 (nice blue hue)
        param_class: string
            The parameter classification for the passed parameter to plot.
            E.g, if param is PM25, param_class = PM; if param is 03,
            param_class = Gases;if param is Temp, param_class = Met.

    Returns:
        If an axis is passed to Scatter_Plotter(), the modified axis with
        plotting detail filled in will be returned. Otherwise, none will be
        returned.
    """
    sns.set_style(kwargs.get('seaborn_style', 'darkgrid'))
    palette = kwargs.get('color_palette', 'seismic')
    sns.set_palette(palette)

    # Option to supply df_list indicies in list for subset of sensors to plot
    if plot_subset is not None:
        # limit dataframe list and sensor serials to selected sensors
        df_list = [df for i, df in enumerate(df_list, 1)
                   if str(i) in plot_subset]
        sensor_serials = {str(i): serial for i, serial in
                          enumerate(sensor_serials.values(), 1)
                          if str(i) in plot_subset}

    fmt_param, fmt_param_units = Format_Param_Name(param)
    fmt_sensor_name = sensor_name.replace('_', ' ')

    # For occasions where a dataframe is passed rather than a list
    if isinstance(df_list, list) is False:
        print('Warning: Dataframe passed to function is not in the form '
              'of a list\n')
        print('Continuing by placing passed dataframe into list')
        df_list = [df_list]

    number_of_sensors = len(df_list)

    fmt_tuple = Sensor_Subplot_Formatting(number_of_sensors, param, font_size,
                                          RH_colormap, report_fmt)

    (Nr, Nc, fig_size, suptitle_xpos, suptitle_ypos, title_textwrap,
     detail_fontsize, wspace, hspace, left, right, top, bottom,
     auto_filename_suffix, cbar_padding, cbar_aspect, font_size) = fmt_tuple

    font_size = kwargs.get('fontsize', font_size)
    detail_fontsize = kwargs.get('detail_fontsize', detail_fontsize)




    if (ax and fig) is None:
        # No axes object passed to function, create unique fig, axes objects
        fig, axs = plt.subplots(Nr, Nc, figsize=fig_size)
        unique_ax_obj = True
    else:
        # Axes object passed to function, set axes within scope of function to
        # passed axes object.
        axs = ax
        unique_ax_obj = False

    fig.subplots_adjust(wspace=kwargs.get('fig_wspace', wspace),
                        hspace=kwargs.get('fig_hspace', hspace),
                        left=kwargs.get('fig_left', left),
                        right=kwargs.get('fig_right', right),
                        top=kwargs.get('fig_top', top),
                        bottom=kwargs.get('fig_bottom', bottom))

    if plot_title is True:
        if title_text is not None:
            title_text = '\n'.join(wrap(title_text,
                                        kwargs.get('title_textwrap',
                                                   title_textwrap)))
            n_lines = len(title_text.split('\n'))
            if n_lines > 2:  # shift the figure down a tad if 3 or more lines
                font_size *= 0.9
                suptitle_ypos *= 1.03

            axs.set_title(title_text,
                          fontsize=font_size,
                          y=kwargs.get('title_yloc', suptitle_ypos),
                          x=kwargs.get('title_xloc', suptitle_xpos))
        else:
            title_text = fmt_sensor_name + ' vs. ' + ref_name + ' ' + \
                time_interval + ' ' + fmt_param
            title_text = '\n'.join(wrap(title_text,
                                        kwargs.get('title_textwrap',
                                                   title_textwrap)))
            n_lines = len(title_text.split('\n'))
            if n_lines > 2:  # shift the figure down a tad if 3 or more lines
                font_size *= 0.9
                suptitle_ypos *= 1.03

            if unique_ax_obj is True:
                fig.suptitle(title_text,
                             fontsize=font_size,
                             y=kwargs.get('title_yloc', suptitle_ypos),
                             x=kwargs.get('title_xloc', suptitle_xpos))
            else:
                axs.set_title(title_text,
                              fontsize=font_size,
                              y=kwargs.get('title_yloc', suptitle_ypos),
                              x=kwargs.get('title_xloc', suptitle_xpos))

    for i in range(Nr):
        for j in range(Nc):
            sensor_number = Nc*i + (j + 1)
            sensor_data_index = sensor_number - 1

            try:
                sensor_df = df_list[sensor_data_index]
            except IndexError:
                print('Sensor index', str(sensor_data_index),
                      'not in dataframe list')

                if len(axs.shape) > 1:
                    ax = axs[i, j]
                else:
                    ax = axs[i]

                ax.remove()
                break

            averaging_interval = sensor_df.index[1] - sensor_df.index[0]

            if (averaging_interval) == pd.Timedelta('1 days'):
                daily_df_obj = [sensor_df]
                hourly_df_obj = None
                hourly_ref_df = None
                daily_ref_df = ref_df

            if (averaging_interval) == pd.Timedelta('1 hour'):
                daily_df_obj = None
                hourly_df_obj = [sensor_df]
                hourly_ref_df = ref_df
                daily_ref_df = None

            if plot_regression is True:
                sensor_stats_df = Regression_Stats(hourly_df_obj=hourly_df_obj,
                                                   daily_df_obj=daily_df_obj,
                                                   hourly_ref_df=hourly_ref_df,
                                                   daily_ref_df=daily_ref_df,
                                                   deploy_dict=deploy_dict,
                                                   param=param,
                                                   serials=sensor_serials,
                                                   sensor_name=sensor_name)
            else:
                sensor_stats_df = None

            try:
                df = pd.DataFrame()
                df['ydata'] = sensor_df[param]
                df['xdata'] = ref_df[param + '_Value']
            except KeyError:
                print(ref_name + ' not in passed reference dataframe.')

            color = None  # variable passed to Comparison_Plotter as monocolor

            # Optional combine of RH data from AIRS and sensor, where the AIRS
            # data is preferred and sensor data used if AIRS RH not available
            if RH_colormap is True:
                if 'mean_RH' in sensor_df:
                    sensor_df = sensor_df.rename(columns={'mean_RH': 'RH'})

                if ((isinstance(met_ref_df, pd.DataFrame)) and
                   (met_ref_df['RH_Value'].dropna().empty is False)):
                    if 'RH' not in sensor_df:
                        sensor_df['RH'] = np.nan

                    # Ref RH data left join with sensor RH data
                    try:
                        df['RH'] = met_ref_df['RH_Value'].combine_first(
                          sensor_df['RH'])
                    except KeyError as missing_param:
                        print(missing_param,
                              'not found in met reference dataframe')

                    cmap_vals = df['RH']
                else:
                    df['RH'] = sensor_df['RH']
                    print('..Reference RH not found, internal sensor RH',
                          'shown in figure')
                    cmap_vals = df['RH']
            else:
                cmap_vals = None
                palette = None
                color = mono_color

            xdata = df['xdata']
            ydata = df['ydata']

            # Choose between serial ID and sensor number labels for legend
            if isinstance(sensor_serials, dict):
                lbl = list(sensor_serials.values())[sensor_number-1]
            else:
                lbl = 'Sensor ' + str(sensor_number)

            param_dict = {'xlabel': ref_name + ' ' + fmt_param + ' ' +
                          fmt_param_units,
                          'ylabel': lbl + ' ' + fmt_param + ' '
                          + fmt_param_units}

            # set appropriate plt axes array index based on # of sensors
            if isinstance(axs, np.ndarray):
                # More than one sensor, axes arranged in array structure
                if len(axs.shape) > 1:
                    ax = axs[i, j]
                else:
                    ax = axs[j]

                ax.set_title(lbl, fontsize=detail_fontsize)
            else:
                ax = axs
                param_dict['ylabel'] = 'Sensor ' + fmt_param + ' ' + \
                    fmt_param_units

            im = Comparison_Plotter(ax,
                                    xdata,
                                    ydata,
                                    param_dict,
                                    sensor_stats_df,
                                    sensor_data_index,
                                    text_position=text_pos,
                                    colormap_vals=cmap_vals,
                                    colormap_name=palette,
                                    monocolor=color,
                                    xlim=xlim,
                                    ylim=ylim,
                                    fontsize=font_size,
                                    detail_fontsize=detail_fontsize,
                                    plot_regression=plot_regression,
                                    plot_trendline=plot_trendline,
                                    plot_rmse=plot_rmse,
                                    plot_spearman=plot_spearman,
                                    plot_n=plot_n,
                                    alpha=alpha,
                                    empty_plot=empty_plot,
                                    **kwargs)

            ax.xaxis.set_major_locator(plt.MultipleLocator(tick_spacing))
            ax.yaxis.set_major_locator(plt.MultipleLocator(tick_spacing))

    # Plot colorbar
    if RH_colormap is True:
        try:
            ctitle = 'Relative Humidity (%)'
            cbar_orien = 'horizontal'
            cbar_size = 0.3

            if number_of_sensors == 1:
                cbar_size = 0.8
                if param == 'O3':
                    cbar_orien = 'vertical'
                    # axes positioning [x0, y0, width, height]
                    caxes_pos = [0.85, 0.15, 0.05, 0.66]
                    ctitle = '\n'.join(wrap(ctitle, 10))
                else:
                    if report_fmt is True:
                        caxes_pos = [0.25, 0.07, 0.50, 0.03]
                    else:
                        caxes_pos = [0.125, 0.05, 0.75, 0.03]
            if number_of_sensors == 3:
                caxes_pos = [0.37, 0.07, 0.26, 0.03]
            if number_of_sensors > 3:
                caxes_pos = [0.37, 0.57, 0.26, 0.02]

            cax = plt.axes(kwargs.get('colorbar_axespos', caxes_pos))
            cbar_orien = kwargs.get('colorbar_orientation', cbar_orien)

            print(im)
            cbar = fig.colorbar(im,
                                cax=cax,
                                orientation=cbar_orien,
                                pad=cbar_padding,
                                aspect=cbar_aspect,
                                shrink=cbar_size)
            cbar.ax.set_title(ctitle,
                              fontsize=detail_fontsize)
            cbar.ax.tick_params(labelsize=.8*font_size)

        # Error when all passed x or y data are empty. Do not write to file.
        except TypeError:
            write_to_file = False
            pass

    if tight_layout is True:
        fig.tight_layout()

    # Save image to folder at figure_path
    if write_to_file is True:

        # Sensor vs ref Temp or RH should be saved to the 'Met' subfolder,
        # modify param for correct file path
        if param_class == 'Met':
            param = param_class

        file_name = (sensor_name + '_vs_'
                     + ref_name).replace(r'/', '').replace('\\', '')

        file_path = figure_path + param + '\\' + file_name

        # if matplotlib axes object not passed to Scatter_Plotter, the figure
        # created will be for data at the averaging interval specified by
        # the time_interval variable. In this case, indicate the avg interval
        # in the filename
        if unique_ax_obj is True and report_fmt is False:
            file_path += '_' + time_interval
        if filename_suffix != '':
            file_path = file_path + '_' + filename_suffix
        else:
            file_path = file_path + '_' + auto_filename_suffix

        todays_date = Get_Date()
        file_path = file_path + '_' + todays_date + '.png'

        fig.savefig(file_path, dpi=300)
        plt.close()

    # Return the ax axes instance for iteration
    if report_fmt is True or unique_ax_obj is False:
        return ax

    # Return a unique axes instance
    if return_axs is True:
        return axs


def Sensor_Timeplot(df_list, ref_df, param=None, sensor_name=None,
                    figure_path=None, start=None, end=None, write_to_file=True,
                    sensor_serials=None, ref_name=None, time_interval=None,
                    return_mpl_obj=True, report_fmt=False, ax=None, fig=None,
                    **kwargs):
    """Generate a timeplot for a specified pollutant alongside FRM/FEM
    concentration values.

    Args:
        df_list: list of dataframes
            list of Pandas dataframes for evaluated sensors containing 1-hour
            averaged data.
        ref_df: Pandas dataframe
            Reference (regulatory) data, plotted as black line on timeplots
        param: string
            Column header name for the pollutant values to be plotted
        sensor_name: string
            Unformatted sensor name, passed to Formatted_Sensor_Name() for
            including formatted version on plot
        figure_path: string
            Path to directory where the figure will be saved
        color_palette: string
            Color palette assigned to relative-humidity colormapped scatter
            plot points
        fontsize: int or float
            The font size for the xlabel, ylabel, and plot text. Passed on to
            Comparison_Plotter() which uses 0.85*font_size for tick labels.
        start: string
            date ('yyyy-mm-dd' format) for beginning of timeseries plot
        end: string
            date ('yyyy-mm-dd' format) for end of timeseries plot
        ylim: tuple of floats/ints
            The y-limits of the plot
        yscale: string
            The scaling for the y-axis. Accepted values include 'linear',
            'log', 'symlog', 'logit', etc.
        write_to_file: bool
            If true, figure is written to file and interactive plot is closed
        date_interval: int
            Number of days between x-axis tick marks with mm-dd-yy timestamps
        title: bool
            To plot or not to plot (the title), that is the question.
        sensor_serials: Nonetype or dictionary
            Optional pass sensor serials dictionary to plot sensor serial IDs
            in the legend instead of numbered sensors.
        filename_suffix: string
            Optional string added to end of filename. Defaults to empty string.
        alpha:
            Set transparency of sensor and reference timeseries
        cmap_norm_range:
            Normalized range (0,1) for colormap hue selection. Limiting this
            range to something like (0.1, 0.9) is useful when using colormaps
            with high contrast extrema and a gradual change in hue is desired
            for plots.
        legend_fontscale:
            Relative scale of fontsize for text in the legend relative to label
            text.
        format_xaxis_weeks:
            Plot the timeseries x-axis (time) in increments of 1 week.
        figsize:
            Tuple for setting the figure size.

    Returns:

    """
    # Determine maximum concentration recorded during timeframe, use to set
    # default ylim
    max_list = [df.loc[start:end, param].max() for df in df_list]
    ref_max = ref_df.loc[start:end, param + '_Value'].max()
    max_list.append(ref_max)
    max_conc = max(max_list)

    # Get keyword argument values if specified, otherwise set default
    sns.set_style(kwargs.get('seaborn_style', 'darkgrid'))
    date_interval = kwargs.get('date_interval', 5)
    yscale = kwargs.get('yscale', 'linear')
    ylims = kwargs.get('ylims', (0, 1.25*max_conc))
    format_xaxis_weeks = kwargs.get('format_xaxis_weeks', False)
    figsize = kwargs.get('figsize', (16, 3.5))
    fontsize = kwargs.get('fontsize', 15)
    legend_fontscale = kwargs.get('legend_fontscale', 0.65)
    cmap_name = kwargs.get('cmap_name', 'Set1')
    cmap_norm_range = kwargs.get('cmap_normrange', (0, 0.4))
    show_title = kwargs.get('show_title', True)
    filename_suffix = kwargs.get('filename_suffix', '')

    # Performance target reporting template formatting for timeseries plots
    # Templates for PM2.5 and O3 evaluations
    if report_fmt is True:

        # PM2.5: Figure consists of two plots (1-hr and 24-hr averaged
        # timeseries [plots arranged as 2 rows, 1 column])
        if 'PM25' in param:
            fontsize = 10.5
            figsize = (10.15, 4.1)
            show_title = True

            # Scaling values for axes box
            box_xscale = kwargs.get('box_xscale', 0.45)  # Translate x-axis loc
            box_yscale = kwargs.get('box_yscale', 1.0)  # Translate y-axis loc
            box_wscale = kwargs.get('box_wscale', 1.0)  # Transform plot width
            box_hscale = kwargs.get('box_hscale', 1.12) # Transform plot height

            title_xpos = 0.5
            # x, y loc of legend (w.r.t axes obj)
            legend_pos = kwargs.get('legend_loc', (1.11, 1.29))
            columnspacing = 0.9  # Legend column spacing

        # O3: Figure consists of one timeseries plot (1-hr)
        # [plot arranged as 1 row, 1 column])
        elif 'O3' in param:
            fontsize = 11
            figsize = (10.16, 3.8)
            show_title = False

            box_xscale = kwargs.get('box_xscale', 1.1)  # Translate x-axis loc
            box_yscale = kwargs.get('box_yscale', 3.1)  # Translate y-axis loc
            box_wscale = kwargs.get('box_wscale', 1.02)  # Transform plot width
            box_hscale = kwargs.get('box_hscale', 0.67) # Transform plot height

            title_xpos = 0.5
            legend_pos = kwargs.get('legend_loc', (0.85, -0.55))
            columnspacing = 0.9

        # If report_fmt is requested by the parameter type is not PM2.5 or O3,
        # reassign report_fmt false so that generic formatting is selected.
        else:
            report_fmt = False

    # Generic figure formatting
    if report_fmt is False:
        box_xscale = kwargs.get('box_xscale', 1.0)
        box_yscale = kwargs.get('box_yscale', 1.2)
        box_wscale = kwargs.get('box_wscale', 0.94)
        box_hscale = kwargs.get('box_hscale', 0.94)

        title_xpos = kwargs.get('title_xloc', 0.5)
        legend_pos = kwargs.get('legend_loc', (1.06, 0.5))
        columnspacing = 1

    # Format the legend, determine how many columns to split legend into
    n_legend_objs = len(sensor_serials) + 1
    if n_legend_objs / 4 > 1:
        leg_ncol = 2
    else:
        leg_ncol = 1

    # Use only one legend column if serial IDs are long
    if max(len(i) for i in sensor_serials.values()) > 6:
        leg_ncol = 1

    if (ax and fig) is None:
        # No axes object passed to function, create unique fig, axes objects
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        unique_ax_obj = True
    else:
        # Axes object passed to function, set axes within scope of function to
        # passed axes object.
        ax = ax
        unique_ax_obj = False

    # Format parameter name and sensor name
    param_name_tup = Format_Param_Name(param)
    fmt_param, fmt_param_unit = param_name_tup
    fmt_sensor_name = sensor_name.replace('_', ' ')

    if show_title is True:
        title_str = (time_interval + " Averaged " + fmt_sensor_name + ' '
                     + fmt_param)
        ax.set_title(title_str, fontsize=fontsize*1.1, x=title_xpos)

    # Set the colormap and configure the range of hues that will be sampled
    colormap = plt.cm.get_cmap(cmap_name)
    cmap_lbound = cmap_norm_range[0]
    cmap_ubound = cmap_norm_range[1]
    colors = [colormap(i) for i in np.linspace(cmap_lbound, cmap_ubound,
              len(df_list))]
    ax.set_prop_cycle('color', kwargs.get('sensor_colors', colors))

    # Loop through sensor dataframes, check data present, plot data
    for i, df in enumerate(df_list):
        try:
            param_data = df[param]
        except KeyError as missing_param:
            print('...Warning', missing_param, 'not found in dataframe'
                  'at index ', str(i))
            continue

        # Choose between serial ID and sensor number labels for plot legend
        if sensor_serials:
            lbl = list(sensor_serials.values())[i]
        else:
            lbl = 'Sensor ' + str(i + 1)

        # Plot each sensor data time series
        ax.plot(df.index, param_data, label=lbl,
                alpha=kwargs.get('sensor_linealpha', .70),
                linewidth=kwargs.get('sensor_linewidth', 1.5),
                linestyle=kwargs.get('sensor_linestyle', '-'))

    # Plot timeseries for regulatory monitor corresponding to the pollutant
    ax.plot(ref_df.index,
            ref_df[param + '_Value'],
            label=ref_name,
            color=kwargs.get('ref_linecolor', 'k'),
            alpha=kwargs.get('ref_linealpha', .97),
            linewidth=kwargs.get('ref_linewidth', 1.5),
            linestyle=kwargs.get('ref_linestyle', '-'))

    # Configure x- and y-axis attributes (scale, labeling, limits, ticks)
    ax.set_yscale(yscale)
    ax.set_ylabel(fmt_param + ' ' + fmt_param_unit, fontsize=fontsize)
    ax.set_xlabel('Date', fontsize=fontsize)
    ax.set_xlim(start, end)
    if ylims:
        ax.set_ylim(ylims[0], ylims[1])
    ax.tick_params(labelsize=.75*fontsize)

    # Format x-axis by weeks (mark 'Week 1', 'Week 2', etc..)
    if format_xaxis_weeks is True:
        week_freq = 1  # Initially mark every week
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=week_freq))
        labels = [item.get_text() for item in ax.get_xticklabels()]

        # If the number of weekly labels exceeds 15, reduce weekly interval
        # until less than 15 left.
        while len(labels) > 15:
            week_freq += 1
            ax.xaxis.set_major_locator(mdates.WeekdayLocator(
                                                        interval=week_freq))
            labels = [item.get_text() for item in ax.get_xticklabels()]

        for i, label in enumerate(labels):
            labels[i] = 'Week ' + str(int(week_freq*i+1))

        ax.set_xticklabels(labels)
        ax.set_xlabel('Duration', fontsize=fontsize)
    # Format x-axis by date and time [MM-DD-YY] at specified date interval
    else:
        date_form = DateFormatter(kwargs.get('date_format', "%m-%d-%y"))
        ax.xaxis.set_major_formatter(date_form)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=date_interval))

    # Set legend position, wrap legend text to fit
    handles, labels = ax.get_legend_handles_labels()
    updated_labels = Wrap_Text(labels)
    ax.legend(handles, updated_labels, bbox_to_anchor=legend_pos, loc='center',
              fontsize=kwargs.get('legend_fontsize',
                                  fontsize*legend_fontscale),
              ncol=leg_ncol, columnspacing=columnspacing,
              handlelength=1.25)

    # Adjust axes dimensions to fit width and height of plot
    box = ax.get_position()
    ax.set_position([box.x0*box_xscale, box.y0*box_yscale,
                     box.width*box_wscale, box.height*box_hscale])

    if unique_ax_obj is True:
        subplot_adjust = kwargs.get('subplots_adjust',
                                    (0.05, 0.9, 0.90, 0.15))
        fig.subplots_adjust(left=subplot_adjust[0],
                            right=subplot_adjust[1],
                            top=subplot_adjust[2],
                            bottom=subplot_adjust[3])

    # Save image to folder at figure_path
    if write_to_file is True:
        todays_date = Get_Date()
        figure_path = (figure_path + param + '\\' + sensor_name +
                       '_timeseries_' + param + '_' + time_interval)

        # Optionally add suffix to filename
        if filename_suffix != '':
            figure_path = figure_path + '_' + filename_suffix

        # Indicate performance targets template formatted, remove time interval
        # info if multiple subplots for 1-hr, 24-hr data used
        if report_fmt is True or unique_ax_obj is False:
            figure_path = figure_path + '_' + 'report_fmt'
            figure_path = figure_path.replace('_' + time_interval, '')

        # Filename suffix for harmonized sensor datasets
        if param.startswith('corrected'):
            figure_path = figure_path + '_' + 'corrected'

        figure_path += '_' + todays_date + '.png'
        plt.savefig(figure_path, dpi=300)
        plt.close()

    if return_mpl_obj is True or report_fmt is True:
        return ax


def Ref_Dist_Plot(ref_df, param_name=None, rec_interval='1-hour', fontsize=18,
                  write_to_file=True, figure_path=None, filename_suffix=''):
    """Plot the distribution of reference values for the passed parameter.

    Args:

    Returns:

    """
    try:
        # Determine name of reference monitor from passed parameter name
        try:
            ref_name = ref_df[param_name + '_Method'].dropna().unique()[0]
        except IndexError:
            ref_name = 'Unspecified Reference'

        # Format the parameter name for plotting
        fmt_tuple = Format_Param_Name(param_name)
        fmt_param, fmt_param_units, fmt_ref_name = fmt_tuple

        # Construct plot instance
        fig, ax = plt.subplots(1, 1, figsize=(6, 5))
        sns.distplot(ref_df[ref_name].dropna(),
                     label=fmt_ref_name+' '+fmt_param, ax=ax)

        # Set axes attributes
        ax.set_xlabel('Reference ' + rec_interval + ' ' + fmt_param +
                      ' ' + fmt_param_units, fontsize=fontsize)
        ax.set_ylabel('Relative Probability', fontsize=fontsize)
        ax.tick_params(axis='both', labelsize=0.75*fontsize)
        plt.legend(fontsize=0.85*fontsize)

        if write_to_file is True:
            todays_date = Get_Date()
            figure_path = figure_path + ref_name + '_DistPlot_' + param_name \
                + '_' + todays_date
            if filename_suffix != '':
                figure_path = figure_path + '_' + filename_suffix
            figure_path += '.png'

            plt.tight_layout()
            plt.savefig(figure_path, dpi=300)
            plt.close()

    # Exception: Column name for reference monitor data not in passed df
    except KeyError as i:
        print(i, 'not found in passed reference dataframe')


def Deployment_Timeline_Plot(deployment_df, cmap_name='Dark2',
                             cmap_norm_range=(.0, .75), fontsize=10,
                             date_interval=1, figsize=(11, 7),
                             write_to_file=True, figure_path=None,
                             tight_layout=False):
    """

    More details about line 70-82 code on barh rounding at MatPlotLib
    documentation on Fancybox https://matplotlib.org/3.1.1/gallery/
    shapes_and_collections/fancybox_demo.html

    Other discrete colormaps: tab10_r, Dark2, Set2_r, tab20b

    Args:

    Returns:

    """
    unique_types = sorted(deployment_df['Sensor Name'].unique().tolist())

    colormap = plt.cm.get_cmap(cmap_name)
    cmap_lbound = cmap_norm_range[0]
    cmap_ubound = cmap_norm_range[1]
    colors = [rgb2hex(colormap(i)[:3]) for i in np.linspace(cmap_lbound,
                                                            cmap_ubound,
                                                            len(unique_types))]

    fig, ax = plt.subplots(1, 1, figsize=figsize)

    wspace = 0.0
    hspace = 0.1
    left = 0.1
    right = 0.99
    top = 0.89
    bottom = 0.1

    fig.subplots_adjust(wspace=wspace,
                        hspace=hspace,
                        left=left,
                        right=right,
                        top=top,
                        bottom=bottom)

    for sensor_type, c in zip(unique_types, colors):

        sensor_type_data = deployment_df.where(
                            deployment_df['Sensor Name'] ==
                            sensor_type).dropna()

        bdate = mdates.date2num(pd.to_datetime(sensor_type_data.Begin))
        edate = mdates.date2num(pd.to_datetime(sensor_type_data.End))
        duration = edate - bdate

        fmt_sensor_type = sensor_type.replace('_', ' ')

        ax.barh(sensor_type_data.Sensor_Serial, duration, .8,
                left=bdate, color=c, alpha=.8, label=fmt_sensor_type)
        ax.xaxis_date()

    ax.legend(fontsize=0.8*fontsize, loc='upper center',
              bbox_to_anchor=(0.5, 1.1), ncol=len(unique_types))

    # Pad the x-axis a little bit on either side of sensor deployment periods
    x_start = pd.to_datetime(
                mdates.num2date(ax.get_xlim()[0])).tz_localize(None)
    new_x_start = x_start - pd.offsets.MonthBegin(1)

    x_end = pd.to_datetime(
                mdates.num2date(ax.get_xlim()[1])).tz_localize(None)
    new_x_end = x_end + pd.offsets.MonthEnd(1)

    ax.set_xlim(new_x_start, new_x_end)

    ax.set_ylabel('Sensor Serial ID', fontsize=fontsize)
    ax.set_xlabel('Date (Month, Year)', fontsize=fontsize)
    ax.tick_params(labelsize=.65*fontsize, axis='y')
    ax.tick_params(labelsize=.85*fontsize, axis='x')

    # Format Date and Time as MM-DD-YY at specified date interval
    date_form = DateFormatter("%m/%y")
    ax.xaxis.set_major_formatter(date_form)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=date_interval))

    # Bit of code below via user 'gereleth' on Stack Overflow post:
    # https://stackoverflow.com/questions/58425392/bar-chart-with-rounded-
    # corners-in-matplotlib
    # Edited for use in rounding edges of sensor deployment duration plot
    new_patches = []

    for patch in reversed(ax.patches):
        bb = patch.get_bbox()
        color = patch.get_facecolor()
        p_bbox = FancyBboxPatch((bb.xmin, bb.ymin),
                                abs(bb.width), abs(bb.height),
                                boxstyle="round, pad=.03, rounding_size=.2",
                                ec="none", fc=color, mutation_scale=3)
        patch.remove()
        new_patches.append(p_bbox)

    for patch in new_patches:
        ax.add_patch(patch)

    if tight_layout is True:
        plt.tight_layout()

    if write_to_file is True:
        todays_date = Get_Date()
        figure_path = figure_path + '\\deployment_timeline_plot' + '_' \
            + todays_date + '.png'

        plt.savefig(figure_path, dpi=300)
        plt.close()


def Stats_Comparison_Plot(stats_df, metric, fontsize=15, cmap_name='Set1',
                          cmap_norm_range=(0, 1), param='PM25', path=None,
                          figsize=(12, 4), write_to_file=True,
                          QC_Cleaning='None', avg_int='Hourly'):
    """Plot all sensor values for passed metric on same figure to compare
    across device types.

    Args:

    Returns:

    """
    # Overall number of devices in stats dataframe
    device_list = sorted(stats_df['Sensor Name'].unique().tolist())
    # Preliminary # axes to plot based on number of devices
    n_ax = len(device_list)

    # Set number of colors to be based on overall number of devices in stats_df
    colormap = plt.cm.get_cmap(cmap_name)
    cmap_lbound = cmap_norm_range[0]
    cmap_ubound = cmap_norm_range[1]
    colors = [rgb2hex(colormap(i)[:3]) for i in np.linspace(cmap_lbound,
                                                            cmap_ubound,
                                                            n_ax)]

    # Filter stats_df to correspond to chosen averaging interval and QC
    stats_df = stats_df.where((stats_df['Averaging Interval'] == avg_int) &
                              (stats_df['QC_Cleaning'] == QC_Cleaning)
                              ).dropna()

    filtered_device_list = sorted(stats_df['Sensor Name'].unique().tolist())

    # Check if filtering reduced # of devices, filter colors so consistent with
    # color prior to filtering
    if device_list == filtered_device_list:
        n_ax = len(device_list)
    else:
        diff = list(set(device_list) - set(filtered_device_list))
        # place color vals into dict for iterating, color idx consistent with
        # device list idx
        color_dict = {i: color for i, color in enumerate(colors)}
        for name in diff:
            idx = device_list.index(name)
            color_dict.pop(idx)

        colors = list(color_dict.values())
        n_ax = len(colors)

    sns.set_context(rc={'patch.linewidth': 0.0, "lines.linewidth": 1.5})
    sensor_names = sorted(stats_df['Sensor Name'].unique().tolist())

    fig, axs = plt.subplots(1, n_ax, figsize=figsize)

    wspace = .0
    hspace = .1
    left = 0.07
    right = 0.93
    top = 0.89
    bottom = 0.1

    fig.subplots_adjust(wspace=wspace,
                        hspace=hspace,
                        left=left,
                        right=right,
                        top=top,
                        bottom=bottom)

    for i, sensor_name, fill_color in zip(range(0, n_ax), sensor_names,
                                          colors):

        fill_color = [fill_color]
        sensor_data = stats_df.where(
                        (stats_df['Sensor Name'] == sensor_name)).dropna()

        fmt_sensor_name = sensor_name.replace('_', ' ')
        sensor_data['Sensor Name'] = fmt_sensor_name

        n_sensors = len(sensor_data)

        if n_sensors < 5 or metric in ['CV (%)', r'RMSE ($\mu g/m^3$)']:
            sns.stripplot(x='Sensor Name', y=metric, palette=fill_color,
                          data=sensor_data, ax=axs[i], size=7, jitter=False)
        else:
            sns.boxplot(x='Sensor Name', y=metric,
                        data=sensor_data, ax=axs[i],
                        showmeans=True, palette=fill_color,
                        meanprops={"marker": "d",
                                   "markerfacecolor": "#cccccc",
                                   'markeredgecolor': '#6f6f6f'})

        boxes = []

        if metric == 'R$^2$':
            if param == 'PM25':
                ymin, ymax = -0.02, 1.01
                hline_y, hline_xmin, hline_xmax = 1.0, -0.75, 0.75
                rec_x0, rec_y0, rec_xspan, rec_yspan = -0.75, 0.7, 1.5, 0.3
            if param == 'O3':
                ymin, ymax = 0.7, 1.02
                hline_y, hline_xmin, hline_xmax = 1.0, -0.75, 0.75
                rec_x0, rec_y0, rec_xspan, rec_yspan = -0.75, 0.8, 1.0, 0.2

        if metric == 'Slope':
            if param == 'PM25':
                ymin, ymax = -1.0, 3
                hline_y, hline_xmin, hline_xmax = 1.0, -0.75, 0.75
                rec_x0, rec_y0, rec_xspan, rec_yspan = -0.75, 0.65, 1.5, 0.7
            if param == 'O3':
                ymin, ymax = 0.0, 2.0
                hline_y, hline_xmin, hline_xmax = 1.0, -0.75, 0.75
                rec_x0, rec_y0, rec_xspan, rec_yspan = -0.75, 0.8, 1.5, 0.4

        if metric == 'Intercept':
            if param == 'PM25':
                ymin, ymax = -10.0, 10.0
                hline_y, hline_xmin, hline_xmax = 0.0,  -0.75, 0.75
                rec_x0, rec_y0, rec_xspan, rec_yspan = -0.75, -5, 1.5, 10.0
            if param == 'O3':
                ymin, ymax = -10.0, 10.0
                hline_y, hline_xmin, hline_xmax = 0.0,  -0.75, 0.75
                rec_x0, rec_y0, rec_xspan, rec_yspan = -0.75, 5.0, 1.5, 10.0

        if metric == 'CV (%)':
            if param == 'PM25':
                ymin, ymax = 0.0, 50
                if QC_Cleaning == 'None':
                    ymin, ymax = 0.1, 2000
                    axs[i].set_yscale('log')
                hline_y, hline_xmin, hline_xmax = 0.0,  -0.75, 0.75
                rec_x0, rec_y0, rec_xspan, rec_yspan = -0.75, 0.0, 1.5, 30.0
            if param == 'O3':
                ymin, ymax = 0.0, 35.0
                hline_y, hline_xmin, hline_xmax = 0.0,  -0.75, 0.75
                rec_x0, rec_y0, rec_xspan, rec_yspan = -0.75, 0.0, 1.5, 30.0

        if metric == r'RMSE ($\mu g/m^3$)':
            if param == 'PM25':
                ymin, ymax = 0.0, 12.0
                if QC_Cleaning == 'None':
                    ymin, ymax = 0.1, 200
                    axs[i].set_yscale('log')
                hline_y, hline_xmin, hline_xmax = 0.0,  -0.75, 0.75
                rec_x0, rec_y0, rec_xspan, rec_yspan = -0.75, 0.0, 1.5, 7.0
            if param == 'O3':
                ymin, ymax = 0.0, 12.0
                hline_y, hline_xmin, hline_xmax = 0.0,  -0.75, 0.75
                rec_x0, rec_y0, rec_xspan, rec_yspan = -0.75, 5.0, 1.5, 5.0

        if i == 0:
            axs[i].set_ylabel(metric, fontsize=fontsize)
        else:
            axs[i].set_ylabel('')
            axs[i].yaxis.set_major_formatter(plt.NullFormatter())

        axs[i].tick_params(labelsize=0.8*fontsize, axis='both')

        axs[i].set_xlabel('')

        axs[i].set_ylim(ymin, ymax)
        # Horizontal line for target goal
        axs[i].hlines(y=hline_y, xmin=hline_xmin, xmax=hline_xmax,
                      linewidth=1.5, color='#8b8b8b')
        axs[i].set_xlim(-.75, .75)
        # Box for target range
        rec_box = Rectangle((rec_x0, rec_y0),
                            rec_xspan,
                            rec_yspan,
                            color='r')
        boxes.append(rec_box)
        pc = PatchCollection(boxes, facecolor='#8b8b8b', alpha=.3)
        axs[i].add_collection(pc)

    if write_to_file is True:
        todays_date = Get_Date()
        if metric == 'CV (%)':
            metric = 'CV'
        if metric == r'RMSE ($\mu g/m^3$)':
            metric = 'RMSE'
        if QC_Cleaning == 'None':
            QC_tag = 'NoQC'
        if QC_Cleaning == 'Yes, Custom':
            QC_tag = 'CustomQC'
        figure_path = path + metric + '_' + 'comparison' + '_' \
            + QC_tag + '_' + avg_int + '_' + todays_date
        figure_path += '.png'
        plt.savefig(figure_path, dpi=300)
        plt.close()


def Plot_Performance_Metrics(stats_df, deploy_dict, param=None,
                             param_averaging=None,
                             font_size=12, path=None, sensor_name=None,
                             write_to_file=True, **kwargs):
    """

    Args:

    Returns:

    """
    sns.set_style('darkgrid')

    eval_params = ['PM25', 'O3']
    if param not in eval_params:
        sys.exit('Performance metrics and target values not set for ' + param)

    plotting_dims = {'PM25':
                     {'ylims': {'rsqr': (-0.02, 1.02),
                                },
                      'hline_dims': {'rsqr': (1.0, -0.50, 1.50),
                                     'slope': (1.0, -0.50, 1.50),
                                     'intercept': (0.0, -0.50, 1.50),
                                     'cv': (0.35, -0.50, 1.50),
                                     'rmse': (0.10, -0.50, 1.50),
                                     'nrmse': (0.35, -0.50, 1.50),
                                     'sd': (0.05, -0.50, 1.50)},
                      'box_dims': {'rsqr': (-0.5, 0.7, 2.0, 0.3),
                                   'slope': (-0.5, 0.65, 2.0, 0.7),
                                   'intercept': (-0.5, -5.0, 2.0, 10),
                                   'cv': (-0.5, 0.0, 2.0, 30.0),
                                   'rmse': (-0.5, 0, 2, 7),
                                   'nrmse': (-0.5, 0, 2, 30),
                                   'sd': (-0.5, 0.0, 2.0, 5.0)}
                      },
                     'O3':
                     {'ylims': {'rsqr': (-0.02, 1.02),
                                },
                      'hline_dims': {'rsqr': (1, -1, 1),
                                     'slope': (1, -1, 1),
                                     'intercept': (0, -1, 1),
                                     'cv': (0.35, -1, 1),
                                     'rmse': (0.10, -1, 1),
                                     'nrmse': (0.35, -1, 1),
                                     'sd': (0.05, -1, 1)},
                      'box_dims': {'rsqr': (-1, 0.8, 2.0, 0.2),
                                   'slope': (-1, 0.8, 2.0, 0.4),
                                   'intercept': (-1, -5.0, 2.0, 10),
                                   'cv': (-1, 0.0, 2.0, 30.0),
                                   'rmse': (-1, 0.0, 2.0, 5.0),
                                   'nrmse': (-1, 0, 2, 30),
                                   'sd': (-1, 0.0, 2.0, 5.0)}
                      }
                     }

    param_dims = plotting_dims.get(param)

    cv_vals = {interval: [] for interval in param_averaging}
    std_vals = {interval: [] for interval in param_averaging}
    rmse_vals = {interval: [] for interval in param_averaging}
    nrmse_vals = {interval: [] for interval in param_averaging}

    interval_to_freq = {'1-hour': 'Hourly',
                        '24-hour': 'Daily'}

    # List of frequencies ('Hourly, Daily') for specified parameter
    param_freq = [interval_to_freq[interval] for interval in param_averaging]

    # Extract metric values into metric dictionaries
    for group in deploy_dict['Deployment Groups']:
        param_stats = deploy_dict['Deployment Groups'][group][param]
        for interval in param_averaging:
            freq = interval_to_freq[interval].lower()
            cv_vals[interval].append(
                                param_stats['Precision']['cv_' + freq])
            std_vals[interval].append(
                                param_stats['Precision']['std_' + freq])
            rmse_vals[interval].append(
                                param_stats['Error']['rmse_' + freq])
            nrmse_vals[interval].append(
                                param_stats['Error']['nrmse_' + freq])

    # Boxplot fill colors
    default_fill = ['#80c5c9', '#4ea1c0']
    fill_color = kwargs.get('fill_color', default_fill)

    # Marker properties
    marker = kwargs.get('marker', 'o')
    marker_size = kwargs.get('marker_size', 7)
    marker_line_width = kwargs.get('marker_line_width', 1)
    mean_marker = kwargs.get('mean_marker', 'd')

    fig_width = kwargs.get('figure_width', 15.7)
    fig_height = kwargs.get('figure_height', 3.9)
    fig, axs = plt.subplots(1, 7, figsize=(fig_width, fig_height))

    n_sensors = stats_df.where((stats_df['Sensor Name'].notna()) &
                               (stats_df['R$^2$'].notna())
                               ).Sensor_Number.nunique()

    metric_names = ['R$^2$', 'Slope', 'Intercept', 'RMSE',
                    'nRMSE', 'CV (%)', 'Standard Deviation']

    stats_df = stats_df[['R$^2$', 'Slope', 'Intercept', 'Averaging Interval']]
    stats_df = stats_df.where(stats_df['Averaging Interval'].isin(param_freq))

    for interval, freq in zip(param_averaging, param_freq):
        header = 'Averaging Interval'
        stats_df[header] = stats_df[header].str.replace(freq, interval)

    for ax_idx, metric_name in enumerate(metric_names):
        with sns.plotting_context(context="notebook", font_scale=1):
            if metric_name in ['R$^2$', 'Slope', 'Intercept']:
                axs[ax_idx].set_title(stats_df.columns[ax_idx],
                                      fontsize=font_size)

                if n_sensors > 3:
                    sns.boxplot(x='Averaging Interval', y=metric_name,
                                data=stats_df,
                                order=param_averaging,
                                ax=axs[ax_idx],
                                palette=fill_color,
                                showmeans=True,
                                meanprops={"marker": mean_marker,
                                           "markerfacecolor": "#8b8b8b",
                                           'markeredgecolor': '#6f6f6f'})
                else:
                    sns.swarmplot(x='Averaging Interval', y=metric_name,
                                  data=stats_df,
                                  order=param_averaging,
                                  ax=axs[ax_idx],
                                  palette=fill_color,
                                  marker=marker,
                                  linewidth=marker_line_width,
                                  size=marker_size)

            else:

                if metric_name == 'CV (%)':
                    metric_data = cv_vals
                if metric_name == 'Standard Deviation':
                    metric_data = std_vals
                if metric_name == 'RMSE':
                    metric_data = rmse_vals
                if metric_name == 'nRMSE':
                    metric_data = nrmse_vals

                data_df = pd.DataFrame(metric_data).T.reset_index()
                data_df.columns = ['Averaging Interval', metric_name]

                sns.stripplot(x='Averaging Interval',
                              y=metric_name,
                              data=data_df,
                              order=param_averaging,
                              ax=axs[ax_idx],
                              palette=fill_color,
                              s=marker_size,
                              marker=marker,
                              linewidth=marker_line_width,
                              jitter=False)

            boxes = []

            if metric_name == 'R$^2$':
                dim_key = 'rsqr'
                lower_lim = None
                upper_lim = None

            if metric_name == 'Slope':
                dim_key = 'slope'
                upper_lim = abs(1.5*stats_df[metric_name]).max()
                lower_lim = 1.5*stats_df[metric_name].min()

                if upper_lim < 2.0 and upper_lim > 0.25:
                    upper_lim = 2.0
                elif upper_lim < 0.25:
                    upper_lim = 2.5

                if lower_lim > 0:
                    lower_lim = -1*upper_lim + 2
                else:
                    lower_lim = 1.5*lower_lim

            if metric_name == 'Intercept':
                dim_key = 'intercept'
                upper_lim = abs(1.5*stats_df[metric_name]).max()
                if upper_lim < 10:
                    upper_lim = 10
                lower_lim = -1*upper_lim

                if param == 'PM25':
                    metric_name = r'Intercept ($\mu g/m^3$)'
                if param == 'O3':
                    metric_name = 'Intercept (ppbv)'

            if metric_name == 'CV (%)':
                dim_key = 'cv'
                lower_lim = 0
                upper_lim = 1.5*data_df[metric_name].max()
                if upper_lim < 50:
                    upper_lim = 50

            if metric_name == 'RMSE':
                dim_key = 'rmse'
                upper_lim = 1.5*data_df[metric_name].max()
                lower_lim = 0
                if upper_lim < 10:
                    upper_lim = 10

                metric_name = r'RMSE ($\mu g/m^3$)'

            if metric_name == 'nRMSE':
                dim_key = 'nrmse'
                lower_lim = 0
                if upper_lim < 50:
                    upper_lim = 50
                metric_name = r'nRMSE ($\%$)'

            if metric_name.startswith('Standard Deviation'):
                dim_key = 'sd'
                lower_lim = 0
                upper_lim = 1.5*data_df[metric_name].max()
                metric_name = r'Standard Dev. ($\mu g/m^3$)'

                if upper_lim < 10:
                    upper_lim = 10

            # Get formatting values
            ylims = kwargs.get(dim_key + '_ylims',
                               param_dims['ylims'].get(dim_key,
                                                       (lower_lim, upper_lim)))
            hline_dims = kwargs.get(dim_key + '_hline_dims',
                                    param_dims.get('hline_dims').get(dim_key))
            box_dims = kwargs.get(dim_key + '_box_dims',
                                  param_dims.get('box_dims').get(dim_key))

            # Assign to local variables
            ymin, ymax = ylims
            hline_y, hline_xmin, hline_xmax = hline_dims
            rec_x0, rec_y0, rec_xspan, rec_yspan = box_dims


            if param == 'PM25':
                axs[ax_idx].set_xlim(-.5, 1.5)
            if param == 'O3':
                axs[ax_idx].set_xlim(-1, 1)

            axs[ax_idx].hlines(y=hline_y, xmin=hline_xmin,
                               xmax=hline_xmax, linewidth=1.5,
                               color=kwargs.get('hline_color', '#8b8b8b'))

            target_rec = Rectangle((rec_x0, rec_y0),
                                   rec_xspan, rec_yspan, color='r')
            boxes.append(target_rec)
            pc = PatchCollection(boxes, alpha=.3,
                                 facecolor=kwargs.get('box_facecolor',
                                                      '#8b8b8b'))
            axs[ax_idx].add_collection(pc)
            axs[ax_idx].set_title(metric_name, fontsize=font_size)
            axs[ax_idx].set_ylim(ymin, ymax)
            axs[ax_idx].yaxis.set_label_text('')

        plt.tight_layout()
        sns.set(font_scale=kwargs.get('font_scale', 1))

    fig.subplots_adjust(wspace=kwargs.get('fig_wspace', 0.35),
                        hspace=kwargs.get('fig_hspace', 0.1),
                        left=kwargs.get('fig_left', 0.03),
                        right=kwargs.get('fig_right', 0.97),
                        top=kwargs.get('fig_top', 0.93),
                        bottom=kwargs.get('fig_bottom', 0.13))

    if write_to_file is True:
        todays_date = Get_Date()

        plt.savefig(path + param + '\\' + sensor_name + '_regression_boxplot_'
                    + param + '_' + todays_date + '.png', dpi=300)
        plt.close()


def Met_Distrib(met_ref_data, figure_path, sensor_name=None,
                write_to_file=True):
    """Create distribution plots for meteorological parameters provided in the
    passed met_ref_data dataframe.


    Args:

    Returns:

    """
    fontsize = 10
    detail_fontsize = 0.8*fontsize
    n_var = len(met_ref_data.count())  # Number of met variables to plot
    fig, axs = plt.subplots(1, n_var, figsize=(5.15, 2.54))
    fill_color = [['#77529A'], ['#b06c8b'], ['#588ded']]
    plt.suptitle('Evaluation Site Meteorological Conditions\n',
                 fontsize=fontsize)  #'R.M. Young 41382VC'

    fig.subplots_adjust(wspace=.6,
                        hspace=.3,
                        left=.12,
                        right=.88,
                        top=.86,
                        bottom=.17)

    for i in range(n_var):
        param = met_ref_data.columns[i]
        sns.distplot(met_ref_data[param].dropna(),
                     ax=axs[i],
                     bins=15,
                     color=fill_color[i][0],
                     hist_kws={'alpha': 0.6})

        if param == 'RH_Value':
            axs[i].set_xlabel('Relative Humidity (%)',
                              fontsize=detail_fontsize)
            axs[i].xaxis.set_major_locator(plt.MultipleLocator(25))

        if param == 'Temp_Value':
            axs[i].set_xlabel('Temperature ($\\degree$C)',
                              fontsize=detail_fontsize)
            axs[i].xaxis.set_major_locator(plt.MultipleLocator(10))

        if param == 'DP_Value':
            axs[i].set_xlabel('Dew Point ($\\degree$C)',
                              fontsize=detail_fontsize)

        axs[i].set_ylabel('Relative Probability',
                          fontsize=detail_fontsize)

        axs[i].tick_params(axis='both', labelsize=detail_fontsize)

    if write_to_file is True:
        todays_date = Get_Date()
        file_path = figure_path + 'Met' + '\\' + sensor_name + '_'\
            'met_distplot_report_fmt' + '_' + todays_date
        plt.savefig(file_path + '.png', dpi=300)
        plt.close()


def Normalized_Met_Scatter(df_list, ref_df, avg_df, met_ref_df=None,
                           figure_path=None,
                           param='PM25', met_param=None, sensor_name=None,
                           xlim=None, ylim=None, point_size=10,
                           plot_error_bars=True,
                           write_to_file=True, fontsize=12, alpha=0.5,
                           plot_legend=True, fig_size=(8, 4),
                           sensor_serials=None, cmap_name='Set1',
                           cmap_norm_range=(0, 1), ref_name=None,
                           report_fmt=False, fig=None, ax=None,
                           empty_plot=False, custom_adjust=None,
                           return_mpl_obj=False, colors=None):
    """Plot parameter values normalized by reference values against either
    temperature or relative humidity.

    Args:

    Returns:

    """
    if met_ref_df[met_param + '_Value'].dropna().empty:
        sys.exit('Reference ' + met_param + ' not found in dataframe')
    # Set xlim and ylim if not specified
    if xlim is None or ylim is None:
        xlim, ylim = Met_Scatter_Lims(met_data=met_ref_df,
                                      met_param=met_param,
                                      xlims=xlim, ylims=ylim,
                                      serials=sensor_serials,
                                      eval_param=param,
                                      avg_df=avg_df)
    if param == 'Temp':
        met_param = 'Temp'
    if param == 'RH':
        met_param = 'RH'
    elif met_param is None:
        print('Enter valid parameter for met_param: Either Temp or RH')

    if (ax and fig) is None:
        # No axes object passed to function, create unique fig, axes objects
        fig, ax = plt.subplots(1, 1, figsize=fig_size)
        unique_ax_obj = True
    else:
        # Axes object passed to function, set axes within scope of function to
        # passed axes object.
        ax = ax
        unique_ax_obj = False

    # Retreive formatted version of sensor and parameter name
    fmt_sensor_name = sensor_name.replace('_', ' ')

    fmt_met_tuple = Format_Param_Name(met_param)
    fmt_met_param, fmt_met_units = fmt_met_tuple

    try:
        met_ref_name = met_ref_df[met_param + '_Method'].dropna().unique()[0]
    except IndexError:
        met_ref_name = 'Unspecified Reference'

    x_label = met_ref_name + ' ' + fmt_met_param + ' ' + fmt_met_units

    fmt_param_tuple = Format_Param_Name(param)
    fmt_param, fmt_param_units = fmt_param_tuple
    title = fmt_sensor_name + ' ' + fmt_param + ' Normalized by '\
        + ref_name

    labels = [title]
    labels = Wrap_Text(labels, max_label_len=40)
    title = labels[0]

    param_dict = {'xlabel': x_label,
                  'ylabel': ''}

    # Compute normalized dataframes
    norm_df_list = Normalize(df_list, ref_df, param, ref_name)

    # Plot 1:1 normalization line
    ax.axhline(y=1.0, linewidth=1.5, color='#8b8b8b', alpha=.8)

    # Set colormap and assign number of discrete colors from colormap
    if len(sensor_serials) <= 3:
        cmap_name = 'Set1'
        cmap_norm_range = (0, 0.4)
    if colors is None:
        colormap = plt.cm.get_cmap(cmap_name)
        cmap_lbound, cmap_ubound = cmap_norm_range[0], cmap_norm_range[1]
        colors = [colormap(i) for i in np.linspace(cmap_lbound, cmap_ubound,
                  len(norm_df_list))]
    ax.set_prop_cycle('color', colors)

    # If the normalized param is temp or RH, the ref_df will be the met_ref_df
    if 'Temperature' in ref_df or 'Relative_Humid' in ref_df:
        met_ref_df = ref_df

    # Generate scatter plots for each normalized sensor dataset
    legend_list = ['1:1']
    for i, (df, sensor_n) in enumerate(zip(norm_df_list, sensor_serials)):
        compare_df = pd.DataFrame()
        compare_df[met_param] = met_ref_df[met_param + '_Value']
        compare_df['Normalized_' + param] = df['Normalized_' + param]
        xdata = compare_df[met_param]
        ydata = compare_df['Normalized_'+param]

        if ydata.dropna().empty is True:
            continue

        Comparison_Plotter(ax, xdata, ydata, param_dict, xlim=xlim, ylim=ylim,
                           pointsize=point_size, fontsize=fontsize,
                           alpha=alpha, plot_regression=False, plot_n=False,
                           plot_rmse=False, plot_spearman=False,
                           plot_one_to_one=False, plot_trendline=False,
                           empty_plot=empty_plot)

        ax.set_title(title, fontsize=fontsize, pad=6)

        # Choose between serial ID and sensor number labels for plot legend
        if sensor_serials is not None:
            lbl = list(sensor_serials.values())[i]
        else:
            lbl = 'Sensor ' + str(i + 1)
        legend_list.append(lbl)

    # Axes object position, dimensions ----------------------------------------
    box = ax.get_position()

    if len(sensor_serials)/8 > 1:
        leg_cols = 2
        col_spacing = 0.8
        if unique_ax_obj is True and report_fmt is True:
            ax.set_position([box.x0*0.75, box.y0, box.width*0.85, box.height])
    else:
        leg_cols = 1
        col_spacing = 0.8
        if unique_ax_obj is True and report_fmt is True:
            ax.set_position([box.x0, box.y0, box.width * 0.90, box.height])

    # Set the ratio of plot dimensions to 2:1
    ratio = 0.5
    xleft, xright = ax.get_xlim()
    ybottom, ytop = ax.get_ylim()
    ax.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)

    ax.set_yticks(np.arange(round(ybottom), round(ytop + 1), 1))

    # Adjust axes dimensions to fit width and height of plot
    if unique_ax_obj is True and report_fmt is True:
        # Adjustments for single plot
        top = 0.9
        bottom = 0.13
        left = 0.04
        right = 0.86
        hspace = 0.20
        wspace = 0.20
        legend_pos = (1.02, 0.5)
        legend_fontsize = 0.70*fontsize
        legend_loc = 'center left'  # position legend based on its center left

    elif custom_adjust is None:
        # axes adjustments for PT report formatted multi-axes plot
        top = 0.95
        bottom = 0.4
        left = 0.05
        right = 0.95
        hspace = 0.20
        wspace = 0.25
        legend_pos = (.5, -0.65)
        legend_fontsize = 0.8*fontsize
        legend_loc = 'center'  # position the legend based on its center
    else:
        custom_adjust = list(custom_adjust.values())
        top = custom_adjust[0]
        bottom = custom_adjust[1]
        left = custom_adjust[2]
        right = custom_adjust[3]
        hspace = custom_adjust[4]
        wspace = custom_adjust[5]
        legend_pos = custom_adjust[6]
        legend_fontsize = 0.8*fontsize
        legend_loc = 'center'  # position the legend based on its center

    fig.subplots_adjust(wspace=wspace,
                        hspace=hspace,
                        left=left,
                        right=right,
                        top=top,
                        bottom=bottom)

    # Error bars --------------------------------------------------------------
    all_sensor_data = pd.DataFrame()
    for i, df in enumerate(norm_df_list, 1):
        sensor_data = df['Normalized_' + param]
        all_sensor_data[param + '_sensor_' + str(i)] = sensor_data
    ydata = all_sensor_data

    if plot_error_bars is True:
        Plot_Error_Bars(xdata, ydata, ax, n_xbins=10,
                        plot_yerror=True, errorbar_c='#151515')

    # Legend position ---------------------------------------------------------
    if plot_legend is True:
        ax.legend(legend_list, fontsize=legend_fontsize, loc=legend_loc,
                  bbox_to_anchor=legend_pos, ncol=leg_cols,
                  columnspacing=col_spacing)

    # Write plot to file ------------------------------------------------------
    if write_to_file is True:
        todays_date = Get_Date()
        figure_path = figure_path + param + '\\' + sensor_name +\
            '_normalized_' + param + '_vs_' + met_param

        # Indicate performance targets template formatted
        if report_fmt is True:
            if unique_ax_obj is False:
                figure_path = figure_path.replace('_vs_' + met_param, '_met')
            figure_path = figure_path + '_' + 'report_fmt'

        # Filename suffix for harmonized sensor datasets
        if param.startswith('corrected'):
            figure_path = figure_path + '_' + 'corrected'

        figure_path += '_' + todays_date + '.png'
        plt.savefig(figure_path, dpi=300)
        plt.close()

    if return_mpl_obj is True or report_fmt is True:
        return ax


def Met_Scatter_Lims(met_data, met_param, xlims, ylims, serials, eval_param,
                     avg_df):
    """

    Args:

    Returns:

    """
    # Automatically generate x-axis limits if none specified
    if xlims is None:
        xmax = met_data[met_param + '_Value'].max()
        xmin = met_data[met_param + '_Value'].min()

        xmax = round(xmax, -1)
        xmin = math.floor(xmin)
    else:
        xmin, xmax = xlims[0], xlims[1]

    # Automatically generate y-axis limits if none specified
    if ylims is None:
        ymin = avg_df[
                    'mean_Normalized_' + eval_param].quantile(0.01)
        ymax = avg_df[
                    'mean_Normalized_' + eval_param].quantile(0.99)
        if ymax < 5.0:
            rounding_place = 1  # round to nearest tenths place
        else:
            rounding_place = -1  # round to nearest tens place

        ymin = math.floor(ymin) - 0.1*ymin
        ymax = round(ymax, rounding_place) + 0.1*ymax

        if ymin == ymax == 0:
            ymin, ymax = -0.1, 1.1
        if ymin < 0.1 and ymin > -.1:
            ymin = -0.5
        if ymax < 1.0:
            ymin = -1*ymax
            ymax = 1.1
    else:
        ymin, ymax = ylims[0], ylims[1]

    return (xmin, xmax), (ymin, ymax)


def Recording_Interval_Histogram(full_df_list, xmin=-10, xmax=120,
                                 bar_width=2, bar_alpha=.4):
    """Plot indicating the uneven time delta in sensor data.

    Graphs bar plot of Log(counts) vs. time delta b/w conseq points

    Args:

    Returns:

    """
    if len(full_df_list) == 3:
        color_list = ['#1f77b4', '#d62728', '#9467bd']  # blue, red, purple
    else:
        color_list = ['#9F99C8', '#fb8072', '#80b1d3', '#8dd3c7',
                      '#ffffb3', '#FD9962', '#b3de69']

    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    for color, df in zip(color_list, full_df_list):
        idx_name = df.index.name
        delta = (df.index[1:] - df.index[0:-1]).to_frame()
        ax.bar(delta[idx_name].value_counts().index.total_seconds(),
               np.log10(delta[idx_name].value_counts().values),
               width=bar_width, alpha=bar_alpha, edgecolor='none',
               color=color)
        ax.set_xlim(xmin, xmax)

    ax.set_xlabel(r'$\Delta t$ (seconds)')
    ax.set_ylabel(r'Log$_{10}$(counts)')
