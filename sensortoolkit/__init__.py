# -*- coding: utf-8 -*-
"""Top-level module for the ``sensortoolkit`` library.

*Please direct all inquiries to:*
    | Andrea Clements Ph.D., Research Physical Scientist
    | U.S. EPA, Office of Research and Development
    | Center for Environmental Measurement and Modeling
    | Air Methods & Characterization Division, Source and Fine Scale Branch
    | 109 T.W. Alexander Drive, Research Triangle Park, NC  27711
    | Office: 919-541-1363 | Email: clements.andrea@epa.gov
    |

===============================================================================

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
