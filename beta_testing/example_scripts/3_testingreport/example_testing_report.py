# -*- coding: utf-8 -*-
"""
@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Fri May 21 15:19:53 2021
Last Updated:
  Thu Jun 24 11:24:00 2021
"""
import sensortoolkit

# full path to where you would like to place data, figures, reports, etc.
work_path = 'path/to/work-directory'
ref_path = work_path + '/Data and Figures/reference_data/airnowtech/processed'

sensor = sensortoolkit.AirSensor(make='Example_Make',
                                 model='Model',
                                 param_headers=['PM25', 'O3'],
                                 project_path=work_path)

#  ----------------------------------------------------------------------------
#   Specify testing organization/location details
#  ----------------------------------------------------------------------------

# Testing organization information
testing_org = {'Deployment name': '[Insert name of deployment]',
               'Org name': ['[Insert organization name]'],
               'Website': {'website name': '[Insert name of website]',
                           'website link': '[Insert website here]'},
               'Contact email': '[Insert email here]',
               'Contact phone': '[Insert phone number here]'}

# Testing location information
testing_loc = {'Site name': '[Insert name of site] ',
               'Site address': '[Insert site address]',
               'Site lat': '[Insert site latitude]',
               'Site long': '[Insert site longitude]',
               'Site AQS ID': '[If applicable, insert site AQS ID]'}

#  ----------------------------------------------------------------------------
#   Instantiate the PerformanceReport class for the example sensor dataset
#  ----------------------------------------------------------------------------
pollutant = sensortoolkit.param.Parameter('PM25')

test_report = sensortoolkit.PerformanceReport(
                                    name='Example_Make_Model',
                                    param=pollutant,
                                    path=work_path,
                                    reference_data=ref_path,
                                    tzone_shift=5,
                                    load_raw_data=False,
                                    write_to_file=True,
                                    testing_org=testing_org,
                                    testing_loc=testing_loc)

# Compile the report and save the file to the reports subfolder
test_report.CreateReport()
