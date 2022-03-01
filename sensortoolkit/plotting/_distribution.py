# -*- coding: utf-8 -*-
"""
Plotting methods for graphing the distribution of measured quantities such as
reference monitor pollutant concentrations (``ref_distrib()``), meteorological
conditions including temperature and relative humidity (``met_distrib()``),
and the distribution of recording intervals (i.e., the time difference between
consecutive timestamps) in sensor datasets (``recording_interval_histogram()``).

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Mon Jan 27 08:49:12 2020
Last Updated:
  Wed Jul 28 14:20:18 2021
"""
import os
from pandas.plotting import register_matplotlib_converters
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sensortoolkit.param import Parameter
from sensortoolkit.datetime_utils import get_todays_date
register_matplotlib_converters()
sns.set_style('darkgrid')


def ref_distrib(ref_df, param=None, averaging_interval='1-hour',
                  font_size=18, write_to_file=True, figure_path=None,
                  filename_suffix=''):
    """Plot the distribution of reference values for the passed parameter.

    Args:
        ref_df (pandas DataFrame):
            Dataframe containing reference data for the parameter ``'param'``
            and logged at the specified ``'averaging_interval'`` .
        param (str, optional):
            The name of the parameter for which the distribution plot will show
            the distribution of reference measurements. Defaults to None.
        averaging_interval (str, optional):
            The averaging interval for the passed dataframe. Defaults to
            '1-hour'.
        font_size (int or float, optional):
            The font size for the figure. Defaults to 18.
        write_to_file (bool, optional):
            If true, the figure will be saved as a png image to the
            ``[project_path]/figures`` subdirectory. Defaults to True.
        figure_path (str):
            The full directory path to the folder where figures are saved.
            This should be located at ``[project_path]/figures``.
        filename_suffix (str, optional):
            Optional suffix that can be added to the end of filenames to ensure
            previously created files with similar naming are not overwritten.
            Defaults to ''.

    Returns:
        None.

    """
    try:
        # Determine name of reference monitor from passed parameter name
        try:
            ref_name = ref_df[param + '_Method'].dropna().unique()[0]
        except IndexError:
            ref_name = 'Unspecified Reference'

        # Format the parameter name for plotting
        param_obj = Parameter(param)
        param_name = param_obj.param_name
        fmt_param = param_obj.param_format_name
        fmt_param_units = param_obj.param_units

        # Construct plot instance
        fig, ax = plt.subplots(1, 1, figsize=(6, 5))
        sns.distplot(ref_df[ref_name].dropna(),
                     label=ref_name +' ' + fmt_param, ax=ax)

        # Set axes attributes
        ax.set_xlabel(f'Reference {averaging_interval} {fmt_param} ({fmt_param_units})',
                      fontsize=font_size)
        ax.set_ylabel('Relative Probability', fontsize=font_size)
        ax.tick_params(axis='both', labelsize=0.75*font_size)
        plt.legend(fontsize=0.85*font_size)

        if write_to_file is True:
            todays_date = get_todays_date()
            figure_path = os.path.join(figure_path,
                                       f'{ref_name}_DistPlot_{param_name}_{todays_date}')
            if filename_suffix != '':
                figure_path = figure_path + '_' + filename_suffix
            figure_path += '.png'

            plt.tight_layout()
            plt.savefig(figure_path, dpi=300)
            plt.close()

    # Exception: Column name for reference monitor data not in passed df
    except KeyError as i:
        print(i, 'not found in passed reference dataframe')


