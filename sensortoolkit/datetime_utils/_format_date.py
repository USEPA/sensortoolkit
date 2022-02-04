# -*- coding: utf-8 -*-
"""
This module contains a method for returning a string indicating the current date
in YYMMDD format.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Fri May  8 09:18:52 2020
Last Updated:
  Wed Jul 14 08:36:29 2021
"""
import pandas as pd


def get_todays_date(fmt='%y%m%d'):
    """Returns a string for today's date in YYMMDD format.

    Returns:
        formatted_date (str):
            String for the date in YYMMDD format.

    """
    datetime = pd.Timestamp.now()
    formatted_date = datetime.strftime(fmt)
    return formatted_date
