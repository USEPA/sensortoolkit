

def performance_metrics():
    """
    **Keyword Arguments:**

    :param str fill_color:
        DESCRIPTION
    :param str marker:
        DESCRIPTION
    :param marker_size:
        DESCRIPTION
    :type marker_size: int or float
    :param marker_line_width:
        DESCRIPTION
    :type marker_line_width: int or float
    :param str mean_marker:
        DESCRIPTION
    :param figure_width:
        DESCRIPTION
    :type figure_width: int or float
    :param figure_height:
        DESCRIPTION
    :type figure_height: int or float
    :param R^2_ylims:
        The y-limits (ymin, ymax) for the metric subplot.
    :type R^2_ylims: Two-element tuple of floats
    :param Slope_ylims:
        The y-limits (ymin, ymax) for the metric subplot.
    :type Slope_ylims: Two-element tuple of floats
    :param Intercept_ylims:
        The y-limits (ymin, ymax) for the metric subplot.
    :type Intercept_ylims: Two-element tuple of floats
    :param CV_ylims:
        The y-limits (ymin, ymax) for the metric subplot.
    :type CV_ylims: Two-element tuple of floats
    :param RMSE_ylims:
        The y-limits (ymin, ymax) for the metric subplot.
    :type RMSE_ylims: Two-element tuple of floats
    :param NRMSE_ylims:
        The y-limits (ymin, ymax) for the metric subplot.
    :type NRMSE_ylims: Two-element tuple of floats
    :param SD_ylims:
        The y-limits (ymin, ymax) for the metric subplot.
    :type SD_ylims: Two-element tuple of floats
    :param R^2_hline_dims:
        Dimensions for the target goal horizontal line. Tuple containing the
        y-coordinate of the target value, x-min (leftmost) coordinate for
        drawing horizontal line, and the x-max (rightmost) coordinate for
        drawing horizontal line).
    :type R^2_hline_dims: Three-element tuple
    :param Slope_hline_dims:
        Dimensions for the target goal horizontal line. Tuple containing the
        y-coordinate of the target value, x-min (leftmost) coordinate for
        drawing horizontal line, and the x-max (rightmost) coordinate for
        drawing horizontal line).
    :type Slope_hline_dims: Three-element tuple
    :param Intercept_hline_dims:
        Dimensions for the target goal horizontal line. Tuple containing the
        y-coordinate of the target value, x-min (leftmost) coordinate for
        drawing horizontal line, and the x-max (rightmost) coordinate for
        drawing horizontal line).
    :type Intercept_hline_dims: Three-element tuple
    :param CV_hline_dims:
        Dimensions for the target goal horizontal line. Tuple containing the
        y-coordinate of the target value, x-min (leftmost) coordinate for
        drawing horizontal line, and the x-max (rightmost) coordinate for
        drawing horizontal line).
    :type CV_hline_dims: Three-element tuple
    :param RMSE_hline_dims:
        Dimensions for the target goal horizontal line. Tuple containing the
        y-coordinate of the target value, x-min (leftmost) coordinate for
        drawing horizontal line, and the x-max (rightmost) coordinate for
        drawing horizontal line).
    :type RMSE_hline_dims: Three-element tuple
    :param NRMSE_hline_dims:
        Dimensions for the target goal horizontal line. Tuple containing the
        y-coordinate of the target value, x-min (leftmost) coordinate for
        drawing horizontal line, and the x-max (rightmost) coordinate for
        drawing horizontal line).
    :type NRMSE_hline_dims: Three-element tuple
    :param SD_hline_dims:
        Dimensions for the target goal horizontal line. Tuple containing the
        y-coordinate of the target value, x-min (leftmost) coordinate for
        drawing horizontal line, and the x-max (rightmost) coordinate for
        drawing horizontal line).
    :type SD_hline_dims: Three-element tuple
    :param R^2_box_dims:
        Dimensions for a box indicating the metric target range. Four element
        tuple containing the x-min (left-most coordinate of the box), y-min
        (bottom-most coordinate of the target range box), x-range (the height
        of the box, or the difference between the x-min coordinate position
        and the x-max coordinate position), and the y-range (the width of the
        box, or the difference between the y-min coordinate position and the
        y-max coordinate position).
    :type R^2_box_dims: Four-element tuple
    :param Slope_box_dims:
        Dimensions for a box indicating the metric target range. Four element
        tuple containing the x-min (left-most coordinate of the box), y-min
        (bottom-most coordinate of the target range box), x-range (the height
        of the box, or the difference between the x-min coordinate position
        and the x-max coordinate position), and the y-range (the width of the
        box, or the difference between the y-min coordinate position and the
        y-max coordinate position).
    :type Slope_box_dims: Four-element tuple
    :param Intercept_box_dims:
        Dimensions for a box indicating the metric target range. Four element
        tuple containing the x-min (left-most coordinate of the box), y-min
        (bottom-most coordinate of the target range box), x-range (the height
        of the box, or the difference between the x-min coordinate position
        and the x-max coordinate position), and the y-range (the width of the
        box, or the difference between the y-min coordinate position and the
        y-max coordinate position).
    :type Intercept_box_dims: Four-element tuple
    :param CV_box_dims:
        Dimensions for a box indicating the metric target range. Four element
        tuple containing the x-min (left-most coordinate of the box), y-min
        (bottom-most coordinate of the target range box), x-range (the height
        of the box, or the difference between the x-min coordinate position
        and the x-max coordinate position), and the y-range (the width of the
        box, or the difference between the y-min coordinate position and the
        y-max coordinate position).
    :type CV_box_dims: Four-element tuple
    :param RMSE_box_dims:
        Dimensions for a box indicating the metric target range. Four element
        tuple containing the x-min (left-most coordinate of the box), y-min
        (bottom-most coordinate of the target range box), x-range (the height
        of the box, or the difference between the x-min coordinate position
        and the x-max coordinate position), and the y-range (the width of the
        box, or the difference between the y-min coordinate position and the
        y-max coordinate position).
    :type RMSE_box_dims: Four-element tuple
    :param NRMSE_box_dims:
        Dimensions for a box indicating the metric target range. Four element
        tuple containing the x-min (left-most coordinate of the box), y-min
        (bottom-most coordinate of the target range box), x-range (the height
        of the box, or the difference between the x-min coordinate position
        and the x-max coordinate position), and the y-range (the width of the
        box, or the difference between the y-min coordinate position and the
        y-max coordinate position).
    :type NRMSE_box_dims: Four-element tuple
    :param SD_box_dims:
        Dimensions for a box indicating the metric target range. Four element
        tuple containing the x-min (left-most coordinate of the box), y-min
        (bottom-most coordinate of the target range box), x-range (the height
        of the box, or the difference between the x-min coordinate position
        and the x-max coordinate position), and the y-range (the width of the
        box, or the difference between the y-min coordinate position and the
        y-max coordinate position).
    :type SD_box_dims: Four-element tuple
    :param str hline_color:
        DESCRIPTION
    :param str box_facecolor:
        DESCRIPTION
    :param font_scale:
        DESCRIPTION
    :type font_scale: int or str
    :param float fig_wspace:
        DESCRIPTION
    :param float fig_hspace:
        DESCRIPTION
    :param float fig_left:
        DESCRIPTION
    :param float fig_right:
        DESCRIPTION
    :param float fig_top:
        DESCRIPTION
    :param float fig_bottom:
        DESCRIPTION

        """

