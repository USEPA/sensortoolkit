# -*- coding: utf-8 -*-
"""Return the current version of sensortoolkit.

Users can verify that the sensortoolkit library is loaded properly by checking
the library version:

>>> print(sensortoolkit.__version__)
    "1.0.0"

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Aug 25 09:12:40 2021
Last Updated:
  Wed Aug 25 09:12:40 2021
"""
import pkg_resources

def _get_version():
    try:
        _version = pkg_resources.require('sensortoolkit')[0].version
        return _version

    except pkg_resources.DistributionNotFound as e:
        print(e)
        return None
