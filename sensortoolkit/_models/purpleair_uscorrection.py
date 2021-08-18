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
  Wed Aug 18 09:09:57 2021
Last Updated:
  Wed Aug 18 09:09:57 2021
"""


def USCorrection(df, param):
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
    if param not in df:
        raise KeyError('Column header "' + param + '" not found in dataframe')
    if 'RH' not in df:
        raise KeyError('Column header "RH" not found in dataframe')

    # US Correction for PA data
    df[param + '_corrected'] = 0.524*df[param] - 0.0852*df['RH'] + 5.72

    return df