def sensor_subplot_formatting():
    """
    **Keyword Arguments:**

    :param bool show_colorbar:
        DESCRIPTION. Defaults to True.
    :param dict sensor_serials:
        DESCRIPTION. Defaults to None.

    """

def draw_scatter():
    """
    **Keyword Arguments:**

    :param str monocolor:
        A single color (specified in hex) for scatter. Scatter are colored
        using monocolor if colormap_vals is empty. Defaults to '#0048AD'.
    :param float point_size:
        The size of the scatter points. Defaults to 20.
    :param float point_alpha:
        The transparency of the scatter plots. Defaults to 0.7.
    :param str plot_aspect:
        Aspect ratio for scatter plot dimensions. Defaults to 'equal'.
    :param float plottext_alpha:
        The transparency of the text drawn on scatter plots indicating
        regression statistics. Defaults to 0.8.
    :param float plottext_size:
        The size of the text drawn on scatter plots indicating
        regression statistics as a fraction of the passed fontsize. Defaults
        to 90% the value of the fontsize.
    :param str plottext_color:
        The color of the text drawn on scatter plots indicating
        regression statistics. Defaults to 'k'.
    :param float plottext_xloc:
        The left-most x-coordinate of the text drawn on scatter plots.
        Default depends on the value passed to the plottext_postion argument.
    :param float plottext_yloc:
        The top-most y-coordinate of the text drawn on scatter plots.
        Default depends on the value passed to the plottext_postion argument.
    :param float plottext_xdisplacement:
        The width displacement between text drawn on scatter plots. Defaults
        to 0.0.
    :param float plottext_ydisplacement:
        The height displacement between rows of text drawn on scatter plots.
        Defaults to 0.08.
    :param str plottext_position:
        Determines position of plot text. Options include 'upper_left' or
        'bottom_right'. Defaults to 'upper_left' if the slope of the '
        regression is greater than  1.75, else default is set to
        'bottom_right'.
    :param bool show_trendline:
        If true, display the OLS trendline on scatter plots. Defaults to True.
    :param bool show_RMSE:
        If true, display the root mean squared error on scatter plots.
        Defaults to True.
    :param bool show_spearman:
        If true, display the spearman correlation on scatterplots. Defaults
        to False.
    :param bool show_N:
        If true, display the number of scatter point pairs displayed on the
        plot. Defaults to True.
    :param bool show_one_to_one:
        If true, display the one-to-one line indicating ideal agreement
        between independent and depdendent variable. Defaults to True.
    :param float trendline_xmax:
        The draw distance (based on the passed x-coordinate) of the OLS
        trendline. Defaults to 120% the maximum of the independent variable.
    :param str trendline_color:
        The color of the trendline. Defaults to 'k' (black).
    :param float trendline_alpha:
        The transparency of the trendline. Defaults to 0.65.

    """

