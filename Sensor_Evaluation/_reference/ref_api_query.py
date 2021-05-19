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
  Mon May  3 12:56:38 2021
Last Updated:
  Wed May 12  9:34:00 2021
"""
import requests
import json
import pandas as pd
from pandas.tseries.offsets import MonthBegin
from pandas.tseries.offsets import MonthEnd
from io import StringIO
import datetime
import pathlib
import os
import sys
import numpy as np
from Sensor_Evaluation._reference.import_airnowtech import Flatten


def Ref_API_Query(query_type=None, param=None, bdate='', edate='',
                  aqs_id=None, airnow_bbox=None, username=None, key=None):
    """
    Send an API data query to the specified service (query_type: 'AQS' or
    'AirNow') for a selected time period (e.g., bdate: '2020-01-01' and
    edate: '2021-12-31' to query data for all of 2020). The label for the
    data parameter queried 'param' will be different for AQS and AirNow. Please
    consult the linked documentation for each of these APIs for additional
    resources.

    AQS Documentation:
        https://aqs.epa.gov/aqsweb/documents/data_api.html
    AirNow Documentation:
        https://docs.airnowapi.org/Data/docs

    More information about AQS Qualifier codes:
        https://aqs.epa.gov/aqsweb/documents/codetables/qualifiers.html
    """
    # Dictionary for translating between parameter terminology used in code and
    # terminology used by AQS/AirNow.
    param_to_api_naming = {'AQS': {'PM25': '88101',
                                   'PM10': '88102',
                                   'O3': '44201',
                                   'CO': '42101',
                                   'NO2': '42602',
                                   'SO2': '42401'},
                           'AirNow': {'PM25': 'pm25',
                                      'PM10': 'pm10',
                                      'O3': 'O3',
                                      'CO': 'co',
                                      'NO2': 'no2',
                                      'SO2': 'so2'},
                           }

    api_param = param_to_api_naming[query_type][param]

    # Caution, Windows only
    method_path = pathlib.PureWindowsPath(
                        os.path.abspath(os.path.join(__file__, '../../..')))
    method_path = (method_path.as_posix() +
                   '/Data and Figures/reference_data/'
                   'method_codes//methods_criteria.csv')

    # Method code lookup dataframe
    method_df = pd.read_csv(method_path)

    month_starts, month_ends = Date_Range_Selector(bdate, edate)
    query_months = Query_Periods(query_type, month_starts, month_ends)

    query_data, raw_data = pd.DataFrame(), pd.DataFrame()
    for month in query_months:
        data_period = list(query_months[month].values())
        time_of_query = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        #  --------------------------------------------------------------------
        #                   | AQS Specific query data tasks |
        #  --------------------------------------------------------------------
        if query_type == 'AQS':
            data = AQS_Query(api_param, data_period, aqs_id, username=username,
                             key=key)
            raw_copy = data.copy()
            if data.empty is False:
                idx = pd.to_datetime(data.date_gmt + ' ' + data.time_gmt)

                # Method code instrument look up
                instrument = method_df.where(
                    (method_df['Parameter Code'] == int(api_param)) &
                    (method_df['Method Code'] == int(
                            data['method_code'].unique()[0]))
                    )['Equivalent Method'].dropna()

                instrument = instrument.values[0].title()
                data['method'] = instrument

                data = data.rename(columns={
                         'latitude': 'Site_Lat',
                         'longitude': 'Site_Lon',
                         'parameter_code': param + '_Param_Code',
                         'poc': param + '_Method_POC',
                         'sample_measurement': param + '_Value',
                         'units_of_measure': param + '_Unit',
                         'method': param + '_Method',
                         'method_code': param + '_Method_Code',
                         'qualifier': param + '_QAQC_Code'
                         })

                data = data.drop(
                        columns=['state_code', 'county_code', 'site_number',
                                 'datum', 'parameter', 'date_local',
                                 'time_local', 'date_gmt', 'time_gmt',
                                 'units_of_measure_code', 'sample_duration',
                                 'sample_duration_code', 'sample_frequency',
                                 'detection_limit', 'uncertainty',
                                 'method_type', 'state', 'county',
                                 'date_of_last_change', 'cbsa_code'])

                if param == 'O3':
                    # Convert to concentrations to ppb
                    data[param + '_Value'] = 1000*data[
                                                    param + '_Value']
                    data[param + '_Unit'] = data[
                        param + '_Unit'].replace('PPB', 'Parts per Billion')

                data['Data_Source'] = 'AQS API'
                data['Data_Acquisition_Date_Time'] = time_of_query

        #  --------------------------------------------------------------------
        #                 | AirNow Specific query data tasks |
        #  --------------------------------------------------------------------
        if query_type == 'AirNow':
            data = AirNow_Query(api_param, data_period, airnow_bbox, key=key)
            raw_copy = data.copy()
            if data.empty is False:
                idx = pd.to_datetime(data.DateTime_UTC)

                rename = {col: col.replace('Param', param)
                          for col in data.columns if col.startswith('Param')}
                data = data.rename(columns=rename)

                data = data.drop(columns=['DateTime_UTC',
                                          param + '_Name',
                                          'Site_Full_AQS'])

                # Note that AirNow doesn't report the reference monitor method
                # so labeling as unknown
                data['Data_Source'] = 'AirNow API'
                data['Data_Acquisition_Date_Time'] = time_of_query
                data[param + '_QAQC_Code'] = np.nan
                data[param + '_Param_Code'] = np.nan
                data[param + '_Method'] = 'Unknown Reference'
                data[param + '_Method_Code'] = np.nan
                data[param + '_Method_POC'] = np.nan

                # Identify periods where data are flagged (conc = -999). Set
                # these hours to NaN and associate QAQC flag with hour
                flag_val = data[param+'_Value'].where(
                                                data[param+'_Value'] == -999)
                flag_idx = flag_val.dropna().index
                data.loc[flag_idx, param + '_QAQC_Code'] = '-999'
                data.loc[flag_idx, param + '_Value'] = np.nan

        # Cleaning up the query dataframe (Set column data types, reorder
        # columns, replace incorrectly cased phrases with correct casing
        if data.empty is False:
            data = data.set_index(idx)

            # Set the data type for columns and reorder column arrangement
            data = Modify_Ref_Cols(data, param)

            # Replace certain phrases with non-title cased phrases
            data = Modify_Ref_Method_Str(data, param)

            data = data.sort_index()

            query_data = query_data.append(data)
            raw_data = raw_data.append(raw_copy)

    query_data.index.name = 'DateTime_UTC'

    return query_data.loc[bdate:edate, :], raw_data


def Modify_Ref_Cols(df, param):
    """Modify the data type of columns in reference data and reorder columns.
    """

    # Column header suffixes for parameter data
    param_attribs = ['_Value', '_Unit', '_QAQC_Code', '_Param_Code',
                     '_Method', '_Method_Code', '_Method_POC']

    # Column header suffixes for site metadata (site name, location, etc.)
    meta_attribs = ['Agency', 'Site_Name', 'Site_AQS',
                    'Site_Lat', 'Site_Lon', 'Data_Source',
                    'Data_Acquisition_Date_Time']

    # Data types for parameter columns
    param_type = {'_Value': float,
                  '_Unit': object,
                  '_QAQC_Code': object,
                  '_Param_Code': float,
                  '_Method': object,
                  '_Method_Code': float,
                  '_Method_POC': float}

    # Data types for metadata columns
    meta_type = {'Agency': object,
                 'Site_Name': object,
                 'Site_AQS': str,
                 'Site_Lat': float,
                 'Site_Lon': float,
                 'Data_Source': object,
                 'Data_Acquisition_Date_Time': object}

    # Sort parameter data columns
    param_cols = []
    for attr in param_attribs:
        param_cols.append(param + attr)
        param_type[param + attr] = param_type.pop(attr)

    # Set the data type of columns
    col_type = {**param_type, **meta_type}
    df = df.astype(col_type)

    # reorder columns
    col_reorder = [param_cols, meta_attribs]
    col_reorder_flat = Flatten(col_reorder)
    df = df[col_reorder_flat]

    return df


def Modify_Ref_Method_Str(df, param):
    """Instrument Method names retrieved from the method code lookup table are
    specified in all upper case characters. These are converted to title cased
    characters (e.g., This Is Title Cased Text). While this imrpoves legibility
    some phrases (particularly acronyms, conjunctions, prepositions, ect.)
    should not be title cased. This function replaces specific phrases with the
    expected format.

    In addition, abbreviated unit names (used by AirNow) are converted to
    long format text to ensure consistency for reference data retreived from
    AQS, AirNow, and AirNowTech, and also to improve legibility.
    """
    # Lookup dictionary of phrases that shouldn't be title cased
    replace = {'Method': {'Api': 'API',
                          'Frm': 'FRM',
                          'Fem': 'FEM',
                          'Lpm': 'LPM',
                          ' At ': ' at ',
                          'Bam': 'BAM',
                          'Pm': 'PM',
                          'Vscc': 'VSCC',
                          'Te': 'TE',
                          ' Or ': ' or ',
                          'W/': 'w/',
                          ' And ': ' and '},
               'Unit': {'PPB': 'Parts per billion',
                        'PPM': 'Parts per million',
                        'UG/M3': 'Micrograms/cubic meter'}
               }

    for attrib in replace:
        for oldstr, newstr in zip(replace[attrib], replace[attrib].values()):
            col = param + '_' + attrib
            df[col] = df[col].astype(str).str.replace(oldstr, newstr)

    return df


def Date_Range_Selector(start_date, end_date):
    """Generate two arrays (month_starts and month_ends) for which queries will
    be constructed in consecutive monthly segments.
    """

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # If start day after first day of start month, set to first day of month
    if start_date.day > (pd.to_datetime(start_date) - MonthBegin(1)).day:
        start_date = pd.to_datetime(start_date) - MonthBegin(1)

    # If end date day before last day of end month, set to first day of month
    if end_date.day < (pd.to_datetime(end_date) + MonthEnd(1)).day:
        end_date = pd.to_datetime(end_date) + MonthEnd(1)

    # Generate series for dates at beginning and end of months to query
    month_starts = pd.date_range(start=start_date, end=end_date, freq='MS',
                                 normalize=True)
    month_ends = pd.date_range(start=start_date, end=end_date, freq='M',
                               normalize=True)

    return month_starts, month_ends


def Query_Periods(query_type=None, month_starts=[], month_ends=[]):
    """Generate a dictionary with consecutive monthly intervals to query where
    dates are formatted a little differently depending on the API to query.
    """
    monthly_periods = {}
    for start, end in zip(month_starts, month_ends):

        month_name = start.month_name()
        year_name = str(start.year)[-2:]

        s_yr = str(start.year)
        s_mo = str(start.month).zfill(2)
        s_day = str(start.day)

        e_yr = str(end.year)
        e_mo = str(end.month).zfill(2)
        e_day = str(end.day)

        if query_type == 'AQS':
            bdate = s_yr + s_mo + '0' + s_day
            edate = e_yr + e_mo + e_day
            monthly_periods.update({month_name + year_name: {'bdate': bdate,
                                                             'edate': edate}})
        if query_type == 'AirNow':
            bdate = (s_yr + '-' + s_mo + '-' + '0' + s_day + 'T00')
            edate = (e_yr + '-' + e_mo + '-' + e_day + 'T23')
            monthly_periods.update({e_yr + s_mo: {'startDate': bdate,
                                                  'endDate': edate}})

    return monthly_periods


def AQS_Query(param, data_period, aqs_id, username=None, key=None):
    """Construct an AQS API query request and parse response.
    """
    if aqs_id is None:
        sys.exit('AQS Site ID missing from API Query')

    print('Querying AQS API')
    begin = (data_period[0][:4] + '-' + data_period[0][4:6]
             + '-' + data_period[0][6:])
    end = (data_period[1][:4] + '-' + data_period[1][4:6]
           + '-' + data_period[1][6:])
    print('..Query start:', begin)
    print('..Query end:', end)

    # API Items
    urlbase = 'https://aqs.epa.gov/data/api/sampleData/bySite?'

    # Construct query URL
    url = urlbase + 'email=' + str(username)
    url += '&key=' + str(key)
    url += '&param=' + str(param)
    url += '&bdate=' + str(data_period[0])
    url += '&edate=' + str(data_period[1])
    url += '&state=' + str(aqs_id["state"])
    url += '&county=' + str(aqs_id["county"])
    url += '&site=' + str(aqs_id["site"])

    # Get query response (two queries: first for reference data, second for
    # site metadata)

    # Query reference concentration data
    ref_data = requests.get(url)

    # Query site information (site name, operating agency, etc.)
    site_data = requests.get(url.replace('sampleData', 'monitors'))
    site_json = json.loads(site_data.text)
    site_data = pd.DataFrame(site_json['Data'])

    # Load data to json module, pandas dataframe
    ref_data_json = json.loads(ref_data.text)
    ref_data = pd.DataFrame(ref_data_json['Data'])

    ref_data['Site_AQS'] = (ref_data.state_code.astype(str) + '-' +
                            ref_data.county_code.astype(str) + '-' +
                            ref_data.site_number.astype(str))

    status = ref_data_json['Header'][0]['status']

    if status == 'Success':
        site_name = list(i for i in site_data.local_site_name.unique())
        agency = list(i for i in site_data.monitoring_agency.unique())
        site_aqs = list(i for i in ref_data.Site_AQS.astype(str).unique())
        site_lat = list(i for i in site_data.latitude.astype(str).unique())
        site_lon = list(i for i in site_data.longitude.astype(str).unique())

        print('..Query site(s):')
        # Since AQS queries are site specific, should only include one site
        for name, aqs, lat, lon in zip(site_name, site_aqs,
                                       site_lat, site_lon):
            print('....Site name:', name)
            print('......AQS ID:', aqs)
            print('......Latitude:', "{0:7.4f}".format(float(lat)))
            print('......Longitude:', "{0:7.4f}".format(float(lon)))

    print('..Query Status:', status)

    ref_data['Agency'] = ','.join(agency)
    ref_data['Site_Name'] = ','.join(site_name)

    return ref_data


def AirNow_Query(param, data_period, bbox, key=None):
    """Construct an AirNow API query request and parse response.
    """
    print('Querying AirNow API')

    begin = data_period[0][:-3]
    end = data_period[1][:-3]
    print('..Query start:', begin)
    print('..Query end:', end)

    # API Items
    urlbase = "http://www.airnowapi.org/aq/data/?"
    dataType = "C"
    dataformat = "text/csv"
    verbose = "1"                    # bool
    nowcastonly = "0"                # bool
    rawconc = "1"                    # bool

    # Construct query URL
    url = urlbase + 'startdate=' + str(data_period[0])
    url += '&enddate=' + str(data_period[1])
    url += '&parameters=' + str(param)
    url += '&bbox=' + str(bbox["minLong"]) + ','
    url += str(bbox["minLat"]) + ','
    url += str(bbox["maxLong"]) + ','
    url += str(bbox["maxLat"])
    url += '&datatype=' + str(dataType)
    url += '&format=' + str(dataformat)
    url += '&verbose=' + str(verbose)
    url += '&nowcastonly=' + str(nowcastonly)
    url += '&includerawconcentrations=' + str(rawconc)
    url += '&api_key=' + str(key)

    # Get query response
    data = requests.get(url)
    fmt_query_data = StringIO(data.text)

    data = pd.read_csv(fmt_query_data, sep=',',
                       names=['Site_Lat', 'Site_Lon', 'DateTime_UTC',
                              'Param_Name', 'Param_NowCast_Value',
                              'Param_Unit', 'Param_Value', 'Site_Name',
                              'Agency', 'Site_AQS', 'Site_Full_AQS'])
    if data.empty:
        status = 'Failed'
    else:
        status = 'Success'

        data['Site_AQS'] = data['Site_AQS'].astype(str)

        state_id = data['Site_AQS'].str.slice(0, 2)
        county_id = data['Site_AQS'].str.slice(2, 5)
        site_id = data['Site_AQS'].str.slice(5, 9)

        data['Site_AQS'] = (state_id + '-' + county_id + '-' + site_id)

        site_name = list(i for i in data.Site_Name.unique())
        site_aqs = list(i for i in data.Site_AQS.astype(str).unique())
        site_lat = list(i for i in data.Site_Lat.astype(str).unique())
        site_lon = list(i for i in data.Site_Lon.astype(str).unique())

        print('..Query site(s):')
        for name, aqs, lat, lon in zip(site_name, site_aqs,
                                       site_lat, site_lon):
            print('....Site name:', name)
            print('......AQS ID:', aqs)
            print('......Latitude:', "{0:7.4f}".format(float(lat)))
            print('......Longitude:', "{0:7.4f}".format(float(lon)))

        # Print warning if data from multiple sites are returned
        if any(len(lst) > 1 for lst in [site_name, site_aqs,
                                        site_lat, site_lon]):
            print('..Warning: Query returned data from multiple sites.',
                  '\n..Site selection can be narrowed by reducing the '
                  'bounding box size.')

    print('..Query Status:', status)

    return data


def Save_Query(query_tuple):
    """Save API query datasets to file
    """
    processed_df, raw_df = query_tuple
    api_src = processed_df['Data_Source'].unique()[0].replace(' API', '')
    print('Writing', api_src, 'query dataframes to csv files')

    begin = 'B' + processed_df.index.min().strftime('%y%m%d')
    end = 'E' + processed_df.index.max().strftime('%y%m%d')
    site_id = processed_df['Site_AQS'].unique()[0]
    params = [col.replace('_Value', '') for col in
              processed_df.columns if col.endswith('_Value')]
    param_str = '_'.join(param for param in params)

    process_filename = '_'.join([api_src, site_id,
                                 param_str, begin, end]) + '.csv'
    raw_filename = '_'.join([api_src, 'raw', site_id,
                             param_str, begin, end]) + '.csv'

    # Caution, Windows only
    outpath = pathlib.PureWindowsPath(
                        os.path.abspath(os.path.join(__file__, '../../..')))
    outpath = (outpath.as_posix() + '/Data and Figures/reference_data/' +
               api_src.lower())

    print('../reference_data/' + api_src.lower() + '/processed/'
          + process_filename)
    processed_df.to_csv(outpath + '/processed/' + process_filename,
                        index_label='DateTime_UTC')

    print('../reference_data/' + api_src.lower() + '/raw_api_datasets/'
          + raw_filename)
    raw_df.to_csv(outpath + '/raw_api_datasets/' + raw_filename,
                  index_label='DateTime_UTC')

    return processed_df
