# -*- coding: utf-8 -*-
"""
sensortoolkit
=============

A Python library for evaluating air sensor data. The library is intended for
use with sensors collocated at ambient air monitoring sites alongside FRM/FEM
monitors for comparison and analysis of sensor data against reference-grade
data.


Key Features
------------

**The primary goal of sensortoolkit is to provide a platform for analyzing air sensor
data regardless of formatting differences across sensor data formatting schemes.**
This goal extends to reference data as well, and interactive setup modules are
included for interpreting the recorded format for datasets for subsequent ingestion
into standardized formatting schemes for sensor and reference data.

- Import sensor data via a standardized ingestion process and interactive setup module
- Average to 1-hour and/or 24-hour averaging intervals.
- Import FRM/FEM reference data from a variety of sources, including ingestion
  modules for importing data from AirNowTech, and modules for querying either
  the AQS or AirNow API services.
- Submit queries for single or multiple parameters, parse datasets into a consistent reference data format and save unmodified and processed datasets to a data directory.
- Conduct analysis with the `SensorEvaluation` module

  *	Compute U.S. EPA’s recommended performance metrics for evaluating :math:`PM_{2.5}` and :math:`O_{3}` sensors.
  *	Visualize sensor performance with various figures and save to file location.

      *	Sensor vs. FRM/FEM scatter plots
      *	Timeseries indicating both sensor and FRM/FEM concentrations
      * Performance metric results and comparison against target values/ranges.
      *	Save performance evaluation results, statistics, and supplemental information detailing the deployment conditions to a deployment JSON file.

- Create testing reports using U.S. EPA’s base-testing report template (PowerPoint file) with the `PerformanceReport` module.
- Additional modules are included for calculating quantities (AQI, :math:`PM_{2.5}` NowCast, application of sensor correction equations, the U.S. Wide correction equation for PurpleAir sensors via Barkjohn et al. 2021 [#f1]_, etc.) and conducting additional analysis (quality control modules for identifying outliers, invalidation of datapoints, A&B channel cleaning for PurpleAir data via Barkjohn et al. 2021 [#f1]_, etc.)
- Access to modules utilized by the `SensorEvaluation` and `PerformanceReport` for greater customization in conducting analysis.

.. rubric:: Footnotes

.. [#f1] Barkjohn, K. K., Gantt, B., and Clements, A. L.: Development and application of a United States-wide correction for PM2.5 data collected with the PurpleAir sensor, Atmos. Meas. Tech., 14, 4617–4637, https://doi.org/10.5194/amt-14-4617-2021, 2021.


EPA Disclaimer
--------------

This software/application was developed by the U.S. Environmental Protection
Agency (USEPA). No warranty expressed or implied is made regarding the accuracy
or utility of the system, nor shall the act of distribution constitute any such
warranty. The USEPA has relinquished control of the information and no longer
has responsibility to protect the integrity, confidentiality or availability of
the information. Any reference to specific commercial products, processes, or
services by service mark, trademark, manufacturer, or otherwise, does not
constitute or imply their endorsement, recommendation or favoring by the USEPA.
The USEPA seal and logo shall not be used in any manner to imply endorsement of
any commercial product or activity by the USEPA or the United States Government.


Contact
-------

*Please direct all inquiries to:*
    | Andrea Clements Ph.D., Research Physical Scientist
    | U.S. EPA, Office of Research and Development
    | Center for Environmental Measurement and Modeling
    | Air Methods & Characterization Division, Source and Fine Scale Branch
    | 109 T.W. Alexander Drive, Research Triangle Park, NC  27711
    | Email: clements.andrea@epa.gov
    |

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

"""
import os as _os
from json import load
from shutil import copy2
from appdirs import user_data_dir

_lib_path = _os.path.dirname(_os.path.abspath(__file__))

_app_name='sensortoolkit'
_app_author='USEPA'
_app_data_dir = user_data_dir(_app_name, _app_author)

# Load in SDFS parameter attributes
_param_dict = {}
data = None
if not _os.path.exists(_app_data_dir):
    _os.makedirs(_app_data_dir)
    # copy param data from site-packages to folder location (initial install)
    copy2(_os.path.join(_lib_path, 'param', 'param_info.json'),
          _os.path.join(_app_data_dir, 'param_info.json'))
else:
    # load in param data at appdata location (including any custom params)
    with open(_os.path.join(_app_data_dir, 'param_info.json'), 'r') as file:
        data = load(file)
        for key, val in data.items():
            _param_dict[key] = val

del load, copy2, user_data_dir, data

# Setup modules and package maintenance
import sensortoolkit.lib_utils as lib_utils

# Utilities for working with timeseries data
import sensortoolkit.datetime_utils as datetime_utils

# Parameter and Targets objects
import sensortoolkit.param as param

# Modules for calculting statistical/environmental quantities
import sensortoolkit.calculate as calculate

# Modules for applying correction methods
import sensortoolkit.model as model

# Modules for cataloging deployment information
import sensortoolkit.deploy as deploy

# Quality Control modules
import sensortoolkit.qc as qc

# Modules for importing and ingesting sensor data
import sensortoolkit.ingest as ingest

# Modules for generating figures
import sensortoolkit.plotting as plotting

# Modules for importing, loading, and retrieving reference data
import sensortoolkit.reference as reference


class _presets:
    """A simple class for setting package-wide attributes.

    Attributes:
        _project_path: The directory where the user intends to store scripts,
        data, and results pertaining to an evaluation.

        test_org: Dictionary with information about the testing organization
        such as the name and contact information for the group.

        test_loc: Dictionary with information about the testing location such
        as site name, address, lat/lon coordinates.

    """
    #_project_path = _os.getcwd()
    _project_path = _lib_path
    _org_keys = ['Deployment name', 'Org name', 'Website',
                 'Contact email', 'Contact phone']
    _loc_keys = ['Site name', 'Site address', 'Site lat',
                 'Site long', 'Site AQS ID']

    def __init__(self):
        # Testing organization information
        self.test_org = {'Deployment name': '',
                         'Org name': ['', ''],
                         'Website': {'website name': '',
                                     'website link': ''},
                         'Contact email': '',
                         'Contact phone': ''}

        # Testing location information
        self.test_loc = {'Site name': '',
                         'Site address': '',
                         'Site lat': '',
                         'Site long': '',
                         'Site AQS ID': ''}

    def set_project_path(self, project_path=None):
        """Configure the path to the directory where evaluation scripts, data
        and results are stored.

        Returns:
            None.

        """
        if project_path is None:
            banner_w = 79
            src_dir = lib_utils._prompt_directory()

            print('Project Path:')
            print('..{0}'.format(src_dir))

            self._project_path = src_dir

        elif _os.path.isdir(project_path):
            self._project_path = project_path
        else:
            raise ValueError('Directory path does not exist')


presets = _presets()

# Import front-facing classes
from .testing_attrib_objs._airsensor import AirSensor
from .testing_attrib_objs._referencemonitor import ReferenceMonitor
from .evaluation_objs._sensor_eval import SensorEvaluation
from .evaluation_objs._performance_report import PerformanceReport
from .param._parameter import Parameter

__version__ = lib_utils._get_version()
