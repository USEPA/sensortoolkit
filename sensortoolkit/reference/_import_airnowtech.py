# -*- coding: utf-8 -*-
"""
Module for importing raw AirNowTech data (table, unpivoted format) queried at
month-long intervals at 1-hr recording frequency for PM2.5, PM10, O3, NO2, CO,
relative humidity, temperature, wind speed, wind direction.

Data are sorted into PM, gas, and met dataframes and a table containing
all AQS method codes is used to associate the recorded method code for data
streams with the instrument used to make the measurement.

Processed dataframes for PM, Gas, and met are then written to separate monthly
csv files where the index is the date and time in UTC.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Fri Jul 17 08:15:17 2020
Last Updated:
  Wed Jul 14 11:02:35 2021
"""
import pandas as pd
import numpy as np
import os
import pathlib
import datetime
from shutil import copy
from sensortoolkit.reference import airnowtech_wide_to_long
from sensortoolkit.lib_utils import flatten_list


def ingest_airnowtech(path, Clean_QC_Code=False):
    """Ingest raw AirNowTech data (table, unpivoted format, 1-hr recording
    freq) and set index column to Date & Time (UTC).

    Args:
        path (str):
            Full directory path to downloaded dataset.
    Returns:
        Clean_QC_Code (bool):
            If true, only keep data where the QC code is zero (indicates no
            issues reported).

    """
    try:
        # Check if dataset is in wide format, convert to long format first.
        df = airnowtech_wide_to_long(path)
    except ValueError:
        # Import csv dataframe, set hourly UTC date and time as index
        df = pd.read_csv(path, parse_dates={'DateTime': ['Date (UTC)',
                                                         'Time (UTC)']},
                         index_col='DateTime')

        df = df.tz_localize('UTC')

    if Clean_QC_Code is True:
        df = df[df['QC Code'] == 0]

    # Regenerate hourly index to fill gaps in dataset
    hourly_index = pd.date_range(df.index.min(), df.index.max(), freq='H')

    # Fill gaps in hourly index
    df = pd.DataFrame(index=hourly_index).join(df)

    # Change AQS ID column dtype to string and remove decimal place
    df['Site AQS'] = df['Site AQS'].astype(str).replace(r'\.0', '', regex=True)
    return df


def sort_airnowtech(df):
    """Data are sorted into PM, gas, and met dataframes and a table containing
    all AQS method codes is used to associate the recorded method code for data
    streams with the instrument used to make the measurement.

    Args:
        df (pandas dataframe):
            Imported airnowtech dataset, may contain data for multilple
            parameter classifications (PM, gases, met) if selected when the
            data were downloaded.
    Returns:
        None, writes processed datasets to airnowtech processed data folder
        path.

    """
    method_path = os.path.abspath(os.path.join(__file__, '..','method_codes',
                                               'methods_criteria.csv'))

    # Method code lookup dataframe
    method_df = pd.read_csv(method_path)

    # Dataframes to be populated
    idx = df.index.drop_duplicates()
    gas_df = pd.DataFrame(index=idx)
    pm_df = pd.DataFrame(index=idx)
    met_df = pd.DataFrame(index=idx)

    # Valid column names for parameters
    pm_list = ['PM10-81102', 'PM10-85101', 'PM2.5-88101', 'PM2.5-88502']
    gas_list = ['CO', 'O3', 'NO2', 'SO2']
    met_list = ['RHUM', 'TEMP', 'WS', 'WD']

    site_cols = ['index', 'Agency', 'Site', 'Site AQS']
    site_df = df.reset_index().drop_duplicates(subset=['index'])[site_cols]
    site_df = site_df.set_index(site_df['index']).drop(columns=['index'])
    site_df = site_df.rename(columns={'Site': 'Site_Name',
                                      'Site AQS': 'Site_AQS'})
    site_df['Site_AQS'] = site_df['Site_AQS'].astype(str)

    state_id = site_df['Site_AQS'].str.slice(0, 2)
    county_id = site_df['Site_AQS'].str.slice(2, 5)
    site_id = site_df['Site_AQS'].str.slice(5, 9)

    site_df['Site_AQS'] = (state_id + '-' + county_id + '-' + site_id)
    for param in df.Param.dropna().unique():

        param_df = df[df.Param == param]

        hourly_index = pd.date_range(param_df.index[0], param_df.index[-1],
                                     freq='H')
        param_df = pd.DataFrame(index=hourly_index).join(param_df)
        param_df = param_df[['Param AQS', 'POC', 'Method',
                             'Value', 'Unit', 'QC Code']]

        param_df = param_df.rename(columns={'Param AQS': param + '_Param_Code',
                                            'POC': param + '_Method_POC',
                                            'Method': param + '_Method_Code',
                                            'Value': param + '_Value',
                                            'Unit': param + '_Unit',
                                            'QC Code': param + '_QAQC_Code'})

        # If multiple instruments present, choose first instrument datastream
        if len(param_df[param + '_Method_POC'].dropna().unique()) > 1:
            param_df = param_df[param_df[param + '_Method_POC'] == 1]
            print(f'..Multiple POCs for {param} found. Retaining data for POC 1.')

        # Method code(s) listed for parameter data
        method_list = param_df[param + '_Method_Code'].dropna().unique()
        # Find instrument corresponding to method code in lookup table
        for method in method_list:
            method_name = method_df.where(
                    method_df['Method Code'
                              ] == method).dropna()['Equivalent Method']

            # Lots of instruments associated with Method Code 11, for eval.
            # purposes likely only assoc with RH values.
            if method == 11:
                method_name = pd.Series(['HYGROTHERMOGRAPH ELEC OR MACH AVG'])

        # If one instrument type used for parameter data stream, record in col
        if (len(method_list) == 1 and len(method_name.values) > 0):
            # Set instrument name via lookup
            data = param_df.where(
                    param_df.isnull().any(axis=1) == False).dropna(axis=0,
                                                                   how='all')
            data[param + '_Method'] = method_name.values[0]
            param_df = data
        else:
            # No name found in method code lookup table
            param_df[param + '_Method'] = np.nan

        if param in pm_list:
            pm_df = pm_df.join(param_df).combine_first(site_df)
        if param in gas_list:
            gas_df = gas_df.join(param_df).combine_first(site_df)
        if param in met_list:
            met_df = met_df.join(param_df).combine_first(site_df)

    return pm_df, gas_df, met_df


