# -*- coding: utf-8 -*-
"""This module contains a method for displaying air sensor performance using
metrics and target values recommended by U.S. EPA for the evaluation of sensors
measuring either PM2.5 or O3.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Mon Jan 27 08:49:12 2020
Last Updated:
  Wed Jul 28 14:24:17 2021
"""
import sys
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
import seaborn as sns
from sensortoolkit.datetime_utils import get_todays_date
from sensortoolkit.param import Parameter
register_matplotlib_converters()


def performance_metrics(stats_df, deploy_dict, param=None,
                        param_averaging=None,
                        font_size=12, path=None, sensor_name=None,
                        write_to_file=True, **kwargs):
    """Display performance metric results via a set of adjacent subplots
    corresponding to each metric. Results are displayed as either dots (if
    the number of sensors is less than four) or via boxplots (number of sensors
    exceeds 3). Target ranges are indicated by gray shaded regions, and target
    goals are indicated by dark gray lines.

    Args:
        stats_df (pandas dataframe):
            A dataframe containing regression statistics (sensor vs. FRM/FEM
            reference) at averaging intervals corresponding to the
            ``param_averaging`` attribute.
        deploy_dict (dict):
            A dictionary containing descriptive statistics and textual
            information about the deployment (testing agency, site, time
            period, etc.), sensors tested, and site conditions during the
            evaluation.
        param (str, optional):
            Parameter name to evaluate. Defaults to None.
        param_averaging (str, optional):
            The measurement averaging intervals commonly utilized for
            analyzing data corresponding the selected parameter. Defaults
            to None.
        font_size (int, optional):
            The font size for text displayed in the figure. Defaults to 12.
        path (str, optional):
            The full directory path to the ``/figures`` subfolder housed
            within the user's project path. Defaults to None.
        sensor_name (str, optional):
            The make and model of the air sensor for which the performance
            evaluation figure is being generated. Defaults to None.
        write_to_file (bool, optional):
            If true, the figure will be written to the /figures/[param] sensor
            subdirectory (where 'param' is the name of the parameter being
            evaluated). Defaults to True.
        **kwargs (TYPE): Plotting keyword arguments.

    Returns:
        None.

    """
    sns.set_style('darkgrid')

    param_obj = Parameter(param)

    targets = param_obj.PerformanceTargets.get_all_metrics()

    if any(metric_info == {} for metric_info in targets.values()):
        sys.exit('Performance metrics and target values not set for ' + param)

    if len(param_obj.averaging) == 2:
        PLOT_XMIN = -0.50
        PLOT_XMAX = 1.5
    if len(param_obj.averaging) == 1:
        PLOT_XMIN = -1
        PLOT_XMAX = 1

    PLOT_XRANGE = PLOT_XMAX - PLOT_XMIN

    plotting_dims = {
        # Plot y-limits
        # y-min, y-max
        'ylims': {'R^2': (-0.02, 1.02)},

        # Target goal horizontal line
        # (y-coord, x-min, x-max)
        'hline_dims': {'R^2': (targets['Linearity']['R^2']['goal'],
                               PLOT_XMIN,
                               PLOT_XMAX),
                       'Slope': (targets['Bias']['Slope']['goal'],
                                 PLOT_XMIN,
                                 PLOT_XMAX),
                       'Intercept': (targets['Bias']['Intercept']['goal'],
                                     PLOT_XMIN,
                                     PLOT_XMAX),
                       'CV': (targets['Precision']['CV']['goal'],
                              PLOT_XMIN,
                              PLOT_XMAX),
                       'RMSE': (targets['Error']['RMSE']['goal'],
                                PLOT_XMIN,
                                PLOT_XMAX),
                       'NRMSE': (targets['Error']['NRMSE']['goal'],
                                 PLOT_XMIN,
                                 PLOT_XMAX),
                       'SD': (targets['Precision']['SD']['goal'],
                              PLOT_XMIN,
                              PLOT_XMAX)},

        # x-min, y-min, x-range, y-range
        'box_dims': {'R^2': (PLOT_XMIN,
                             targets['Linearity']['R^2']['bounds'][0],
                             PLOT_XRANGE,
                             targets['Linearity']['R^2']['bounds'][1] -
                             targets['Linearity']['R^2']['bounds'][0]),
                     'Slope': (PLOT_XMIN,
                               targets['Bias']['Slope']['bounds'][0],
                               PLOT_XRANGE,
                               targets['Bias']['Slope']['bounds'][1] -
                               targets['Bias']['Slope']['bounds'][0]),
                     'Intercept': (PLOT_XMIN,
                                   targets['Bias']['Intercept']['bounds'][0],
                                   PLOT_XRANGE,
                                   targets['Bias']['Intercept']['bounds'][1] -
                                   targets['Bias']['Intercept']['bounds'][0]),
                     'CV': (PLOT_XMIN,
                            targets['Precision']['CV']['bounds'][0],
                            PLOT_XRANGE,
                            targets['Precision']['CV']['bounds'][1] -
                            targets['Precision']['CV']['bounds'][0]),
                     'RMSE': (PLOT_XMIN,
                              targets['Error']['RMSE']['bounds'][0],
                              PLOT_XRANGE,
                              targets['Error']['RMSE']['bounds'][1] -
                              targets['Error']['RMSE']['bounds'][0]),
                     'NRMSE': (PLOT_XMIN,
                               targets['Error']['NRMSE']['bounds'][0],
                               PLOT_XRANGE,
                               targets['Error']['NRMSE']['bounds'][1] -
                               targets['Error']['NRMSE']['bounds'][0]),
                     'SD': (PLOT_XMIN,
                            targets['Precision']['SD']['bounds'][0],
                            PLOT_XRANGE,
                            targets['Precision']['SD']['bounds'][1] -
                            targets['Precision']['SD']['bounds'][0])}
        }

    remove_keys = {}
    for category in targets.keys():
        for metric in targets[category].keys():
            goal = targets[category][metric]['goal']
            if goal is None:
                remove_keys[category] = metric

    for category in remove_keys:
        metric = remove_keys[category]
        targets[category].pop(metric)
        plotting_dims['hline_dims'].pop(metric)
        plotting_dims['box_dims'].pop(metric)

    cv_vals = {interval: [] for interval in param_averaging}
    std_vals = {interval: [] for interval in param_averaging}
    rmse_vals = {interval: [] for interval in param_averaging}
    nrmse_vals = {interval: [] for interval in param_averaging}

    # Extract metric values into metric dictionaries
    for group in deploy_dict['Deployment Groups']:
        param_stats = deploy_dict['Deployment Groups'][group][param]
        for interval in param_averaging:
            cv_vals[interval].append(
                                param_stats['Precision']['cv_' + interval])
            std_vals[interval].append(
                                param_stats['Precision']['std_' + interval])
            rmse_vals[interval].append(
                                param_stats['Error']['rmse_' + interval])
            nrmse_vals[interval].append(
                                param_stats['Error']['nrmse_' + interval])

    # Boxplot fill colors
    default_fill = ['#80c5c9', '#4ea1c0']
    fill_color = kwargs.get('fill_color', default_fill)

    # Marker properties
    marker = kwargs.get('marker', 'o')
    marker_size = kwargs.get('marker_size', 7)
    marker_line_width = kwargs.get('marker_line_width', 1)
    mean_marker = kwargs.get('mean_marker', 'd')

    # List of metrics to plot
    metrics = []
    for category in targets:
        metrics.extend(targets[category].keys())

    metric_names = ['R$^2$', 'Slope', 'Intercept', 'RMSE',
                    'NRMSE', 'CV', 'SD']

    if 'NRMSE' in remove_keys.values():
        metric_names.remove('NRMSE')

    fig_width = kwargs.get('figure_width', 15.7)
    fig_height = kwargs.get('figure_height', 3.9)
    fig, axs = plt.subplots(1, len(metrics), figsize=(fig_width, fig_height))

    n_sensors = stats_df.where((stats_df['Sensor Name'].notna()) &
                               (stats_df['R$^2$'].notna())
                               ).Sensor_Number.nunique()

    stats_df = stats_df[['R$^2$', 'Slope', 'Intercept', 'Averaging Interval']]
    stats_df = stats_df.where(
                    stats_df['Averaging Interval'].isin(param_averaging))

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

                if metric_name == 'CV':
                    metric_data = cv_vals
                if metric_name == 'SD':
                    metric_data = std_vals
                if metric_name == 'RMSE':
                    metric_data = rmse_vals
                if metric_name == 'NRMSE':
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
                dim_key = 'R^2'
                lower_lim = None
                upper_lim = None

            if metric_name == 'Slope':
                dim_key = 'Slope'
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
                dim_key = 'Intercept'
                upper_lim = abs(1.5*stats_df[metric_name]).max()
                if upper_lim < 10:
                    upper_lim = 10
                lower_lim = -1*upper_lim

                metric_name = rf'{metric_name} ({param_obj.units})'

            if metric_name == 'CV':
                dim_key = 'CV'
                lower_lim = 0
                upper_lim = 1.5*data_df[metric_name].max()
                if upper_lim < 50:
                    upper_lim = 50
                metric_name = rf'{metric_name} (%)'

            if metric_name == 'RMSE':
                dim_key = 'RMSE'
                upper_lim = 1.5*data_df[metric_name].max()
                lower_lim = 0
                if upper_lim < 10:
                    upper_lim = 10

                metric_name = rf'{metric_name} ({param_obj.units})'

            if metric_name == 'NRMSE':
                dim_key = 'NRMSE'
                lower_lim = 0
                if upper_lim < 50:
                    upper_lim = 50
                metric_name = r'NRMSE ($\%$)'

            if metric_name == 'SD':
                dim_key = 'SD'
                lower_lim = 0
                upper_lim = 1.5*data_df[metric_name].max()
                metric_name = rf'{metric_name} ({param_obj.units})'

                if upper_lim < 10:
                    upper_lim = 10

            # Get formatting values
            ylims = kwargs.get(dim_key + '_ylims',
                plotting_dims['ylims'].get(dim_key, (lower_lim, upper_lim)))
            hline_dims = kwargs.get(dim_key + '_hline_dims',
                                plotting_dims.get('hline_dims').get(dim_key))
            box_dims = kwargs.get(dim_key + '_box_dims',
                                  plotting_dims.get('box_dims').get(dim_key))

            # Assign to local variables
            ymin, ymax = ylims
            hline_y, hline_xmin, hline_xmax = hline_dims
            rec_x0, rec_y0, rec_xspan, rec_yspan = box_dims

            axs[ax_idx].set_xlim(PLOT_XMIN, PLOT_XMAX)

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
        todays_date = get_todays_date()

        plt.savefig(path + param + '\\' + sensor_name + '_regression_boxplot_'
                    + param + '_' + todays_date + '.png', dpi=300)
        plt.close()
