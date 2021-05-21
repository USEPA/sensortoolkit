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
  Thu Dec 10 15:13:44 2020
"""
from Sensor_Evaluation.sensor_eval_class import SensorEvaluation


# Aeroqual AQY example evaluation functions -----------------------------------
"""
Evaluation(s): PM2.5, O3
"""
aqy_PM_25 = SensorEvaluation(sensor_name='Aeroqual_AQY',
                             eval_param='PM_25',
                             write_to_file=False)
aqy_PM_25.DeployDict()

aqy_PM_25.CalculateMetrics()

# AQY PM2.5 Performance Target Report plots
aqy_PM_25.Timeplot(format_xaxis_weeks=False, yscale='linear', date_interval=5,
                   pt_formatting=True)
aqy_PM_25.SensorParamScatter(plot_subset=['2'], pt_formatting=False,
                             plot_limits=(-1, 30), axes_spacing=5,
                             text_pos='upper_left')
aqy_PM_25.PlotMetrics()
aqy_PM_25.NormMetBias(pt_formatting=True,
                      plot_error_bars=False)
aqy_PM_25.PlotMetDist()

# Additional plots
aqy_PM_25.Timeplot('1-hour', format_xaxis_weeks=False, yscale='log',
                   date_interval=7)

aqy_PM_25.Timeplot('24-hour', format_xaxis_weeks=False, yscale='log',
                   date_interval=7)

aqy_PM_25.SensorParamScatter('1-hour', plot_limits=(-1, 20),
                             axes_spacing=5, text_pos='upper_left')
aqy_PM_25.SensorParamScatter('24-hour', plot_limits=(-1, 20),
                             axes_spacing=5, text_pos='upper_left')
aqy_PM_25.SensorParamScatter('1-hour', plot_subset=['2'],
                             plot_limits=(-1, 30),
                             axes_spacing=5, text_pos='upper_left')
aqy_PM_25.SensorParamScatter('24-hour', plot_subset=['2'],
                             plot_limits=(-1, 20),
                             axes_spacing=5, text_pos='upper_left')

aqy_PM_25.NormMetBias(met_param='Temperature', plot_error_bars=True,
                      xlims=(5, 40), ylims=(-0.25, 2.25))
aqy_PM_25.NormMetBias(met_param='Relative_Humid', plot_error_bars=False,
                      xlims=(20, 100), ylims=(-0.25, 2.25))

# AQY Ozone evaluation
aqy_O3 = SensorEvaluation(sensor_name='Aeroqual_AQY',
                          eval_param='O3',
                          write_to_file=True)
aqy_O3.DeployDict()
aqy_O3.CalculateMetrics()
aqy_O3.Timeplot('1-hour', format_xaxis_weeks=True, date_interval=1,
                pt_formatting=True)
aqy_O3.SensorParamScatter('1-hour', plot_limits=(-1, 80),
                          axes_spacing=5, text_pos='upper_left')

aqy_O3.SensorParamScatter('1-hour', plot_subset=['2'],
                          plot_limits=(-1, 70),
                          axes_spacing=10, text_pos='upper_left',
                          pt_formatting=True)
aqy_O3.PlotMetrics()
aqy_O3.NormMetBias(met_param='Temperature', plot_error_bars=False,
                   xlims=(5, 40), ylims=(-0.25, 2.25))
aqy_O3.NormMetBias(met_param='Relative_Humid', plot_error_bars=False,
                   xlims=(20, 100), ylims=(-0.25, 2.25))
aqy_O3.NormMetBias(pt_formatting=True,
                   plot_error_bars=False)
