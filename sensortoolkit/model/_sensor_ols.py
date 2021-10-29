# -*- coding: utf-8 -*-
"""This module contains a method for computing the ordinary least-squares (OLS)
regression between collocated sensor and FRM/FEM reference measurements.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Mon Jul 27 09:21:14 2020
Last Updated:
  Mon Jul 27 10:47:00 2020
"""
import statsmodels.formula.api as smf


def sensor_ols(df, ref_df, y_var=None, x_vars=[]):
    """

    Generates a statsmodels OLS Regressions Results summary for selected
    x (independent) and y (dependent) variables for sensor data.

    Args:
        df (Pandas Dataframe):
            Sensor data.
        ref_df (Pandas Dataframe):
            Reference data.
        y_var (str):
            Name of dependent variable (often sensor concentration
            values).
        x_vars (list):
            Column names for independent variables (reference conc.,
            met params, etc.).

    Returns:
        results:
            statsmodels.regression.linear_model.RegressionResults instance. See
            the link below for more info on attributes:

            https://www.statsmodels.org/stable/generated/statsmodels.regression.
            linear_model.RegressionResults.html

    """
    # Search for reference name based on dependent variable, append to sensor
    # dataframe
    df = df.join(ref_df[y_var]).dropna()

    # Create a string for the RHS of OLS equation
    x_str = ''
    for i, var in enumerate(x_vars, 1):
        if i < len(x_vars):
            x_str += var + ' + '
        else:
            x_str += var

    # OLS regression
    ols_eqn = y_var + ' ~ ' + x_str
    results = smf.ols(ols_eqn, data=df).fit()

    print(results.summary())
    return results
