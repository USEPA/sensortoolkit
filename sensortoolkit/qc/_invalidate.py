# -*- coding: utf-8 -*-
"""
Description.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Tue Aug 17 15:25:16 2021
Last Updated:
  Tue Aug 17 15:25:16 2021
"""
import numpy as np

def invalidate_period(df, param, bdate, edate):
    """Invalidate data by manually indicating a period of time.

    Data within the indicated start and end timestamps will be invaldiated
    (i.e., values set np.nan) and the parameter QAQC column will indicate data
    have been modified by flagging as type #2

    # TODO: Come back to flagging number scheme

    Args:
        df (TYPE): DESCRIPTION.
        param (TYPE): DESCRIPTION.
        bdate (TYPE): DESCRIPTION.
        edate (TYPE): DESCRIPTION.

    Returns:
        df (TYPE): DESCRIPTION.

    """
    df.loc[bdate:edate, param] = np.nan
    df.loc[bdate:edate, param + '_QAQC_Code'] = 2  # temporary flag
    return df
