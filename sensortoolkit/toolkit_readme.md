# `sensortoolkit` Documentation

*Last Updated: August 18th, 2021*

The sensortoolkit library is organized into seven primary directories: `_analysis`, `_format`, `_ingest`, `_models`, `_plotting`, `_qc`, and `_reference`. Each directory contains modules and methods that support both the `SensorEvaluation` and `PerformanceReport` classes. A listing of `sensortoolkit` library methods is provided below.

## Readme Guide
* [Analysis Modules](#analysis)
* [Formatting Modules](#format)
* [Ingestion Modules](#ingest)
* [Modeling Modules](#models)
* [Plotting Modules](#plotting)
* [Quality Control (QC) Modules](#qc)
* [Reference Data Modules](#reference)

---
## `_analysis` <a name="analysis"></a>

The `_analysis` subdirectory contains modules that support the calculation of parameter quantities and statistical metrics that are either recommended by EPA's Performance Targets Reports, or may be used to compliment performance evaluation efforts.

### `aqi_calculator.py`
| Methods |
| ------- |
 `AQI_Calculator`

### `concurr_deploy_grps.py`
| Methods |
| ------- |
`Deployment_Groups`
`Reference_Stats`
`Meteorological_Stats`
`Measure_Recording_Interval`

### `cv_calculator.py`
| Methods |
| ------- |
`CV_Calculator`
`Compute_CV`

### `deployment_period.py`
| Methods |
| ------- |
`Deployment_Period`

### `dewpoint.py`
| Methods |
| ------- |
`Dewpoint`

### `duplicate_removal.py`
| Methods |
| ------- |
`Remove_Duplicates`

### `intersensor_mean.py`
| Methods |
| ------- |
`Intersensor_Mean`

### `model_analysis.py`
| Methods |
| ------- |
`Regression_Stats`
`Compute_RMSE`

### `normalize_calculator.py`
| Methods |
| ------- |
`Normalize`

### `pm25_nowcast.py`
| Methods |
| ------- |
`PM25NowCast`

### `synoptic_idx.py`
| Methods |
| ------- |
| `AQI_Calculator` |
`Synoptic_Index`

### `time_averaging.py`
| Methods |
| ------- |
| `AQI_Calculator` |
`Sensor_Averaging`
`Interval_Averaging`

### `uptime_calculator.py`
| Methods |
| ------- |
`Uptime_Calculator`

---
## `_format` <a name="format"></a>
Description.

### `format_date.py`
| Methods |
| ------- |
`Get_Date`

### `format_names.py`
| Methods |
| ------- |
`Format_Param_Name`
`Format_Metric_Name`

### `sensor_subfolders.py`
| Methods |
| ------- |
`Create_Sensor_Directories`

---
## `_ingest` <a name="ingest"></a>

### `processed_data_loader.py`
| Methods |
| ------- |
`Processed_Data_Search`
`Set_DateTime_Index`

### `sensor_import.py`
| Methods |
| ------- |
`Import`
`Ingest_Wrapper`
`Ingest_Example_Make_Model`
`Ingest_Sensit_RAMP`
`Ingest_PurpleAir_PAII`

### `setup.py`
| Methods |
| ------- |
`Setup`

### `standardized_ingest.py`
| Methods |
| ------- |
`Ingest`

---
## `_models` <a name="models"></a>
### `apply_correction.py`
| Methods |
| ------- |
`Individual_Correction`

### `purpleair_uscorrection.py`
| Methods |
| ------- |
`USCorrection`

### `sensor_ols.py`
| Methods |
| ------- |
`Sensor_OLS`

---
## `_plotting` <a name="plotting"></a>
### `distribution.py`
| Methods |
| ------- |
`Ref_Dist_Plot`
`Met_Distrib`
`Recording_Interval_Histogram`

### `errorbars.py`
| Methods |
| ------- |
`Plot_Error_Bars`

### `intrasensor_comparison.py`
| Methods |
| ------- |
`Stats_Comparison_Plot`

### `plot_formatting.py`
| Methods |
| ------- |
`Set_Fontsize`
`Wrap_Text`
`Met_Distrib`
`Get_Max`
`Sensor_Subplot_Formatting`
`Met_Scatter_Lims`

### `plot_performance_metrics.py`
| Methods |
| ------- |
`Plot_Performance_Metrics`

### `scatter.py`
| Methods |
| ------- |
`Draw_Scatter`
`Scatter_Plotter`
`Normalized_Met_Scatter`

### `timeseries.py`
| Methods |
| ------- |
`Sensor_Timeplot`
`Deployment_Timeline_Plot`

---
## `_qc` <a name="qc"></a>
### `interval_downsampling.py`
| Methods |
| ------- |
`Sensor_TimeDelta`
`Plot_RecordingInterval`
`TimeDelta_Quantiles`
`DownSampling_Interval`
`Apply_DownSampling`
`Plot_TimeDelta_Quantiles`

### `invalidate.py`
| Methods |
| ------- |
`QC_Invalidate_Period`

### `outlier_detection.py`
| Methods |
| ------- |
`Cooks_Outlier_QC`

### `persistent_values.py`
| Methods |
| ------- |
`QC_Persistent_Values`

### `purpleair_abcleaning.py`
| Methods |
| ------- |
`Compute_AB_Averages`

---
## `_reference` <a name="reference"></a>

### `import_airnowtech.py`
| Methods |
| ------- |
`Ingest_AirNowTech`
`Sort_AirNowTech`
`Write_To_File`
`Import_AirNowTech`
`Flatten`

### `load_ref_data.py`
| Methods |
| ------- |
`Load_Ref_DataFrames`
`Import_Ref_DataFrame`
`Timeframe_Search`

### `ref_api_query.py`
| Methods |
| ------- |
`Ref_API_Query`
`Modify_Ref_Cols`
`Modify_Ref_Method_Str`
`Date_Range_Selector`
`Query_Periods`
`AQS_Query`
`AirNow_Query`
`Save_Query`
