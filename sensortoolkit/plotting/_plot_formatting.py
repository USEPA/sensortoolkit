# -*- coding: utf-8 -*-
"""
This module contains methods for configuring various plot formatting presets
(e.g., configuring the fontsize, wrapping long figure titles over multiple
lines, specifying figure dimensions for formatting figures with multiple
subplots, each displaying sensor data, etc.).

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Mon Jan 27 08:49:12 2020
Last Updated:
  Wed Jul 28 14:13:57 2021
"""
from pandas.plotting import register_matplotlib_converters
import numpy as np
from textwrap import wrap
import math
register_matplotlib_converters()


def set_fontsize(serials):
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
    elif (n_sensors < 7 and n_sensors > 1):
        fontsize = 12.75
    else:
        fontsize = 11.7

    return fontsize


def wrap_text(labels, max_label_len=10):
    """Formats plotting text with line breaks based on specified text length.

    Code modified via Stack Overflow user DavidG code
    (https://stackoverflow.com/questions/47057789/matplotlib-wrap-text-in-legend)

    Args:
        labels (list):
            list plotting labels (strings) such as header/title text
        max_label_len (int):
            The maximum number of characters on a single line. Labels longer
            than this will have a newline character inserted at every
            max_label_len number of characters.

    Returns:
        labels (list):
            Modified list of labels with the newline character inserted for
            labels exceeding the max_label_len.

    """
    labels = ['\n'.join(wrap(l, max_label_len)) for l in labels]

    return labels


def subplot_dims(n_sensors):
    """Recommends subplot dimensions based on the nearest perfect square for
    number of sensors (except when n%10, n_cols in multiples of 5)

    Args:
        n_sensors (int):
            The number of sensors in the deployment group.
    Returns:
        (tuple): Two-element tuple containing:

            - **n_rows** (*int*): The number of subplot rows.
            - **n_cols** (*int*): The number of subplot columns.

    """
    sqr = np.sqrt(n_sensors)
    n_rows = math.floor(sqr)
    if n_sensors % 10 == 0:
        n_rows = math.floor(n_sensors/5)
    n_cols = math.ceil(n_sensors / n_rows)

    return (n_rows, n_cols)


