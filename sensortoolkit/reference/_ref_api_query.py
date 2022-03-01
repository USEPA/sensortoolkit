# -*- coding: utf-8 -*-
"""
This module contains methods for querying reference data APIs, including the
AirNow and Air Quality System (AQS) API services.

These services are operated by the U.S. EPA, and users should have previously
registered with either service before submitting queries (authentication tokens
are required for each service to validate query requests).

Resources
---------

- **AQS API documentation**: https://aqs.epa.gov/aqsweb/documents/data_api.html

  .. note::

    Information about registering an account with the AQS API can be found under
    the 'Sign Up' section.

- **AirNow API documentation**: https://docs.airnowapi.org/

  .. note::

    Information about registering an account with the AirNow API can be
    found at the following link (https://docs.airnowapi.org/account/request/)

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Mon May  3 12:56:38 2021
Last Updated:
  Wed Jul 14 14:27:21 2021
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
from sensortoolkit.lib_utils import flatten_list
from sensortoolkit.param import Parameter
from sensortoolkit.calculate import convert_temp


def ref_api_query(query_type=None, param=None, bdate='', edate='',
                  aqs_id=None, airnow_bbox=None, username=None, key=None,
                  path=None):
    """Wrapper function for sending an API data query to either the AQS or
    AirNow API for a specified parameter (``param``).

    Data returned by queries are parsed into pandas DataFrames and processed
    to convert header labels and column data types into a consistent standard
    for reference data sets.

    .. note::

        This method is configured to return datasets for parameters with the
        same parameter classification. The sensortoolkit Data Formatting Scheme
        (SDFS) organizes reference data into three primary
        classifications (datasets containing parameters corresponding to
        particulate matter are given the 'PM' classification, datasets
        containing gaseous parameters are assigned the 'Gases' classification,
        and datasets with meteorological parameters are assigned the 'Met'
        classification).

        If users wish to query multiple parameters in one API call, the
        parameters passed to the ref_api_query() function via the ``param``
        argument must be of the same parameter classification. For example,
        passing ``param = ['PM25', 'PM10']`` would result in a valid query
        request, as both PM25 and PM10 have the same classification (PM). If
        instead, a user passed ``param = ['PM25', 'O3']``, this would result
        in the function exiting execution as PM25 and O3 have different
        parameter classifications (PM and Gases).

        Also, please note that AQS and AirNow use different naming conventions
        for parameters (e.g., AQS uses the parameter code 88101 for PM2.5 and
        AirNow uses 'PM25'). These naming conventions are each different than
        the parameter naming convention used for this library. The
        ``param_to_api_naming`` dictionary provides a lookup dictionary for
        translating from sensortoolkit's SDFS parameter naming convention to
        each of the API services, however, the list of associated parameter API
        names is not comprehensive. Users wishing to query parameters outside
        those listed below will need to modify this method accordingly.

        For additional resources, please consult the linked documentation below
        for each API service:

            - **AQS Documentation**:
              https://aqs.epa.gov/aqsweb/documents/data_api.html
            - **AirNow Documentation**:
              https://docs.airnowapi.org/Data/docs
            - **More information about AQS Qualifier codes**:
              https://aqs.epa.gov/aqsweb/documents/codetables/qualifiers.html

    Args:
        query_type (str):
            The API service to query (either ``'AQS'`` or ``'AirNow'``).
        param (str):
            The evaluation parameter for which to return API query data.
        bdate (str):
            The overall starting date for the API query.
        edate (str):
            The overall ending date for the API query.
        aqs_id (dict):
            AQS only: AQS site ID separated into state, county, and
            site ID components.
        airnow_bbox (dict):
            AirNow only: Bounding box of latitude and longitude values.
        username (str):
            AQS only: email associated with API account
        key (str):
            Both AQS and AirNow: API authentication key code.

    Returns:
        (tuple): two-element tuple containing:

            - **query_data** (*pandas DataFrame*): Data returned by the API for
              the specified parameter and time frame. Data have been processed
              with column headers converted into standard naming scheme and
              column data types converted into a consistent formatting scheme
              for reference datasets.
            - **raw_data** (*pandas DataFrame*): An unmodified version of the
              dataset returned by the API query.

    """
    if type(param) is str:
        param_list = [param]
    elif type(param) is list:
        param_list = param
    else:
        raise TypeError('Invalid type passed to "param". Must be either type'
                        ' string or list.')

    # Create a dictionary of parameters to query. Keys are the SDFS parameter
    # name, entries include the api name associated with the SDFS name,
    # classification for parameter, etc.
    param_dict = {}
    classes = []
    for param in param_list:

        param_obj = Parameter(param)
        param_class = param_obj.classifier
        classes.append(param_class)

        # Dictionary for translating between parameter terminology used in code and
        # terminology used by AQS/AirNow. Note that this list is not comprehensive,
        # and users wishing to query parameters outside those listed below will
        # need to modify this method accordingly.
        param_to_api_naming = {'AQS': {'PM25': '88101',
                                       'PM10': '88102',
                                       'O3': '44201',
                                       'CO': '42101',
                                       'NO2': '42602',
                                       'SO2': '42401',
                                       'Temp': '62101', # or 68105?
                                       'RH': '62201',
                                       },
                               'AirNow': {'PM25': 'PM25',
                                          'PM10': 'PM10',
                                          'O3': 'OZONE',
                                          'CO': 'CO',
                                          'NO2':  'NO2',
                                          'SO2': 'SO2'
                                          },
                               }
        try:
            api_param = param_to_api_naming[query_type][param]
        except KeyError:
            print('Invalid API service name passed to query_type, pass either'
                  ' "AQS" or "AirNow"')

        param_dict[param] = {}
        param_dict[param]['parameter_object'] = param_obj
        param_dict[param]['api_name'] = api_param
        param_dict[param]['classifier'] = param_class


    if classes.count(classes[0]) != len(classes):
        sys.exit('Query parameters have mixed classifications (i.e., some '
                 'combination of PM, gases, or meteorological parameters). '
                 'Only pass parameters of the same classification (e.g., '
                 'PM25 and PM10 (PM classif.) or Temp and RH (Met classif.).')

    api_param_list = [param_dict[param]['api_name']
                          for param in param_dict]

    # Method code lookup tables
    criteria_methods_path = os.path.abspath(os.path.join(__file__,
                                  '..', 'method_codes', 'methods_criteria.csv'))
    criteria_lookup_table = pd.read_csv(criteria_methods_path)

    met_methods_path = os.path.abspath(os.path.join(__file__,
                                  '..', 'method_codes', 'methods_met.csv'))
    met_lookup_table = pd.read_csv(met_methods_path)

    # Monthly intervals to query
    month_starts, month_ends = date_range_selector(bdate, edate)
    query_months = query_periods(query_type, month_starts, month_ends)

    # Loop over monthly intervals, query API, process datasets, save .csv files
    full_query, raw_full_query = pd.DataFrame(), pd.DataFrame()
    for month in query_months:
        month_param_list = param_list.copy()
        data_period = list(query_months[month].values())
        time_of_query = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # AQS Specific query data tasks ---------------------------------------
        if query_type == 'AQS':
            print('Querying AQS API')
            print('..Parameter(s): {0}'.format(', '.join(month_param_list)))

            query_data = query_aqs(api_param_list, data_period, aqs_id,
                                   username=username, key=key)
            raw_query = query_data.copy()

            # If query did not return data, continue with next month query
            if query_data.empty:
                continue

            # Loop over query params to modify parameter-specific columns
            for param in param_dict.copy():
                api_param = param_dict[param]['api_name']
                param_class = param_dict[param]['classifier']

                param_data = query_data[[col for col in query_data.columns
                                         if col.endswith(api_param)]]
                param_cols = param_data.columns
                if param_data.dropna(how='all', axis=1).empty:
                    print(f'......{param} returned no data')
                    query_data = query_data.drop(columns=param_cols)
                    month_param_list.remove(param)
                    continue

                if param_class == 'Met':
                    lookup_table = met_lookup_table
                else:
                    lookup_table = criteria_lookup_table

                # Modify header names, drop unused columns
                query_data, idx = ingest_aqs(query_data, param, api_param,
                                             param_class, time_of_query,
                                             lookup_table)

            data = query_data
            data = data.loc[idx.index, :]
            data = data.set_index(idx)

        # AirNow Specific query data tasks ------------------------------------
        if query_type == 'AirNow':
            print('Querying AirNow API')
            print('..Parameter(s): {0}'.format(', '.join(month_param_list)))

            query_data = query_airnow(api_param_list, data_period,
                                      airnow_bbox, key=key)
            raw_query = query_data.copy()

            # If query did not return data, continue with next month query
            if query_data.empty:
                continue

            # Loop over query params to modify parameter-specific columns
            merge_data = pd.DataFrame()
            for param in param_dict:
                api_param = param_dict[param]['api_name']
                param_class = param_dict[param]['classifier']

                if api_param == 'PM25':
                    api_param = 'PM2.5'

                param_data = query_data[query_data.Param_Name==api_param]

                if param_data.empty:
                    month_param_list.remove(param)
                    print(f'......{param} returned no data')
                    continue

                # Modify header names, drop unused columns
                param_data = ingest_airnow(param_data, param,
                                                time_of_query)
                merge_data = merge_data.combine_first(param_data)

            data = merge_data
        # ---------------------------------------------------------------------

        # Cleaning up the query dataframe (Set column data types, reorder
        # columns, replace incorrectly cased phrases with correct casing

        merge_data = pd.DataFrame()
        for param in month_param_list:

            param_data_cols = [col for col in data.columns if
                               col.startswith(param)]
            site_cols =['Site_AQS', 'Site_Lat', 'Site_Lon', 'Agency',
                        'Site_Name', 'Data_Source',
                        'Data_Acquisition_Date_Time']
            param_data_cols.extend(site_cols)

            param_data = data[param_data_cols]

            if param_data[param+ '_Method_POC'].unique().shape[0] > 1:
                param_data = select_poc(param_data, param)

            # Set the data type for columns and reorder column arrangement
            param_data = modify_ref_cols(param_data, param)

            # Replace certain phrases with non-title cased phrases
            param_data = modify_ref_method_str(param_data, param)

            merge_data = merge_data.combine_first(param_data)

        process_df = merge_data.sort_index()

        process_df.index.name = 'DateTime'
        process_df = process_df.tz_localize('UTC')

        # Save monthly datasets
        save_api_dataset(process_df, raw_query, path,
                         query_type, param_class, data_period)

        full_query = full_query.append(process_df)
        raw_full_query = raw_full_query.append(raw_query)

    full_query.index.name = 'DateTime'

    bdate = pd.to_datetime(bdate).strftime('%Y-%m-%d')
    edate = pd.to_datetime(edate).strftime('%Y-%m-%d')
    return full_query.loc[bdate:edate, :]


def select_poc(df, param):
    """Ask the user for a single POC if multiple codes present in dataset.

    Args:
        df (pandas DataFrame):
            Query dataset containing data for a particular parameter. The
            dataset contains multiple POC entries (i.e., reference data from
            multiple instruments).
        param (str):
            The evaluation parameter.

    Returns:
        df (pandas DataFrame):
            Modified dataset containing measurement data for the indicated POC.

    """
    print('')
    print(f'The following parameter occurrence codes (POCs) for '
         f'{param} were found:')
    poc_dict = df[param+ '_Method_POC'].value_counts().to_dict()
    for poc in poc_dict:
        poc_sample_count = df[df[param+ '_Method_POC']==poc][param + '_Value'].count()

        print(f'..POC: {poc}, number of entries: {poc_sample_count}')

    poc_list = list(poc_dict.keys())
    valid = False
    while valid is False:
        keep_poc = input('Enter the POC for data entries you wish to keep: ')
        try:
            keep_poc = int(keep_poc)

            if keep_poc not in poc_list:
                print(f'..invalid entry, enter one of the following: {poc_list}')
            else:
                valid = True
        except ValueError:
            print('..invalid entry, enter an integer value')

    df = df[df[param+ '_Method_POC']==keep_poc]
    print('')

    return df

def modify_ref_cols(df, param):
    """Modify the data type of columns in reference data and reorder columns.

    Args:
        df (pandas DataFrame):
            Dataframe resulting from API query.
        param (str):
            The evaluation parameter.

    Returns:
        df (pandas DataFrame):
            Modified dataframe column data types correected and column ordering
            reorganized.

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
    col_reorder_flat = flatten_list(col_reorder)
    df = df[col_reorder_flat]

    return df


