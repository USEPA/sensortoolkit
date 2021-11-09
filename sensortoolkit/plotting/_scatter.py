# -*- coding: utf-8 -*-
"""
This module contains methods for constructing scatter plot figures.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Mon Jan 27 08:49:12 2020
Last Updated:
  Wed Jul 28 14:11:14 2021
"""
import sys
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from textwrap import wrap
from sensortoolkit.calculate import regression_stats
from sensortoolkit.param import Parameter
from sensortoolkit.datetime_utils import get_todays_date
from sensortoolkit.calculate import normalize
from sensortoolkit.deploy import get_max_conc
from sensortoolkit.plotting import (set_fontsize,
     sensor_subplot_formatting, met_scatter_lims, wrap_text, error_bars)
register_matplotlib_converters()


def draw_scatter(ax, xdata, ydata, param_dict, sensor_stats=None,
                 xlims=None, ylims=None, fontsize=None,
                 detail_fontsize=None, param=None,
                 plot_regression=True, colormap_vals=None,
                 colormap_name=None, **kwargs):
    """A helper function to draw scatterplots with linear regressions on passed
    matplotlib axes instance

    Args:
        ax (Matplotlib axes instance):
            The axes object on which the scatter plot is drawn
        xdata: numpy array or pandas series):
            The x data (reference data)
        ydata: numpy array or pandas series):
            The y data (sensor data)
        param_dict (dict):
            Dictionary of kwargs to pass to ax.plot
        sensor_stats (pandas DataFrame):
            Dataframe contain regression statistics for single sensor (subset
            of the full stats_df object)
        xlims (tuple):
          The domain of the graph
        ylims (tuple):
          The range of the graph
        fontsize (int):
            Selects the fontsize of regression statistics
        detail_fontsize (int or float):
            Fontsize for axes tick labels
        param (str):
            The name of the parameter for which measurements will be plotted.
        plot_regression (bool):
            True plots linear regression, regression equation, R^2, and RMSE
        colormap_vals (Dataframe column or none):
            Data that are used to set the colormap value.
        colormap_name (string or none):
            The name of the colormap which the scatter plot will be assigned

    Keyword arguments:

        - **monocolor** (*TYPE*):
            DESCRIPTION
        - **point_size** (*TYPE*):
            DESCRIPTION
        - **point_alpha** (*TYPE*):
            DESCRIPTION
        - **plot_aspect** (*TYPE*):
            DESCRIPTION
        - **plottext_alpha** (*TYPE*):
            DESCRIPTION
        - **plottext_size** (*TYPE*):
            DESCRIPTION
        - **plottext_color** (*TYPE*):
            DESCRIPTION
        - **plottext_xloc** (*TYPE*):
            DESCRIPTION
        - **plottext_yloc** (*TYPE*):
            DESCRIPTION
        - **plottext_xdisplacement** (*TYPE*):
            DESCRIPTION
        - **plottext_ydisplacement** (*TYPE*):
            DESCRIPTION
        - **plottext_position** (*TYPE*):
            DESCRIPTION
        - **show_trendline** (*TYPE*):
            DESCRIPTION
        - **show_RMSE** (*TYPE*):
            DESCRIPTION
        - **show_spearman** (*TYPE*):
            DESCRIPTION
        - **show_N** (*TYPE*):
            DESCRIPTION
        - **show_one_to_one** (*TYPE*):
            DESCRIPTION
        - **trendline_xmax** (*TYPE*):
            DESCRIPTION
        - **trendline_color** (*TYPE*):
            DESCRIPTION
        - **trendline_alpha** (*TYPE*):
            DESCRIPTION

    Returns:
        plotobj:
            Matplotlib axes instance with scatter drawn along with additional
            elements specified in the kwargs (text, colormap)

    """
    # Set keyword arguments to passed values or defaults
    pointsize = kwargs.get('point_size', 20)
    alpha = kwargs.get('point_alpha', 0.7)
    default_text_pos = 'upper_left'
    if sensor_stats is not None:
        slope = sensor_stats.Slope[0]
        if slope > 1.75:
            default_text_pos = 'bottom_right'
        else:
            default_text_pos = 'upper_left'
    text_position = kwargs.get('plottext_position', default_text_pos)
    plot_trendline = kwargs.get('show_trendline', True)
    plot_rmse = kwargs.get('show_RMSE', True)
    plot_spearman = kwargs.get('show_spearman', False)
    plot_n = kwargs.get('show_N', True)
    plot_one_to_one = kwargs.get('show_one_to_one', True)
    monocolor = kwargs.get('monocolor', '#0048AD')

    # Set text position
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

    # Plot scatterplot with colormap, based on the colormap_vals data. If none,
    # plot scatter with single color (monocolor)
    if isinstance(colormap_vals, pd.core.series.Series):
        norm = mpl.colors.Normalize(vmin=0, vmax=100)
        plotobj = ax.scatter(xdata, ydata, s=pointsize, alpha=alpha,
                             c=colormap_vals, cmap=colormap_name,
                             norm=norm)
    else:
        plotobj = ax.scatter(xdata, ydata, color=monocolor,
                             s=pointsize, alpha=alpha)

    # Set axes labels, ticks, limits
    ax.set_xlabel(param_dict['xlabel'], fontsize=fontsize)
    ax.set_ylabel(param_dict['ylabel'], fontsize=fontsize)
    ax.tick_params(labelsize=detail_fontsize)
    ax.set_aspect(kwargs.get('plot_aspect', 'equal'))
    ax.set_xlim(xlims)
    ax.set_ylim(ylims)

    # Check for regression statistics
    if sensor_stats is not None:
        intercept = sensor_stats.loc[0, 'Intercept']
        slope = sensor_stats.loc[0, 'Slope']
        if pd.isna(intercept) and pd.isna(slope):
            plot_regression = False
            plot_n = False

    # Draw regression equation, R^2 (or spearman), RMSE, N
    if plot_regression is True:
        X = pd.Series(xdata)
        Y = pd.Series(ydata)

        if plot_trendline:
            try:
                trendline_xmax = kwargs.get('trendline_xmax', 1.2*X.max())
                trend_data = np.linspace(X.min(), trendline_xmax, 2)
                trendline_color = kwargs.get('trendline_color', 'k')
                trendline_alpha = kwargs.get('trendline_alpha', 0.65)
                ax.plot(trend_data, slope*trend_data + intercept,
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
        ax.text(text_x, text_y,
                linear_reg_str.format(slope, intercept),
                transform=ax.transAxes, color=text_color,
                alpha=text_alpha, size=text_size)

        # Pearson Correlation Coefficient
        r_square = sensor_stats.loc[0, 'R$^2$']
        ax.text(text_x - text_xdisplacement,
                text_y - text_ydisplacement,
                '$R^2={:.2f}$'.format(r_square),
                transform=ax.transAxes, color=text_color,
                alpha=text_alpha, size=text_size)

        # Spearman Correlation
        if plot_spearman is True:
            spearman_corr = X.corr(Y, method='spearman')
            ax.text(text_x - 2*text_xdisplacement,
                    text_y - 2*text_ydisplacement,
                    '$\rho={:.2f}$'.format(spearman_corr),
                    transform=ax.transAxes, color=text_color,
                    alpha=text_alpha, size=text_size)

        # Root Mean Square Error
        if plot_rmse is True:
            RMSE = sensor_stats.loc[0, 'Sensor RMSE']

        if plot_spearman is False and plot_rmse is True:
            ax.text(text_x - 2*text_xdisplacement,
                    text_y - 2*text_ydisplacement,
                    '$RMSE={:.2f}$'.format(RMSE),
                    transform=ax.transAxes, color=text_color,
                    alpha=text_alpha, size=text_size)

    # Draw the number of scatterplot points graphed
    if plot_n is True:
        n_count = int(sensor_stats.loc[0, 'N'])
        # place the text below Rsqr text by same coord diff
        ax.text(text_x - 3*text_xdisplacement,
                text_y - 3*text_ydisplacement,
                '$N= $'+str(n_count),
                transform=ax.transAxes, color=text_color,
                alpha=text_alpha, size=text_size)

    # One-to-one dashed line for reference
    if plot_one_to_one is True:
        one_to_one = np.linspace(ylims[0], ylims[1], int(10*ylims[1]))
        ax.plot(one_to_one, one_to_one, linestyle='--',
                color='grey', alpha=0.7)

    return plotobj


def scatter_plotter(df_list, ref_df, stats_df=None, plot_subset=None,
                    param=None, sensor_name=None, figure_path=None,
                    write_to_file=True, averaging_interval=None,
                    met_ref_df=None, deploy_dict=None, sensor_serials=None,
                    ax=None, fig=None, report_fmt=False, return_axs=False,
                    param_class=None, **kwargs):
    """Front-end function for creating scatter plots.

    Calls Draw_Scatter for lower-end tasks and sets formatting for plots
    based off passed parameters.

    Args:
        df_list (list):
            A list containing the sensor dataframes from which data is plotted
        ref_df (pandas DataFrame):
            Reference dataframe
        stats_df (pandas DataFrame):
            Regression statistics dataframe for the sensor evaluation set
        plot_subset (Nonetype or list of strings):
            To plot a subset of evaluated sensors, pass a list of the sensor
            numbers ('1', '2', '3', etc.) as assigned in the sensor serial
            dictionary. For example, plotting a subset for sensors '1', '3',
            and '5' in an evaluation is achieved by passing
            plot_subset=['1', '3', '5'].
        param (str):
            Column header name for the pollutant values to be plotted
        sensor_name (str):
            Unformatted sensor name, passed to Formatted_Sensor_Name() for
            including formatted version on plot
        figure_path (str):
            Path to directory where the figure will be saved
        write_to_file (bool):
            If true, writes to file and figure is closed. False skips file
            writing and does not close the figure
        averaging_interval (str):
            The averaging interval of the sensor and reference datasets, either
            '1-hour' or '24-hour'.
        met_ref_df (Nonetype or pandas DataFrame):
            Reference dataframe for met data. Used as an alternative to sensor
            met data for plotting colormap of relative humidity on scatterplot
            points. If passed, the reference met data takes precedence over
            any existing sensor met data.
        deploy_dict (dict):
            DEFINITION
        sensor_serials (dict):
            DEFINITION
        ax (matplotlib axes instance):
            DEFINITION
        fig (matplotlib fig instance):
            DEFINITION
        report_fmt (bool):
            DEFINITION
        return_axs (bool):
            DEFINITION
        param_class (str):
            The parameter classification for the passed parameter to plot.
            E.g, if param is PM25, param_class = PM; if param is 03,
            param_class = Gases;if param is Temp, param_class = Met.

    Keyword arguments:

        - **color_palette** (*TYPE*):
          Color palette assigned to relative-humidity colormapped scatter
          plot points
        - **colorbar_axespos** (*TYPE*):
          DEFINITION
        - **colorbar_orientation** (*TYPE*):
          DEFINITION
        - **colorbar_title_fontsize** (*TYPE*):
          DEFINITION
        - **colorbar_title_ypos** (*TYPE*):
          DEFINITION
        - **colorbar_tick_labelsize** (*TYPE*):
          DEFINITION
        - **colorbar_tick_length** (*TYPE*):
          DEFINITION
        - **colorbar_tick_width** (*TYPE*):
          DEFINITION
        - **draw_cbar** (*TYPE*):
          DEFINITION
        - **fig_wspace** (*TYPE*):
          DEFINITION
        - **fig_hspace** (*TYPE*):
          DEFINITION
        - **fig_left** (*TYPE*):
          DEFINITION
        - **fig_right** (*TYPE*):
          DEFINITION
        - **fig_top** (*TYPE*):
          DEFINITION
        - **fig_bottom** (*TYPE*):
          DEFINITION
        - **filename_suffix** (*TYPE*):
          Optional string added to end of filename. Defaults to empty string.
        - **fontsize** (*TYPE*):
          The font size for the xlabel, ylabel, and plot text. Passed on to
          Draw_Scatter() which uses 0.85*font_size for tick labels.
        - **monocolor** (*TYPE*, passed to ``Draw_Scatter()``):
          A single color (specified in hex) for scatter plots.
          Recommend #2251D0 (nice blue hue).
        - **detail_fontsize** (*TYPE*):
          DEFINITION
        - **point_size** (*TYPE, passed to Draw_Scatter()*):
          The size of the scatterpoint plots
        - **point_alpha** (*TYPE*):
          DEFINITION
        - **plot_aspect** (*TYPE, passed to Draw_Scatter()*):
          DEFINITION
        - **plottext_alpha** (*TYPE, passed to Draw_Scatter()*):
          DEFINITION
        - **plottext_size** (*TYPE, passed to Draw_Scatter()*):
          DEFINITION
        - **plottext_color** (*TYPE, passed to Draw_Scatter()*):
          DEFINITION
        - **plottext_xloc** (*TYPE, passed to Draw_Scatter()*):
          DEFINITION
        - **plottext_yloc** (*TYPE, passed to Draw_Scatter()*):
          DEFINITION
        - **plottext_xdisplacement** (*TYPE, passed to Draw_Scatter()*):
          DEFINITION
        - **plottext_ydisplacement** (*TYPE, passed to Draw_Scatter()*):
          DEFINITION
        - **plottext_position** (*TYPE, passed to Draw_Scatter()*):
           Determines position of plot text. Can either pass 'upper_left' or
           'bottom_right'
        - **ref_name** (*TYPE*):
          DEFINITION
        - **seaborn_style** (*TYPE*):
          DEFINITION
        - **show_colorbar** (*TYPE*):
          If true, relative humidity values will be used as a colormap on the
          scatterplot points.
        - **show_title** (*TYPE*):
          Show the title at the top of the plot. Includes the name of the
          sensor, the averaging interval, the evaluation parameter, and
          the name of the reference against which sensor data are compared.
        - **show_regression** (*TYPE*):
          Pass on to underlying Draw_Scatter function. Defaults to
          True. If false, regression lines on plots will not be generated.
        - **show_trendline** (*TYPE*):
          DEFINITION
        - **show_RMSE** (*TYPE, passed to Draw_Scatter()*):
          DEFINITION
        - **show_spearman** (*TYPE, passed to Draw_Scatter()*):
          DEFINITION
        - **show_N** (*TYPE, passed to Draw_Scatter()*):
          DEFINITION
        - **show_one_to_one** (*TYPE, passed to Draw_Scatter()*):
          DEFINITION
        - **tight_layout** (*TYPE*):
          Passed to matplotlib's ``fig.tight_layout()`` for narrow formatting
        - **tick_spacing** (*TYPE*):
          DEFINITION
        - **title_text** (*TYPE*):
          DEFINITION
        - **title_textwrap** (*TYPE*):
          DEFINITION
        - **title_xloc** (*TYPE*):
          DEFINITION
        - **title_yloc** (*TYPE*):
          DEFINITION
        - **trendline_xmax** (*TYPE, passed to Draw_Scatter()*):
          DEFINITION
        - **trendline_color** (*TYPE, passed to Draw_Scatter()*):
          DEFINITION
        - **trendline_alpha** (*TYPE, passed to Draw_Scatter()*):
          DEFINITION
        - **xlims** (*TYPE*):
          The x-limits of the scatter plot
        - **ylims** (*TYPE*):
          The y-limits of the scatter plot

    Returns:
        (matplotlib axes instance or None):
            If an axis is passed to ``Scatter_Plotter()``, the modified axis
            with plotting detail filled in will be returned. Otherwise, none
            will be returned.

    """
    sns.set_style(kwargs.get('seaborn_style', 'darkgrid'))
    palette = kwargs.get('color_palette', 'seismic')
    sns.set_palette(palette)

    RH_colormap = kwargs.get('show_colorbar', True)
    plot_title = kwargs.get('show_title', True)
    plot_regression = kwargs.get('show_regression', True)

    title_text = kwargs.get('title_text', None)
    ref_name = kwargs.get('ref_name', 'Unknown Reference')
    tight_layout = kwargs.get('tight_layout', False)
    filename_suffix = kwargs.get('filename_suffix', '')

    if RH_colormap:
        draw_cbar = kwargs.get('draw_cbar', True)

    if param_class == 'Met':
        met_ref_df = ref_df

    # Option to supply df_list indicies in list for subset of sensors to plot
    if plot_subset is not None:

        # Subset by serial ID
        if all(name in sensor_serials.values() for name in plot_subset):
            subset_keys = [item[0] for item in sensor_serials.items()
                           if item[1] in plot_subset]
            plot_subset = subset_keys
        # Subset by the integer number associated with the serial ID
        elif all(name in sensor_serials.keys() for name in plot_subset):
            pass
        else:
            raise ValueError('Invalid list of subset keys. Pass either a list'
                             ' of serial IDs or a list of the integer indices'
                             ' associated with each serial ID.')

        # limit dataframe list and sensor serials to selected sensors
        df_list = [df for i, df in enumerate(df_list, 1)
                   if str(i) in plot_subset]
        sensor_serials = {str(i): serial for i, serial in
                          enumerate(sensor_serials.values(), 1)
                          if str(i) in plot_subset}

    param_obj = Parameter(param)
    param_name = param_obj.name
    fmt_param = param_obj.format_name
    fmt_param_units = param_obj.units

    fmt_sensor_name = sensor_name.replace('_', ' ')

    # For occasions where a dataframe is passed rather than a list
    if isinstance(df_list, list) is False:
        print('Warning: Dataframe passed to function is not in the form '
              'of a list\n')
        print('Continuing by placing passed dataframe into list')
        df_list = [df_list]

    number_of_sensors = len(df_list)
    kwargs['sensor_serials'] = sensor_serials
    fmt_tuple = sensor_subplot_formatting(number_of_sensors, param_obj,
                                          report_fmt, **kwargs)

    (Nr, Nc, fig_size, suptitle_xpos, suptitle_ypos, title_textwrap,
     detail_fontsize, wspace, hspace, left, right, top, bottom,
     auto_filename_suffix, cbar_padding, cbar_aspect, font_size) = fmt_tuple

    # Update fontsize if particular value specified
    font_size = kwargs.get('fontsize', font_size)
    # dropped, variable 'font_size' passed to Draw_Scatter
    kwargs.pop('fontsize', None)  # Avoids multiple args passed to same param
    detail_fontsize = kwargs.get('detail_fontsize', detail_fontsize)

    # Set concentration limits for x and y axes to the nearest multilple of
    # 5 for 125% of the max concentration recorded by collocated sensors.
    start = min([df.index.min() for df in df_list])
    end = max([df.index.max() for df in df_list])
    max_conc = get_max_conc(param_name, df_list=df_list, ref_df=ref_df,
                            bdate=start, edate=end)

    divisions  = 100
    default_tick_spacing = 0
    while divisions > 7:
        default_tick_spacing += 5
        divisions = round(1.25*max_conc / default_tick_spacing)

    tick_spacing = kwargs.get('tick_spacing', default_tick_spacing)

    xlims = kwargs.get('xlims',
                       (0, tick_spacing*round(1.25*max_conc/tick_spacing)))
    ylims = kwargs.get('ylims',
                       (0, tick_spacing*round(1.25*max_conc/tick_spacing)))

    xlims = tuple(float(val) for val in xlims)
    ylims = tuple(float(val) for val in ylims)

    # Remove axes limits from kwargs if specified
    kwargs.pop('xlims', None)
    kwargs.pop('ylims', None)

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
        if title_text is None:
            title_text = (fmt_sensor_name + ' vs. ' + ref_name + ' ' +
                          averaging_interval + ' ' + fmt_param)

        title_text = '\n'.join(wrap(title_text,
                                    kwargs.get('title_textwrap',
                                               title_textwrap)))

        n_lines = len(title_text.split('\n'))
        if n_lines > 2:  # shift the figure down a tad if 3 or more lines
            font_size *= 0.9
            suptitle_ypos *= 1.03

        if unique_ax_obj is True:
            fig.suptitle(title_text, fontsize=font_size,
                         y=kwargs.get('title_yloc', suptitle_ypos),
                         x=kwargs.get('title_xloc', suptitle_xpos))
        else:
            axs.set_title(title_text, fontsize=font_size,
                          y=kwargs.get('title_yloc', suptitle_ypos),
                          x=kwargs.get('title_xloc', suptitle_xpos))

    for i in range(Nr):
        for j in range(Nc):
            sensor_number = Nc*i + (j + 1)
            sensor_idx = sensor_number - 1

            # set appropriate plt axes array index based on # of sensors
            if isinstance(axs, np.ndarray):
                # More than one sensor, axes arranged in array structure
                if len(axs.shape) > 1:
                    ax = axs[i, j]
                else:
                    ax = axs[j]
            else:
                ax = axs

            if sensor_number > number_of_sensors:
                ax.remove()
                auto_filename_suffix = auto_filename_suffix.replace(
                         str(Nr*Nc), str(Nr*Nc - 1))
                continue

            # Initialize sensor, reference dataframe objects to None
            sensor_stats = None
            hourly_df_obj = None
            hourly_ref_df = None
            daily_df_obj = None
            daily_ref_df = None

            # Choose between serial ID and sensor number labels for legend
            if isinstance(sensor_serials, dict):
                lbl = list(sensor_serials.values())[sensor_idx]
            else:
                lbl = 'Sensor ' + str(sensor_number)

            param_dict = {'xlabel': f'{ref_name} {fmt_param} ({fmt_param_units})',
                          'ylabel': f'{lbl} {fmt_param} ({fmt_param_units})'}

            # set appropriate plt axes array index based on # of sensors
            if isinstance(axs, np.ndarray):
                ax.set_title(lbl, fontsize=detail_fontsize)

            try:
                sensor_df = df_list[sensor_idx]
            except IndexError:
                print('Sensor index', str(sensor_idx), 'not in dataframe list')
                ax.remove()
                auto_filename_suffix = auto_filename_suffix.replace(
                                        str(Nr*Nc), str(Nr*Nc - 1))
                break

            tdelta_interval = sensor_df.index[1] - sensor_df.index[0]

            if (tdelta_interval) == pd.Timedelta('1 days'):
                daily_df_obj = [sensor_df]
                daily_ref_df = ref_df

            if (tdelta_interval) == pd.Timedelta('1 hour'):
                hourly_df_obj = [sensor_df]
                hourly_ref_df = ref_df

            if plot_regression is True:
                sensor_stats = regression_stats(sensor_df_obj=sensor_df,
                                                ref_df_obj=ref_df,
                                                deploy_dict=deploy_dict,
                                                param=param,
                                                serials=sensor_serials,
                                                verbose=False)

            try:
                df = pd.DataFrame()
                df['ydata'] = sensor_df[param_name + '_Value']
                df['xdata'] = ref_df[param_name + '_Value']
            except KeyError:
                print(ref_name + ' not in passed reference dataframe.')

            # Optional combine of RH data from AIRS and sensor, where the AIRS
            # data is preferred and sensor data used if AIRS RH not available
            if RH_colormap is True:
                if 'mean_RH_Value' in sensor_df:
                    sensor_df = sensor_df.rename(columns={'mean_RH_Value':
                                                          'RH_Value'})

                if ((isinstance(met_ref_df, pd.DataFrame)) and
                   (met_ref_df['RH_Value'].dropna().empty is False)):
                    if 'RH_Value' not in sensor_df:
                        sensor_df['RH_Value'] = np.nan

                    # Ref RH data left join with sensor RH data
                    try:
                        df['RH_Value'] = met_ref_df['RH_Value'].combine_first(
                          sensor_df['RH_Value'])
                    except KeyError as missing_param:
                        print(missing_param,
                              'not found in met reference dataframe')

                    cmap_vals = df['RH_Value']
                else:
                    df['RH_Value'] = sensor_df['RH_Value']
                    print('..Reference RH not found, internal sensor RH',
                          'shown in figure')
                    cmap_vals = df['RH_Value']
            else:
                cmap_vals = None
                palette = None

            xdata = df['xdata']
            ydata = df['ydata']

            im = draw_scatter(ax,
                              xdata,
                              ydata,
                              param_dict,
                              sensor_stats,
                              colormap_vals=cmap_vals,
                              colormap_name=palette,
                              xlims=xlims,
                              ylims=ylims,
                              fontsize=font_size,
                              detail_fontsize=detail_fontsize,
                              plot_regression=plot_regression,
                              **kwargs)

            ax.xaxis.set_major_locator(plt.MultipleLocator(tick_spacing))
            ax.yaxis.set_major_locator(plt.MultipleLocator(tick_spacing))

    # Plot colorbar
    if RH_colormap is True:
        try:
            ctitle = 'Relative Humidity (%)'
            cbar_orien = 'horizontal'
            cbar_size = 0.3
            cbar_ypos = 0.6

            if number_of_sensors == 1:
                cbar_size = 0.8
                if len(param_obj.averaging) == 1:
                    cbar_orien = 'vertical'
                    cbar_ypos = 1.01
                    # axes positioning [x0, y0, width, height]
                    caxes_pos = [0.85, 0.15, 0.05, 0.66]
                    ctitle = '\n'.join(wrap(ctitle, 10))
                else:
                    if report_fmt is True:
                        caxes_pos = [0.25, 0.07, 0.50, 0.03]
                    else:
                        caxes_pos = [0.125, 0.05, 0.75, 0.03]
            elif number_of_sensors in (2, 3):
                caxes_pos = [0.37, 0.07, 0.26, 0.03]
            else:
                caxes_pos = [0.37, 0.07, 0.26, 0.02]

            cbar_pos = kwargs.get('colorbar_axespos', caxes_pos)
            cbar_orien = kwargs.get('colorbar_orientation', cbar_orien)

            # For cases where axes object passed to function: Checkl if the
            # colorbar has been drawn onto the passed axes. If so, dont
            # duplicate to avoid matplotlib depreciation warning
            if draw_cbar is True:
                cbar = fig.colorbar(im, cax=fig.add_axes(cbar_pos),
                                    orientation=cbar_orien, pad=cbar_padding,
                                    aspect=cbar_aspect, shrink=cbar_size)
                cbar.ax.set_title(ctitle,
                        fontsize=kwargs.get('colorbar_title_fontsize',
                                            detail_fontsize),
                        y=kwargs.get('colorbar_title_ypos', cbar_ypos))
                cbar.ax.tick_params(
                        labelsize=kwargs.get('colorbar_tick_labelsize',
                                             detail_fontsize),
                        length=kwargs.get('colorbar_tick_length', 4),
                        width=kwargs.get('colorbar_tick_width', 1))

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
            param_name = param_class

        file_name = (sensor_name + '_vs_'
                     + ref_name).replace(r'/', '').replace('\\', '')

        file_path = figure_path + param_name + '\\' + file_name

        # if matplotlib axes object not passed to Scatter_Plotter, the figure
        # created will be for data at the averaging interval specified by
        # the averaging_interval variable. In this case, indicate the avg interval
        # in the filename
        if unique_ax_obj is True and report_fmt is False:
            file_path += '_' + averaging_interval
        if filename_suffix != '':
            file_path = file_path + '_' + filename_suffix
        else:
            file_path = file_path + '_' + auto_filename_suffix

        todays_date = get_todays_date()
        file_path = file_path + '_' + todays_date + '.png'

        fig.savefig(file_path, dpi=300)
        plt.close()

    # Return the ax axes instance for iteration
    if report_fmt is True or unique_ax_obj is False:
        return ax

    # Return a unique axes instance
    if return_axs is True:
        return axs


def normalized_met_scatter(df_list, ref_df, avg_df, met_ref_df=None,
                           figure_path=None, param=None,
                           met_param=None,
                           sensor_name=None, write_to_file=True,
                           sensor_serials=None, ref_name=None,
                           report_fmt=False, fig=None, ax=None,
                           return_mpl_obj=False, **kwargs):
    """Plot parameter values normalized by reference values against either
    temperature or relative humidity.

    Args:
        df_list (TYPE): DESCRIPTION.
        ref_df (TYPE): DESCRIPTION.
        avg_df (TYPE): DESCRIPTION.
        met_ref_df (TYPE, optional): DESCRIPTION. Defaults to None.
        figure_path (TYPE, optional): DESCRIPTION. Defaults to None.
        param (TYPE, optional): DESCRIPTION. Defaults to None.
        met_param (TYPE, optional): DESCRIPTION. Defaults to None.
        sensor_name (TYPE, optional): DESCRIPTION. Defaults to None.
        write_to_file (TYPE, optional): DESCRIPTION. Defaults to True.
        sensor_serials (TYPE, optional): DESCRIPTION. Defaults to None.
        ref_name (TYPE, optional): DESCRIPTION. Defaults to None.
        report_fmt (TYPE, optional): DESCRIPTION. Defaults to False.
        fig (TYPE, optional): DESCRIPTION. Defaults to None.
        ax (TYPE, optional): DESCRIPTION. Defaults to None.
        return_mpl_obj (TYPE, optional): DESCRIPTION. Defaults to False.
        **kwargs (TYPE): DESCRIPTION.

    Returns:
        ax (TYPE): DESCRIPTION.

    """
    param_obj = Parameter(param)
    param_name = param_obj.name
    fmt_param = param_obj.format_name
    fmt_param_units = param_obj.units

    met_param_obj = Parameter(met_param)
    met_param_name = met_param_obj.name
    fmt_met_param = met_param_obj.format_name
    fmt_met_units = met_param_obj.units

    sns.set_style(kwargs.get('seaborn_style', 'darkgrid'))

    kwargs['show_N'] = False
    kwargs['show_RMSE'] = False
    kwargs['show_spearman'] = False
    kwargs['show_one_to_one'] = False
    kwargs['show_trendline'] = False
    kwargs['point_size'] = kwargs.get('point_size', 12)
    kwargs['point_alpha'] = kwargs.get('point_alpha', 0.5)

    point_colors = kwargs.get('point_colors', None)
    xlims = kwargs.get('xlims', None)
    ylims = kwargs.get('ylims', None)
    cmap_norm_range = kwargs.get('cmap_norm_range', (0, 0.4))
    cmap_name = kwargs.get('cmap_name', 'Set1')
    fontsize = kwargs.get('fontsize', 12)
    detail_fontsize = kwargs.get('detail_fontsize', 10)
    subplot_adjust = kwargs.get('subplot_adjust', None)

    show_errorbars = kwargs.get('show_errorbars', False)
    show_legend = kwargs.get('show_legend', True)

    # Remove attributes from kwargs if specified
    kwargs.pop('fontsize', None)
    kwargs.pop('ylims', None)
    kwargs.pop('xlims', None)

    data = met_ref_df
    if data[met_param_name + '_Value'].dropna().empty:
        print(f'..Met data empty for {met_param_name}, trying sensor measurements')

        try:
            data = avg_df['mean_' + met_param_name + '_Value'].dropna()
            data = data.to_frame().rename(columns={'mean_' + met_param_name + '_Value':
                                                   met_param_name + '_Value'})
            sensor_data = True
        except KeyError:
            print('..{met_param_name} not measured by sensor, unable to plot '
                  'distribution')
            return
        if data.empty:
            print('..no intersensor averaged {met_param_name} data, unable to plot '
                  'distribution')
            return

    # Set xlim and ylim if not specified
    if xlims is None or ylims is None:
        # Determine which limits need to be set based on whether values have
        # been passed to kwargs for xlims or ylims
        set_xlims = True
        set_ylims = True
        if xlims is not None:
            set_xlims = False
        if ylims is not None:
            set_ylims = False

        lim_tup = met_scatter_lims(met_data=data,
                                   param=param_name,
                                   met_param=met_param_name,
                                   xlims=xlims,
                                   ylims=ylims,
                                   serials=sensor_serials,
                                   avg_df=avg_df)

        if set_xlims:
            xlims = lim_tup[0]
        if set_ylims:
            ylims = lim_tup[1]

    if param_name == 'Temp':
        met_param_name = 'Temp'
    if param_name == 'RH':
        met_param_name = 'RH'
    elif met_param_name is None:
        print('Enter valid parameter for met_param_name: Either Temp or RH')

    if (ax and fig) is None:
        # No axes object passed to function, create unique fig, axes objects
        fig, ax = plt.subplots(1, 1, figsize=kwargs.get('fig_size', (8, 4)))
        unique_ax_obj = True
    else:
        # Axes object passed to function, set axes within scope of function to
        # passed axes object.
        ax = ax
        unique_ax_obj = False

    # Retreive formatted version of sensor and parameter name
    fmt_sensor_name = sensor_name.replace('_', ' ')

    try:
        met_ref_name = data[met_param_name + '_Method'].dropna().unique()[0]
    except IndexError:
        met_ref_name = 'Unspecified Reference'
    except KeyError:
        met_ref_name = sensor_name

    x_label = f'{met_ref_name} {fmt_met_param} ({fmt_met_units})'

    title = fmt_sensor_name + ' ' + fmt_param + ' Normalized by ' + ref_name

    labels = [title]
    labels = wrap_text(labels, max_label_len=40)
    title = labels[0]

    param_dict = {'xlabel': x_label,
                  'ylabel': ''}

    # Compute normalized dataframes
    norm_df_list = normalize(df_list, ref_df, param_name, ref_name)

    # Plot 1:1 normalization line
    ax.axhline(y=1.0, linewidth=1.5, color='#8b8b8b', alpha=.8)

    # Set colormap and assign number of discrete colors from colormap
    if point_colors is None:
        colormap = plt.cm.get_cmap(cmap_name)
        cmap_lbound, cmap_ubound = cmap_norm_range[0], cmap_norm_range[1]
        colors = [colormap(i) for i in np.linspace(cmap_lbound, cmap_ubound,
                  len(norm_df_list))]
    else:
        colors = point_colors

    ax.set_prop_cycle('color', colors)

    # If the normalized param is temp or RH, the ref_df will be the met_ref_df
    if any(col.startswith('Temp') or col.startswith('RH') for col in ref_df):
        data = ref_df

    # Generate scatter plots for each normalized sensor dataset
    legend_list = ['1:1']
    for i, (df, sensor_n) in enumerate(zip(norm_df_list, sensor_serials)):
        compare_df = pd.DataFrame()
        compare_df[met_param_name + '_Value'] = data[met_param_name + '_Value']
        compare_df['Normalized_' + param_name + '_Value'] = df['Normalized_' + param_name + '_Value']
        xdata = compare_df[met_param_name + '_Value']
        ydata = compare_df['Normalized_'+param_name + '_Value']

        if ydata.dropna().empty is True:
            continue

        try:
            kwargs['monocolor'] = colors[i]
        except IndexError:
            print('..warning: length of point colors list does not match'
                  ' number of sensor datasets')
            print('..assigning first point color to unspecified point color '
                  'index')
            kwargs['monocolor'] = colors[0]

        draw_scatter(ax, xdata, ydata, param_dict,
                     xlims=xlims, ylims=ylims, fontsize=fontsize,
                     detail_fontsize=detail_fontsize,
                     plot_regression=False, **kwargs)

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
        legend_fontsize = detail_fontsize
        legend_loc = 'center left'  # position legend based on its center left

    elif subplot_adjust is None:
        # axes adjustments for PT report formatted multi-axes plot
        top = 0.95
        bottom = 0.4
        left = 0.05
        right = 0.95
        hspace = 0.20
        wspace = 0.25
        legend_pos = (.5, -0.65)
        legend_fontsize = detail_fontsize
        legend_loc = 'center'  # position the legend based on its center
    else:
        subplot_adjust = list(subplot_adjust.values())
        top = subplot_adjust[0]
        bottom = subplot_adjust[1]
        left = subplot_adjust[2]
        right = subplot_adjust[3]
        hspace = subplot_adjust[4]
        wspace = subplot_adjust[5]
        legend_pos = subplot_adjust[6]
        legend_fontsize = detail_fontsize
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
        sensor_data = df['Normalized_' + param_name  + '_Value']
        all_sensor_data[param_name  + '_Value' + '_sensor_' + str(i)] = sensor_data
    ydata = all_sensor_data

    if show_errorbars is True:
        error_bars(xdata, ydata, ax, plot_yerror=True,
                   n_xbins=kwargs.get('errorbar_nbins', 10),
                   errorbar_c=kwargs.get('errorbar_color', '#151515'))

    # Legend position ---------------------------------------------------------
    if show_legend is True:
        ax.legend(legend_list, fontsize=legend_fontsize, loc=legend_loc,
                  bbox_to_anchor=kwargs.get('legend_pos', legend_pos),
                  ncol=leg_cols, columnspacing=col_spacing)

    # Write plot to file ------------------------------------------------------
    if write_to_file is True:
        todays_date = get_todays_date()
        figure_path = figure_path + param_name + '\\' + sensor_name +\
            '_normalized_' + param_name + '_vs_' + met_param_name

        # Indicate performance targets template formatted
        if report_fmt is True:
            if unique_ax_obj is False:
                figure_path = figure_path.replace('_vs_' + met_param_name, '_met')
            figure_path = figure_path + '_' + 'report_fmt'

        # Filename suffix for harmonized sensor datasets
        if param_name.startswith('corrected'):
            figure_path = figure_path + '_' + 'corrected'

        figure_path += '_' + todays_date + '.png'
        plt.savefig(figure_path, dpi=300)
        plt.close()

    if return_mpl_obj is True or report_fmt is True:
        return ax
