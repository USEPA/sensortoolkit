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
  Fri Jul 31 08:39:37 2020
Last Updated:
  Wed Jul 7 15:01:00 2021
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
import math
import json
import sys
import os
import matplotlib.pyplot as plt
import Sensor_Evaluation as se


class SensorEvaluation:
    """A class for evaluating the performance of air sensors for use in
    ambient, outdoor, fixed site, non-regulatory supplemental and informational
    monitoring applications.

    As of February 2021, U.S. EPA has released two reports detailing
    recommended performance testing protocols, metrics, and target values for
    the evaluation of sensors measuring either fine particulate matter (PM2.5)
    or ozone (O3). More detail about EPA's sensor evaluation research as well
    as both reports can be found online at EPA's Air Sensor Toolbox:
        https://www.epa.gov/air-sensor-toolbox

    Please direct all inquiries to:
        Andrea Clements Ph.D., Research Physical Scientist
        U.S. EPA, Office of Research and Development
        Center for Environmental Measurement and Modeling
        Air Methods & Characterization Division, Source and Fine Scale Branch
        109 T.W. Alexander Drive, Research Triangle Park, NC  27711
        Office: 919-541-1363 | Email: clements.andrea@epa.gov

    Args:
        sensor_name              Name of sensor (format: manufacturer_device)
        eval_param               Parameter name to evaluate (e.g. PM25 or O3)
        load_raw_data            Import recorded (non-processed) sensor data
        write_to_file            Boolean variable for writing stats to file

    Attributes:
        avg_daily_df             Inter-sensor averaged dataframe at 24-hr res.
        avg_hourly_df            Inter-sensor averaged dataframe at 1-hr res.
        avg_stats_df             Inter-sensor averaged sensor-sensor reg. stats
        daily_df_list            List of 24-hr averaged sensor dataframes
        daily_ref_df             24-hr averaged reference dataframe
        data_path
        deploy_dict
        deployment_df
        figure_path              Directory path for figures
        full_df_list             List of recorded time res. sensor dataframes
        gas_hourly_ref_df        Hourly reference data for gas pollutants
        gas_list                 Common gas params in sensor dataframes
        gas_ref_columns          List of names for gas reference data
        hourly_ref_df            Reference dataframe for selected eval_param
        met_daily_ref_df         Daily avg. reference data for met pollutants
        met_hourly_ref_df        Hourly avg. reference data for met pollutants
        met_list                 Common met params in sensor dataframes
        met_ref_columns          List of names for met reference data
        pm_hourly_ref_df         Hourly reference data for pm pollutants
        pm_list                  Common pm params in sensor dataframes
        pm_ref_columns           List of names for pm reference data
        processed_path           Directory path for averaged sensor dataframes
        ref_dict                 Dictionary with uptime info for pm, gas, met
        ref_tup                  Tuple for unpacking reference data
        sensor_df_tuple          Tuple for unpacking sensor dataframes
        serials                  Sensor serial IDs for evaluated devices
        stats_df                 Statistics dataframe for sensor-ref regression
        stats_path               Path to directory where stats_df saved to csv
        tzone_shift              Integer variable for shifting ref data to UTC
    """
    # Dictionary of parameter names, organized by parameter type.
    param_dict = {'PM': ['PM1', 'PM25', 'PM10'],
                  'Gases': ['O3', 'NO2', 'NO', 'NOx',
                            'SO2', 'SOx', 'CO', 'CO2'],
                  'Met': ['Temp', 'RH', 'Press', 'DP', 'WS', 'WD']}

    param_formatting_dict = {'PM1': {'baseline': 'PM',
                                     'subscript': '1'},
                             'PM25': {'baseline': 'PM',
                                      'subscript': '2.5'},
                             'PM10': {'baseline': 'PM',
                                      'subscript': '10'},
                             'O3': {'baseline': 'O',
                                    'subscript': '3'},
                             'NO2': {'baseline': 'NO',
                                     'subscript': '2'},
                             'NO': {'baseline': 'NO',
                                    'subscript': None},
                             'NOx': {'baseline': 'NO',
                                     'subscript': 'x'},
                             'SO2': {'baseline': 'SO',
                                     'subscript': '2'},
                             'SOx': {'baseline': 'SO',
                                     'subscript': 'x'},
                             'CO': {'baseline': 'CO',
                                    'subscript': None},
                             'Temp': {'baseline': 'Temperature',
                                      'subscript': None},
                             'RH': {'baseline': 'Relative Humidity',
                                    'subscript': None},
                             'DP': {'baseline': 'Dew Point',
                                    'subscript': None},
                             'WS': {'baseline': 'Wind Speed',
                                    'subscript': None},
                             'WD': {'baseline': 'Wind Direction',
                                    'subscript': None}}

    # Absolute path for Sensor_Evaluation library and related work
    lib_path = os.path.abspath(os.path.join(__file__, '../..'))

    # API Credentials
    aqs_username = None
    aqs_key = None
    airnow_key = None

    def __init__(self, sensor_name, eval_param, load_raw_data=False,
                 reference_data=None, ref_name=None, serials=None,
                 tzone_shift=0, bbox=None, aqs_id=None, write_to_file=False):

        self.sensor_name = sensor_name
        self.eval_param = eval_param
        self.load_raw_data = load_raw_data
        self.write_to_file = write_to_file
        self.serials = serials
        self.tzone_shift = tzone_shift
        self.bbox = bbox
        self.aqs_id = aqs_id

        # path to raw sensor data
        self.data_path = '\\'.join((self.lib_path, 'Data and Figures',
                                    'sensor_data', self.sensor_name,
                                    'raw_data', ''))
        # path to sensor figures
        self.figure_path = '\\'.join((self.lib_path, 'Data and Figures',
                                      'figures', self.sensor_name, ''))
        # path to processed sensor data
        self.processed_path = '\\'.join((self.lib_path, 'Data and Figures',
                                         'sensor_data', self.sensor_name,
                                         'processed_data', ''))
        # path to evaluation statistics
        self.stats_path = '\\'.join((self.lib_path, 'Data and Figures',
                                     'eval_stats', self.sensor_name, ''))

        # Import sensor data
        df_tuple = se.Import(sensor_name=self.sensor_name,
                             sensor_serials=self.serials,
                             tzone_shift=self.tzone_shift,
                             load_raw_data=self.load_raw_data,
                             data_path=self.data_path,
                             processed_path=self.processed_path,
                             write_to_file=self.write_to_file)

        # Unpack the dataframe tuple
        self.full_df_list, self.hourly_df_list, self.daily_df_list = df_tuple

        # Check whether sensor type dataframes contained passed eval param
        self.sensor_params = []
        for df in self.full_df_list:
            cols = list(df.columns)
            self.sensor_params.extend(cols)
        self.sensor_params = set(self.sensor_params)

        # Exit if passed evaluation parameter not in sensor dataframes
        if self.eval_param not in self.sensor_params:
            sys.exit(self.eval_param + ' not measured by '
                     + self.sensor_name)

        # Compute sensor deployment period and concurrent deployment groups
        self.deploy_period_df = se.Deployment_Period(self.full_df_list,
                                                     self.sensor_name,
                                                     self.serials)

        self.deploy_dict = se.Deployment_Groups(self.deploy_period_df,
                                                self.full_df_list,
                                                self.hourly_df_list,
                                                self.daily_df_list,
                                                self.sensor_name)

        self.eval_param_class = ','.join([key for key in self.param_dict.keys()
                                          if self.eval_param in
                                          self.param_dict[key]])

        deploy_grps = self.deploy_dict['Deployment Groups']

        self.deploy_bdate = min([pd.to_datetime(deploy_grps[grp]['eval_start'])
                                 for grp in deploy_grps.keys()])
        self.deploy_edate = max([pd.to_datetime(deploy_grps[grp]['eval_end'])
                                 for grp in deploy_grps.keys()])

        # Averaging intervals for parameters (some parameters like ozone have
        # diurnal trends, making 24-hour averages less useful)
        # This attribute is useful for the performance_report subclass
        self.param_averaging_dict = {'PM25': ['1-hour', '24-hour'],
                                     'O3': ['1-hour']
                                     }
        try:
            self.eval_param_averaging = self.param_averaging_dict[
                                                            self.eval_param]
        except KeyError as e:
            # if the eval param is not in the param averaging dict, assume
            # both 1-hour and 24-hour averages are of interest
            print(e, 'not specified in parameter averaging dictionary')
            print('Falling back with 1-hour and 24-hour averages')
            self.eval_param_averaging = ['1-hour', '24-hour']

        # Retrieve reference data
        if reference_data is not None:
            self.ref_dict = {'PM': pd.DataFrame(),
                             'Gases': pd.DataFrame(),
                             'Met': pd.DataFrame()}
            if reference_data == 'AirNow':
                # Call AirNow API
                if self.bbox is None:
                    console_out = (
                                   'Bounding Box required for AirNow '
                                   'API query')
                    sys.exit(console_out)

                airnow_df = se.Save_Query(se.Ref_API_Query(
                                            query_type=reference_data,
                                            param=self.eval_param,
                                            bdate=self.deploy_bdate,
                                            edate=self.deploy_edate,
                                            airnow_bbox=self.bbox,
                                            key=self.airnow_key))

                self.ref_dict[self.eval_param_class] = airnow_df

            elif reference_data == 'AQS':
                # Call AQS API
                if self.aqs_id is None:
                    sys.exit(
                                   'AQS Site ID required for AQS API query')
                aqs_df = se.Save_Query(se.Ref_API_Query(
                                             query_type=reference_data,
                                             param=self.eval_param,
                                             bdate=self.deploy_bdate,
                                             edate=self.deploy_edate,
                                             aqs_id=self.aqs_id,
                                             username=self.aqs_username,
                                             key=self.aqs_key))

                self.ref_dict[self.eval_param_class] = aqs_df

            elif os.path.exists(reference_data):
                if reference_data.endswith('airnowtech/processed'):
                    # Load AirNowTech data
                    self.ref_dict = se.Load_Ref_DataFrames(
                                            self.hourly_df_list,
                                            reference_data,
                                            self.sensor_params)

                else:
                    pass
                    # Place custom written import module for ref data here

            else:
                sys.exit(reference_data
                         + ' is not a valid API name or reference'
                         ' data file path')
        else:
            sys.exit('Please specify an API or reference '
                     'data file path via the "reference_data" variable')
            # Do not load or download any reference data

        # Set reference dataframe based on evaluation parameter classification
        self.hourly_ref_df = self.ref_dict[self.eval_param_class]
        hourly_ref_idx = self.hourly_ref_df.index

        ref_param_cols = ['_Value', '_Unit', '_QAQC_Code', '_Param_Code',
                          '_Method', '_Method_Code', '_Method_POC']

        site_cols = ['Agency', 'Site_Name', 'Site_AQS',
                     'Site_Lat', 'Site_Lon', 'Data_Source',
                     'Data_Acquisition_Date_Time']

        # Unpack the ref data into dataframes. If no reference data found,
        # return a dataframe backfilled with nulls.
        if not self.ref_dict['PM'].empty:
            self.pm_hourly_ref_df = self.ref_dict['PM']
        else:
            cols = ['PM25' + col for col in ref_param_cols]
            cols = cols + site_cols
            self.pm_hourly_ref_df = pd.DataFrame(np.nan,
                                                 index=hourly_ref_idx,
                                                 columns=cols,
                                                 dtype=object)

        if not self.ref_dict['Gases'].empty:
            self.gas_hourly_ref_df = self.ref_dict['Gases']
        else:
            cols = ['O3' + col for col in ref_param_cols]
            cols = cols + site_cols
            self.gas_hourly_ref_df = pd.DataFrame(np.nan,
                                                  index=hourly_ref_idx,
                                                  columns=cols,
                                                  dtype=object)

        if not self.ref_dict['Met'].empty:
            self.met_hourly_ref_df = self.ref_dict['Met']
        else:
            cols = [met_param + col for col in ref_param_cols
                    for met_param in ['RH', 'Temp']]

            cols = cols + site_cols
            self.met_hourly_ref_df = pd.DataFrame(np.nan,
                                                  index=hourly_ref_idx,
                                                  columns=cols,
                                                  dtype=object)
        # Get the name of the reference monitor
        try:
            self.ref_name = self.hourly_ref_df[self.eval_param + '_Method'
                                               ].dropna().unique()[0]
        except IndexError:
            self.ref_name = 'Unknown Reference'

        # Compute 24-hr averaged data
        self.daily_ref_df = se.Interval_Averaging(self.hourly_ref_df,
                                                  freq='D',
                                                  interval_count=24,
                                                  thres=0.75)

        self.met_daily_ref_df = se.Interval_Averaging(self.met_hourly_ref_df,
                                                      freq='D',
                                                      interval_count=24,
                                                      thres=0.75)

        # Compute normalized param values
        self.hourly_df_list = se.Normalize(self.hourly_df_list,
                                           self.hourly_ref_df,
                                           param=self.eval_param,
                                           ref_name=self.ref_name)

        self.daily_df_list = se.Normalize(self.daily_df_list,
                                          self.hourly_ref_df,
                                          param=self.eval_param,
                                          ref_name=self.ref_name)

        # Compute inter-sensor averaged parameter dataframes
        self.avg_hrly_df = se.Intersensor_Mean(self.hourly_df_list,
                                               self.deploy_dict)

        self.avg_daily_df = se.Intersensor_Mean(self.daily_df_list,
                                                self.deploy_dict)

    def add_deploy_dict_stats(self):
        """
        Populate deployment dictionary with precision and error performance
        targets metrics. Also include details about reference (for selected
        evaluation parameter) and monitor statistics for meteorological
        parameters (Temp, RH).
        """
        # Compute inter-sensor precision and error metric values
        # CV: 1-hour averaged sensor param
        self.deploy_dict = se.Compute_CV(self.hourly_df_list,
                                         self.deploy_dict,
                                         param=self.eval_param)

        # CV: 24-hour averaged sensor param
        self.deploy_dict = se.Compute_CV(self.daily_df_list,
                                         self.deploy_dict,
                                         param=self.eval_param)

        # RMSE: 1-hour averaged sensor param
        self.deploy_dict = se.Compute_RMSE(self.hourly_df_list,
                                           self.hourly_ref_df,
                                           self.deploy_dict,
                                           param=self.eval_param)

        # RMSE: 24-hour averaged sensor param
        self.deploy_dict = se.Compute_RMSE(self.daily_df_list,
                                           self.daily_ref_df,
                                           self.deploy_dict,
                                           param=self.eval_param)

        # Reference details for param evaluation (hourly data)
        self.deploy_dict = se.Reference_Stats(self.deploy_dict,
                                              self.hourly_ref_df,
                                              param=self.eval_param,
                                              ref_name=self.ref_name)

        # Reference details for param evaluation (daily data)
        self.deploy_dict = se.Reference_Stats(self.deploy_dict,
                                              self.daily_ref_df,
                                              param=self.eval_param,
                                              ref_name=self.ref_name)

        # Reference details for meteorological data (1-hr averages)
        self.deploy_dict = se.Meteorological_Stats(self.deploy_dict,
                                                   self.hourly_df_list,
                                                   self.met_hourly_ref_df)

        # Reference details for meteorological data (24-hr averages)
        self.deploy_dict = se.Meteorological_Stats(self.deploy_dict,
                                                   self.daily_df_list,
                                                   self.met_daily_ref_df)

        if self.write_to_file is True:

            today = se.Get_Date()

            # check if sensor-specific subfolder exists
            if not os.path.exists(self.stats_path):
                os.makedirs(self.stats_path)

            with open(self.stats_path + self.sensor_name + '_' +
                      self.eval_param + "_Evaluation_" + today +
                      ".json", "w") as outfile:
                deploy_json = json.dumps(self.deploy_dict, indent=4)
                outfile.write(deploy_json)

    def calculate_metrics(self):
        """
        Compute hourly, daily, and inter-sensor averaged statistics dataframes
        """
        try:
            self.deploy_dict['Deployment Groups']['Group 1'][self.eval_param]
        except KeyError:
            print('Populating deployment dataframe with evaluation statistics')
            self.add_deploy_dict_stats()

        # Sensor param vs. reference monitor (hourly, daily averages)
        self.stats_df = se.Regression_Stats(
                                       hourly_df_obj=self.hourly_df_list,
                                       daily_df_obj=self.daily_df_list,
                                       hourly_ref_df=self.hourly_ref_df,
                                       daily_ref_df=self.daily_ref_df,
                                       deploy_dict=self.deploy_dict,
                                       param=self.eval_param,
                                       ref_name=self.ref_name,
                                       serials=self.serials,
                                       path=self.stats_path,
                                       write_to_file=self.write_to_file)

        # Sensor param vs. inter-sensor average (hourly, daily averages)
        self.avg_stats_df = se.Regression_Stats(
                                       hourly_df_obj=self.hourly_df_list,
                                       daily_df_obj=self.daily_df_list,
                                       hourly_ref_df=self.avg_hrly_df,
                                       daily_ref_df=self.avg_daily_df,
                                       deploy_dict=self.deploy_dict,
                                       param=self.eval_param,
                                       serials=self.serials,
                                       path=self.stats_path,
                                       write_to_file=self.write_to_file)

    def plot_timeseries(self, **kwargs):
        """
        Plot parameter concentrations over time alongside reference

        """
        timestamp_fmt = '%Y-%m-%d %H:%M:%S'
        t_start = (self.avg_hrly_df.dropna(how='all',
                                        axis=0).index[0] - pd.Timedelta('1D')
                   ).strftime(timestamp_fmt)
        t_end = (self.avg_hrly_df.dropna(how='all',
                                        axis=0).index[-1] + pd.Timedelta('1D')
                 ).strftime(timestamp_fmt)

        if len(self.serials) <= 3:
            cmap_name = 'Set1'
            cmap_norm_range = (0, 0.4)

        avg_list = self.eval_param_averaging
        report_fmt = kwargs.get('report_fmt', False)

        if len(avg_list) == 2 and report_fmt is True:
            fig, axs = plt.subplots(2, 1, figsize=(10.15, 4.1))
            fig.subplots_adjust(hspace=0.7)
            for i, avg_interval in enumerate(avg_list):

                if avg_interval == '1-hour':
                    sensor_data = self.hourly_df_list
                    ref_data = self.hourly_ref_df
                if avg_interval == '24-hour':
                    sensor_data = self.daily_df_list
                    ref_data = self.daily_ref_df

                # Prevent Sensor_Timeplot from writing to file on first
                # iteration of loop
                if i == 0:
                    write_to_file = False
                if i == len(avg_list) - 1:
                    write_to_file = self.write_to_file

                axs[i] = se.Sensor_Timeplot(
                            sensor_data,
                            ref_data,
                            sensor_serials=self.serials,
                            param=self.eval_param,
                            figure_path=self.figure_path,
                            sensor_name=self.sensor_name,
                            ref_name=self.ref_name,
                            start_time=t_start,
                            end_time=t_end,
                            time_interval=avg_interval,
                            cmap_name=cmap_name,
                            cmap_norm_range=cmap_norm_range,
                            date_interval=kwargs.get('date_interval', 5),
                            title=True,
                            yscale=kwargs.get('yscale', 'linear'),
                            ylim=kwargs.get('ylims', (0, 30)),
                            report_fmt=report_fmt,
                            format_xaxis_weeks=kwargs.get('format_xaxis_weeks',
                                                          False),
                            write_to_file=write_to_file,
                            ax=axs[i],
                            fig=fig)
                if i == 0:
                    axs[i].get_legend().remove()
        else:

            averaging_interval = kwargs.get('averaging_interval', '1-hour')

            if '1-hour' in avg_list and averaging_interval == '1-hour':
                sensor_data = self.hourly_df_list
                ref_data = self.hourly_ref_df
            if '24-hour' in avg_list and averaging_interval == '24-hour':
                sensor_data = self.daily_df_list
                ref_data = self.daily_ref_df

            try:
                sensor_data
            except NameError as e:
                sys.exit(e)

            se.Sensor_Timeplot(
                    sensor_data,
                    ref_data,
                    sensor_serials=self.serials,
                    param=self.eval_param,
                    figure_path=self.figure_path,
                    sensor_name=self.sensor_name,
                    ref_name=self.ref_name,
                    start_time=t_start,
                    end_time=t_end,
                    time_interval=averaging_interval,
                    cmap_name=cmap_name,
                    cmap_norm_range=cmap_norm_range,
                    date_interval=kwargs.get('date_interval', 5),
                    title=True,
                    yscale=kwargs.get('yscale', 'linear'),
                    report_fmt=report_fmt,
                    format_xaxis_weeks=kwargs.get('format_xaxis_weeks', False),
                    write_to_file=self.write_to_file)

    def plot_metrics(self):
        """
        Regression dot/boxplots for U.S EPA performance metrics and targets
        developed for PM2.5 and O3 sensor evaluations.
        """
        try:
            self.deploy_dict['Deployment Groups']['Group 1'][self.eval_param]
        except KeyError:
            print('Populating deployment dataframe with evaluation statistics')
            self.add_deploy_dict_stats()

        try:
            self.stats_df
        except AttributeError:
            print('Calculating OLS regression statistics for 1-hr and 24-hr '
                  'sensor vs. reference measurements')
            self.calculate_metrics()

        se.Plot_Performance_Metrics(self.stats_df,
                                    self.deploy_dict,
                                    param=self.eval_param,
                                    path=self.figure_path,
                                    sensor_name=self.sensor_name,
                                    write_to_file=self.write_to_file)

    def plot_sensor_scatter(self, averaging_interval='24-hour',
                            text_pos='upper_left', plot_limits=(-1, 25),
                            point_size=20, tick_spacing=5, RH_colormap=True,
                            plot_title=True, plot_subset=None,
                            report_fmt=False):
        """
        """
        self.plot_title = plot_title

        try:
            self.deploy_dict['Deployment Groups']['Group 1'][self.eval_param]
        except KeyError:
            print('Populating deployment dataframe with evaluation statistics')
            self.add_deploy_dict_stats()

        try:
            self.stats_df
        except AttributeError:
            print('Calculating OLS regression statistics for 1-hr and 24-hr '
                  'sensor vs. reference measurements')
            self.calculate_metrics()

        if plot_subset is None:
            fontsize = se.Set_Fontsize(self.serials)
        else:
            subset_serials = {str(i): serial for i, serial in
                              enumerate(self.serials.values(), 1)
                              if str(i) in plot_subset}
            fontsize = se.Set_Fontsize(subset_serials)

        avg_list = self.eval_param_averaging

        if (report_fmt is True and plot_subset is not None):
            if self.eval_param == 'PM25':
                # Create a 1x2 subplot, 1-hr scatter on left and 24-hr scatter
                # on right for a single sensor unit (performance report page
                # 1 plot)
                figsize = (5.29, 3.17)
            elif self.eval_param == 'O3':
                # Create a 1x1 subplot, 1-hr scatter with vertical colorbar
                figsize = (4.3, 3.91)
            else:
                sys.exit('Reporting template formatted '
                         'figure not specified for ' + self.eval_param)

            fig, axs = plt.subplots(1, len(avg_list), figsize=figsize)

            fig.subplots_adjust(hspace=0.7)
            fontsize = 9
            for i, avg_interval in enumerate(self.eval_param_averaging):

                if avg_interval == '1-hour':
                    sensor_data = self.hourly_df_list
                    ref_data = self.hourly_ref_df
                    met_data = self.met_hourly_ref_df
                if avg_interval == '24-hour':
                    sensor_data = self.daily_df_list
                    ref_data = self.daily_ref_df
                    met_data = self.met_daily_ref_df

                # Prevent Sensor_Timeplot from writing to file on first
                # iteration of loop
                if i == 0:
                    write_to_file = False
                if i == len(self.eval_param_averaging) - 1:
                    write_to_file = self.write_to_file

                if isinstance(axs, np.ndarray):
                    ax = axs[i]
                    multiplot = True
                else:
                    ax = axs
                    multiplot = False

                ax = se.Scatter_Plotter(
                                   sensor_data,
                                   ref_data,
                                   self.stats_df,
                                   deploy_dict=self.deploy_dict,
                                   met_ref_df=met_data,
                                   sensor_serials=self.serials,
                                   param=self.eval_param,
                                   figure_path=self.figure_path,
                                   sensor_name=self.sensor_name,
                                   ref_name=self.ref_name,
                                   text_pos=text_pos,
                                   time_interval=avg_interval,
                                   xlim=plot_limits,
                                   ylim=plot_limits,
                                   font_size=fontsize,
                                   point_size=point_size,
                                   RH_colormap=RH_colormap,
                                   plot_title=plot_title,
                                   plot_subset=plot_subset,
                                   tick_spacing=tick_spacing,
                                   write_to_file=write_to_file,
                                   report_fmt=True,
                                   ax=ax,
                                   fig=fig)
                if multiplot:
                    axs[i] = ax
                else:
                    axs = ax

        # Create scatter for all sensors in an evaluation at a specified
        # averaging interval
        else:
            # Assuming avg_list contains either only 1-hour or 24-hour
            if '1-hour' in avg_list and averaging_interval == '1-hour':
                sensor_data = self.hourly_df_list
                ref_data = self.hourly_ref_df
            if '24-hour' in avg_list and averaging_interval == '24-hour':
                sensor_data = self.daily_df_list
                ref_data = self.daily_ref_df

            try:
                sensor_data
            except NameError as e:
                sys.exit(e)

            se.Scatter_Plotter(sensor_data,
                               ref_data,
                               self.stats_df,
                               deploy_dict=self.deploy_dict,
                               met_ref_df=self.met_hourly_ref_df,
                               sensor_serials=self.serials,
                               param=self.eval_param,
                               figure_path=self.figure_path,
                               sensor_name=self.sensor_name,
                               ref_name=self.ref_name,
                               text_pos=text_pos,
                               time_interval=averaging_interval,
                               xlim=plot_limits,
                               ylim=plot_limits,
                               font_size=fontsize,
                               point_size=point_size,
                               RH_colormap=RH_colormap,
                               plot_title=plot_title,
                               plot_subset=plot_subset,
                               tick_spacing=tick_spacing,
                               report_fmt=report_fmt,
                               write_to_file=self.write_to_file)

    def plot_met_dist(self):
        """
        Relative frequency distribution plots for temperature and relative
        humidity recorded by the R.M. Young 41382VC at AIRS
        """
        met_params = ['Temp_Value', 'RH_Value']

        se.Met_Distrib(self.met_hourly_ref_df[met_params],
                       figure_path=self.figure_path,
                       sensor_name=self.sensor_name,
                       write_to_file=self.write_to_file)

    def plot_met_influence(self, met_param=None, cmap_name='tab10',
                           cmap_norm_range=(0.00, 1.00), point_size=15,
                           alpha=0.50, fontsize=14, plot_legend=True,
                           xlims=None, plot_error_bars=True, ylims=None,
                           report_fmt=False, empty_plot=False,
                           custom_adjust=None):
        """
        Normalized Sensor param vs. AIRS RH
        """
        # Reference data header names for met data
        met_params = ['Temp', 'RH']

        if report_fmt is True:
            fig, axs = plt.subplots(1, 2, figsize=(8.1, 3.8))
            fig.subplots_adjust(hspace=0.7)
            fontsize = 10
            ylims = (-.3, 4)

            for i, met_param in enumerate(met_params):
                # Prevent writing to file on first iteration of loop
                if i == 0:
                    write_to_file = False
                if i == 1:
                    write_to_file = self.write_to_file

                axs[i] = se.Normalized_Met_Scatter(
                                          self.hourly_df_list,
                                          self.hourly_ref_df,
                                          self.avg_hrly_df,
                                          self.met_hourly_ref_df,
                                          self.figure_path,
                                          param=self.eval_param,
                                          sensor_serials=self.serials,
                                          sensor_name=self.sensor_name,
                                          met_param=met_param,
                                          cmap_name=cmap_name,
                                          cmap_norm_range=cmap_norm_range,
                                          point_size=point_size,
                                          alpha=alpha,
                                          xlim=xlims,
                                          ylim=ylims,
                                          fontsize=fontsize,
                                          plot_legend=plot_legend,
                                          plot_error_bars=plot_error_bars,
                                          ref_name=self.ref_name,
                                          write_to_file=write_to_file,
                                          report_fmt=report_fmt,
                                          fig=fig,
                                          ax=axs[i],
                                          empty_plot=empty_plot)
                if i == 0:
                    axs[i].get_legend().remove()
        else:
            se.Normalized_Met_Scatter(self.hourly_df_list,
                                      self.hourly_ref_df,
                                      self.avg_hrly_df,
                                      self.met_hourly_ref_df,
                                      self.figure_path,
                                      param=self.eval_param,
                                      sensor_serials=self.serials,
                                      sensor_name=self.sensor_name,
                                      met_param=met_param,
                                      cmap_name=cmap_name,
                                      cmap_norm_range=cmap_norm_range,
                                      point_size=point_size,
                                      alpha=alpha,
                                      xlim=xlims,
                                      ylim=ylims,
                                      fontsize=fontsize,
                                      plot_legend=plot_legend,
                                      plot_error_bars=plot_error_bars,
                                      ref_name=self.ref_name,
                                      write_to_file=self.write_to_file,
                                      custom_adjust=custom_adjust,
                                      empty_plot=empty_plot)

    def plot_sensor_met_scatter(self, averaging_interval, met_param,
                                text_pos='upper_left', fontsize=14,
                                mono_color='#0048AD', alpha=0.5,
                                tick_spacing=10, RH_colormap=False):
        """
        Creates one of the following scatter plots:
            Internal sensor RH vs. Reference monitor RH
            Internal sensor Temp vs. Reference monitor Temp
        """
        if averaging_interval == '1-hour':
            sensor_data = self.hourly_df_list
            ref_data = self.met_hourly_ref_df
        if averaging_interval == '24-hour':
            sensor_data = self.daily_df_list
            ref_data = self.met_daily_ref_df

        ymin = math.floor(self.avg_hrly_df['mean_Normalized_'
                                           + self.eval_param].min())
        ymax = round(self.avg_hrly_df['mean_Normalized_'
                                      + self.eval_param].max(), -1)

        xmin, xmax = ymin, ymax

        try:
            self.deploy_dict['Deployment Groups']['Group 1'][self.eval_param]
        except KeyError:
            print('Populating deployment dataframe with evaluation statistics')
            self.create_deploy_dict()

        try:
            self.stats_df
        except AttributeError:
            print('Calculating OLS regression statistics for 1-hr and 24-hr '
                  'sensor vs. reference measurements')
            self.calculate_metrics()

        fontsize = se.Set_Fontsize(self.serials)

        se.Scatter_Plotter(sensor_data,
                           ref_data,
                           self.stats_df,
                           deploy_dict=self.deploy_dict,
                           param=met_param,
                           sensor_name=self.sensor_name,
                           time_interval=averaging_interval,
                           figure_path=self.figure_path,
                           write_to_file=self.write_to_file,
                           xlim=(xmin, xmax),
                           ylim=(ymin, ymax),
                           text_pos=text_pos,
                           font_size=fontsize,
                           mono_color=mono_color,
                           alpha=alpha,
                           tick_spacing=tick_spacing,
                           RH_colormap=RH_colormap,
                           sensor_serials=self.serials)

    def print_eval_metrics(self, avg_interval='Daily'):
        try:
            self.deploy_dict
        except AttributeError:
            self.create_deploy_dict()
        try:
            self.stats_df
        except AttributeError:
            self.calculate_metrics()

        param = self.eval_param

        avg_interval = avg_interval.title()
        lcase_interval = avg_interval.lower()

        deploy_dic = self.deploy_dict
        deploy_stats = self.stats_df.where(
                           self.stats_df['Averaging Interval'] == avg_interval)

        print(88*'-')
        print('{:^88s}'.format(self.sensor_name + ' '
                               + avg_interval +
                               ' Performance Evaluation Results'))
        print('{:^88s}'.format('Reference Method: ' + self.ref_name))
        print(88*'-')
        print('{:^6s}|{:^24s}|{:^24s}|{:^24s}|{:^6s}'.format('CV', 'Slope',
              'Intercept', 'R^2', 'RMSE'))
        print(88*'-')
        cv_data = [(deploy_dic['Deployment Groups'][group]
                              [param]['Precision']['cv_'+lcase_interval])
                   for group in deploy_dic['Deployment Groups']]

        slope_avg = deploy_stats.Slope.mean()
        slope_min = deploy_stats.Slope.min()
        slope_max = deploy_stats.Slope.max()

        intercept_avg = deploy_stats.Intercept.mean()
        intercept_min = deploy_stats.Intercept.min()
        intercept__max = deploy_stats.Intercept.max()

        linearity_avg = deploy_stats['R$^2$'].mean()
        linearity_min = deploy_stats['R$^2$'].min()
        linearity_max = deploy_stats['R$^2$'].max()

        rmse_data = [(deploy_dic['Deployment Groups'][group]
                      [param]['Error']['rmse_'+lcase_interval])
                     for group in deploy_dic['Deployment Groups']]

        print(('{:^6.1f}|{:^24.2f}|'
               '{:^24.2f}|{:^24.2f}|{:^6.1f}').format(cv_data[0],
                                                      slope_avg,
                                                      intercept_avg,
                                                      linearity_avg,
                                                      rmse_data[0]))

        print(5*' ',
              ('|     ({:4.2f} to {:4.2f})     '
               '|    ({:4.2f} to {:4.2f})    '
               '|     ({:4.2f} to {:4.2f})     |').format(slope_min,
                                                          slope_max,
                                                          intercept_min,
                                                          intercept__max,
                                                          linearity_min,
                                                          linearity_max),
              5*' ')

    def print_eval_conditions(self, avg_interval='Daily'):
        try:
            self.deploy_dict
        except AttributeError:
            self.create_deploy_dict()
        try:
            self.stats_df
        except AttributeError:
            self.calculate_metrics()

        avg_interval = avg_interval.title()

        if avg_interval == 'Hourly':
            ref_df = self.hourly_ref_df
            met_ref_df = self.met_hourly_ref_df
        if avg_interval == 'Daily':
            ref_df = self.daily_ref_df
            met_ref_df = self.met_daily_ref_df

        deploy_dict = self.deploy_dict
        deploy_stats = self.stats_df.where(
                            self.stats_df['Averaging Interval'] == avg_interval
                            ).dropna(how='all', axis=0)
        n_sensors = len(self.serials)

        print(88*'-')
        print('{:^88s}'.format(self.sensor_name + ' (' + str(n_sensors) + ') '
                               + avg_interval + ' Evaluation Conditions'))

        print(88*'-')
        print('{:^14s}|{:^14s}|{:^14s}|{:^14s}|{:^14s}|{:^14s}'.format(
                'Eval period', 'Duration', 'Sensor ' + self.eval_param,
                'Ref ' + self.eval_param, 'Temp', 'RH'))
        print(88*'-')

        deploy_loc = deploy_dict['Deployment Groups']

        eval_start = [pd.to_datetime(deploy_loc[group]['eval_start']
                                     ).strftime('%m-%d-%y')
                      for group in deploy_loc]

        eval_end = [pd.to_datetime(deploy_loc[group]['eval_end']
                                   ).strftime('%m-%d-%y')
                    for group in deploy_loc]

        eval_duration = [str(pd.to_timedelta(
                            deploy_loc[group]['eval_duration']
                                             ).round('D').days) + ' days'
                         for group in deploy_dict['Deployment Groups']]

        sensor_min = format(deploy_stats.Sensor_Min.min(), '3.1f')
        sensor_max = format(deploy_stats.Sensor_Max.max(), '3.1f')
        sensor_mean = format(deploy_stats.Sensor_Mean.mean(), '3.1f')

        ref_min = format(ref_df[self.eval_param + '_Value'].min(), '3.1f')
        ref_max = format(ref_df[self.eval_param + '_Value'].max(), '3.1f')
        ref_mean = format(ref_df[self.eval_param + '_Value'].mean(), '3.1f')

        temp_min = format(met_ref_df['Temp_Value'].min(), '2.0f')
        temp_max = format(met_ref_df['Temp_Value'].max(), '2.0f')
        temp_mean = format(met_ref_df['Temp_Value'].mean(), '2.0f')

        rh_min = format(met_ref_df['RH_Value'].min(), '2.0f')
        rh_max = format(met_ref_df['RH_Value'].max(), '2.0f')
        rh_mean = format(met_ref_df['RH_Value'].mean(), '2.0f')

        print(('{:^14s}|{:^14s}|{:^14s}|{:^14s}|{:^14s}|{:^14s}'
               ).format(eval_start[0]+'-',
                        eval_duration[0],
                        sensor_mean,
                        ref_mean,
                        temp_mean,
                        rh_mean))

        print(('{:^14s}|{:^14s}|{:^14s}|{:^14s}|{:^14s}|{:^14s}'
               ).format(eval_end[0],
                        '',
                        '(' + sensor_min + ' to ' + sensor_max + ')',
                        '(' + ref_min + ' to ' + ref_max + ')',
                        '(' + temp_min + ' to ' + temp_max + ')',
                        '(' + rh_min + ' to ' + rh_max + ')'))

    def Cooks_Outlier_QC(self, invalidate=False):
        """Estimate outliers via cooks distance for 1-hr averaged dfs
        """

        for serial, sensor_df in zip(self.serials.values(),
                                     self.hourly_df_list):
            print('Flagged timestamps for', serial)
            xdata = self.hourly_ref_df[self.eval_param + '_Value']
            ydata = sensor_df[self.eval_param]
            df = pd.DataFrame({'x': xdata, 'y': ydata}).dropna()

            n_obs = df.shape[0]
            thres = (4 / n_obs)

            x = df['x']
            y = df['y']
            x = sm.add_constant(x)
            model = sm.OLS(y, x).fit()

            # Compute cooks distance for ref vs. average sensor conc.
            infl = model.get_influence()
            cooks = infl.cooks_distance
            cooks_df = pd.DataFrame({'distance': cooks[0],
                                     'p_val': cooks[1]})
            outliers = cooks_df[cooks_df.distance > thres]

            # Outlier timestamps
            outlier_times = df.index[outliers.index]

            # Thresholds for flagging data points
            abs_diff = abs(sensor_df[self.eval_param] -
                           self.hourly_ref_df[self.eval_param + '_Value'])
            abs_diff_thres = abs_diff.median() + 2*abs_diff.std()

            p_diff = 2*abs_diff / (sensor_df[self.eval_param] +
                           self.hourly_ref_df[self.eval_param + '_Value'])
            p_diff_thres = p_diff.median() + 2*p_diff.std()

            # Create a column for flagging data points
            sensor_df.loc[:, self.eval_param + '_QAQC_Code'] = np.nan
            # Ensure that outlier times exceeding cooks thres. justify flagging
            # by exceeding thresholds for abs diff and percent diff
            flag_count = 0
            for time in outlier_times:
                if (abs_diff[time] > abs_diff_thres and
                   p_diff[time] > p_diff_thres):
                    # TODO: Temporary flag assignment. Need to consult QC flag
                    # template
                    sensor_df.loc[time, self.eval_param + '_QAQC_Code'] = 1
                    if invalidate:
                        sensor_df.loc[time, self.eval_param] = np.nan
                    print('..' + str(time))
                    flag_count += 1
            if flag_count == 0:
                print('..No data points flagged')
