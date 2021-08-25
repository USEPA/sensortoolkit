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
  Wed Aug 25 09:12:40 2021
Last Updated:
  Wed Aug 25 09:12:40 2021
"""
import pkg_resources

def Get_Version():
    try:
        _version = pkg_resources.require('sensortoolkit')[0].version
        return _version

    except pkg_resources.DistributionNotFound as e:
        print(e)
        return None
