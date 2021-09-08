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
  Fri May 21 15:19:53 2021
Last Updated:
  Thu Jun 24 11:24:00 2021
"""
import sensortoolkit

# full path to where you would like to place data, figures, reports, etc.
work_path = 'path/to/work-directory'
ref_path = work_path + '/Data and Figures/reference_data/airnowtech/processed'

#  ----------------------------------------------------------------------------
#   Specify testing organization/location details
#  ----------------------------------------------------------------------------

# Testing organization information
testing_org = {'Deployment name': 'Deployment #1',
               'Org name': ['U.S. Environmental Protection Agency',
                            'Office of Research and Development'],
               'Website': {'website name': 'Air Sensor Toolbox | U.S. EPA Website',
                           'website link': 'https://www.epa.gov/air-sensor-toolbox/'
                                           'evaluation-emerging-air-sensor-performance'},
               'Contact email': 'PI: Clements.Andrea@epa.gov',
               'Contact phone': '919-541-1364'}

# Testing location information
testing_loc = {'Site name': 'Ambient Monitoring Innovative '
                            'Research Station (AIRS) ',
               'Site address': 'Research Triangle Park, NC',
               'Site lat': '35.889510N',
               'Site long': '-78.874572W',
               'Site AQS ID': '37 – 063 – 0099'}

#  ----------------------------------------------------------------------------
#   Instantiate the PerformanceReport class for the example sensor dataset
#  ----------------------------------------------------------------------------
PM25 = sensortoolkit.param.Parameter('PM25')

test_report = sensortoolkit.PerformanceReport(
                                    name='Example_Make_Model',
                                    param=PM25,
                                    path=work_path,
                                    reference_data=ref_path,
                                    serials={'1': 'SN01',
                                             '2': 'SN02',
                                             '3': 'SN03'},
                                    tzone_shift=5,
                                    load_raw_data=False,
                                    write_to_file=True,
                                    testing_org=testing_org,
                                    testing_loc=testing_loc)

# Compile the report and save the file to the reports subfolder
test_report.CreateReport()
