# -*- coding: utf-8 -*-
"""
@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Fri May  8 09:18:52 2020
Last Updated:
  Wed Jul 14 08:36:29 2021
"""
import pandas as pd


def get_todays_date():
    """Returns a string for today's date in YYMMDD format.

    Args:
        None
    Returns:
        formatted_date (str):
            String for the date in YYMMDD format.
    """
    datetime = pd.Timestamp.now()
    formatted_date = datetime.strftime('%y%m%d')
    return formatted_date
