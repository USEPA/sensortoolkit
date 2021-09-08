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
  Tue Aug 17 15:25:16 2021
Last Updated:
  Tue Aug 17 15:25:16 2021
"""
import numpy as np

def invalidate_period(df, param, start, end):
    """Invalidate data by manually indicating a period of time.

    Data within the indicated start and end timestamps will be invaldiated
    (i.e., values set np.nan) and the parameter QAQC column will indicate data
    have been modified by flagging as type #2

    # TODO: Come back to flagging number scheme

    Args:
        df (TYPE): DESCRIPTION.
        param (TYPE): DESCRIPTION.
        start (TYPE): DESCRIPTION.
        end (TYPE): DESCRIPTION.

    Returns:
        df (TYPE): DESCRIPTION.

    """
    df.loc[start:end, param] = np.nan
    df.loc[start:end, param + '_QAQC_Code'] = 2  # temporary flag
    return df
