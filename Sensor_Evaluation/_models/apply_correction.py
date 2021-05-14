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
  Fri Oct 30 08:53:18 2020
Last Updated:
  Fri Oct 30 08:53:18 2020
"""


def Individual_Correction(param=None, df_list=None, stats_df=None):
    hourly_corr_list = []

    for df, m, b in zip(df_list, stats_df.Slope, stats_df.Intercept):
        corr = (df[param] - b) / m
        hourly_corr_list.append(corr.to_frame())

    return hourly_corr_list
