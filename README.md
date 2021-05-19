# Air Sensor Evaluation Library

*Samuel Frederick, NSSC Contractor (ORAU)*\
*Office: 919-541-4086 | Email: frederick.samuel@epa.gov*

![Sensors at the Air Innovation Research Site](Data%20and%20Figures/figures/_readme_/sensors_at_airs.jpg)

**Warning: This code is currently under development and is intended for internal EPA use only. Please do not distribute or share components of this repository with individuals external to EPA.**
****

## Overview
A Python library for evaluating the performance of air sensors for use in
ambient, outdoor, fixed site, non-regulatory supplemental and informational
monitoring applications.

In February 2021, EPA released [two reports](https://www.epa.gov/air-sensor-toolbox/air-sensor-performance-targets-and-testing-protocols#reports) detailing recommended performance testing protocols, metrics, and target values for the evaluation of sensors measuring either fine particulate matter (PM<sub>2.5</sub>) or ozone (O<sub>3</sub>). This library provides modules for testing air sensors measuring PM<sub>2.5</sub> and O<sub>3</sub> against FRM/FEM reference measurements collected at an ambient air monitoring site. Included modules calculation of performance metrics and comparison against target ranges recommended by EPA.

##### Below is a summary of key features contained in this library:
* Time averaging of timeseries data to 1-hour and 24-hour intervals with configurable data completeness threshold for computing averages (default 75%).
* Reference data retrieval from AirNow and AQS APIs (user API accounts and keys must be specified). Ingestion of reference data into a consistent data formatting standard. Import and ingestion of reference data from AirNowTech including multiple parameters and pollutant types. Reference data are sorted by parameter type (particulate matter, gaseous pollutants, and meteorological parameters) and files are saved in monthly increments to .csv files.
* *Under construction*

Users must provide an ingestion module for importing recorded sensor data into a data formatting standard developed for this project.

#### Built with:
* Python 3.7.4
* pandas 0.25.1
* numpy 1.16.5
* matplotlib 3.1.1
* seaborn 0.9.0
* statsmodels 0.10.1
* pathlib2 2.3.5
* requests 2.25.1
* ~~python-pptx 0.6.18~~ *not in current build*

### Contact and Resources
*Please direct all inquiries to*\
&nbsp;&nbsp;&nbsp;&nbsp;Andrea Clements Ph.D., Research Physical Scientist\
&nbsp;&nbsp;&nbsp;&nbsp;U.S. EPA, Office of Research and Development\
&nbsp;&nbsp;&nbsp;&nbsp;Center for Environmental Measurement and Modeling\
&nbsp;&nbsp;&nbsp;&nbsp;Air Methods & Characterization Division, Source and Fine Scale Branch\
&nbsp;&nbsp;&nbsp;&nbsp;109 T.W. Alexander Drive, Research Triangle Park, NC  27711\
&nbsp;&nbsp;&nbsp;&nbsp;Office: 919-541-1363 | Email: clements.andrea@epa.gov

Additional information about EPA's research involving air sensors including the reports for fine particulate matter sensors and ozone sensors, past evaluation results, and additional documentation are located at EPA's [Air Sensor Toolbox](https://www.epa.gov/air-sensor-toolbox).

****
## Installation
Under construction

****
## Using SensorEvaluation
The SensorEvaluation library comes with an example sensor dataset. The example sensor is given the name `Example_Make_Model` and users are encouraged to adopt a similar naming scheme for conducting analysis with the sensor name comprised of the manufacturer make and sensor model separated by an underscore '_'. The example sensor dataset is provided to help users familiarize themselves with the structure of the library's supporting files and the functionality of modules within the library.

Data, figures, and statistical results for sensors must be located in the `Data and Figures` folder. Below is a diagram showing the file structure for the Sensor Evaluation library with the `Data and Figures` folder on the first branch. Within this folder, subfolders contain evaluation statistics, figures, reference data, and sensor data (including both recorded or 'raw' and processed datasets). The `eval_stats`, `figures`, and `sensor_data` subfolders are further organized by sensor name. **Currently, the user must create these sensor-specific subfolders, otherwise the Sensor Evaluation library will not be able to read or write data and figures to the expected folder location. It is important that users follow this folder structure shown for the `Example_Make_Model` sensor below to avoid issues when using this library.**

#### Library file structure
```
├───Data and Figures
│   ├───eval_stats
│   │   └───Example_Make_Model
│   ├───figures
│   │   ├───Example_Make_Model
│   │   │   ├───deployment
│   │   │   ├───O3
│   │   │   └───PM25
│   │   └───_readme_
│   ├───reference_data
│   │   ├───airnow
│   │   │   ├───processed
│   │   │   └───raw_api_datasets
│   │   ├───airnowtech
│   │   │   ├───downloaded_datasets
│   │   │   └───processed
│   │   ├───aqs
│   │   │   ├───processed
│   │   │   └───raw_api_datasets
│   │   └───method_codes
│   └───sensor_data
│       ├───processed_data
│       │   └───Example_Make_Model
│       └───raw_data
│           └───Example_Make_Model
├───Documentation
├───Reports
│   └───templates
│       ├───O_3
│       └───PM_25
└───Sensor_Evaluation
    ├───_analysis
    ├───_format
    ├───_ingest
    ├───_models
    ├───_plotting
    └───_reference
```

Analysis is built around the `SensorEvaluation` class. To begin analysis, users create an instance of the class where various attributes are declared upon instantiation (e.g., the name of the sensor `sensor_name`, the evaluation parameter `eval_param`, the location of reference data or name of API service to query `reference_data`, a dictionary containing serial identifiers for each sensor unit tested `serials`, shifting of sensor data by hourly intervals to time align sensor data timestamps with reference data `tzone_shift`, etc.).

Upon creation of a class instance, the user must indicate what reference data to use. Users can either specify that reference data should be retrieved by API query (AirNow or AQS) or imported from a local destination (e.g., .csv files downloaded from AirNowTech). Note that both the AirNow and AQS APIs require users have an account to and key verify queries. AirNowTech also requires a user account to access its online data portal. Accounts for these services are free and can created via the following links ([AirNowTech account request](https://www.airnowtech.org/requestAccnt.cfm), [AirNow API account request](https://docs.airnowapi.org/account/request/), [AQS API sign up](https://aqs.epa.gov/aqsweb/documents/data_api.html#signup)).

Below, numerous examples are given for creating a class instance `eval`. If the user specifies that either the AirNow or AQS API should be queried for retrieving reference data, the user must specify API dependent parameters. More detail about each scenario is provided for the following examples.


#### Example using AirNow for retrieving reference data
In order to specify the location of reference data to query, AirNow requires that users pass a bounding box indicating a range of latitude and longitude to the API.

Users are encouraged to configure a bounding box with narrow margins as shown below. This reduces the likelihood that data from multiple nearby air monitoring sites will be returned by the API.

In addition, users must specify an AirNow account key to query the API. More information about obtaining an AirNow account can be found [here](https://docs.airnowapi.org/account/request/).
```python
from Sensor_Evaluation.sensor_eval_class import SensorEvaluation

# bounding box for AIRS [set narrow margins (+/- 0.01 deg) around known coordinates]
AIRS_bbox = {"minLat": "35.88",
             "maxLat": "35.89",
             "minLong": "-78.88",
             "maxLong": "-78.87"}

# AirNow credentials
SensorEvaluation.airnow_key = 'Your-AirNow-Key-Here'

# Mock evaluation using AIRS reference data obtained from the AirNow API
eval = SensorEvaluation(sensor_name='Example_Make_Model',
                        eval_param='PM25',
                        reference_data='AirNow',
                        bbox=AIRS_bbox,
                        serials={'1': 'SN01',
                                 '2': 'SN02',
                                 '3': 'SN03'},
                        tzone_shift=5,
                        load_raw_data=False,
                        write_to_file=False)
```
When creating an evaluation class instance with the code snippet above, the following will be printed to the console:
```
Loading processed sensor data
..Example_Make_Model_SN01_daily.csv
..Example_Make_Model_SN01_full.csv
..Example_Make_Model_SN01_hourly.csv
..Example_Make_Model_SN02_daily.csv
..Example_Make_Model_SN02_full.csv
..Example_Make_Model_SN02_hourly.csv
..Example_Make_Model_SN03_daily.csv
..Example_Make_Model_SN03_full.csv
..Example_Make_Model_SN03_hourly.csv
Querying AirNow API
..Query start: 2019-08-01
..Query end: 2019-08-31
..Query site(s):
....Site name: Burdens Creek
......AQS ID: 37-063-0099
......Latitude: 35.8894
......Longitude: -78.8747
..Query Status: Success
Querying AirNow API
..Query start: 2019-09-01
..Query end: 2019-09-30
..Query site(s):
....Site name: Burdens Creek
......AQS ID: 37-063-0099
......Latitude: 35.8894
......Longitude: -78.8747
..Query Status: Success
Writing AirNow query dataframes to csv files
../reference_data/airnow/processed/AirNow_37-063-0099_PM25_B190801_E190902.csv
../reference_data/airnow/raw_api_datasets/AirNow_raw_37-063-0099_PM25_B190801_E190902.csv
Computing normalized PM25 values (by Unknown Reference)
Computing normalized PM25 values (by Unknown Reference)
Computing mean parameter values across concurrent sensor datasets
Computing mean parameter values across concurrent sensor datasets
```
Below is a step-by-step description of the console output:
* Processed sensor data are loaded
* The AirNow API is queried in monthly intervals for `PM25` reference data recorded at monitoring sites within the specified bounding box. AirNow returns a successful query, and the console indicates data were retrieved from the Burdens Creek monitoring site. AirNow data are then parsed into the reference data format described in the reference data dictionary below. Both raw (datasets as returned by the API) and processed datasets are written to .csv files at the folder path indicated.
* Sensor `PM25` concentrations are normalized against reference measurements (AirNow does not indicate the name of the reference instrument for the evaluation parameter, so the reference is referred to as `Unknown Reference`).
* The mean across sensor measurements is also calculated.

#### Example using AQS for retrieving reference data
In order to specify the location of reference data to query, AQS requires that users provide the AQS site ID for the monitoring site of interest. The AQS site ID is composed of three components: state and county FIPS codes, and a site specific identifier.

To explore nearby sites, users may use EPA's [AirData Map](https://epa.maps.arcgis.com/apps/webappviewer/index.html?id=5f239fd3e72f424f98ef3d5def547eb5&extent=-146.2334,13.1913,-46.3896,56.5319), which allows users to view active (and inactive) monitors for crtieria pollutants at monitoring sites across the U.S. Clicking on map icons for monitors brings up a brief description of the site (including the site AQS ID), as well as details about the monitor and historical data.

In addition, users must specify an AQS account username (registered email) and a key to query the API. More information about obtaining an AQS account can be found [here](https://aqs.epa.gov/aqsweb/documents/data_api.html#signup).
```python
from Sensor_Evaluation.sensor_eval_class import SensorEvaluation

# Mock evaluation using Triple Oak AQS site (nearby AIRS) reference data
# obtained from the AQS API
triple_oaks_ID = {"state": "37",
                  "county": "183",
                  "site": "0021"}

# AQS credentials
SensorEvaluation.aqs_username = 'username_address@email.com'
SensorEvaluation.aqs_key = 'Your-AQS-Key-Here'

# Mock evaluation using Triple Oaks reference data obtained from the AQS API
eval = SensorEvaluation(sensor_name='Example_Make_Model',
                        eval_param='PM25',
                        reference_data='AQS',
                        aqs_id=triple_oaks_ID,
                        serials={'1': 'SN01',
                                 '2': 'SN02',
                                 '3': 'SN03'},
                        tzone_shift=5,
                        load_raw_data=False,
                        write_to_file=False)
```

#### Example using downloaded AirNowTech datasets
If users have an existing account with AirNowTech, datasets downloaded directly from the AirNowTech data portal can be imported via the `Import_AirNowTech()` module.

[Specifics about data downloaded from AirNowTech]
```python
from Sensor_Evaluation.sensor_eval_class import SensorEvaluation

ref_path = 'path/to/project/.../Sensor Evaluation/Data and Figures/reference_data'

# Pre-process downloaded AirNowTech file, create separate, monthly files for PM, gas, and met
airnowtech_path = (ref_path + '/airnowtech/downloaded_datasets/' +
                   'AirNowTech_BurdensCreek_20190801_20190902_PMGasMet.csv')
se.Import_AirNowTech(airnowtech_path)

# Mock evaluation using AIRS reference data downloaded from AirNowTech
eval = SensorEvaluation(
                sensor_name='Example_Make_Model',
                eval_param='PM25',
                reference_data=ref_path.as_posix() + '/airnowtech/processed',
                serials={'1': 'SN01',
                         '2': 'SN02',
                         '3': 'SN03'},
                tzone_shift=5,
                load_raw_data=False,
                write_to_file=True)
```

When creating an evaluation class instance with the code snippet above, the following will be printed to the console:
```
Loading processed sensor data
..Example_Make_Model_SN01_daily.csv
..Example_Make_Model_SN01_full.csv
..Example_Make_Model_SN01_hourly.csv
..Example_Make_Model_SN02_daily.csv
..Example_Make_Model_SN02_full.csv
..Example_Make_Model_SN02_hourly.csv
..Example_Make_Model_SN03_daily.csv
..Example_Make_Model_SN03_full.csv
..Example_Make_Model_SN03_hourly.csv
Loading reference dataframes
..2019-08
....H_201908_PM.csv
....H_201908_Met.csv
....H_201908_Gases.csv
..2019-09
....H_201909_PM.csv
....H_201909_Met.csv
....H_201909_Gases.csv
Computing normalized PM25 values (by T-API T640X at 16.67 LPM)
Computing normalized PM25 values (by T-API T640X at 16.67 LPM)
Computing mean parameter values across concurrent sensor datasets
Computing mean parameter values across concurrent sensor datasets
```
Below is a step-by-step description of the console output:
* Processed sensor data are loaded
* AirNowTech reference data for the sensor testing timeframe are loaded in monthly intervals for parameter types present in the recorded sensor data (`PM` for parameters headers labeled `PM1`, `PM25`, and `PM10`; `Gases` for parameters headers labeled `O3`, `NO2`, `NO`, `NOx`, `SO2`, `SOx`, `CO`, and `CO2`; `Met` for parameters headers labeled `Temp`, `RH`, `Press`, `DP`, `WS`, and `WD`). The test dataset includes `PM25`, `PM10`, `NO2`, `O3`, `Temp`, and `RH`, so reference data sets for `PM`, `Gases`, and `Met`.
* Sensor `PM25` concentrations are normalized against reference measurements.
* The mean across sensor measurements is also calculated.


****
## Data Dictionary

#### Sensor data
Below is a list of sensor parameters supported by the `SensorEvaluation` class. **Please note that currently, only `PM25` and `O3` are fully supported for all performance evaluation modules in accordance with EPA's [reports](https://www.epa.gov/air-sensor-toolbox/air-sensor-performance-targets-and-testing-protocols#reports) for these pollutants.** Limited functionality is available for all other pollutants.

| Parameter Classification | Parameter Label             | Description                                              | Units                       |
| ------------------------ | -------------------------- | -------------------------------------------------------- | --------------------------- |
| Pollutant; PM            | `PM1`                        | Particulate matter < 1 micrometer in aerosol diameter    | Micrograms/cubic meter      |
| Pollutant; Criteria; PM  | `PM25`                       | Particulate matter < 2.5 micrometers in aerosol diameter | Micrograms/cubic meter      |
| Pollutant; Criteria; PM  | `PM10`                       | Particulate matter < 10 micrometers in aerosol diameter  | Micrograms/cubic meter      |
| Pollutant; Criteria; Gas | `O3`                         | Ozone                                                    | Parts per billion by volume |
| Pollutant; Gas           | `NO`                         | Nitrogen Monoxide                                        |                             |
| Pollutant; Criteria; Gas | `NO2`                        | Nitrogen Dioxide                                         | Parts per billion by volume |
| Pollutant; Gas           | `NOx`                        | Nitrogen Oxides                                          |                             |
| Pollutant; Criteria; Gas | `SO2`                        | Sulfur Dioxide                                           | Parts per billion by volume |
| Pollutant; Gas           | `SOx`                        | Sulfur Dioxides                                          |                             |
| Pollutant; Criteria; Gas | `CO`                         | Carbon Monoxide                                          | Parts per million by volume |
| Pollutant; Gas           | `CO2`                        | Carbon Dioxide                                           |                             |
| Meteorological           | `RH`                         | Relative Humidity                                        | Percent                     |
| Meteorological           | `Temp`                       | Temperature                                              | Degrees Celsius             |
| Meteorological           | `DP`*                       | Dewpoint                                                 | Degrees Celsius             |
| Meteorological           | `WS`                         | Wind Speed                                               | Meters/second               |
| Meteorological           | `WD`                         | Wind Direction                                           | Radians                     |
| Meteorological           | `Press`                      | Pressure                                                 |                             |
| Metadata                 | `[param name]_QC`         | Parameter QC Code                                        | N/a                         |
| Metadata; Sensor Siting  | `Sensor_Lat`                | Latitude of sensor                                       | Decimal degrees             |
| Metadata; Sensor Siting  | `Sensor_Lon`                | Longitude of sensor                                      | Decimal degrees             |
| Performance evaluation   | `[param name]_Normalized` | Parameter data normalized by corresponding reference     | N/a                         |


*If internal Temp and RH are measured, but not DP, DP is calculated via the `Dewpoint()` module and is labeled `DP_calculated`
#### Reference data
Below is a description of reference data formatting expected by the `SensorEvaluation` class. Example values result from `PM25` data queried from the AQS API for the Triple Oak monitoring site. The column naming scheme for parameter data is consistent across queried parameters (columns with the prefix '`PM25`' are replaced by the parameter of interest) and columns formatting is consistent across data sources. Note that the AirNow API does not return QC codes, parameter AQS codes, method names, method AQS codes, or parameter occurrence codes. These columns are set null (i.e., all values set to `np.nan`). In addition, AirNowTech does not return method names, site latitude, or site longitude, and these columns are set null if reference data from AirNowTech are selected.

| Column Header                 | Description                                          | Example                                         | Data type        |
| ----------------------------- | ---------------------------------------------------- | ----------------------------------------------- | ---------------- |
| `DateTime_UTC`                 | Timestamp, set as index                                            | `8/1/2019 13:00`                                  | `datetime64[ns]` |
| `PM25_Value`                   | Parameter value                                      | `9`                                               | `float64`          |
| `PM25_Unit`                    | Parameter units                                      | `Micrograms/cubic meter (LC)`                     | `object`           |
| `PM25_QAQC_Code`              | Parameter QC code or AQS qualifier                                   | `V - Validated Value.`                            | `float64`          |
| `PM25_Param_Code`             | Parameter AQS code                                   | `88101`                                           | `float64`          |
| `PM25_Method`                  | Parameter method (Instrument)                        | `Met One BAM-1022 PM2.5 w/ VSCC or TE-PM2.5C FEM` | `object`           |
| `PM25_Method_Code`            | Parameter method AQS code                            | `209`                                             | `float64`          |
| `PM25_Method_POC`             | Parameter Occurance Code (POC)                             | `3`                                               | `float64`          |
| `Agency`                        | Reporting agency overseeing site                     | `North Carolina Dept Of Environmental Quality`    | `object`           |
| `Site_Name`                    | Name of monitoring site                              | `Triple Oak`                                      | `object`           |
| `Site_AQS`                     | Site AQS ID (state, county, site FIPS codes separated by '-') | `37-183-0021`                                     | `object`           |
| `Site_Lat`                     | Site latitude                                        | `35.8652`                                         | `float64`          |
| `Site_Lon`                     | Site longitude                                       | `-78.8197`                                       | `float64`          |
| `Data_Source`                  | Name of API data source                              | `AQS API`                                         | `object`           |
| `Data_Acquisition_Date_Time` | Date and time of data query, acquisition             | `5/18/2021 8:44`                                  | `datetime64[ns]`           |

Note that AirNow, AirNowTech, and AQS report QC or instrument status codes in different ways. AirNow reports `-999` if instrument failures or other issues occur, AirNowTech reports integer values ranging from '0' (normal operation) to `9` (instrument failure)

## Modules
#### `SensorEvaluation.print_eval_metrics()`

```python
Eval.print_eval_metrics(avg_interval='Hourly')
```

```
----------------------------------------------------------------------------------------
                Example_Make_Model Hourly Performance Evaluation Results                
                       Reference Method: T-API T640X at 16.67 LPM                       
----------------------------------------------------------------------------------------
  CV  |         Slope          |       Intercept        |          R^2           | RMSE
----------------------------------------------------------------------------------------
 13.1 |          0.77          |         -1.56          |          0.52          | 3.7  
      |     (0.72 to 0.80)     |    (-1.59 to -1.52)    |     (0.50 to 0.53)     |      
----------------------------------------------------------------------------------------
```


```python
Eval.print_eval_metrics(avg_interval='Daily')
```

```
                Example_Make_Model Daily Performance Evaluation Results                 
                       Reference Method: T-API T640X at 16.67 LPM                       
----------------------------------------------------------------------------------------
  CV  |         Slope          |       Intercept        |          R^2           | RMSE
----------------------------------------------------------------------------------------
 7.1  |          0.87          |         -2.38          |          0.59          | 3.6  
      |     (0.84 to 0.92)     |    (-2.56 to -2.11)    |     (0.54 to 0.63)     |   
```
#### `SensorEvaluation.print_eval_conditions()`
```python
Eval.print_eval_conditions(avg_interval='Hourly')
```

```
----------------------------------------------------------------------------------------
                  Example_Make_Model (3) Hourly Evaluation Conditions                   
----------------------------------------------------------------------------------------
 Eval period  |   Duration   | Sensor PM25  |   Ref PM25   |     Temp     |      RH      
----------------------------------------------------------------------------------------
  08-01-19-   |   32 days    |     4.4      |     7.7      |      26      |      71      
   09-02-19   |              |(0.9 to 13.8) |(3.3 to 15.3) |  (14 to 38)  |  (24 to 97)  
----------------------------------------------------------------------------------------
```


```python
Eval.print_eval_conditions(avg_interval='Daily')
```

```
                   Example_Make_Model (3) Daily Evaluation Conditions                   
----------------------------------------------------------------------------------------
 Eval period  |   Duration   | Sensor PM25  |   Ref PM25   |     Temp     |      RH      
----------------------------------------------------------------------------------------
  08-01-19-   |   32 days    |     4.4      |     7.7      |      26      |      71      
   09-02-19   |              | (1.2 to 8.1) |(4.9 to 11.0) |  (21 to 29)  |  (60 to 88)  
```
#### `SensorEvaluation.plot_timeseries()`
```python
# Timeseries plots for both 1-hour and 24-hour averaged data
Eval.plot_timeseries(format_xaxis_weeks=False,
                     yscale='linear',  # set y-axis format to linear scaling
                     date_interval=5)  # place 5 days between xticks
```
![Example_Make_Model Performance Evaluation Results](Data%20and%20Figures/figures/Example_Make_Model/PM25/Example_Make_Model_timeseries_PM25_1-hour_210519.png)

#### `SensorEvaluation.plot_sensor_scatter()`
```Python
test.plot_sensor_scatter('1-hour',
                         plot_limits=(-1, 20),
                         axes_spacing=5,
                         text_pos='upper_left')
```
```
Creating subplot for 3 sensors with 1 row and 3 columns
Computing regression statistics for Example_Make_Model vs T-API T640X at 16.67 LPM
Computing regression statistics for Example_Make_Model vs T-API T640X at 16.67 LPM
Computing regression statistics for Example_Make_Model vs T-API T640X at 16.67 LPM
```
![Example_Make_Model Performance Evaluation Results](Data%20and%20Figures/figures/Example_Make_Model/PM25/Example_Make_Model_vs_T-API%20T640X%20at%2016.67%20LPM_1-hour_3_sensors_210519.png)

#### `SensorEvaluation.plot_metrics()`
![Example_Make_Model Performance Evaluation Results](Data%20and%20Figures/figures/Example_Make_Model/PM25/Example_Make_Model_regression_boxplot_PM25_210517.png)

#### `SensorEvaluation.plot_met_influence()`

#### `SensorEvaluation.plot_met_dist()`