def scatter_plotter():
    """
    **Keyword Arguments:**

    :param str color_palette:
        Color palette assigned to relative-humidity colormapped scatter
        plot points
    :param TYPE colorbar_axespos:
        DEFINITION
    :param str colorbar_orientation:
        DEFINITION
    :param TYPE colorbar_title_fontsize:
        DEFINITION
    :param TYPE colorbar_title_ypos:
        DEFINITION
    :param TYPE colorbar_tick_labelsize:
        DEFINITION
    :param TYPE colorbar_tick_length:
        DEFINITION
    :param TYPE colorbar_tick_width:
        DEFINITION
    :param TYPE draw_cbar:
        DEFINITION
    :param TYPE fig_wspace:
        DEFINITION
    :param TYPE fig_hspace:
        DEFINITION
    :param TYPE fig_left:
        DEFINITION
    :param TYPE fig_right:
        DEFINITION
    :param TYPE fig_top:
        DEFINITION
    :param TYPE fig_bottom:
        DEFINITION
    :param TYPE filename_suffix:
        Optional string added to end of filename. Defaults to empty string.
    :param fontsize:
        The font size for the xlabel, ylabel, and plot text. Passed on to
        Draw_Scatter() which uses 0.85*font_size for tick labels.
    :type fontsize: str, passed to Draw_Scatter()
    :param monocolor:
        A single color (specified in hex) for scatter. Scatter are colored
        using monocolor if show_colorbar is False. Recommend #2251D0 (nice
        blue hue).
    :type monocolor: str, passed to Draw_Scatter()
    :param detail_fontsize:
        DEFINITION
    :param point_size:
        The size of the scatter points. Defaults to 20.
    :type point_size: int or float, passed to Draw_Scatter()
    :param float point_alpha:
        The transparency of the scatter plots. Defaults to 0.7.
    :param plot_aspect:
        Aspect ratio for scatter plot dimensions. Defaults to 'equal'.
    :type plot_aspect: str, passed to Draw_Scatter()
    :param plottext_alpha:
        The transparency of the text drawn on scatter plots indicating
        regression statistics. Defaults to 0.8.
    :type plottext_alpha: float, passed to Draw_Scatter()
    :param plottext_size:
        The size of the text drawn on scatter plots indicating
        regression statistics as a fraction of the passed fontsize. Defaults
        to 90% the value of the fontsize.
    :type plottext_size: float, passed to Draw_Scatter()
    :param plottext_color:
        The color of the text drawn on scatter plots indicating
        regression statistics. Defaults to 'k'.
    :type plottext_color: str, passed to Draw_Scatter()
    :param plottext_xloc:
        The left-most x-coordinate of the text drawn on scatter plots.
        Default depends on the value passed to the plottext_postion argument.
    :type plottext_xloc: float, passed to Draw_Scatter()
    :param plottext_yloc:
       The top-most y-coordinate of the text drawn on scatter plots.
        Default depends on the value passed to the plottext_postion argument.
    :type plottext_yloc: float, passed to Draw_Scatter()
    :param plottext_xdisplacement:
        The width displacement between text drawn on scatter plots. Defaults
        to 0.0.
    :type plottext_xdisplacement: float, passed to Draw_Scatter()
    :param plottext_ydisplacement:
        The height displacement between rows of text drawn on scatter plots.
        Defaults to 0.08.
    :type plottext_ydisplacement: float, passed to Draw_Scatter()
    :param plottext_position:
        Determines position of plot text. Options include 'upper_left' or
        'bottom_right'. Defaults to 'upper_left' if the slope of the '
        regression is greater than  1.75, else default is set to
        'bottom_right'.
    :type plottext_position: TYPE, passed to Draw_Scatter()
    :param str ref_name:
        DEFINITION
    :param str seaborn_style:
        DEFINITION
    :param bool show_colorbar:
        If true, relative humidity values will be used as a colormap on the
        scatterplot points.
    :param bool show_title:
        Show the title at the top of the plot. Includes the name of the
        sensor, the averaging interval, the evaluation parameter, and
        the name of the reference against which sensor data are compared.
    :param bool show_regression:
        If true, display the OLS regression equation on scatter plots.
        Defaults to True.
    :param bool show_trendline:
        If true, display the OLS trendline on scatter plots. Defaults to True.
    :param show_RMSE:
        If true, display the root mean squared error on scatter plots.
        Defaults to True.
    :type show_RMSE: bool, passed to Draw_Scatter()
    :param show_spearman:
        If true, display the spearman correlation on scatterplots. Defaults
        to False.
    :type show_spearman: bool, passed to Draw_Scatter()
    :param show_N:
        If true, display the number of scatter point pairs displayed on the
        plot. Defaults to True.
    :type show_N: bool, passed to Draw_Scatter()
    :param show_one_to_one:
        If true, display the one-to-one line indicating ideal agreement
        between independent and depdendent variable. Defaults to True.
    :type show_one_to_one: bool, passed to Draw_Scatter()
    :param bool tight_layout:
        Passed to matplotlib's ``fig.tight_layout()`` for narrow formatting
    :param TYPE tick_spacing:
        DEFINITION
    :param TYPE title_text:
        DEFINITION
    :param TYPE title_textwrap:
        DEFINITION
    :param TYPE title_xloc:
        DEFINITION
    :param TYPE title_yloc:
        DEFINITION
    :param trendline_xmax:
        The draw distance (based on the passed x-coordinate) of the OLS
        trendline. Defaults to 120% the maximum of the independent variable.
    :type trendline_xmax: TYPE, passed to Draw_Scatter()
    :param trendline_color:
        The color of the trendline. Defaults to 'k' (black).
    :type trendline_color: str, passed to Draw_Scatter()
    :param trendline_alpha:
        The transparency of the trendline. Defaults to 0.65.
    :type trendline_alpha: float, passed to Draw_Scatter()
    :param xlims:
        The x-limits of the scatter plot. Defaults to zero for the lower
        limit. For the upper limit, the following forumla is used:

        .. math::

            x_{max} = 1.25\\timesC_{max} + (\\Delta_{tick} - 1.25\\timesC_{max}\\%\\Delta_{tick})

        where:

          - :math:`x_{max}` is the upper limit of the x-axis

          - :math:`C_{max}` is the maximum value for either dependent or
            independent variable

          - :math:`\\%` is the modulo operator

          - :math:`\\Delta_{tick}` is the spacing between ticks along the
            x and y-axes (set by the ``tick_spacing`` argument)

        This forumla can be described in the following way:
        The upper limit is set to 125% the nearest multiple of the tick_spacing
        argument to the maximum concentration recorded by either independent
        or dependent variable (e.g., if the max concentration recorded by
        either sensor or reference is 22.4 ug/m^3 and the tick_spacing is set
        to divisions of 5 ug/m^3, the x upper limit will be set to 1.25*22.4
        = 28 -> rounded to the nearest multiple of 5 ug/m^3 becomes 30 ug/m^3.

    :type xlims: Two-element tuple of floats
    :param ylims:
        The y-limits of the scatter plot. Defaults to zero for the lower
        limit. For the upper limit, the same formula used for the x-limits is
        used.
    :type ylims: Two-element tuple of floats

    """

