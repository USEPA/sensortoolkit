# -*- coding: utf-8 -*-
"""
The ``sensortoolkit.reference`` subpackage contains various modules for the
ingestion and import of reference datasets. Methods are also included for
querying reference data API services such as EPA's Air Quality System (AQS) and
the AirNow API.

===============================================================================

@Author:
    | Samuel Frederick, NSSC Contractor (ORAU)
    | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Sep  8 12:33:10 2021
Last Updated:
  Wed Sep  8 12:33:10 2021
"""
from ._airnowtech_to_long import airnowtech_wide_to_long
from ._import_airnowtech import preprocess_airnowtech
from ._load_ref_data import load_ref_dataframes
from ._ref_api_query import (ref_api_query, query_airnow, query_aqs)
from ._ref_flags import reference_flags
