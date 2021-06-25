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
  Tue Apr 21 14:09:25 2020
Last Updated:
  Tue May 11 16:18:00 2021
"""


def Format_Param_Name(param):
    """
    Return formatted version of parameter column for plot, axis titles
    """
    try:
        if param.startswith('PM25'):
            fmt_param = 'PM$_{2.5}$'
            fmt_param_units = r'($\mu g/m^3$)'

        elif param.startswith('PM10'):
            fmt_param = 'PM$_{10}$'
            fmt_param_units = r'($\mu g/m^3$)'

        elif param.startswith('PM1'):
            fmt_param = 'PM$_{1}$'
            fmt_param_units = r'($\mu g/m^3$)'

        elif param == 'O3':
            fmt_param = '$O_3$'
            fmt_param_units = '(ppbv)'

        elif param == 'CO':
            fmt_param = '$CO$'
            fmt_param_units = '(ppbv)'

        elif param == 'NO2':
            fmt_param = '$NO_2$'
            fmt_param_units = '(ppbv)'

        elif param == 'Temp':
            fmt_param = 'Temperature'
            fmt_param_units = r'($\degree$C)'

        elif param == 'RH':
            fmt_param = 'Relative Humidity'
            fmt_param_units = '(%)'

        elif param == 'DP':
            fmt_param = 'Dewpoint'
            fmt_param_units = r'($\degree$C)'

        return fmt_param, fmt_param_units
    except NameError:
        print('Pollutant name not found. Please locate the proper '
              'pollutant header name in the sensor hourly dataframe.')
        return


#def Formatted_Sensor_Name(sensor_name):
#    """
#    Return formatted version of sensor names for plots. Legibility of sensor
#    names is improved by replacing underscores with blank spaces and adding
#    hyphens where relevant.
#    """
#    try:
#        if sensor_name == 'QuantAQ_ARISense':
#            fmt_sensor_name = 'QuantAQ ARISense'
#
#        if sensor_name == 'Apis_APM01':
#            fmt_sensor_name = 'Apis APM01'
#
#        if sensor_name == 'Clarity_Node_and_S':
#            fmt_sensor_name = 'Clarity Node & Node-S'
#
#        if sensor_name == 'Clarity_Node':
#            fmt_sensor_name = 'Clarity Node'
#
#        if sensor_name == 'Clarity_NodeS':
#            fmt_sensor_name = 'Clarity Node-S'
#
#        if sensor_name == 'Vaisala_AQT420':
#            fmt_sensor_name = 'Vaisala AQT-420'
#
#        if sensor_name == 'Sensit_RAMP':
#            fmt_sensor_name = 'SENSIT RAMP'
#
#        if sensor_name == 'APT_Maxima':
#            fmt_sensor_name = 'APT Maxima'
#
#        if sensor_name == 'Aeroqual_AQY':
#            fmt_sensor_name = 'Aeroqual AQY'
#
#        if sensor_name == 'IQAir_AirVisual_Pro':
#            fmt_sensor_name = 'IQAir AirVisual Pro'
#
#        if sensor_name == 'PurpleAir_PAII':
#            fmt_sensor_name = 'PurpleAir PA-II-SD'
#
#        if sensor_name == 'Canary_S':
#            fmt_sensor_name = 'Canary-S'
#
#        if sensor_name == 'Empty':  # Special condition for PT template
#            fmt_sensor_name = ''
#
#        return fmt_sensor_name
#
#    except NameError:
#        print('Sensor name not found. Please enter a valid sensor name from '
#              'the following list: ')
#        print('Clarity_Node/S; Clarity_Node; Clarity_NodeS; Vaisala_AQT420; '
#              'Sensit_RAMP; APT_Maxima; Aeroqual_AQY; AirVisual_Pro; '
#              'ARISense; PurpleAir_PAII; '
#              'Empty (Performance Targets reporting template)')


def Format_Metric_Name(metric):
    """
    Return formatted version of performance target metric with units
    """
    try:
        if metric.startswith('RMSE'):
            fmt_metric = 'RMSE'
            fmt_metric_units = r'($\mu g/m^3$)'
        if metric.startswith('CV'):
            fmt_metric = 'CV'
            fmt_metric_units = '(%)'
        if metric.startswith('std'):
            fmt_metric = 'Standard Deviation'
            fmt_metric_units = r'($\mu g/m^3$)'

        return fmt_metric, fmt_metric_units

    except NameError as E:
        print(E)
