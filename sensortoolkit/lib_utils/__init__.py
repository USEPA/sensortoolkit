# -*- coding: utf-8 -*-
"""
The ``sensortoolkit.lib_utils`` subpackage contains general utilities that are
accessed by various methods that contain interactive components or assist in
configuring the project workspace.

===============================================================================

@Author:
    | Samuel Frederick, NSSC Contractor (ORAU)
    | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Sep  8 10:07:09 2021
Last Updated:
  Wed Sep  8 10:07:09 2021
"""

from ._check_type import check_type
from ._version import _get_version
from ._input_tools import validate_entry, enter_continue
from ._copy_datasets import copy_datasets, _prompt_directory
from ._sensor_subfolders import create_sensor_directories
from ._flatten_list import flatten_list
from ._flatten_datasets import flatten_datasets
from ._setup import SensorSetup
from ._setup import ReferenceSetup
