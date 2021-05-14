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
  Mon Jan 27 11:42:49 2020
Last Updated:
  Thu Nov 19 11:12:00 2020
"""
import numpy as np


def Dewpoint(df_list):
    """
    Magnus Formula for dewpoint. Constants via U.S EPA Performance Targets
    documents for particulate matter and ozone air sensors.
    """
    for i, df in enumerate(df_list):

        beta = 17.625
        lbda = 243.04  # degrees C

        if 'Temp' and 'RH' in df:
            T = df.Temp
            RH = df.RH
        else:
            print('Warning, Temperature and RH labels not recognized, DP not '
                  'computed')
            print(df.columns)
            return df_list

        numerator = lbda*(np.log(RH/100) + (beta*T)/(lbda+T))
        denominator = beta - (np.log(RH/100) + (beta*T)/(lbda+T))
        Dp = numerator / denominator

        df['DP_calculated'] = Dp

        df_list[i] = df

    return df_list