def write_to_file(df, path, outpath):
    """Processed dataframes for PM, Gas, and met written to separate monthly
    csv files where the index is the date and time in UTC.

    Args:
        df (pandas dataframe):
            Processed airnowtech data for one of the following parameter
            classifications (PM, Gases, or Met)
        path (str):
            The full directory path to the downloded airnowtech dataset.
            Used to determine the date and time that the data were downloaded
            and added to the dataframe as the 'Data_Acquisition_Date_Time'.
        outpath (str):
            The full directory path where the processed dataframe will be saved
    Returns:
        None

    """
    folder = None
    # Dictionary for renaming AirNowTech parameter names to common format
    renaming = {'PM10-81102': 'PM10',
                'PM10-85101': 'PM10',
                'PM2.5-88101': 'PM25',
                'PM2.5-88502': 'PM25',
                'O3': 'O3',
                'CO': 'CO',
                'NO2': 'NO2',
                'SO2': 'SO2',
                'RHUM': 'RH',
                'TEMP': 'Temp',
                'WS': 'WS',
                'WD': 'WD'}

    # Column names associated with each parameter
    aqs_attribs = ['_Value', '_Unit', '_QAQC_Code', '_Param_Code',
                   '_Method', '_Method_Code', '_Method_POC']

    # Method names are listed in all upper case in the method code lookup
    # table, so I use .title() to leave only the first letter of each word
    # describing the reference method. These are some exceptions:
    replace = {'Api': 'API',
               'Frm': 'FRM',
               'Fem': 'FEM',
               'Lpm': 'LPM',
               ' At ': ' at ',
               'Bam': 'BAM',
               'Pm': 'PM',
               'Vscc': 'VSCC',
               ' Te ': ' TE ',
               ' Or ': ' or ',
               'W/': 'w/',
               ' And ': ' and '}

    orig_inpath = path
    orig_outpath = outpath

    # Require non-empty dataframe
    if not df.empty:
        print('Writing AirNow-Tech data sets to csv files')

        start_month = df.index[0].strftime('%Y-%m')
        end_month = df.index[-1].strftime('%Y-%m')

        for month_period in pd.period_range(start=start_month,
                                            end=end_month, freq='M'):

            # Reassign path name scope since modified when saving files
            outpath = orig_outpath
            path = orig_inpath

            month = month_period.month
            year = month_period.year

            month_df = df.loc[str(month_period), :]

            # Valid column names for parameters
            pm_list = ['PM10-81102', 'PM10-85101', 'PM2.5-88101', 'PM2.5-88502']
            gas_list = ['CO', 'O3', 'NO2', 'SO2']
            met_list = ['RHUM', 'TEMP', 'WS', 'WD']

            if any(i + '_Value' in month_df for i in pm_list):
                param_type = 'PM'

            if any(i + '_Value' in month_df for i in gas_list):
                param_type = 'Gases'

            if any(i + '_Value' in month_df for i in met_list):
                param_type = 'Met'

            param_list = list(set([param.split('_')[0] for
                                   i, param in enumerate(month_df.columns)]))
            try:
                for i in ['Site', 'Agency']:
                    param_list.remove(i)
            except ValueError as E:
                print(E)

            # Rename column headers with standard naming scheme for parameters
            for param in param_list:
                try:
                    month_df = month_df.rename(
                                 columns={param + attr: renaming[param] + attr
                                          for attr in aqs_attribs})

                    # replace naming scheme for units
                    month_df[renaming[param] + '_Unit'] = month_df[
                                renaming[param] + '_Unit'].replace('PPB',
                                                         'Parts per Billion')
                    month_df[renaming[param] + '_Unit'] = month_df[
                                renaming[param] + '_Unit'].replace('PPM',
                                                         'Parts per Million')

                    ref_method = month_df[renaming[param] + '_Method']
                    if ref_method.dropna().empty:
                        ref_name = 'Unspecified Reference'
                    else:
                        ref_name = month_df[
                                    renaming[param] + '_Method'].str.title()
                    month_df[renaming[param] + '_Method'] = ref_name

                    # Phrases that shouldn't be lower cased (FRM, FEM, etc.)
                    for oldstr, newstr in zip(replace, replace.values()):
                        month_df[renaming[param] + '_Method'] = month_df[
                                renaming[param] + '_Method'].str.replace(
                                                                oldstr, newstr)
                except KeyError:
                    continue

            month_df['Site_Lat'] = np.nan
            month_df['Site_Lon'] = np.nan
            month_df['Data_Source'] = 'AirNowTech'

            # Get the date and time the file was downloaded
            file_createtime = pathlib.Path(path).stat().st_ctime
            file_createtimef = datetime.datetime.fromtimestamp(
                                file_createtime).strftime('%Y-%m-%d %H:%M:%S')
            month_df['Data_Acquisition_Date_Time'] = file_createtimef

            param_cols = []
            for param in param_list:
                for attr in aqs_attribs:
                    param_cols.append(renaming[param] + attr)

            col_reorder = [param_cols, 'Agency', 'Site_Name', 'Site_AQS',
                           'Site_Lat', 'Site_Lon', 'Data_Source',
                           'Data_Acquisition_Date_Time']

            col_reorder_flat = flatten_list(col_reorder)
            month_df = month_df[col_reorder_flat]

            year = str(month_df.iloc[0].name.year)
            month = str(month_df.iloc[0].name.month).zfill(2)
            tdelta = month_df.iloc[1].name - month_df.iloc[0].name
            interval = tdelta.resolution_string
            filename = (interval + '_' + year + month + '_'
                        + param_type + '.csv')

            # Require at least 12 hours present within dataframe to write to
            # file (fixes issue with UTC shifted datasets with ~5 hours shifted
            # into the next month)
            if month_df.shape[0] > 11:

                # Use the site name and AQS ID to name subfolder containing
                # site data
                try:
                    site_name = month_df['Site_Name'].mode()[0]
                    site_name = site_name.replace(' ', '_')
                except KeyError:
                    site_name = 'Unspecified_Site_Name'

                try:
                    site_aqs = month_df['Site_AQS'].mode()[0]
                    site_aqs = str(site_aqs).zfill(9)
                    site_aqs = site_aqs.replace('-', '').replace(' ', '')
                except KeyError:
                    site_aqs = 'Unspecified_Site_AQS_ID'

                folder = '{0}_{1}'.format(site_name, site_aqs)

                outpath = os.path.join(outpath, folder)

                if not os.path.exists(outpath):
                    os.makedirs(outpath)

                print('../reference_data/airnowtech/processed/' + folder
                      + '/' + filename)
                month_df.to_csv(os.path.join(outpath, filename),
                                index_label='DateTime')

    return folder


def preprocess_airnowtech(file_path, project_path):
    """Wrapper module for pre-processing datasets downloaded as .csv files
    from airnowtech.org. When downloading data, the table box under "Display
    Settings" should be checked and configured to 'unpivoted' format.

    Args:
        path (str):
            Full path to downloaded AirNowTech dataset.
    Returns:
        None

    """
    ant_df = ingest_airnowtech(file_path)

    outpath = os.path.join(os.path.abspath(project_path), 'data',
                           'reference_data', 'airnowtech', 'processed')

    for df in sort_airnowtech(ant_df):
        site_folder = write_to_file(df, file_path, outpath)

    # Copy the downloaded dataset to site specific subfolder
    # if site_folder is not None:
    #     dest_inpath = os.path.abspath(
    #                         os.path.join(file_path, '..', site_folder))

    #     if not os.path.exists(dest_inpath):
    #         os.makedirs(dest_inpath)

    #     copy(file_path, dest_inpath)
