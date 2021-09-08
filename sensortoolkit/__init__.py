# -*- coding: utf-8 -*-
"""Top-level module for the ``sensortoolkit`` library.
"""

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
import sensortoolkit.sensor_ingest as sensor_ingest

# Modules for generating figures
import sensortoolkit.plotting as plotting

# Modules for importing, loading, and retrieving reference data
import sensortoolkit.reference as reference

# Import front-facing classes
from .evaluation._sensor_eval import SensorEvaluation
from .performancereport._performance_report import PerformanceReport

__version__ = lib_utils._get_version()