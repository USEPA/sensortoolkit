# -*- coding: utf-8 -*-
"""
@Author:
    | Samuel Frederick, NSSC Contractor (ORAU)
    | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Mon Jan 27 08:49:12 2020
Last Updated:
  Wed Jul 28 14:20:18 2021
"""
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

    Returns:

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
        ax.set_xlabel('Reference ' + averaging_interval + ' ' + fmt_param +
                      ' ' + fmt_param_units, fontsize=font_size)
        ax.set_ylabel('Relative Probability', fontsize=font_size)
        ax.tick_params(axis='both', labelsize=0.75*font_size)
        plt.legend(fontsize=0.85*font_size)

        if write_to_file is True:
            todays_date = get_todays_date()
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


def met_distrib(met_ref_data, figure_path, sensor_name=None,
                write_to_file=True):
    """Create distribution plots for meteorological parameters provided in the
    passed met_ref_data dataframe.


    Args:

    Returns:

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
        param = met_ref_data.columns[i]
        sns.histplot(met_ref_data[param].dropna(),
                     ax=axs[i],
                     bins=15,
                     kde=True,
                     color=fill_color[i][0],
                     **{'alpha': 0.6})

        if param == 'RH_Value':
            axs[i].set_xlabel('Relative Humidity (%)',
                              fontsize=detail_font_size)
            axs[i].xaxis.set_major_locator(plt.MultipleLocator(25))

        if param == 'Temp_Value':
            axs[i].set_xlabel('Temperature ($\\degree$C)',
                              fontsize=detail_font_size)
            axs[i].xaxis.set_major_locator(plt.MultipleLocator(10))

        if param == 'DP_Value':
            axs[i].set_xlabel('Dew Point ($\\degree$C)',
                              fontsize=detail_font_size)

        axs[i].set_ylabel('Relative Probability',
                          fontsize=detail_font_size)

        axs[i].tick_params(axis='both', labelsize=detail_font_size)

    if write_to_file is True:
        todays_date = get_todays_date()
        file_path = figure_path + 'Met' + '\\' + sensor_name + '_'\
            'met_distplot_report_fmt' + '_' + todays_date
        plt.savefig(file_path + '.png', dpi=300)
        plt.close()


def recording_interval_histogram(full_df_list, xmin=-10, xmax=120,
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