def normalized_met_scatter():
    """

    **Keyword Arguments:**

    :param point_size:
        The size of the scatter points. Defaults to 12
    :type point_size: float or int, passed to Draw_Scatter()
    :param point_alpha:
        The transparency of the scatter plots. Defaults to 0.5.
    :type point_alpha: float, passed to Draw_Scatter()
    :param list point_colors:
        DESCRIPTION. Defaults to None.
    :param xlims:
        DESCRIPTION. Defaults to None.
    :type xlims: Two-element tuple
    :param ylims:
        DESCRIPTION. Defaults to None.
    :type ylims: Two-element tuple
    :param cmap_norm_range:
        DESCRIPTION. Defaults to (0, 0.4).
    :type cmap_norm_range: Two-element tuple
    :param cmap_name:
        The name of the colormap which the scatter plot will be assigned.
        Defaults to 'Set1'.
    :type cmap_name: str, passed to Draw_Scatter()
    :param fontsize:
        The fontsize of plot titles and labels. Defaults to 12.
    :type fontsize: int or float, passed to Draw_Scatter()
    :param detail_fontsize:
        Fontsize for axes tick labels. Defaults to 10.
    :type detail_fontsize: int or float, passed to Draw_Scatter()
    :param TYPE subplot_adjust:
        DESCRIPTION.
        Defaults to None.
    :param bool show_errorbars:
        Defaults to False.
    :param bool show_legend:
        Defaults to True.
    :param fig_size:
        Defaults to (8, 4).
    :type fig_size: Two-element tuple
    :param int errorbar_nbins:
        Defaults to 10.
    :param str errorbar_color:
        Defaults to #151515.
    :param TYPE legend_pos:
        DESCRIPTION.


    """

