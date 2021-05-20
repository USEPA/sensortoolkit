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
  Thu Dec 10 15:13:44 2020
Last Updated:
  Tue May 11 16:18:00 2021
"""
import os
import pathlib
os.chdir('..')
import Sensor_Evaluation as se
from Sensor_Evaluation.sensor_eval_class import SensorEvaluation

ref_path = os.path.abspath(__file__ + '../../reference_data')

# Caution, Windows only
ref_path = pathlib.PureWindowsPath(ref_path)

#  ----------------------------------------------------------------------------
# Uncomment the following block of code to run pre-processing on downloaded
# AirNowTech data.

# Pre-process downloaded AirNowTech file, create separate, monthly files for
# PM, gas, and met
airnowtech_path = (ref_path.as_posix() + '/airnowtech/downloaded_datasets/' +
                   'AirNowTech_BurdensCreek_20190801_20190902_PMGasMet.csv')
se.Import_AirNowTech(airnowtech_path)


# Mock evaluation using AIRS reference data downloaded from AirNowTech
Eval = SensorEvaluation(
                sensor_name='Example_Make_Model',
                eval_param='PM25',
                reference_data=ref_path.as_posix() + '/airnowtech/processed',
                serials={'1': 'SN01',
                         '2': 'SN02',
                         '3': 'SN03'},
                tzone_shift=5,
                load_raw_data=False,
                write_to_file=True)

#  ----------------------------------------------------------------------------
# bbox for AIRS [set narrow margins (+/- 0.01 deg) around known coordinates]
AIRS_bbox = {"minLat": "35.88",
             "maxLat": "35.89",
             "minLong": "-78.88",
             "maxLong": "-78.87"}

SensorEvaluation.airnow_key = 'Your-AirNow-Key-Here'

# Mock evaluation using AIRS reference data obtained from the AirNow API
Eval = SensorEvaluation(sensor_name='Example_Make_Model',
                        eval_param='PM25',
                        reference_data='AirNow',
                        bbox=AIRS_bbox,
                        serials={'1': 'SN01',
                                 '2': 'SN02',
                                 '3': 'SN03'},
                        tzone_shift=5,
                        load_raw_data=False,
                        write_to_file=False)


#  ----------------------------------------------------------------------------
# Mock evaluation using Triple Oak AQS site (nearby AIRS) reference data
# obtained from the AQS API
triple_oaks_ID = {"state": "37",
                  "county": "183",
                  "site": "0021"}

SensorEvaluation.aqs_username = 'username_address@email.com'
SensorEvaluation.aqs_key = 'Your-AQS-Key-Here'

Eval = SensorEvaluation(sensor_name='Example_Make_Model',
                        eval_param='PM25',
                        reference_data='AQS',
                        aqs_id=triple_oaks_ID,
                        serials={'1': 'SN01',
                                 '2': 'SN02',
                                 '3': 'SN03'},
                        tzone_shift=5,
                        load_raw_data=False,
                        write_to_file=False)

#  ----------------------------------------------------------------------------

# Print performance target evaluation results to console
Eval.print_eval_metrics(avg_interval='Hourly')
Eval.print_eval_metrics(avg_interval='Daily')

# Print site testing conditions (concentration range, RH/temp range)
Eval.print_eval_conditions(avg_interval='Hourly')
Eval.print_eval_conditions(avg_interval='Daily')

# Timeseries plots for both 1-hour and 24-hour averaged data
Eval.plot_timeseries(format_xaxis_weeks=False,
                     yscale='linear',  # set y-axis format to linear scaling
                     date_interval=5,  # place 5 days between xticks
                     report_fmt=True)  # Reporting template formatting presets

# Scatter plots for all sensors (sensor vs. ref), scatter are colored by RH
Eval.plot_sensor_scatter('1-hour',
                         plot_limits=(-1, 20),
                         axes_spacing=5,
                         text_pos='upper_left')

# Plot sensor base testing results for performance metrics and target ranges
Eval.plot_metrics()

# Plot normalized sensor concentrations (sensor/reference) vs. temp and RH
Eval.plot_met_influence(report_fmt=True,
                        plot_error_bars=False)

# Plot the distribution of temp and RH observed durng the testing period
Eval.plot_met_dist()