def modify_ref_method_str(df, param):
    """Subroutine for Ref_API_Query tha replaces various characters in data
    columns containing text, including the method name and the parameter units.

    Instrument Method names retrieved from the method code lookup table are
    specified in all upper case characters. These are converted to title cased
    characters (e.g., This Is Title Cased Text). While this imrpoves legibility
    some phrases (particularly acronyms, conjunctions, prepositions, ect.)
    should not be title cased. This function replaces specific phrases with the
    expected format.

    In addition, abbreviated unit names (used by AirNow) are converted to
    long format text to ensure consistency for reference data retreived from
    AQS, AirNow, and AirNowTech, and also to improve legibility.

    Args:
        df (pandas DataFrame):
            Dataframe resulting from API query.
        param (str):
            The evaluation parameter.

    Returns:
        df (pandas DataFrame):
            Modified dataframe with method and unit strings corrected.

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


def date_range_selector(start_date, end_date):
    """Generate two arrays (month_starts and month_ends) for which queries will
    be constructed in consecutive monthly segments.

    Args:
        start_date (str):
            Query period will begin on this date. Should be specified in a
            format accepted by pandas to_datetime module.
        end_date (str)
            Query period will end on this date. Should be specified in a
            format accepted by pandas to_datetime module.

    Returns:
        (tuple): two-element tuple containing:

            - **month_starts** (*pandas datetimeindex*): An array of monthly
              start dates.

              Example:

              .. code-block:: python

                DatetimeIndex(['2021-01-01', '2021-02-01',
                               '2021-03-01', '2021-04-01',
                               '2021-05-01', '2021-06-01'],
                               dtype='datetime64[ns]', freq='MS')

            - **month_ends** (*pandas DateTimeIndex*): An array of monthly end
              dates.

              Example:

              .. code-block:: python

                DatetimeIndex(['2021-01-31', '2021-02-28',
                               '2021-03-31', '2021-04-30',
                               '2021-05-31', '2021-06-30'],
                                dtype='datetime64[ns]', freq='M')

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


