# -*- coding: utf-8 -*-
"""
Method for converting datasets downloaded from the AirNow-Tech website from
wide format (data are organized by row for each day and by column for each
hour of the day) to long format (data are organized by row for consecutive
timestamps).

===============================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Tue Oct 12 08:25:24 2021
Last Updated:
  Tue Oct 12 08:25:24 2021
"""
import datetime
import pandas as pd
import numpy as np
import pytz
from pytz.exceptions import UnknownTimeZoneError
from sensortoolkit.lib_utils import validate_entry


def airnowtech_wide_to_long(path):
    """Convert downloaded AirNowTech datasets from wide format to long format.

    When users download datasets from the `AirNowTech website <airnowtech.org/data>`_,
    users may select various options for how the data
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

    Raises:
        ValueError: If the shape of the passed dataset does not correspond to
            an expected width (ncols = 28 for abbreviated wide datasets,
            ncols = 36 for full wide datasets). This likely occurs if an
            unpivoted (long format) AirNow-Tech dataset is passed to the
            function, which has a width of 16 columns.

    Returns:
        data (pandas DataFrame):
            An unpivoted, long format version of the passed dataset. Should be
            passed to ``sensortoolkit.reference.preprocess_airnowtech()`` for

    """
    unpivot_cols = {'Agency': str,
                    'Site': str,
                    'Site AQS': str,
                    'Param': str,
                    'Param AQS': int,
                    'POC': int,
                    'Method': str,
                    'Duration': str,
                    'Date (LST)': str,
                    'Time (LST)': str,
                    'Offset': str,
                    'Value': float,
                    'Unit': str,
                    'QC Code': str}

    df = pd.read_csv(path)

    shape = df.shape

    if shape[1] == 28:
        full = False
        dt_fmt = '%m/%d/%y %H:%M:%S'
    elif shape[1] == 36:
        full = True
        dt_fmt = '%m/%d/%Y %H:%M:%S'
    else:
        raise ValueError(f'Invalid dataframe shape: {shape}')

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
        melt['DateTime'] = (melt['Date (LST)'] + ' ' +
                             melt['variable'].str.zfill(2) + ':00:00')
        melt['DateTime'] = pd.to_datetime(melt['DateTime'],
                                           format=dt_fmt)
        melt = melt.set_index(melt['DateTime'])
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
            else:
                melt.loc[row.Index, 'Param AQS'] = np.nan
                melt.loc[row.Index, 'Unit'] = np.nan
                melt.loc[row.Index, 'Method'] = np.nan
                melt.loc[row.Index, 'Duration'] = np.nan
                melt.loc[row.Index, 'Agency'] = np.nan

        # Drop timestamp columns (keep timestamp index)
        melt = melt.drop(columns=['Date (LST)', 'variable', 'DateTime'])

        # reset name of the value column to indicate parameter values
        param = param_id.split(' ')[0]
        melt = melt.rename(columns={'value': 'Value'})

        data = data.append(melt)

    # Rearrange column order to match unpivoted column order
    rearr_cols = []
    for col, dtype in unpivot_cols.items():
        if col in data:
            rearr_cols.append(col)
            data[col] = data[col].astype(dtype, errors='ignore')
    data = data[rearr_cols]

    data['QC Code'] = ''

    invalid = True
    while invalid is True:
        val = input('AirNow-Tech data are reported in LST. Enter the time zone '
                    'name corresponding \nto the LST timestamps: ')

        try:
            time_zone = pytz.timezone(val)
        except UnknownTimeZoneError:
            print(f'..invalid time zone "{val}"')
            continue

        confirm = validate_entry()
        if confirm == 'y':
            invalid = False


    dt = datetime.datetime.utcnow()
    offset = time_zone.utcoffset(dt) / pd.to_timedelta('1 hour')
    print('')
    print(f'..converting datetime index from {time_zone} (UTC {offset} '
          'hours) to UTC.')
    data = data.tz_localize(val).tz_convert('UTC')

    return data



if __name__ == '__main__':

    # abbreviated
    path = r"C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\kitchen_sink_pivoted_abbrev.csv"

    # full
    #path = r"C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\kitchen_sink_pivoted_full.csv"

    # long format dataset
    #path = r"C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\kitchen_sink_unpivoted.csv"

    df = airnowtech_wide_to_long(path)
