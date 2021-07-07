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
  Wed Jul  7 13:32:49 2021
"""
import pandas as pd
import numpy as np


def Compute_AB_Averages(df, cleaning=True, a_col_name=None,
                        b_col_name=None):
    """Clean PurpleAir datasets using Barkjohn et al. 2021 QC criteria for
    computing AB averages.
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
    # US Correction for PA data
    df[param + '_corrected'] = 0.524*df[param] - 0.0852*df['RH'] + 5.72
    return df
