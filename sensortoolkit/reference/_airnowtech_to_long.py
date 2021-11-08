# -*- coding: utf-8 -*-
"""
Description.

===============================================================================

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
    """Convert downloaded AirNowTech datasets from wide format to long format.

    When users download datasets from the AirNowTech website
    (airnowtech.org/data), users may select various options for how the data
    are displayed under the 'Display Settings' menu. Next to the 'Display'
    section within the menu, the checkbox 'Table' should be selected by
    default. Next to the 'Table' checkbox is a dropdown menu with options for
    how the table will be displayed. Users can choose from 'Unpivoted',
    'Pivoted By Hour - Abbrev.', 'Pivoted By Hour - Full', 'Pivoted By
    Dataset', or 'Unpivoted'.

    The sensortoolkit library works with timeseries data in unpivoted, long
    format. In turn, if users select one of the pivoted options in the display
    menu, this module should be used to convert pivoted (wide format) datasets
    to long format.

    .. note::

        The timezone is not indicated in pivoted datasets; however, nonpivoted
        versions of the same dataset downloaded from AirNowTech indicate the
        time stamp to be local standard time (LST) for matching measurement
        values in pivoted and non-pivoted datasets.

        **In turn, timestamps in datasets returned by this module should be
        considered to be logged in LST.**

    Args:
        path (str):
            Full path to the downloaded  airnowtech dataset in pivoted (wide)
            format.

    Returns:
        data (pandas DataFrame):
            An unpivoted, long format version of the passed dataset. Should be
            passed to ``sensortoolkit.reference.preprocess_airnowtech()`` for
            ingestion to SDFS formatted dataset.

    """
    unpivot_cols = ['Agency', 'Site', 'Site AQS', 'Param',
                    'Param AQS', 'POC', 'Method', 'Duration',
                    'Date (LST)', 'Time (LST)', 'Offset', 'Value', 'Unit']

    df = pd.read_csv(path)

    shape = df.shape

    if shape[1] == 28:
        full = False
        dt_fmt = '%m/%d/%y %H:%M:%S'
    elif shape[1] == 36:
        full = True
        dt_fmt = '%m/%d/%Y %H:%M:%S'
    else:
        raise ValueError('Invalid dataframe shape')

    if full is False:
        df = pd.read_csv(path, names=['Site/Site AQS/Param/POC', 'Date (LST)',
                                      '0', '1', '2', '3', '4', '5',
                                      '6', '7', '8', '9', '10', '11',
                                      '12', '13', '14', '15', '16', '17',
                                      '18', '19', '20', '21', '22', '23',
                                      'Average', 'Max'])
        df = df.drop([0])

        site_cols = ['Site', 'Site_AQS', 'Param', 'POC']
        df[site_cols] = df['Site/Site AQS/Param/POC'].str.split('/',
                                                                expand=True)

    else:
        df = df.rename(columns={'Site AQS': 'Site_AQS',
                                'Param AQS': 'Param_AQS'})

    df['unique_param_ids'] = df.Param.astype(str) + ' ' + df.POC.astype(str)
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
                                           format=dt_fmt)
        melt = melt.set_index(melt['timestamp'])
        melt = melt.sort_index()

        # Loop over each day and assign the indicated site, poc to long fmt df
        param_data = param_data.set_index(param_data['Date (LST)'])
        for row in param_data.itertuples():
            melt.loc[row.Index, 'Site'] = row.Site
            melt.loc[row.Index, 'Site AQS'] = row.Site_AQS
            melt.loc[row.Index, 'Param'] = row.Param
            melt.loc[row.Index, 'POC'] = row.POC
            # Additional attributes for full pivoted datasets
            if full:
                melt.loc[row.Index, 'Param AQS'] = row.Param_AQS
                melt.loc[row.Index, 'Unit'] = row.Unit
                melt.loc[row.Index, 'Method'] = row.Method
                melt.loc[row.Index, 'Duration'] = row.Duration
                melt.loc[row.Index, 'Agency'] = row.Agency

        # Drop timestamp columns (keep timestamp index)
        melt = melt.drop(columns=['Date (LST)', 'variable', 'timestamp'])

        # reset name of the value column to indicate parameter values
        param = param_id.split(' ')[0]
        melt = melt.rename(columns={'value': 'Value'})

        data = data.combine_first(melt)

    # Rearrange column order to match unpivoted column order
    rearr_cols = []
    for col in unpivot_cols:
        if col in data:
            rearr_cols.append(col)
    data = data[rearr_cols]

    return data


if __name__ == '__main__':

    # abbreviated
    path = r"C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\ant_pivoted_abbrev.csv"

    # full
    path = r"C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\ant_pivoted_full.csv"

    df = airnowtech_wide_to_long(path)
