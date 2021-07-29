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
  Wed Jul 28 14:24:17 2021
"""
import sys
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
import seaborn as sns
from Sensor_Evaluation._format.format_date import Get_Date
register_matplotlib_converters()


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

    #interval_to_freq = {'1-hour': 'Hourly',
     #                   '24-hour': 'Daily'}

    # List of frequencies ('Hourly, Daily') for specified parameter
    #param_freq = [interval_to_freq[interval] for interval in param_averaging]

    # Extract metric values into metric dictionaries
    for group in deploy_dict['Deployment Groups']:
        param_stats = deploy_dict['Deployment Groups'][group][param]
        for interval in param_averaging:
            #freq = interval_to_freq[interval].lower()
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

    fig_width = kwargs.get('figure_width', 15.7)
    fig_height = kwargs.get('figure_height', 3.9)
    fig, axs = plt.subplots(1, 7, figsize=(fig_width, fig_height))

    n_sensors = stats_df.where((stats_df['Sensor Name'].notna()) &
                               (stats_df['R$^2$'].notna())
                               ).Sensor_Number.nunique()

    metric_names = ['R$^2$', 'Slope', 'Intercept', 'RMSE',
                    'nRMSE', 'CV (%)', 'Standard Deviation']

    stats_df = stats_df[['R$^2$', 'Slope', 'Intercept', 'Averaging Interval']]
    stats_df = stats_df.where(
                    stats_df['Averaging Interval'].isin(param_averaging))

#    for interval, freq in zip(param_averaging, param_freq):
#        header = 'Averaging Interval'
#        stats_df[header] = stats_df[header].str.replace(freq, interval)

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
