# -*- coding: utf-8 -*-
"""
The ``sensortoolkit.ingest`` subpackage contains modules and methods for the
import and ingestion of sensor and reference datasets into the SDFS format as
well as a method for loading previously processed datasets. 

===============================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Sep  8 11:40:27 2021
Last Updated:
  Wed Sep  8 11:40:27 2021
"""

from ._processed_data_loader import processed_data_search
from ._standard_ingest import standard_ingest
from ._sensor_import import sensor_import
