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
  Wed Jul  7 13:32:49 2021
Last Updated:
  Tue Jul 13 11:34:00 2021
"""
import pandas as pd
import numpy as np


def Compute_AB_Averages(df, cleaning=True, a_col_name=None,
                        b_col_name=None):
    """Average A and B channel data for  PurpleAir sensors.

    QC criteria via Barkjohn et al. 2021, publication link:
        https://amt.copernicus.org/articles/14/4617/2021/

    Args:
        df (pandas dataframe):
            PurpleAir dataframe containing columns with A and B channel PM2.5
            data.
        cleaning (bool):
            If true, datapoints outside the QC criteria of Barkjohn et al. 2021
            will be invalidated (set null). Else, QC criteria will not be
            applied.
        a_col_name (str):
            The column header name for PM2.5 data from channel A.
        b_col_name (str):
            The column header name for PM2.5 data from channel B.

    Returns:
        df (pandas dataframe):
            Modified PurpleAir dataframe with computed AB averages
    """
    if cleaning is True:
        # Compute (A-B) difference
        AB_diff = df[a_col_name] - df[b_col_name]

        # Absolute value of (A-B)
        AB_absdiff = abs(AB_diff)

        # Compute percent difference of A and B
        AB_pdiff = 2*(df[a_col_name] - df[b_col_name]) / \
                     (df[a_col_name] + df[b_col_name])

        # Exclusion thresholds
        pm_thres = 5.0  # ug/m^3
        AB_pdiff_thres = 0.70  # exclude > 70% difference

        df = pd.concat([df, AB_absdiff, AB_pdiff],
                       axis=1).rename(columns={0: 'PM25_AB_absdiff',
                                               1: 'PM25_AB_pdiff'})

        # Datapoint exclusion mask
        invalid = ((df['PM25_AB_absdiff'] > pm_thres) &
                   (abs(df['PM25_AB_pdiff']) > AB_pdiff_thres)) | \
                   (df[a_col_name].isnull()) | \
                   (df[b_col_name].isnull())

        # Raw AB averages
        df['PM25_AB_raw'] = (df[a_col_name] + df[b_col_name])/2

        # Extract as series
        AB_avgs = df['PM25_AB_raw']

        # Cleaned AB averages
        AB_avgs[invalid] = np.nan

        # Assign cleaned AB averaged data to dataframe
        df['PM25'] = AB_avgs

        #df = QC_flags(df, a_col_name, b_col_name)

    else:
        # Raw AB averages
        df['PM25_AB_raw'] = (df[a_col_name] + df[b_col_name])/2
        # Extract as series
        AB_avgs = df['PM25_AB_raw']

        # Assign AB averaged data to dataframe
        df['PM25'] = AB_avgs

    return df


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
