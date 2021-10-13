# -*- coding: utf-8 -*-
"""
Description.

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
