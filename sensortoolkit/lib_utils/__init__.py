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
  Wed Sep  8 10:07:09 2021
Last Updated:
  Wed Sep  8 10:07:09 2021
"""

from ._version import _get_version
from ._copy_datasets import copy_datasets
from ._sensor_subfolders import create_sensor_directories
from ._flatten_list import flatten_list
from ._setup import Setup


