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
  Wed Jul 28 14:19:13 2021
"""
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import rgb2hex
import seaborn as sns
from sensortoolkit.param import Parameter
from sensortoolkit.datetime_utils import get_todays_date
from sensortoolkit.plotting import wrap_text, get_colormap_range
from sensortoolkit.deploy import get_max_conc
register_matplotlib_converters()


def sensor_timeplot(df_list, ref_df, param=None, sensor_name=None,
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
            Draw_Scatter() which uses 0.85*font_size for tick labels.
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
    max_conc = get_max_conc(param, df_list=df_list, ref_df=ref_df,
                       start=start, end=end)

    cmap_range = get_colormap_range(df_list)


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
    cmap_norm_range = kwargs.get('cmap_normrange', cmap_range)
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
    param_obj = Parameter(param)
    param_name = param_obj.name
    fmt_param = param_obj.format_name
    fmt_param_units = param_obj.units
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
    ax.set_ylabel(fmt_param + ' ' + fmt_param_units, fontsize=fontsize)
    ax.set_xlabel('Date', fontsize=fontsize)

    ax.set_xlim(pd.to_datetime(start), pd.to_datetime(end))
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
    updated_labels = wrap_text(labels)
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
        todays_date = get_todays_date()
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


def deployment_timeline(deployment_df, cmap_name='Dark2',
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
        todays_date = get_todays_date()
        figure_path = figure_path + '\\deployment_timeline_plot' + '_' \
            + todays_date + '.png'

        plt.savefig(figure_path, dpi=300)
        plt.close()