# -*- coding: utf-8 -*-
"""
Top-level analysis module for the ``sensortoolkit`` library. Contains the
front-facing ``SensorEvaluation`` class for conducting analysis of sensor data.

================================================================================

@Author:
    | Samuel Frederick, NSSC Contractor (ORAU)
    | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Fri Jul 31 08:39:37 2020
Last Updated:
  Wed Jul 7 15:01:00 2021
"""
import pandas as pd
import numpy as np
import math
import json
import sys
import os
import matplotlib.pyplot as plt
import sensortoolkit.calculate
import sensortoolkit.datetime_utils
import sensortoolkit.deploy
import sensortoolkit.lib_utils
import sensortoolkit.model
import sensortoolkit.param
import sensortoolkit.plotting
import sensortoolkit.qc
import sensortoolkit.reference
import sensortoolkit.ingest


class SensorEvaluation:
    """Evaluate air sensor performance for use in NSIM applications.

    A class for conducting analysis for air sensors deployed at ambient,
    outdoor, fixed monitoring sites using U.S. EPA's performance metrics and
    targets for sensors measuring PM2.5 or O3. U.S. EPA's testing protocols and
    performance metrics are intended for use with devices deployed for
    non-regulatory supplemental and informational monitoring (NSIM)
    applications.

    Args:
        sensor (AirSensor object): Description.
        param (Parameter object): Description.
        reference (ReferenceMethod object): Description.
        reference_data (str): The service or folder directory from which
            reference data are acquired.
        write_to_file (bool): If true, evaluation statistics will be written
            to the ``Data and Figures`` and ``eval_stats`` sensor subdirectory.
            Figures will also be written to the appropriate figures
            subdirectory.
        **kwargs: Keyword arguments that may be passed to the function for
            particulate use cases. Includes ``testing_org`` (a dictionary of
             organization information that is included in deploy_dict),
            ``testing_loc`` (a dictionary of testing location information also
            included in ``deploy_dict``).

    Attributes:
        figure_path (str): The full directory path to figures for a given
            sensor make and model.
        stats_path: The full directory path to evaluation statistics for a
            given sensor make and model.
        full_df_list (:obj:`list` of :obj: `pandas dataframes`): List of sensor
            data frames of length N (where N is the number of sensor units in a
            testing group). frames indexed by DateTime_UTC at recorded sampling
            frequency.
        hourly_df_list (list of pandas dataframes): List of sensor data frames
            of length N (where N is the number of sensor units in a testing
            group). frames indexed by DateTime_UTC at 1-hour averaged sampling
            frequency.
        daily_df_list (list of pandas dataframes): List of sensor data frames
            of length N (where N is the number of sensor units in a testing
            group). frames indexed by DateTime_UTC at 24-hour averaged sampling
            frequency.
        deploy_period_df (pandas dataframe): A data frame containing the start
            time (‘Begin’), end time (‘End’), and total duration of evaluation
            period for each sensor in a deployment group.
        deploy_dict (dict): A dictionary containing descriptive statistics and
            textual information about the deployment (testing agency, site,
            time period, etc.), sensors tested, and site conditions during the
            evaluation.
        deploy_bdate (pandas timestamp object): Overall start date of
            deployment. Determined by selecting the earliest recorded timestamp
            in sensor data frames.
        deploy_edate (pandas timestamp object): Overall end date of deployment.
            Determined by selecting the latest recorded timestamp in sensor
            data frames.
        eval_param_averaging (list): A subset of param_averaging_dict, the list
            of averaging intervals corresponding to the evaluation parameter.
        ref_dict (dict):
            Description.
        hourly_ref_df (pandas dataframe):
            Description.
        pm_hourly_ref_df (pandas dataframe):
            Description.
        gas_hourly_ref_df (pandas dataframe):
            Description.
        met_hourly_ref_df (pandas dataframe):
        ref_name (str): The make and model of the FRM/FEM instrument used as
            reference for the selected evaluation parameter. Both AirNowTech
            and AQS return the AQS method code, and the AQS Sampling Methods
            Reference table is used to determine the instrument name associated
            with this code. AirNow does not return method codes or instrument
            names. When the name and type of the FRM/FEM instrument are
            unknown, ref_name takes the value ‘unknown_reference’.
        daily_ref_df (pandas dataframe):
            Description.
        met_daily_ref_df (pandas dataframe):
            Description.
        avg_hrly_df (pandas dataframe): Data frame containing the inter-sensor
            average for concurrent sensor measurements at 1-hour averaging
            intervals.
        avg_daily_df (pandas dataframe): Data frame containing the inter-sensor
            average for concurrent sensor measurements at 24-hour averaging
            intervals.
        stats_df (pandas dataframe): Data frame with OLS regression (sensor vs.
            FRM/FEM) statistics, including R2, slope, intercept, RMSE, N
            (Number of sensor-FRM/FEM data point pairs), as well as the
            minimum, maximum, and the mean sensor concentration.
        avg_stats_df (pandas dataframe): Data frame with OLS regression (sensor
            vs. intersensor average) statistics, including R2, slope,
            intercept, RMSE, N (Number of concurrent sensor measurements during
            which all sensors in the testing group reported values), as well as
            the minimum, maximum, and the mean sensor concentration.

    """

    def __init__(self, sensor, param, reference, write_to_file=False,
                 **kwargs):

        self.sensor = sensor
        self.name = sensor.name
        self.reference = reference

        try:
            self.sensor.data
        except AttributeError as e:
            sys.exit(f'{e}, use the AirSensor.load_data() method to import'
                     f' data')

        self.path = sensor.project_path
        self.serials = sensor.serials

        # Private to avoid confusion between SensorEvaluation attribute and
        # paraeter attribute
        self.param = param
        self._param_name = param.name

        if self._param_name not in self.sensor.param_headers:
            raise AttributeError(f'{self._param_name} is not in the list of '
                                 f'parameters measured by {self.name}')

        self.write_to_file = write_to_file

        # Add keyword arguments (testing_loc, testing_org, etc.)
        self.__dict__.update(**kwargs)
        self.kwargs = kwargs

        # path to sensor figures
        self.figure_path = os.path.join(self.path, 'Data and Figures',
                                        'figures', self.name, '')

        # path to evaluation statistics
        self.stats_path = os.path.join(self.path, 'Data and Figures',
                                       'eval_stats', self.name, '')

        rec_int = self.sensor.recording_interval
        self.full_df_list = list(self.sensor.data[rec_int].values())
        self.hourly_df_list = list(self.sensor.data['1-hour'].values())
        self.daily_df_list = list(self.sensor.data['24-hour'].values())

        # Compute sensor deployment period and concurrent deployment groups
        self.deploy_period_df = sensortoolkit.deploy.deployment_period(
                                                        self.full_df_list,
                                                        self.name,
                                                        self.serials)

        self.deploy_dict = sensortoolkit.deploy.construct_deploy_dict(
                                                        self.deploy_period_df,
                                                        self.full_df_list,
                                                        self.hourly_df_list,
                                                        self.daily_df_list,
                                                        self.name,
                                                        **self.kwargs)

        deploy_grps = self.deploy_dict['Deployment Groups']

        deploy_bdate = min([pd.to_datetime(deploy_grps[grp]['eval_start'])
                            for grp in deploy_grps.keys()])
        self.deploy_bdate = self.kwargs.get('deploy_bdate', deploy_bdate)
        deploy_edate = max([pd.to_datetime(deploy_grps[grp]['eval_end'])
                            for grp in deploy_grps.keys()])
        self.deploy_edate = self.kwargs.get('deploy_edate', deploy_edate)

        # Averaging intervals for parameters
        self.eval_param_averaging = self.param.averaging

        # Retrieve reference data
        self.ref_dict = self.reference.data

        # Set reference dataframe based on evaluation parameter classification
        self.hourly_ref_df = self.ref_dict[self.param.classifier]['1-hour']
        hourly_ref_idx = self.hourly_ref_df.index

        ref_param_cols = ['_Value', '_Unit', '_QAQC_Code', '_Param_Code',
                          '_Method', '_Method_Code', '_Method_POC']

        site_cols = ['Agency', 'Site_Name', 'Site_AQS',
                     'Site_Lat', 'Site_Lon', 'Data_Source',
                     'Data_Acquisition_Date_Time']

        # Unpack the ref data into dataframes. If no reference data found,
        # return a dataframe backfilled with nulls.
        if not self.ref_dict['PM']['1-hour'].empty:
            self.pm_hourly_ref_df = self.ref_dict['PM']['1-hour']
            self.pm_daily_ref_df = self.ref_dict['PM']['24-hour']
        else:
            cols = ['PM25' + col for col in ref_param_cols]
            cols = cols + site_cols
            self.pm_hourly_ref_df = pd.DataFrame(np.nan,
                                                 index=hourly_ref_idx,
                                                 columns=cols,
                                                 dtype=object)
            # Replace null method names with 'Unspecified Reference'
            for col_name in [col for col in cols if col.endswith('_Method')]:
                self.pm_hourly_ref_df[col_name] = 'Unknown Reference'

            self.pm_daily_ref_df = sensortoolkit.datetime_utils.interval_averaging(
                                            self.pm_hourly_ref_df,
                                            freq='D',
                                            interval_count=24,
                                            thres=0.75)

        if not self.ref_dict['Gases']['1-hour'].empty:
            self.gas_hourly_ref_df = self.ref_dict['Gases']['1-hour']
            self.gas_daily_ref_df = self.ref_dict['Gases']['24-hour']
        else:
            cols = ['O3' + col for col in ref_param_cols]
            cols = cols + site_cols
            self.gas_hourly_ref_df = pd.DataFrame(np.nan,
                                                  index=hourly_ref_idx,
                                                  columns=cols,
                                                  dtype=object)
            # Replace null method names with 'Unspecified Reference'
            for col_name in [col for col in cols if col.endswith('_Method')]:
                self.gas_hourly_ref_df[col_name] = 'Unknown Reference'

            self.gas_daily_ref_df = sensortoolkit.datetime_utils.interval_averaging(
                                            self.gas_hourly_ref_df,
                                            freq='D',
                                            interval_count=24,
                                            thres=0.75)

        if not self.ref_dict['Met']['1-hour'].empty:
            self.met_hourly_ref_df = self.ref_dict['Met']['1-hour']
            self.met_daily_ref_df = self.ref_dict['Met']['24-hour']
        else:
            cols = [met_param + col for col in ref_param_cols
                    for met_param in ['RH', 'Temp']]

            cols = cols + site_cols
            self.met_hourly_ref_df = pd.DataFrame(np.nan,
                                                  index=hourly_ref_idx,
                                                  columns=cols,
                                                  dtype=object)
            # Replace null method names with 'Unspecified Reference'
            for col_name in [col for col in cols if col.endswith('_Method')]:
                self.met_hourly_ref_df[col_name] = 'Unknown Reference'

            self.met_daily_ref_df = sensortoolkit.datetime_utils.interval_averaging(
                                            self.met_hourly_ref_df,
                                            freq='D',
                                            interval_count=24,
                                            thres=0.75)

        # Get the name of the reference monitor
        self.ref_name = self.reference.get_method_name(self.param.name)

        self.daily_ref_df = self.ref_dict[self.param.classifier]['24-hour']

        # Compute normalized param values
        self.hourly_df_list = sensortoolkit.calculate.normalize(
                                            self.hourly_df_list,
                                            self.hourly_ref_df,
                                            param=self._param_name,
                                            ref_name=self.ref_name)

        self.daily_df_list = sensortoolkit.calculate.normalize(
                                            self.daily_df_list,
                                            self.hourly_ref_df,
                                            param=self._param_name,
                                            ref_name=self.ref_name)

        # Compute inter-sensor averaged parameter dataframes
        self.avg_hrly_df = sensortoolkit.calculate.intersensor_mean(
                                            self.hourly_df_list,
                                            self.deploy_dict)

        self.avg_daily_df = sensortoolkit.calculate.intersensor_mean(
                                            self.daily_df_list,
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
        self.deploy_dict = sensortoolkit.calculate.cv(
                                            self.hourly_df_list,
                                            self.deploy_dict,
                                            param=self._param_name)

        # CV: 24-hour averaged sensor param
        self.deploy_dict = sensortoolkit.calculate.cv(
                                            self.daily_df_list,
                                            self.deploy_dict,
                                            param=self._param_name)

        # RMSE: 1-hour averaged sensor param
        self.deploy_dict = sensortoolkit.calculate.rmse(
                                            self.hourly_df_list,
                                            self.hourly_ref_df,
                                            self.deploy_dict,
                                            param=self._param_name)

        # RMSE: 24-hour averaged sensor param
        self.deploy_dict = sensortoolkit.calculate.rmse(
                                            self.daily_df_list,
                                            self.daily_ref_df,
                                            self.deploy_dict,
                                            param=self._param_name)

        # Reference details for param evaluation (hourly data)
        self.deploy_dict = sensortoolkit.deploy.deploy_ref_stats(
                                            self.deploy_dict,
                                            self.hourly_ref_df,
                                            param=self._param_name,
                                            ref_name=self.ref_name)

        # Reference details for param evaluation (daily data)
        self.deploy_dict = sensortoolkit.deploy.deploy_ref_stats(
                                            self.deploy_dict,
                                            self.daily_ref_df,
                                            param=self._param_name,
                                            ref_name=self.ref_name)

        # Reference details for meteorological data (1-hr averages)
        self.deploy_dict = sensortoolkit.deploy.deploy_met_stats(
                                                self.deploy_dict,
                                                self.hourly_df_list,
                                                self.met_hourly_ref_df)

        # Reference details for meteorological data (24-hr averages)
        self.deploy_dict = sensortoolkit.deploy.deploy_met_stats(
                                                self.deploy_dict,
                                                self.daily_df_list,
                                                self.met_daily_ref_df)

        if self.write_to_file is True:

            today = sensortoolkit.datetime_utils.get_todays_date()

            # check if sensor-specific subfolder exists
            if not os.path.exists(self.stats_path):
                os.makedirs(self.stats_path)

            with open(self.stats_path + self.name + '_' +
                      self._param_name + "_Evaluation_" + today +
                      ".json", "w") as outfile:
                deploy_json = json.dumps(self.deploy_dict, indent=4)
                outfile.write(deploy_json)

    def calculate_metrics(self):
        """Compute hourly, daily, and inter-sensor statistics dataframes.

        Returns:
            None.

        """
        try:
            self.deploy_dict['Deployment Groups']['Group 1'][self._param_name]
        except KeyError:
            print('Populating deployment dataframe with evaluation statistics')
            self.add_deploy_dict_stats()

        hourly_stats = sensortoolkit.calculate.regression_stats(
                                        sensor_df_obj=self.hourly_df_list,
                                        ref_df_obj=self.hourly_ref_df,
                                        deploy_dict=self.deploy_dict,
                                        param=self._param_name,
                                        serials=self.serials
                                        )

        daily_stats = sensortoolkit.calculate.regression_stats(
                                        sensor_df_obj=self.daily_df_list,
                                        ref_df_obj=self.daily_ref_df,
                                        deploy_dict=self.deploy_dict,
                                        param=self._param_name,
                                        serials=self.serials
                                        )

        # Combine the statistics dataframes into one
        self.stats_df = sensortoolkit.calculate.join_stats(
                                        hourly_stats,
                                        daily_stats,
                                        stats_path=self.stats_path,
                                        write_to_file=self.write_to_file)

        avg_hourly_stats = sensortoolkit.calculate.regression_stats(
                                sensor_df_obj=self.hourly_df_list,
                                ref_df_obj=self.hourly_ref_df,
                                deploy_dict=self.deploy_dict,
                                param=self._param_name,
                                serials=self.serials
                                )

        avg_daily_stats = sensortoolkit.calculate.regression_stats(
                                        sensor_df_obj=self.daily_df_list,
                                        ref_df_obj=self.daily_ref_df,
                                        deploy_dict=self.deploy_dict,
                                        param=self._param_name,
                                        serials=self.serials
                                        )

        # Combine the statistics dataframes into one
        self.avg_stats_df = sensortoolkit.calculate.join_stats(
                                        avg_hourly_stats,
                                        avg_daily_stats,
                                        stats_path=self.stats_path,
                                        write_to_file=self.write_to_file)

    def plot_timeseries(self, report_fmt=True, **kwargs):
        """Plot parameter concentrations over time alongside reference.

        Args:
            report_fmt (TYPE, optional): DESCRIPTION. Defaults to True.
            **kwargs (TYPE): DESCRIPTION.

        Returns:
            None.

        """
        timestamp_fmt = '%Y-%m-%d %H:%M:%S'
        t_start = (self.avg_hrly_df.dropna(how='all', axis=0).index[0] -
                   pd.Timedelta('1D')).strftime(timestamp_fmt)
        t_end = (self.avg_hrly_df.dropna(how='all', axis=0).index[-1] +
                 pd.Timedelta('1D')).strftime(timestamp_fmt)

        avg_list = self.eval_param_averaging

        if len(avg_list) == 2 and report_fmt is True:
            fig, axs = plt.subplots(2, 1, figsize=(10.15, 4.1))
            fig.subplots_adjust(hspace=0.7)
            for i, averaging_interval in enumerate(avg_list):

                if averaging_interval == '1-hour':
                    sensor_data = self.hourly_df_list
                    ref_data = self.hourly_ref_df
                if averaging_interval == '24-hour':
                    sensor_data = self.daily_df_list
                    ref_data = self.daily_ref_df

                # Prevent Sensor_Timeplot from writing to file on first
                # iteration of loop
                if i == 0:
                    write_to_file = False
                if i == len(avg_list) - 1:
                    write_to_file = self.write_to_file

                axs[i] = sensortoolkit.plotting.sensor_timeplot(
                                            sensor_data,
                                            ref_data,
                                            sensor_serials=self.serials,
                                            param=self._param_name,
                                            figure_path=self.figure_path,
                                            sensor_name=self.name,
                                            ref_name=self.ref_name,
                                            bdate=t_start,
                                            edate=t_end,
                                            averaging_interval=averaging_interval,
                                            report_fmt=report_fmt,
                                            write_to_file=write_to_file,
                                            ax=axs[i],
                                            fig=fig,
                                            **kwargs)

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

            sensortoolkit.plotting.sensor_timeplot(
                    sensor_data,
                    ref_data,
                    sensor_serials=self.serials,
                    param=self._param_name,
                    figure_path=self.figure_path,
                    sensor_name=self.name,
                    ref_name=self.ref_name,
                    bdate=t_start,
                    edate=t_end,
                    averaging_interval=averaging_interval,
                    report_fmt=report_fmt,
                    write_to_file=self.write_to_file,
                    **kwargs)

    def plot_metrics(self, **kwargs):
        """Regression dot/boxplots for U.S EPA performance metrics and targets
        developed for PM2.5 and O3 sensor evaluations.


        Args:
            **kwargs (TYPE): DESCRIPTION.

        Returns:
            None.

        """
        try:
            self.deploy_dict['Deployment Groups']['Group 1'][self._param_name]
        except KeyError:
            print('Populating deployment dataframe with evaluation statistics')
            self.add_deploy_dict_stats()

        try:
            self.stats_df
        except AttributeError:
            print('Calculating OLS regression statistics for 1-hr and 24-hr '
                  'sensor vs. reference measurements')
            self.calculate_metrics()

        sensortoolkit.plotting.performance_metrics(self.stats_df,
                                    self.deploy_dict,
                                    param=self._param_name,
                                    param_averaging=self.eval_param_averaging,
                                    path=self.figure_path,
                                    sensor_name=self.name,
                                    write_to_file=self.write_to_file,
                                    **kwargs)

    def plot_sensor_scatter(self, averaging_interval='24-hour',
                            plot_subset=None, report_fmt=False, **kwargs):
        """

        Args:
            averaging_interval (TYPE, optional): DESCRIPTION. Defaults to
            '24-hour'.
            plot_subset (TYPE, optional): DESCRIPTION. Defaults to None.
            report_fmt (TYPE, optional): DESCRIPTION. Defaults to False.
            **kwargs (TYPE): DESCRIPTION.

        Returns:
            None.

        """

        try:
            self.deploy_dict['Deployment Groups']['Group 1'][self._param_name]
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
            sensor_serials = self.serials
        else:
            subset_serials = {str(i): serial for i, serial in
                              enumerate(self.serials.values(), 1)
                              if str(i) in plot_subset}
            sensor_serials = subset_serials

        avg_list = self.eval_param_averaging

        if averaging_interval not in avg_list:
            txt = ('Invalid averaging interval, choose from the following: '
                   + ', '.join(avg_list))
            sys.exit(txt)

        if (report_fmt is True and plot_subset is not None):
            if self._param_name == 'PM25':
                # Create a 1x2 subplot, 1-hr scatter on left and 24-hr scatter
                # on right for a single sensor unit (performance report page
                # 1 plot)
                figsize = (5.29, 3.17)
            elif self._param_name == 'O3':
                # Create a 1x1 subplot, 1-hr scatter with vertical colorbar
                figsize = (4.3, 3.91)
            else:
                sys.exit('Reporting template formatted '
                         'figure not specified for ' + self._param_name)

            fig, axs = plt.subplots(1, len(avg_list), figsize=figsize)
            kwargs['fontsize'] = 9
            fig.subplots_adjust(hspace=0.7)
            for i, averaging_interval in enumerate(self.eval_param_averaging):

                if averaging_interval == '1-hour':
                    sensor_data = self.hourly_df_list
                    ref_data = self.hourly_ref_df
                    met_data = self.met_hourly_ref_df
                if averaging_interval == '24-hour':
                    sensor_data = self.daily_df_list
                    ref_data = self.daily_ref_df
                    met_data = self.met_daily_ref_df

                # Prevent sub-routine from writing to file on first
                # iteration of loop, also dont draw cbar on first loop
                if i == 0:
                    write_to_file = False
                    kwargs['draw_cbar'] = False
                if i == len(self.eval_param_averaging) - 1:
                    write_to_file = self.write_to_file
                    kwargs['draw_cbar'] = True

                if isinstance(axs, np.ndarray):
                    ax = axs[i]
                    multiplot = True
                else:
                    ax = axs
                    multiplot = False

                ax = sensortoolkit.plotting.scatter_plotter(
                                        sensor_data,
                                        ref_data,
                                        self.stats_df,
                                        deploy_dict=self.deploy_dict,
                                        met_ref_df=met_data,
                                        sensor_serials=sensor_serials,
                                        param=self._param_name,
                                        figure_path=self.figure_path,
                                        sensor_name=self.name,
                                        ref_name=self.ref_name,
                                        averaging_interval=averaging_interval,
                                        plot_subset=plot_subset,
                                        write_to_file=write_to_file,
                                        report_fmt=True,
                                        ax=ax,
                                        fig=fig,
                                        **kwargs)

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

            sensortoolkit.plotting.scatter_plotter(
                               sensor_data,
                               ref_data,
                               self.stats_df,
                               deploy_dict=self.deploy_dict,
                               met_ref_df=self.met_hourly_ref_df,
                               sensor_serials=sensor_serials,
                               param=self._param_name,
                               figure_path=self.figure_path,
                               sensor_name=self.name,
                               ref_name=self.ref_name,
                               averaging_interval=averaging_interval,
                               plot_subset=plot_subset,
                               report_fmt=report_fmt,
                               write_to_file=self.write_to_file,
                               **kwargs)

    def plot_met_dist(self):
        """Relative frequency distribution plots for temperature and relative
        humidity recorded by meterological instruments at the collocation site.


        Returns:
            None.

        """
        met_params = ['Temp_Value', 'RH_Value']

        sensortoolkit.plotting.met_distrib(self.met_hourly_ref_df[met_params],
                       self.avg_hrly_df,
                       figure_path=self.figure_path,
                       sensor_name=self.name,
                       write_to_file=self.write_to_file)

    def plot_met_influence(self, met_param=None, report_fmt=True,
                           **kwargs):
        """Normalized Sensor param vs. AIRS RH


        Args:
            met_param (TYPE, optional): DESCRIPTION. Defaults to None.
            report_fmt (TYPE, optional): DESCRIPTION. Defaults to True.
            **kwargs (TYPE): DESCRIPTION.

        Returns:
            None.

        """
        # Reference data header names for met data
        met_params = ['Temp', 'RH']

        if report_fmt is True:
            fig, axs = plt.subplots(1, 2, figsize=(8.1, 3.8))
            fig.subplots_adjust(hspace=0.7)
            kwargs['fontsize'] = kwargs.get('fontsize', 10)
            kwargs['ylims'] = kwargs.get('ylims', (-.3, 4))

            for i, met_param in enumerate(met_params):
                # Prevent writing to file on first iteration of loop
                if i == 0:
                    write_to_file = False
                if i == 1:
                    write_to_file = self.write_to_file

                axs[i] = sensortoolkit.plotting.normalized_met_scatter(
                                          self.hourly_df_list,
                                          self.hourly_ref_df,
                                          self.avg_hrly_df,
                                          self.met_hourly_ref_df,
                                          self.figure_path,
                                          param=self._param_name,
                                          sensor_serials=self.serials,
                                          sensor_name=self.name,
                                          met_param=met_param,
                                          ref_name=self.ref_name,
                                          write_to_file=write_to_file,
                                          report_fmt=report_fmt,
                                          fig=fig,
                                          ax=axs[i],
                                          **kwargs)
                if i == 0:
                    axs[i].get_legend().remove()
        else:
            # Either Temp or RH must be passed to met_param if not using report
            # formatting. Report formatted plots dont require a value for
            # met_param as both Temp and RH scatter are automatically plotted.
            if met_param not in met_params:
                sys.exit('Invalid parameter name: ' + str(met_param))

            sensortoolkit.plotting.normalized_met_scatter(
                                      self.hourly_df_list,
                                      self.hourly_ref_df,
                                      self.avg_hrly_df,
                                      self.met_hourly_ref_df,
                                      self.figure_path,
                                      param=self._param_name,
                                      sensor_serials=self.serials,
                                      sensor_name=self.name,
                                      met_param=met_param,
                                      ref_name=self.ref_name,
                                      write_to_file=self.write_to_file,
                                      **kwargs)

    def plot_sensor_met_scatter(self, averaging_interval='1-hour',
                                met_param=None,
                                **kwargs):
        """
        Creates one of the following scatter plots:
            Internal sensor RH vs. Reference monitor RH
            Internal sensor Temp vs. Reference monitor Temp
        """
        # Data header names for met data
        met_params = ['Temp', 'RH']

        if met_param not in met_params:
            sys.exit('Invalid parameter name: ' + str(met_param))

        if averaging_interval not in  self.eval_param_averaging:
            txt = ('Invalid averaging interval, choose from the following: '
                   + ', '.join(self.eval_param_averaging))
            sys.exit(txt)

        if averaging_interval == '1-hour':
            sensor_data = self.hourly_df_list
            ref_data = self.met_hourly_ref_df
        if averaging_interval == '24-hour':
            sensor_data = self.daily_df_list
            ref_data = self.met_daily_ref_df
        ref_name = ref_data[met_param + '_Method'].unique()[0]

        ymin = math.floor(self.avg_hrly_df[
                                'mean_' + met_param].min())
        ymax = round(self.avg_hrly_df[
                                'mean_' + met_param].max(), -1)

        xmin, xmax = ymin, ymax

        try:
            self.deploy_dict['Deployment Groups']['Group 1'][self._param_name]
        except KeyError:
            print('Populating deployment dataframe with evaluation statistics')
            self.add_deploy_dict_stats()

        try:
            self.stats_df
        except AttributeError:
            print('Calculating OLS regression statistics for 1-hr and 24-hr '
                  'sensor vs. reference measurements')
            self.calculate_metrics()

        fontsize = sensortoolkit.Set_Fontsize(self.serials)

        # Set keyword argument values to defaults or passed values
        kwargs['fontsize'] = kwargs.get('fontsize', fontsize)
        kwargs['ylims'] = kwargs.get('ylims', (ymin, ymax))
        kwargs['xlims'] = kwargs.get('xlims', (xmin, xmax))
        kwargs['param_class'] = 'Met'
        kwargs['tick_spacing'] = kwargs.get('tick_spacing', 10)

        sensortoolkit.plotting.scatter_plotter(
                           sensor_data,
                           ref_data,
                           deploy_dict=self.deploy_dict,
                           param=met_param,
                           sensor_name=self.name,
                           ref_name=ref_name,
                           averaging_interval=averaging_interval,
                           figure_path=self.figure_path,
                           write_to_file=self.write_to_file,
                           sensor_serials=self.serials,
                           **kwargs)

    def print_eval_metrics(self, averaging_interval='24-hour'):
        """Summary of performance evaluation results using
        EPA’s recommended performance metrics (‘PM25’ and ‘O3’). The
        coefficient of variation, sensor vs. FRM/FEM OLS regression slope,
        intercept, and R2, and RMSE are displayed. Regression statistics
        are computed for each sensor, and the mean metric value is
        presented alongside the range (min to max).

        Args:
            averaging_interval (TYPE, optional): DESCRIPTION. Defaults to
            '24-hour'.

        Returns:
            None.

        """


        try:
            self.deploy_dict
        except AttributeError:
            self.create_deploy_dict()
        try:
            self.stats_df
        except AttributeError:
            self.calculate_metrics()

        param = self._param_name

        deploy_dic = self.deploy_dict
        deploy_stats = self.stats_df.where(
                           self.stats_df['Averaging Interval'] == averaging_interval)

        print(88*'-')
        print('{:^88s}'.format(self.name + ' '
                               + averaging_interval +
                               ' Performance Evaluation Results'))
        print('{:^88s}'.format('Reference Method: ' + self.ref_name))
        print(88*'-')
        print('{:^6s}|{:^24s}|{:^24s}|{:^24s}|{:^6s}'.format('CV', 'Slope',
              'Intercept', 'R^2', 'RMSE'))
        print(88*'-')
        cv_data = [(deploy_dic['Deployment Groups'][group]
                              [param]['Precision']['cv_' + averaging_interval])
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
                      [param]['Error']['rmse_' + averaging_interval])
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

    def print_eval_conditions(self, averaging_interval='24-hour'):
        """Testing conditions for the evaluation parameter
        and meteorological conditions during the testing period. Values for
        the evaluation parameter recorded by the sensor, FRM/FEM
        instrument, and temperature and relative humidity values are
        displayed by the mean of 1-hour or 24-hour averages during the
        testing period. The range (min to max) of each parameter is listed
        below the mean in parentheses.

        Args:
            averaging_interval (TYPE, optional): DESCRIPTION. Defaults to '24-hour'.

        Returns:
            None.

        """
        try:
            self.deploy_dict
        except AttributeError:
            self.create_deploy_dict()
        try:
            self.stats_df
        except AttributeError:
            self.calculate_metrics()

        if averaging_interval == '1-hour':
            ref_df = self.hourly_ref_df
            met_ref_df = self.met_hourly_ref_df
        if averaging_interval == '24-hour':
            ref_df = self.daily_ref_df
            met_ref_df = self.met_daily_ref_df

        deploy_dict = self.deploy_dict
        deploy_stats = self.stats_df.where(
                            self.stats_df['Averaging Interval'] == averaging_interval
                            ).dropna(how='all', axis=0)
        n_sensors = len(self.serials)

        print(88*'-')
        print('{:^88s}'.format(self.name + ' (' + str(n_sensors) + ') '
                               + averaging_interval + ' Evaluation Conditions'))

        print(88*'-')
        print('{:^14s}|{:^14s}|{:^14s}|{:^14s}|{:^14s}|{:^14s}'.format(
                'Eval period', 'Duration', 'Sensor ' + self._param_name,
                'Ref ' + self._param_name, 'Temp', 'RH'))
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

        ref_min = format(ref_df[self._param_name + '_Value'].min(), '3.1f')
        ref_max = format(ref_df[self._param_name + '_Value'].max(), '3.1f')
        ref_mean = format(ref_df[self._param_name + '_Value'].mean(), '3.1f')

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