def query_periods(query_type=None, month_starts=[], month_ends=[]):
    """Generate a dictionary with consecutive monthly intervals to query where
    dates are formatted a little differently depending on the API to query.

    API date formatting:

    - AirNow API: Expects dates in format ``'YYYY-MM-DDTHH'``
        - Example: ``'2019-08-01T00'``
    - AQS API: Expects dates in format ``'YYYYMMDD'``
        - Example: ``'20190801'``

    Args:
        query_type (str):
            The name of the API to query (either 'AirNow' or 'AQS').
        month_starts (pandas datetimeindex):
            An array of monthly start dates generated by Date_Range_Selector
        month_ends (pandas datetimeindex):
            An array of monthly end dates generated by Date_Range_Selector
    Returns:
        monthly_periods (dict):
            Dictionary with monthly beginning and end dates formatted to the
            scheme expected by the API to be queried.

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
        elif query_type == 'AirNow':
            bdate = (s_yr + '-' + s_mo + '-' + '0' + s_day + 'T00')
            edate = (e_yr + '-' + e_mo + '-' + e_day + 'T23')
            monthly_periods.update({e_yr + s_mo: {'startDate': bdate,
                                                  'endDate': edate}})
        else:
            raise ValueError(f'Invalid value for query_type: {query_type}.'
                             ' Accepted values include "AQS" and "AirNow"')

    return monthly_periods


def query_aqs(param, data_period, aqs_id, username=None, key=None,
              query_type='sampleData', **kwargs):
    """Construct an AQS API query request and parse response.

    Args:
        param (str or list of str values):
            The evaluation parameter(s) for which to query data.
        data_period (list):
            List with two elements, the first is the start date and time for
            the query and the second is the end date and time for the query.
            The API is sequentially queried in monthly intervals, so the start
            date will usually be something like '20210101' and the end
            date will follow as '20210131'.
        aqs_id (str):
            The AQS site ID for the air monitoring site from which reference
            measurements will be returned by the API.
        username (str):
            AQS API username assigned to the user during API registration.
        key (str):
            User key for API authentication.
        query_type (str):
            The type of data query to request from AQS.

            - Metadata and listings:
                - ``metadata``
                - ``list``
                - ``monitors``
            - Monitor Data:
                - ``sampleData``
                - ``dailyData``
                - ``quarterlyData``
                - ``annualData``
            - Quality Assurance Assessments and Audits:
                - ``qaAnnualPerformanceEvaluations``
                - ``qaBlanks``
                - ``qaCollocatedAssessments``
                - ``qaFlowRateVerifications``
                - ``qaFlowRateAudits``
                - ``qaOnePointQcRawData``
                - ``qaPepAudits``

    **Keyword Arguments:**

    :param bool get_monitor_info:
        If True, a secondary AQS query will be submitted for adding
        reference monitor and site metadata to the dataset returned by
        this method.
    :param str sample_duration:
        The duration of recorded reference data the user wishes to retreive.

    Returns:
        data (pandas DataFrame):
            Data returned by the API for the specified query parameter and
            time period.

    """
    get_monitor_info = kwargs.get('get_monitor_info', True)
    sample_duration = kwargs.get('sample_duration', '1 HOUR')

    query_types = ['sampleData', 'monitors', 'qaBlanks',
                   'qaCollocatedAssessments', 'qaFlowRateVerifications',
                   'qaFlowRateAudits', 'qaOnePointQcRawData', 'qaPepAudits',
                   'transactionsQaAnnualPerformanceEvaluations']

    if query_type not in query_types:
        raise ValueError(f'Invalid query type: {query_type}')

    if type(param) is str:
        param_list = [param]
    elif type(param) is list:
        param_list = param
    else:
        raise TypeError('Invalid type specified for "param". Must be either '
                        'str or list.')

    if aqs_id is None:
        sys.exit('AQS Site ID missing from API Query')

    begin = (data_period[0][:4] + '-' + data_period[0][4:6]
             + '-' + data_period[0][6:])
    end = (data_period[1][:4] + '-' + data_period[1][4:6]
           + '-' + data_period[1][6:])
    print('..Query start:', begin)
    print('..Query end:', end)

    urlbase = f'https://aqs.epa.gov/data/api/{query_type}/bySite?'

    # Construct query URL
    url = urlbase + 'email=' + str(username)
    url += '&key=' + str(key)
    url += '&param=' + ','.join(param_list)
    url += '&bdate=' + str(data_period[0])
    url += '&edate=' + str(data_period[1])
    url += '&state=' + str(aqs_id["state"])
    url += '&county=' + str(aqs_id["county"])
    url += '&site=' + str(aqs_id["site"])

    # Query API for specified query type and load to json
    data = requests.get(url)
    json_data = json.loads(data.text)

    status = json_data['Header'][0]['status']
    print('..Response status: {0}'.format(status))
    if status == 'Success':
        # Convert data to pandas DataFrame
        data = pd.DataFrame(json_data['Data'])

        if query_type == 'sampleData':
            data = parse_sample_data(data, get_monitor_info,
                                     param_list=param_list,
                                     data_period=data_period,
                                     aqs_id=aqs_id, username=username, key=key,
                                     sample_duration=sample_duration)

        return data

    elif status == 'No data matched your selection':
        return pd.DataFrame()
    elif status == 'Failed':
        raise ValueError(json_data['Header'][0]['error'][0])


def parse_sample_data(sample_data, get_monitor_info, param_list, **kwargs):
    """Helper function for ingesting AQS ``'sampleData'`` queries.

    The parser searches for data matching the specified ``'sample_duration'``
    (default ``'1 HOUR'``). Metadata columns are added to the passed dataset
    indicating site and reference monitor attributes.

    Args:
        sample_data (pandas DataFrame):
            Data returned by the AQS API for a query with type ``'sampleData'``.
        get_monitor_info (bool):
            If True, a secondary AQS query will be submitted for adding
            reference monitor and site metadata to the dataset returned by
            this method.
        param_list (list):
            A list of parameters for which the user wishes to query the
            AQS API.

    **Keyword Arguments:**

    :param list data_period:
        List with two elements, the first is the start date and time for
        the query and the second is the end date and time for the query.
        The API is sequentially queried in monthly intervals, so the start
        date will usually be something like '20210101' and the end
        date will follow as '20210131'.
    :param dict aqs_id:
        The AQS site ID for the air monitoring site from which reference
        measurements will be returned by the API.
    :param str username:
        AQS API username assigned to the user during API registration.
    :param str key:
        User key for API authentication.
    :param str sample_duration:
        The duration of recorded reference data the user wishes to retreive.

    Returns:
        sample_data (pandas DataFrame):
            Modified API query dataset.

    """
    if get_monitor_info:
        kwargs['param'] = param_list
        monitorinfo = query_aqs(query_type='monitors', **kwargs)

        site_name = list(i for i in monitorinfo.local_site_name.unique())
        agency = list(i for i in monitorinfo.monitoring_agency.unique())
        site_lat = list(i for i in monitorinfo.latitude.astype(str).unique())
        site_lon = list(i for i in monitorinfo.longitude.astype(str).unique())

    # Keep 1-hour averaged sample_data by default
    duration = kwargs.get('sample_duration', '1 HOUR')
    sample_data = sample_data[sample_data.sample_duration == duration]

    sample_data.loc[:, 'Site_AQS'] = (sample_data.state_code.astype(str) + '-'
                                      + sample_data.county_code.astype(str) +
                                      '-' + sample_data.site_number.astype(str)
                                      )

    site_aqs = list(i for i in sample_data.Site_AQS.astype(str).unique())

    print('..Query site(s):')
    # Since AQS queries are site specific, should only include one site
    for name, aqs, lat, lon in zip(site_name, site_aqs,
                                   site_lat, site_lon):
        print('....Site name:', name)
        print('......AQS ID:', aqs)
        print('......Latitude:', "{0:7.4f}".format(float(lat)))
        print('......Longitude:', "{0:7.4f}".format(float(lon)))

    query_df = pd.DataFrame()
    for code in param_list:
        param_df = sample_data[
            sample_data.parameter_code == code].reset_index(drop=True)
        param_df = param_df.add_suffix('_' + code)
        query_df = query_df.combine_first(param_df)

    sample_data = query_df

    sample_data.loc[:, 'Agency'] = ','.join(agency)
    sample_data.loc[:, 'Site_Name'] = ','.join(site_name)

    return sample_data


def ingest_aqs(data, param, api_param, param_classifier,
               time_of_query, lookup_table):
    """Convert AQS query data to SDFS formatted datasets.

    Args:
        data (pandas DataFrame):
            Query data received from the AQS API.
        param (str):
            The name of the SDFS parameter for which data were queried.
        api_param (str):
            The name assigned by the API service associated with the SDFS
            parameter for which data will be queried.
        param_classifier (str):
            A term for sorting the parameter into one of three environmental
            parameter classifications, either ‘PM’ for particulate matter
            pollutants, ‘Gases’ for gaseous pollutants, or ‘Met’ for
            meteorological environmental parameters.
        time_of_query (str):
            The time of the API query, expressed as a string with datetime
            format '%Y-%m-%d %H:%M:%S'.
        lookup_table (pandas DataFrame):
            A lookup table of FRM/FEM methods associated with the queried
            parameter, including the method code for determining the name of
            the reference instrument if none given. For criteria pollutants,
            the following lookup table is used
            ('<https://aqs.epa.gov/aqsweb/documents/codetables/methods_criteria.html>'_).
            For meteorological parameters, the following lookup table is used
            (`<https://aqs.epa.gov/aqsweb/documents/codetables/methods_met.html>`_)

    Returns:
        (tuple): two-element tuple containing:

            - **data** (*pandas DataFrame*): SDFS formatted dataset.
            - **idx** (*pandas DateTimeIndex*): The datetime index (UTC) for the
              data received from the API query.

    """
    idx = pd.to_datetime(data['date_gmt_' + api_param] + ' '
                         + data['time_gmt_' + api_param])
    idx.name = 'DateTime'

    idx = idx.dropna()

    # Method code instrument look up
    if param_classifier == 'Met':
        row = lookup_table.where(
                (lookup_table['Parameter Code'] == int(api_param)) &
                (lookup_table['Method Code'] == int(data['method_code_' + api_param].unique()[0]))
                ).dropna(how='all', axis=0)
        instrument = row['Collection Description'] + row['Analysis Description']
        instrument = instrument.mode()[0]

        # replace various phrases that are not the instrument name
        remove_phrases = ['Instrumental', 'INSTRUMENTAL', 'Electronic',
                          'Barometric Sensor']
        for phrase in remove_phrases:
            instrument = instrument.replace(phrase, '')
        if instrument.replace(' ', '') == '':
            instrument = 'Unspecified_Reference'

    else:
        instrument = lookup_table.where(
            (lookup_table['Parameter Code'] == int(api_param)) &
            (lookup_table['Method Code'] == int(data['method_code_' + api_param].unique()[0]))
            )['Equivalent Method'].dropna()
        instrument = instrument.mode()[0]

    data['method_' + api_param] = instrument


    site_headers = {'Site_AQS_' + api_param: 'Site_AQS',
                     'latitude_' + api_param: 'Site_Lat',
                     'longitude_' + api_param: 'Site_Lon'}

    for site_col in site_headers:
            if site_headers[site_col] in data:
                data = data.drop(columns=[site_col])

    data = data.rename(columns={
             'Site_AQS_' + api_param: 'Site_AQS',
             'latitude_' + api_param: 'Site_Lat',
             'longitude_' + api_param: 'Site_Lon',
             'parameter_code_' + api_param: param + '_Param_Code',
             'poc_' + api_param: param + '_Method_POC',
             'sample_measurement_' + api_param: param + '_Value',
             'units_of_measure_' + api_param: param + '_Unit',
             'method_' + api_param: param + '_Method',
             'method_code_' + api_param: param + '_Method_Code',
             'qualifier_' + api_param: param + '_QAQC_Code'
             })


    api_param = str(api_param)
    data = data.drop(columns=[
        'state_code_' + api_param,  # rolled into Site_AQS column
        'county_code_' + api_param,  # rolled into Site_AQS column
        'site_number_' + api_param,  # rolled into Site_AQS column
        'datum_' + api_param,  # geodetic reference system [METADATA]
        'parameter_' + api_param,  # parameter code, redundant
        'date_local_' + api_param,  # local date
        'time_local_' + api_param,  # local time
        'date_gmt_' + api_param,  # UTC date (assigned as index)
        'time_gmt_' + api_param,  # UTC date (assigned as index)
        'units_of_measure_code_' + api_param,  # code for parameter units
        'sample_duration_' + api_param,  # The duration for samples
        'sample_duration_code_' + api_param,  # code assigned to duration
        'sample_frequency_' + api_param,  # reporting interval for samples
        'detection_limit_' + api_param,
        'uncertainty_' + api_param,
        'method_type_' + api_param,
        'state_' + api_param,
        'county_' + api_param,
        'date_of_last_change_' + api_param,
        'cbsa_code_' + api_param
        ])

    if param == 'O3':
        # Convert to concentrations to ppb
        data[param + '_Value'] = 1000*data[
                                        param + '_Value']
        data[param + '_Unit'] = data[
            param + '_Unit'].replace('PPB', 'Parts per Billion')

    if param == 'Temp' and data[param + '_Unit'].unique()[0] == 'Degrees Fahrenheit':
        # Convert to concentrations to ppb
        data[param + '_Value'] = convert_temp(data[param + '_Value'],
                                              from_unit='F', to_unit='C')
        data[param + '_Unit'] = 'Degrees Celsius'

    data['Data_Source'] = 'AQS API'
    data['Data_Acquisition_Date_Time'] = time_of_query

    return data, idx


def query_airnow(param, data_period, bbox, key=None):
    """Construct an AirNow API query request and parse response.

    Args:
        param (str):
            The evaluation parameter for which to query data.
        data_period (list):
            List with two elements, the first is the start date and time for
            the query and the second is the end date and time for the query.
            The API is sequentially queried in monthly intervals, so the start
            date will usually be something like '2021-01-01T00' and the end
            date will follow as '2021-01-31T23'.
        bbox (dict):
            Bounding box of latitude andlongitude values for AirNow API
            queries.
        key (str):
            User key for API authentication.

    Returns:
        data (pandas DataFrame):
            Data returned by the API for the specified query parameter and
            time period.
    """
    if type(param) is str:
        param_list = [param]
    elif type(param) is list:
        param_list = param
    else:
        raise TypeError('Invalid type specified for "param". Must be either '
                        'str or list.')

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
    url += '&parameters=' + ','.join(param_list)
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
                       names=['Site_Lat', 'Site_Lon', 'DateTime',
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


def ingest_airnow(data, param, time_of_query):
    """Convert AirNow query data to SDFS formatted datasets.

    Args:
        data (pandas DataFrame):
            Query data received from the AirNow API.
        param (str):
            The name of the SDFS parameter for which data were queried.
        time_of_query (str):
            The time of the API query, expressed as a string with datetime
            format '%Y-%m-%d %H:%M:%S'.

    Returns:
        data (pandas DataFrame): SDFS formatted dataset.

    """
    idx = pd.to_datetime(data.DateTime)

    rename = {col: col.replace('Param', param)
              for col in data.columns if col.startswith('Param')}
    data = data.rename(columns=rename)

    data = data.drop(columns=['DateTime',
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

    data = data.set_index(idx)

    return data


def save_api_dataset(process_df, raw_df, path, query_type, param_class,
                     data_period):
    """Save processed datasets at regular monthly intervals.

    Args:
        process_df (pandas DataFrame):
            An SDFS formatted dataset for query data returned by the API
            service.
        raw_df (pandas DataFrame):
            A dataset containing unmodified data returned by the API service.
        path (str):
            The project path where the ``/data/reference_data`` subdirectory
            is housed. Data are saved at the refrence data subdirectory
            structure within this parent directory.
        query_type (str):
            The name of the API service used to retreieve query data.
        param_class (sstr):
            A term for sorting the parameter into one of three environmental
            parameter classifications, either ‘PM’ for particulate matter
            pollutants, ‘Gases’ for gaseous pollutants, or ‘Met’ for
            meteorological environmental parameters.
        data_period (list):
            A list of length 2, containing the start date for the monthly
            period (index position 0), and end date (index position 1). Each
            element is a string with date format 'YYYYMMDD'.

    Returns:
        None.

    """
    # Use the site name and AQS ID to name subfolder containing
    # site data
    try:
        site_name = process_df['Site_Name'].mode()[0]
        site_list = site_name.title().split(None)
        site_name = '_'.join(site_list)
    except KeyError:
        site_name = 'Unspecified_Site_Name'

    try:
        site_aqs = process_df['Site_AQS'].mode()[0]
        site_aqs = site_aqs.replace('-', '').replace(' ', '')
    except KeyError:
        site_aqs = 'Unspecified_Site_ID'

    folder = '{0}_{1}'.format(site_name, site_aqs)

    data_path = os.path.join(path,
                             'data',
                             'reference_data',
                             query_type.lower())

    process_path = os.path.join(data_path, 'processed', folder)
    raw_path = os.path.join(data_path, 'raw', folder)

    if not os.path.exists(process_path):
        os.makedirs(process_path)
    if not os.path.exists(raw_path):
        os.makedirs(raw_path)

    year_month = pd.to_datetime(data_period[0]).strftime('%Y%m')
    filename = f'H_{year_month}_{param_class}.csv'

    process_df.to_csv(os.path.join(process_path, filename))
    raw_df.to_csv(os.path.join(raw_path, filename))
