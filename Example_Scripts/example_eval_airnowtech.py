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
  Fri May 21 15:07:04 2021
Last Updated:
  Fri May 21 15:07:04 2021
"""
import os
import pathlib
import sys
lib_path = os.path.abspath(__file__ + '../../..')
if lib_path not in sys.path:
    sys.path.append(lib_path)
import Sensor_Evaluation as se
from Sensor_Evaluation.sensor_eval_class import SensorEvaluation


#  ----------------------------------------------------------------------------
#   Construct file structure for sensor, specify ingestion formatting scheme
#  ----------------------------------------------------------------------------
# Run the next line of code to create sub-dirs for sensor data, figures, etc.
se.Create_Sensor_Directories(name='New_Sensor_Make_Model',
                             eval_params=['PM25', 'O3'])

# Run the next line of code to configure the formatting scheme for converting
# recorded sensor data to a standardized format utilized by SensorEvaluation
IngestionConfig = se.Setup()

#  ----------------------------------------------------------------------------
#   Prepare the reference datasets and instantiate the SensorEvaluation class
#  ----------------------------------------------------------------------------
# Pre-process AirNowTech files, create separate, monthly files for PM, gas, met
ref_path = os.path.abspath(lib_path + '/Data and Figures/reference_data')
ref_path = pathlib.PureWindowsPath(ref_path)
filename = 'AirNowTech_BurdensCreek_20190801_20190902_PMGasMet.csv'
airnowtech_path = (ref_path.as_posix()
                   + '/airnowtech/downloaded_datasets/' + filename)
se.Import_AirNowTech(airnowtech_path)


#  ----------------------------------------------------------------------------
#   Instantiate the SensorEvaluation class
#  ----------------------------------------------------------------------------
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
                write_to_file=False)


#  ----------------------------------------------------------------------------
#   Testing statisitics and plots for the example evaluation
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
                         tick_spacing=5,
                         text_pos='upper_left')

# Plot sensor base testing results for performance metrics and target ranges
Eval.plot_metrics()

# Plot normalized sensor concentrations (sensor/reference) vs. temp and RH
Eval.plot_met_influence(report_fmt=True,
                        plot_error_bars=False)

# Plot the distribution of temp and RH observed durng the testing period
Eval.plot_met_dist()
