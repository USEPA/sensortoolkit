# -*- coding: utf-8 -*-
"""
This module contains a method for detecting potential outliers in sensor
datasets by computing the Cook's distance for measurements in 1-hour averaged
sensor measurements relative to reference measurements.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Tue Aug 17 15:29:14 2021
Last Updated:
  Tue Aug 17 15:29:14 2021
"""
import statsmodels.api as sm
import pandas as pd
import numpy as np


def cooks_outlier_detection(hourly_df_list, hourly_ref_df, param, serials,
                            invalidate=False):
    """Estimate outliers via Cook’s distance for 1-hr sensor vs. ref. regress.

    Values for timestamps exceeding a threshold of 4/L (L is the total
    number of sensor-FRM/FEM  data pairs) are indicated by Cooks distance
    to be potential outliers. To ensure that data points identified by
    Cooks distance are likely outliers, the absolute difference (AD) and
    percent difference (PD) (and their respective standard deviations (SD))
    are computed between sensor and reference data. The median plus twice
    the SD of both the AD and PD are computed, and each data point
    identified by Cook’s distance is compared against these thresholds.
    If the AD and PD for the potential outlier data point exceed these
    thresholds, a QA/QC code is assigned to the corresponding time stamp.

    If ``‘invalidate’`` is true, sensor evaluation parameter data points that
    are identified by Cook’s distance as potential outliers and exceed the
    AD and PD thresholds are set to null.

    Args:
        hourly_df_list (list):
            List of sensor datasets at 1-hour averaged intervals.
        hourly_ref_df (pandas DataFrame):
            Reference dataframe at 1-hour averaged intervals for the passed
            parameter.
        param (str):
            Column header name for the parameter values.
        serials (dict):
            A dictionary of unique serial identifiers for each sensor in the
            testing group.
        invalidate (bool, optional):
            If True, outlier entries will be set null (np.nan). Defaults to
            False.

    Returns:
        hourly_df_list (list):
            A list of modified sensor datasets.

    """

    for i, (serial, sensor_df) in enumerate(zip(serials.values(),
                                                hourly_df_list)):
        print('Flagged timestamps for', serial)
        xdata = hourly_ref_df[param + '_Value']
        ydata = sensor_df[param + '_Value']
        df = pd.DataFrame({'x': xdata, 'y': ydata}).dropna()

        n_obs = df.shape[0]
        thres = (4 / n_obs)

        # Compute OLS regression for sensor vs. reference
        x = df['x']
        y = df['y']
        x = sm.add_constant(x)
        model = sm.OLS(y, x).fit()

        # Compute cooks distance for ref vs. average sensor conc.
        infl = model.get_influence()
        cooks = infl.cooks_distance
        cooks_df = pd.DataFrame({'distance': cooks[0],
                                 'p_val': cooks[1]})
        outliers = cooks_df[cooks_df.distance > thres]

        # Outlier timestamps
        outlier_times = df.index[outliers.index]

        # Thresholds for flagging data points
        abs_diff = abs(sensor_df[param + '_Value'] -
                       hourly_ref_df[param + '_Value'])
        abs_diff_thres = abs_diff.median() + 2*abs_diff.std()

        p_diff = 2*abs_diff / (sensor_df[param + '_Value'] +
                               hourly_ref_df[param + '_Value'])
        p_diff_thres = p_diff.median() + 2*p_diff.std()

        # Create a column for flagging data points
        if param + '_QAQC_Code' not in sensor_df:
            sensor_df.loc[:, param + '_QAQC_Code'] = np.nan
        # Ensure that outlier times exceeding cooks thres. justify flagging
        # by exceeding thresholds for abs diff and percent diff
        flag_count = 0
        for time in outlier_times:
            if (abs_diff[time] > abs_diff_thres and
               p_diff[time] > p_diff_thres):
                # TODO: Temporary flag assignment. Need to consult QC flag
                # template
                sensor_df.loc[time, param + '_QAQC_Code'] = 3
                if invalidate:
                    sensor_df.loc[time, param + '_Value'] = np.nan
                print('..' + str(time))
                flag_count += 1
        if flag_count == 0:
            print('..No data points flagged')

        hourly_df_list[i] = sensor_df

    return hourly_df_list
