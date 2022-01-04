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
    | Office: 919-541-1363 | Email: clements.andrea@epa.gov
    |

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

"""
_param_dict = {}
from json import load
from pathlib import Path
with open(f'{Path(__file__).parent}/param/param_info.json', 'r') as file:
    data = load(file)
    for key, val in data.items():
        _param_dict[key] = val
del data, file, key, val
del Path, load

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


# Import front-facing classes
from .testing_attrib_objs._airsensor import AirSensor
from .testing_attrib_objs._referencemonitor import ReferenceMonitor
from .evaluation_objs._sensor_eval import SensorEvaluation
from .evaluation_objs._performance_report import PerformanceReport
from .param._parameter import Parameter

__version__ = lib_utils._get_version()

from os import getcwd

class _presets:
    """A simple class for setting package-wide attributes.

    Attributes:
        _project_path: The directory where the user intends to store scripts,
        data, and results pertaining to an evaluation.

    """
    _project_path = getcwd()

    def __init__(self):
        pass

    def set_project_path(self):
        """Configure the path to the directory where evaluation scripts, data
        and results are stored.

        Returns:
            None.

        """

        banner_w = 79
        src_dir = lib_utils._prompt_directory()

        print('Project Path:')
        print('..{0}'.format(src_dir))

        self._project_path = src_dir

presets = _presets()

del getcwd