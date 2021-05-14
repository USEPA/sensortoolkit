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
  Tue Mar 17 14:41:13 2020
Last Updated:
  Thu Oct 1 13:11:00 2020
"""
import numpy as np


def Normalize(df_list, ref_df, param=None, ref_name=None):
    print('Computing normalized', param, 'values (by', ref_name + ')')

    for i, df in enumerate(df_list):
        try:
            df['Normalized_'+param] = df[param] / ref_df[param + '_Value']
        except KeyError as k:
            print('...Warning', k, 'not found in dataframe at index ', str(i))
            df['Normalized_' + param] = np.nan
        df_list[i] = df

    return df_list