def met_distrib(met_ref_data, avg_hrly_df, figure_path, sensor_name=None,
                write_to_file=True):
    """Create distribution plots for meteorological parameters provided in the
    passed met_ref_data dataframe.

    Distributions are displayed as relative frequencies (i.e., percentages of
    the total distribution of measurements).

    Args:
        met_ref_data (pandas DataFrame):
            Meteorological reference data (1-hour averages) for temperature,
            relative humidity, and dew point measurements.
        avg_hrly_df (pandas DataFrame):
            Dataframe containing the inter-sensor average value for 1-hour
            averaged air sensor measurements.
        figure_path (str):
            The full directory path to the folder where figures are saved.
            This should be located at ``[project_path]/figures``.
        sensor_name (str, optional):
            The name of the air sensor (make, manufacturer). Defaults to None.
        write_to_file (bool, optional):
            If true, the figure will be saved as a png image to the
            ``[project_path]/figures`` subdirectory. Defaults to True.

    Returns:
        None.

    """
    font_size = 10
    detail_font_size = 0.8*font_size
    n_var = len(met_ref_data.count())  # Number of met variables to plot
    fig, axs = plt.subplots(1, n_var, figsize=(5.15, 2.54))

    fill_color = [['#77529A'], ['#b06c8b'], ['#588ded']]
    plt.suptitle('Evaluation Site Meteorological Conditions\n',
                 fontsize=font_size)

    fig.subplots_adjust(wspace=.6,
                        hspace=.3,
                        left=.12,
                        right=.88,
                        top=.86,
                        bottom=.17)

    for i in range(n_var):
        sensor_data = False
        param = met_ref_data.columns[i]

        data = met_ref_data[param].dropna()

        if data.empty:
            print(f'..Met data empty for {param}, trying sensor measurements')

            try:
                data = avg_hrly_df['mean_' + param].dropna()
                sensor_data = True
            except KeyError:
                print('..{param} not measured by sensor, unable to plot '
                      'distribution')
                continue
            if data.empty:
                print('..no intersensor averaged {param} data, unable to plot '
                      'distribution')
                continue

        sns.histplot(data,
                     ax=axs[i],
                     bins=15,
                     stat='percent',
                     kde=True,
                     color=fill_color[i][0],
                     **{'alpha': 0.6})

        if param.startswith('RH'):
            label = 'Relative Humidity (%)'
            if sensor_data:
                axs[i].set_title('*Sensor Measurements Shown*',
                                 fontsize=detail_font_size, y=0.97)
            axs[i].set_xlabel(label, fontsize=detail_font_size)
            axs[i].xaxis.set_major_locator(plt.MultipleLocator(25))

        if param.startswith('Temp'):
            label = 'Temperature ($\\degree$C)'
            if sensor_data:
                axs[i].set_title('*Sensor Measurements Shown*',
                                 fontsize=detail_font_size, y=0.97)
            axs[i].set_xlabel(label, fontsize=detail_font_size)
            axs[i].xaxis.set_major_locator(plt.MultipleLocator(10))

        if param.startswith('DP'):
            label = 'Dew Point ($\\degree$C)'
            if sensor_data:
                axs[i].set_title('*Sensor Measurements Shown*',
                                 fontsize=detail_font_size, y=0.97)
            axs[i].set_xlabel(label, fontsize=detail_font_size)

        axs[i].set_ylabel('Relative Probability (%)',
                          fontsize=detail_font_size)

        axs[i].tick_params(axis='both', labelsize=detail_font_size)

    if write_to_file is True:
        todays_date = get_todays_date()
        file_path = os.path.join(figure_path, 'Met',
                                 f'{sensor_name}_met_distplot_report_fmt_{todays_date}')
        plt.savefig(file_path + '.png', dpi=300)
        plt.close()


def recording_interval_histogram(full_df_list, xlims=(-10, 120), bar_width=2,
                                 bar_alpha=.4):
    """Plot indicating the uneven time delta in sensor data.

    Graphs bar plot of Log(counts) vs. time delta between consecutive timestamp
    entries.

    Args:
        full_df_list (list):
            List of pandas DataFrames containing timeseries data at the original
            recorded sampling frequency.
        xlims (Two-element tuple, optional):
            The x-axis limits (in seconds) for displaying the distribution of
            consecutive intervals between recorded timestamps. Defaults to
            (-10, 120).
        bar_width (int or float, optional):
            The width of bars displayed in the figure. Defaults to 2.
        bar_alpha (float, optional):
            The transparency of bars displayed in the figure. Defaults to .4.

    Returns:
        None.

    """
    xmin, xmax = xlims
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
