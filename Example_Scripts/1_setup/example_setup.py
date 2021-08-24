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
  Tue Aug 24 15:46:29 2021
Last Updated:
  Tue Aug 24 15:46:29 2021
"""
import sensortoolkit

# full path to where you would like to place data, figures, reports, etc.
work_path = 'path/to/work-directory'

"""
  ----------------------------------------------------------------------------
   Construct file structure for sensor, specify ingestion formatting scheme
  ----------------------------------------------------------------------------
"""
# Run the next line of code to create sub-dirs for sensor data, figures, etc.
sensortoolkit.Create_Sensor_Directories(name='Example_Make_Model',
                                        eval_params=['PM25', 'O3'],
                                        work_path=work_path
                                        )

# Run the next line of code to configure the formatting scheme for converting
# recorded sensor data to a standardized format utilized by SensorEvaluation
IngestionConfig = sensortoolkit.Setup()

"""
  ----------------------------------------------------------------------------
   OPTIONAL: If working with AirNowTech datasets, uncomment the following
   lines of code to pre-process AirNowTech files, create separate monthly
   files for PM, gas, met
  ----------------------------------------------------------------------------
"""
# ref_path = os.path.abspath(lib_path + '/Data and Figures/reference_data')
# ref_path = pathlib.PureWindowsPath(ref_path)
# filename = 'AirNowTech_BurdensCreek_20190801_20190902_PMGasMet.csv'
# airnowtech_path = (ref_path.as_posix()
#                    + '/airnowtech/downloaded_datasets/' + filename)
# sensortoolkit.Import_AirNowTech(airnowtech_path)