def sensor_subplot_formatting(number_of_sensors, param_obj, report_fmt,
                              **kwargs):
    """Configure subplot parameters that control the spacing of subplots,
    number of subplots and dimensions of the Matplotliub axes object array,
    color bar formatting, etc.

    Args:
        number_of_sensors (int): DESCRIPTION.
        param_obj (sensortoolkit.Parameter): DESCRIPTION.
        report_fmt (bool): DESCRIPTION.

    Keyword arguments:

        - **show_colorbar** (*bool*):
          DESCRIPTION. Defaults to True.
        - **sensor_serials** (*dict*):
          DESCRIPTION. Defaults to None.

    Raises:
        ValueError: DESCRIPTION.

    Returns:
        (tuple): 17-element tuple containing:

            - **Nr** (*int*): The number of rows of subplots for the figure
              instance.
            - **Nc** (*int*): The number of columns of subplots for the figure
              instance.
            - **fig_size** (*tuple*): The size of the figure instance (x_width,
              y_width).
            - **suptitle_xpos** (*float*): The relative x-coordinate position of
              the figure title.
            - **suptitle_ypos** (*float*): The relative y-coordinate position of
              the figure title.
            - **title_text_wrap** (*int*): The number of characters to include
              on a single line of the title before inserting a new line.
            - **detail_fontsize** (*int* or *float*): DESCRIPTION.
            - **wspace** (*float*): The width (x-distance) between each subplot.
            - **hspace** (*float*): The height (y-distance) between each
              subplot.
            - **left** (*float*): The left-most (x-min) limits at which the
              subplots will be drawn.
            - **right** (*float*): The right-most (x-max) limits at which the
              subplots will be drawn.
            - **top** (*float*): The top-most (y-max) limits at which the
              subplots will be drawn.
            - **bottom** (*float*): The bottom-most (y-min) limits at which the
              subplots will be drawn.
            - **filename_suffix** (*str*): DESCRIPTION.
            - **cbar_padding** (*float*): DESCRIPTION.
            - **cbar_aspect** (*int* or *float*): DESCRIPTION.
            - **font_size** (*int* or *float*): DESCRIPTION.

    """
    RH_colormap = kwargs.get('show_colorbar', True)
    serials = kwargs.get('sensor_serials', None)
    param_averaging = param_obj.averaging

    Nr, Nc = subplot_dims(number_of_sensors)

    sensor_plural, row_plural, column_plural = '', '', ''

    if number_of_sensors > 1:
        sensor_plural = 's'
    if Nr > 1:
        row_plural = 's'
    if Nc > 1:
        column_plural = 's'

    print('..creating subplot for', str(number_of_sensors),
          'sensor' + sensor_plural, 'with', str(Nr),
          'row' + row_plural,  'and', str(Nc), 'column' + column_plural)

    # Get default fontsize to fall back on if none specified
    font_size = set_fontsize(serials)

    if number_of_sensors == 1:  # 1x1 subplot

        if RH_colormap is True:
            if len(param_averaging) == 1:
                font_size = 12
                fig_size = (4.3, 3.91)
                wspace = .1
                hspace = .1
                left = 0.12
                right = 0.8
                top = 0.85
                bottom = 0.15
                suptitle_xpos = 0.46
                suptitle_ypos = 0.95
                title_text_wrap = 30
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

        suptitle_xpos = 0.50
        suptitle_ypos = 0.98
        title_text_wrap = 35
        detail_fontsize = .75*font_size
        filename_suffix = '1_sensor'
        cbar_padding = .13
        cbar_aspect = 20

    elif number_of_sensors in (2, 3):  # 3x1 subplot

        if RH_colormap is True:
            fig_size = (12.3, 5.12)
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

        suptitle_xpos = 0.50
        suptitle_ypos = 0.99
        title_text_wrap = 70
        detail_fontsize = .9*font_size
        filename_suffix = '3_sensors'
        cbar_padding = .16
        cbar_aspect = 20

    elif number_of_sensors in (4, 5, 6):  # 2x3 subplot
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

        suptitle_xpos = 0.50
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

        suptitle_xpos = 0.50
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

        suptitle_xpos = 0.50
        detail_fontsize = .85*font_size
        filename_suffix = '9_sensors'
        cbar_padding = .06
        cbar_aspect = 20
    else:
        raise ValueError('No formatting presets configured for',
                         str(number_of_sensors))

    if report_fmt is True:
        # Plot 1-hour averaged dataset
        if len(param_averaging) == 1:
            font_size = 12
            fig_size = (4.3, 3.91)
            wspace = .1
            hspace = .1
            left = 0.12
            right = 0.8
            top = 0.85
            bottom = 0.15
            suptitle_xpos = 0.5
            suptitle_ypos = 1.01
            title_text_wrap = 30
            suptitle_ypos = 0.95
        # Plot both 1-hour and 24-hour averaged datasets
        else:
            wspace = .4
            hspace = .08
            left = 0.1
            right = 0.92
            top = 0.9
            bottom = 0.30
            cbar_padding = .0
            cbar_aspect = 20
            font_size = 9
            detail_fontsize = 0.9*font_size
        filename_suffix = 'report_fmt'

    return (Nr, Nc, fig_size, suptitle_xpos, suptitle_ypos, title_text_wrap,
            detail_fontsize, wspace, hspace, left, right, top, bottom,
            filename_suffix, cbar_padding, cbar_aspect, font_size)


def get_colormap_range(df_list):
    """Set default range for colormap based on number of sensors

    The range is normalized to between zero and one (0.0, 1.0)


    Args:
        df_list (list): Sensor datasets.

    Returns:
        cmap_range (tuple): Tuple of length 2 containing the lower and upper
        bounds for the normalized colormap range.

    """
    if len(df_list) < 4:
        cmap_range = (0, 0.4)
    else:
        cmap_range = (0, 1)

    return cmap_range


def met_scatter_lims(met_data, param, met_param, xlims, ylims, serials,
                     avg_df):
    """Set x and y limits for plots generated by normalized_met_scatter()

    Args:
        met_data (TYPE): DESCRIPTION.
        param (TYPE): DESCRIPTION.
        met_param (TYPE): DESCRIPTION.
        xlims (TYPE): DESCRIPTION.
        ylims (TYPE): DESCRIPTION.
        serials (TYPE): DESCRIPTION.
        avg_df (TYPE): DESCRIPTION.

    Returns:
        (tuple): Four-element tuple containing:
            - **xmin** (*float*)
            - **xmax** (*float*)
            - **ymin** (*float*)
            - **ymax** (*float*)

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
        ymin = avg_df['mean_Normalized_' + param + '_Value'].quantile(0.01)
        ymax = avg_df['mean_Normalized_' + param + '_Value'].quantile(0.99)

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
