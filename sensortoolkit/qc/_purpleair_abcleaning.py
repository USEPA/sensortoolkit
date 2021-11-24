# -*- coding: utf-8 -*-
"""
This module contains a method for averaging the dual PMS5003 PM2.5 data channels
for PurpleAir PA-II and PA-II-SD sensors. This method of data averaging was
developed by Barkjohn et al. 2021 [#f1]_, and is discussed in detail in the
publication section 3.2.3 "Comparison of A and B channels". Briefly, quality
control (QC) criteria are applied during data averaging, whereby the absolute
and percent difference between concurrent (nearest neighbor by logged timestamp)
A and B channel measurement pairs are calculated. If both of these QC criteria
do not exceed respective thesholds, the A and B channels are averaged. Otherwise,
occasions where the A and B channel differ by a margin greater than the QC
criteria thresholds are set null.

.. rubric:: Footnotes

.. [#f1] Barkjohn, K. K., Gantt, B., and Clements, A. L.: Development and application of a United States-wide correction for PM2.5 data collected with the PurpleAir sensor, Atmos. Meas. Tech., 14, 4617–4637, https://doi.org/10.5194/amt-14-4617-2021, 2021.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Jul  7 13:32:49 2021
Last Updated:
  Wed Aug 18 09:10:24 2021
"""
import pandas as pd
import numpy as np


def purpleair_ab_averages(df, cleaning=True, a_col_name=None,
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
        df['PM25_Value'] = AB_avgs

        #df = QC_flags(df, a_col_name, b_col_name)

    else:
        # Raw AB averages
        df['PM25_AB_raw'] = (df[a_col_name] + df[b_col_name])/2
        # Extract as series
        AB_avgs = df['PM25_AB_raw']

        # Assign AB averaged data to dataframe
        df['PM25_value'] = AB_avgs

    return df
