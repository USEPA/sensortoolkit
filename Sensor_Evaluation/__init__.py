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
  Mon Jan 27 08:41:23 2020
Last Updated:
  Wed Jul 7 15:01:00 2021
"""

# Modules that do not require functions in other Sensor_Evaluation modules
from ._analysis.dewpoint import Dewpoint
from ._analysis.pm25_nowcast import PM25NowCast
from ._analysis.aqi_calculator import AQI_Calculator
from ._analysis.time_averaging import Sensor_Averaging, Interval_Averaging
from ._analysis.uptime_calculator import Uptime_Calculator
from ._analysis.deployment_period import Deployment_Period
from ._analysis.duplicate_removal import Remove_Duplicates
from ._analysis.normalize_calculator import Normalize
from ._analysis.purpleair_modules import Compute_AB_Averages, USCorrection
from ._format.format_date import Get_Date
from ._format.format_names import Format_Param_Name, Format_Metric_Name
from ._format.sensor_subfolders import Create_Sensor_Directories
from ._ingest.processed_data_loader import Processed_Data_Search
from ._ingest.setup import Setup
from ._ingest.standardized_ingest import Ingest
from ._models.apply_correction import Individual_Correction
from ._plotting.plot_formatting import (Set_Fontsize,
     Sensor_Subplot_Formatting, Get_Max, Met_Scatter_Lims, Wrap_Text)
from ._plotting.errorbars import Plot_Error_Bars
from ._reference.import_airnowtech import Import_AirNowTech, Flatten
from ._reference.load_ref_data import Load_Ref_DataFrames

# Modules calling functions in other Sensor_Evaluation modules
from ._reference.ref_api_query import (Ref_API_Query, Save_Query,
                                       AQS_Query, AirNow_Query)
from ._reference.import_oaqps import Ingest_OAQPS
from ._analysis.synoptic_idx import Synoptic_Index
from ._analysis.concurr_deploy_grps import (Deployment_Groups,
                                            Reference_Stats,
                                            Meteorological_Stats)
from ._analysis.cv_calculator import CV_Calculator, Compute_CV
from ._models.sensor_ols import Sensor_OLS
from ._analysis.model_analysis import Regression_Stats, Compute_RMSE
from ._plotting.distribution import (Ref_Dist_Plot, Met_Distrib,
                                     Recording_Interval_Histogram)
from ._plotting.intrasensor_comparison import Stats_Comparison_Plot
from ._plotting.plot_performance_metrics import Plot_Performance_Metrics
from ._plotting.timeseries import Sensor_Timeplot, Deployment_Timeline_Plot
from ._plotting.scatter import (Draw_Scatter, Scatter_Plotter,
                                Normalized_Met_Scatter)
from ._analysis.intersensor_mean import Intersensor_Mean
from ._ingest.sensor_import import Import
