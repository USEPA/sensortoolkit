# -*- coding: utf-8 -*-
"""
This module contains methods for applying correction equations specific to the
PurpleAir PA-II sensor. These correction methods apply published equations
by authors whose work is cited in the docstring of the function pertaining to
each correction equation.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Aug 18 09:09:57 2021
Last Updated:
  Wed Aug 18 09:09:57 2021
"""


def purpleair_us_corr(df, param):
    """US-Wide Correction equation of Barkjohn et al. 2021 for PurpleAir PA-II
    sensors.

    Publication Link:
        https://amt.copernicus.org/articles/14/4617/2021/

    Args:
        df (pandas dataframe):
            Dataframe with PurpleAir PA-II concentration values for PM2.5
    Returns:
        df (pandas dataframe):
            Modified dataframe with US-Correction applied to param values (
            under column header param + '_corrected')

    Raises:
        KeyError: If passed param name not in dataframe
        KeyError: If 'RH' not in passed dataframe

    """
    # US Correction for PA data
    df[param + '_corrected'] = 0.524*df[param + '_Value'] - 0.0852*df['RH_Value'] + 5.72

    return df
