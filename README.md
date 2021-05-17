# Air Sensor Evaluation Library

*Samuel Frederick, NSSC Contractor (ORAU)*\
*Office: 919-541-4086 | Email: frederick.samuel@epa.gov*

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

### Contact and Resources
*Please direct all inquiries to*\
&nbsp;&nbsp;&nbsp;&nbsp;Andrea Clements Ph.D., Research Physical Scientist\
&nbsp;&nbsp;&nbsp;&nbsp;U.S. EPA, Office of Research and Development\
&nbsp;&nbsp;&nbsp;&nbsp;Center for Environmental Measurement and Modeling\
&nbsp;&nbsp;&nbsp;&nbsp;Air Methods & Characterization Division, Source and Fine Scale Branch\
&nbsp;&nbsp;&nbsp;&nbsp;109 T.W. Alexander Drive, Research Triangle Park, NC  27711\
&nbsp;&nbsp;&nbsp;&nbsp;Office: 919-541-1363 | Email: clements.andrea@epa.gov

Additional information about EPA's research involving air sensors including the reports for fine particulate matter sensors and ozone sensors, past evaluation results, and additional documentation are located at EPA's [Air Sensor Toolbox](https://www.epa.gov/air-sensor-toolbox).

## Installation
Under construction
## Using SensorEvaluation
Analysis is built around the `SensorEvaluation` class is supported by modules within the `Sensor_Evaluation` library. Below is an example evaluation for a test sensor dataset. Various attributes are passed to the class upon instantiation, including the name of the sensor `sensor_name`, the evaluation parameter `eval_param`, the location of reference data or name of API service to query `reference_data`, a dictionary containing serial identifiers for each sensor unit tested `serials`, shifting of sensor data by hourly intervals to time align sensor data timestamps with reference data `tzone_shift`, etc.

Reference data can be retrieved by either API query or import of local data files, and numerous examples are given below for selecting each reference data option.


#### Example using AirNow for retrieving reference data
```python
from Sensor_Evaluation.sensor_eval_class import SensorEvaluation

# bounding box for AIRS [set narrow margins (+/- 0.01 deg) around known coordinates]
AIRS_bbox = {"minLat": "35.88",
             "maxLat": "35.89",
             "minLong": "-78.88",
             "maxLong": "-78.87"}

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

#### Example using AQS for retrieving reference data
```python
from Sensor_Evaluation.sensor_eval_class import SensorEvaluation

# Mock evaluation using Triple Oak AQS site (nearby AIRS) reference data
# obtained from the AQS API
triple_oaks_ID = {"state": "37",
                  "county": "183",
                  "site": "0021"}

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



## Data Dictionary

#### Sensor data
| Parameter Classification | Description                                              | Label                      | Units                       |
| ------------------------ | -------------------------------------------------------- | -------------------------- | --------------------------- |
| Pollutant; PM            | Particulate matter < 1 micrometer in aerosol diameter    | PM1                        | Micrograms/cubic meter      |
| Pollutant; Criteria; PM  | Particulate matter < 2.5 micrometers in aerosol diameter | PM25                       | Micrograms/cubic meter      |
| Pollutant; Criteria; PM  | Particulate matter < 10 micrometers in aerosol diameter  | PM10                       | Micrograms/cubic meter      |
| Pollutant; Criteria; Gas | Ozone                                                    | O3                         | Parts per billion by volume |
| Pollutant; Gas           | Nitrogen Monoxide                                        | NO                         |                             |
| Pollutant; Criteria; Gas | Nitrogen Dioxide                                         | NO2                        | Parts per billion by volume |
| Pollutant; Gas           | Nitrogen Oxides                                          | NOx                        |                             |
| Pollutant; Criteria; Gas | Sulfur Dioxide                                           | SO2                        | Parts per billion by volume |
| Pollutant; Gas           | Sulfur Dioxides                                          | SOx                        |                             |
| Pollutant; Criteria; Gas | Carbon Monoxide                                          | CO                         | Parts per million by volume |
| Pollutant; Gas           | Carbon Dioxide                                           | CO2                        |                             |
| Meteorological           | Relative Humidity                                        | RH                         | Percent                     |
| Meteorological           | Temperature                                              | Temp                       | Degrees Celsius             |
| Meteorological           | Dewpoint                                                 | DP\*                       | Degrees Celsius             |
| Meteorological           | Wind Speed                                               | WS                         | Meters/second               |
| Meteorological           | Wind Direction                                           | WD                         | Radians                     |
| Meteorological           | Pressure                                                 | Press                      |                             |
| Metadata                 | Parameter QC Code                                        | \[param name\]\_QC         | N/a                         |
| Metadata; Sensor Siting  | Latitude of sensor                                       | Sensor\_Lat                | Decimal degrees             |
| Metadata; Sensor Siting  | Longitude of sensor                                      | Sensor\_Lon                | Decimal degrees             |
| Performance evaluation   | Parameter data normalized by corresponding reference     | \[param name\]\_Normalized | N/a                         |
#### Reference data
