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
  Fri May  8 09:18:52 2020
Last Updated:
  Fri May  8 09:20:52 2020
"""
import pandas as pd


def Get_Date():
    """
    Returns a string for today's date in YYMMDD format
    """
    datetime = pd.Timestamp.now()
    formatted_date = datetime.strftime('%y%m%d')
    return formatted_date
