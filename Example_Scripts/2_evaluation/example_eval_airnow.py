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
  Fri May 21 15:12:05 2021
Last Updated:
  Fri May 21 15:12:05 2021
"""
import sensortoolkit

# full path to where you would like to place data, figures, reports, etc.
work_path = 'path/to/work-directory'

#  ----------------------------------------------------------------------------
#   Instantiate the SensorEvaluation class
#  ----------------------------------------------------------------------------
# bbox for AIRS [set narrow margins (+/- 0.01 deg) around known coordinates]
AIRS_bbox = {"minLat": "35.88",
             "maxLat": "35.89",
             "minLong": "-78.88",
             "maxLong": "-78.87"}

sensortoolkit.SensorEvaluation.airnow_key = 'Your-AirNow-Key-Here'

# Mock evaluation using AIRS reference data obtained from the AirNow API
Eval = sensortoolkit.SensorEvaluation(sensor_name='Example_Make_Model',
                                      eval_param='PM25',
                                      work_path=work_path,
                                      reference_data='AirNow',
                                      bbox=AIRS_bbox,
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
Eval.print_eval_metrics(avg_interval='1-hour')
Eval.print_eval_metrics(avg_interval='24-hour')

# Print site testing conditions (concentration range, RH/temp range)
Eval.print_eval_conditions(avg_interval='1-hour')
Eval.print_eval_conditions(avg_interval='24-hour')

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
