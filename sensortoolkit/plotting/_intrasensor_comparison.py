# -*- coding: utf-8 -*-
"""
@Author:
    | Samuel Frederick, NSSC Contractor (ORAU)
    | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Mon Jan 27 08:49:12 2020
Last Updated:
  Wed Jul 28 14:22:18 2021
"""
from pandas.plotting import register_matplotlib_converters
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.colors import rgb2hex
from matplotlib.patches import Rectangle
import seaborn as sns
from sensortoolkit.datetime_utils import get_todays_date
register_matplotlib_converters()
sns.set_style('darkgrid')


def compare_sensors(stats_df, metric, fontsize=15, cmap_name='Set1',
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
        todays_date = get_todays_date()
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