def sensor_timeplot():
    """

    **Keyword Arguments:**

    :param str seaborn_style:
        The plotting style based on seaborn's style options. Defaults to
        'darkgrid'. Values must be a valid seaborn style name.
    :param int date_interval:
        Number of days between x-axis tick marks with 'mm-dd-yy' timestamps.
    :param str yscale:
        The scaling for the y-axis. Accepted values include 'linear',
        'log', 'symlog', 'logit', etc.
    :param ylims:
        The y-limits of the plot
    :type ylims: Two-element tuple of floats or ints
    :param bool format_xaxis_weeks:
        Plot the timeseries x-axis (time) in increments of 1 week. Defaults
        to False.
    :param fig_size:
        Tuple for setting the figure size.
    :type fig_size: Two-element tuple of floats or ints
    :param fontsize int or float:
        The font size for the xlabel, ylabel, and plot text. Passed on to
        Draw_Scatter() which uses 0.85*font_size for tick labels.
    :type fontsize: int or float
    :param font legend_fontscale:
        Relative scale of fontsize for text in the legend relative to label
        text.
    :param str cmap_name:
        The name of the palette assigned to relative-humidity colormapped
        scatter plot points
    :param cmap_normrange:
        Normalized range (0,1) for colormap hue selection. Limiting this
        range to something like (0.1, 0.9) is useful when using colormaps
        with high contrast extrema and a gradual change in hue is desired
        for plots.
    :type cmap_normrange: Two-element tuple
    :param bool show_title:
        If true, display the title for the figure. Defaults to True.
    :param str filename_suffix:
        Optional string added to end of filename. Defaults to empty string.
    :param TYPE box_xscale:
        DESCRIPTION. Defaults to
    :param TYPE box_yscale:
        DESCRIPTION. Defaults to
    :param TYPE box_wscale:
        DESCRIPTION. Defaults to
    :param TYPE box_hscale:
        DESCRIPTION. Defaults to
    :param TYPE legend_loc:
        DESCRIPTION. Defaults to
    :param TYPE sensor_colors:
        Default set by chosen colormap (cmap_name) and the normalized range
        for the colormap.
    :param float sensor_linealpha:
        The transparency of the lines indicating sensor measurements. Defaults
        to 0.70
    :param float sensor_linewidth:
        The width (thickness) of the lines indicating sensor measurements.
        Defaults to 1.5.
    :param str sensor_linestyle:
        The style of the lines indicating sensor measurements. Passed
        to matplotlib linestyles. Defaults to '-'.
    :param str ref_linecolor:
        The color of the line indicating reference measurements. Defaults
        to 'k'.
    :param float ref_linealpha:
        The transparency of the line indicating reference measurements.
        Defaults to 0.97
    :param float ref_linewidth:
        The width (thickness) of the line indicating reference measurements.
        Defaults to 1.5
    :param str ref_linestyle:
        The style of the lines indicating reference measurements. Passed
        to matplotlib linestyles. Defaults to '-'.
    :param str date_format:
        The strftime format in which dates will be displayed along the x-axis
        if 'format_xaxis_weeks' is False. Defaults to "%m-%d-%y".
    :param TYPE legend_fontsize:
        DESCRIPTION. Defaults to
    :param TYPE subplots_adjust:
        DESCRIPTION. Defaults to

    """
