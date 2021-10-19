# -*- coding: utf-8 -*-
"""
Description.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Tue Oct 12 08:25:24 2021
Last Updated:
  Tue Oct 12 08:25:24 2021
"""
import pandas as pd
import numpy as np

def airnowtech_wide_to_long(path):

    df = pd.read_csv(path, names=['Site/Site AQS/Param/POC', 'Date (LST)',
                                  '0', '1', '2', '3', '4', '5',
                                  '6', '7', '8', '9', '10', '11',
                                  '12', '13', '14', '15', '16', '17',
                                  '18', '19', '20', '21', '22', '23',
                                  'Average', 'Max'])
    df = df.drop([0])

    site_cols = ['Site', 'Site AQS', 'Param', 'POC']
    df[site_cols] = df['Site/Site AQS/Param/POC'].str.split('/', expand=True)

    df['unique_param_ids'] = df.Param + ' ' + df.POC
    unique_param_ids = df['unique_param_ids'].unique()

    data = pd.DataFrame()
    for param_id in unique_param_ids:

        # Data for each parameter in the downloaded dataset
        param_data = df[df.unique_param_ids == param_id]
        param_data = param_data.reset_index()

        # col names for hourly data
        value_cols = [str(i) for i in np.arange(0, 24, 1)]

        # convert hourly data to long format
        melt = pd.melt(param_data, id_vars='Date (LST)', value_vars=value_cols)

        # Add formatted timestamp, set as index
        melt['timestamp'] = (melt['Date (LST)'] + ' ' +
                             melt['variable'].str.zfill(2) + ':00:00')
        melt['timestamp'] = pd.to_datetime(melt['timestamp'],
                                           format='%m/%d/%y %H:%M:%S')
        melt = melt.set_index(melt['timestamp'])
        melt = melt.sort_index()

        # Drop timestamp columns (keep timestamp index)
        melt = melt.drop(columns=['Date (LST)', 'variable', 'timestamp'])

        # reset name of the value column to indicate parameter values
        param = param_id.split(' ')[0]
        melt = melt.rename(columns={'value': param})

        data = data.combine_first(melt)

    return data


if __name__ == '__main__':
    path = r"C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\AirNowTech_pivoted_test.csv"

    df = airnowtech_wide_to_long(path)
