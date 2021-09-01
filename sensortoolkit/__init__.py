# -*- coding: utf-8 -*-
"""Top-level module for the ``sensortoolkit`` library.
"""
# Package maintenance
from ._pkg.get_version import Get_Version
__version__ = Get_Version()

# Modules that do not require functions in other sensortoolkit modules
from ._analysis.dewpoint import Dewpoint
from ._analysis.pm25_nowcast import PM25NowCast
from ._analysis.aqi_calculator import AQI_Calculator
from ._analysis.time_averaging import Sensor_Averaging, Interval_Averaging
from ._analysis.uptime_calculator import Uptime_Calculator
from ._analysis.deployment_period import Deployment_Period
from ._analysis.duplicate_removal import Remove_Duplicates
from ._analysis.normalize_calculator import Normalize
from ._format.format_date import Get_Date
from ._format.format_names import Format_Param_Name, Format_Metric_Name
from ._format.sensor_subfolders import Create_Sensor_Directories
from ._format.copy_datasets import CopySensorData
from ._ingest.processed_data_loader import Processed_Data_Search
from ._ingest.standardized_ingest import Ingest
from ._models.purpleair_uscorrection import USCorrection
from ._models.apply_correction import Individual_Correction
from ._plotting.plot_formatting import (Set_Fontsize,
     Sensor_Subplot_Formatting, Get_Max, Met_Scatter_Lims, Wrap_Text,
     Get_Colormap_Norm_Range)
from ._plotting.errorbars import Plot_Error_Bars
from ._qc.purpleair_abcleaning import Compute_AB_Averages
from ._reference.import_airnowtech import PreProcess_AirNowTech, Flatten
from ._reference.load_ref_data import Load_Ref_DataFrames

# Modules calling functions in other sensortoolkit modules
from ._reference.ref_api_query import (Ref_API_Query, Save_Query,
                                       AQS_Query, AirNow_Query)
from ._reference.import_oaqps import Ingest_OAQPS, Process_OAQPS
from ._analysis.synoptic_idx import Synoptic_Index
from ._analysis.create_deploy_dict import (Construct_Deploy_Dict,
                                           Add_Ref_Stats,
                                           Add_Met_Stats)
from ._analysis.cv_calculator import CV_Calculator, Compute_CV
from ._models.sensor_ols import Sensor_OLS
from ._analysis.model_analysis import (Regression_Stats, Join_Stats,
                                       Compute_RMSE)
from ._plotting.distribution import (Ref_Dist_Plot, Met_Distrib,
                                     Recording_Interval_Histogram)
from ._plotting.intrasensor_comparison import Stats_Comparison_Plot
from ._plotting.plot_performance_metrics import Plot_Performance_Metrics
from ._plotting.timeseries import Sensor_Timeplot, Deployment_Timeline_Plot
from ._plotting.scatter import (Draw_Scatter, Scatter_Plotter,
                                Normalized_Met_Scatter)
from ._analysis.intersensor_mean import Intersensor_Mean
from ._ingest.sensor_import import Import
from ._ingest.setup import Setup

# Import front-facing classes
from ._performancereport.performance_report import PerformanceReport
from ._evaluation.sensor_eval import SensorEvaluation
