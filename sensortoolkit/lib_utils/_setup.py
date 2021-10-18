# -*- coding: utf-8 -*-
"""
Description.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Mon Jul 19 08:25:55 2021
Last Updated:
  Mon Jul 19 08:25:55 2021
"""
import os
import sys
from textwrap import wrap
import json
import pandas as pd
import pprint
import pytz
from pytz.exceptions import UnknownTimeZoneError
from sensortoolkit.lib_utils import flatten_list, validate_entry, enter_continue, copy_datasets
from sensortoolkit.param import Parameter
from sensortoolkit.reference import preprocess_airnowtech
from sensortoolkit.ingest import standard_ingest


class _Setup:
    """Setup methods for Sensor and Reference data ingestion configuration.

    Arguments:
        path
    """

    params = ['PM1', 'PM25', 'PM10', 'O3', 'NO2', 'NO', 'NOx',
              'SO2', 'SOx', 'CO', 'CO2', 'Temp', 'RH', 'Press',
              'DP', 'WS', 'WD']
    data_types = ['.csv', '.txt', '.xlsx']
    __banner_w__ = 79
    pp = pprint.PrettyPrinter()
    #pd.set_option('max_colwidth', __banner_w__)

    def __init__(self, path=None):
        if path is None:
            raise AttributeError('Path for working directory not specified')

        self.path = path
        self.data_rel_path = None
        self.data_type = None
        self.file_extension = None
        self.header_names = None
        self.header_iloc = None
        self.data_row_idx = None
        self.sdfs_header_names = []
        self.all_col_headers = []
        self.timestamp_col_headers = []
        self.col_headers = {}

    def config(self):
        # Indicate the dataset file type (.csv, .txt, .xlsx)
        self.setDataExtension()

        # Ask user for either directory or files to load in, parse datasets
        # and could make call to copy datasets to transfer to data and figures
        self.setDataRelPath()
        self.selectDataSets()
        self.copyDataSets()

        self.setHeaderIndex()

        if self.header_iloc is None:
            # Manually specify column names if none provided
            self.setColumnHeaders()
        # otherwise, specify column headers in parsedatasets, infer header at
        # iloc position
        self.parseDataSets()
        self.setTimeHeaders()
        self.setParamHeaders()
        self.setDateTimeFormat()
        self.setTimeZone()

    def printSelectionBanner(self, select_type, options=[], notes=[]):

        self.end_str = '..press X to end adding entries'
        self.del_str = '..press D to delete the previous entry'
        self.skip_str = '..press enter to skip columns that will be dropped'

        banner_c = int(self.__banner_w__ / 2)
        select_len = len(select_type)
        select_start = banner_c - int(select_len / 2) - 1
        n_left, n_right = select_start, select_start

        if select_len % 2 != 0:
            n_right -= 1

        flier = (n_left*'=' + ' ' + select_type + ' ' + n_right*'=')
        print(flier)

        if options != []:
            print('Options\n-------')
            options = ['\n'.join(wrap(str(l),
                                 width=self.__banner_w__)) for l in options]
            for line in options:
                print(line)

        if notes != []:
            if options!= []:
                print('')
            print('Notes\n-----')
            notes = ['\n'.join(wrap(str(l),
                                 width=self.__banner_w__)) for l in notes]
            for line in notes:
                print(line)

        print(len(flier)*'=')


    def add_param_attrib(self, param, attrib_key, attrib_val):
        """Assign parameter header attribute

        Search through the column index entries, if the parameter name within the
        column index subdictionary, add the passed attribute key and value.

        Args:
            data (TYPE): self.col_headers dictionary.
            param (TYPE): DESCRIPTION.
            attrib_key (TYPE): DESCRIPTION.
            attrib_val (TYPE): DESCRIPTION.

        Returns:
            data (TYPE): DESCRIPTION.

        """
        for col_idx in self.col_headers.keys():
            if param in self.col_headers[col_idx]:
                self.col_headers[col_idx][param][attrib_key] = attrib_val


    def setDataExtension(self):
        self.printSelectionBanner('Select Data Type',
                                  options=[self.data_types])

        valid = False
        while valid is False:
            console_text = (f'Enter the {self.data_type} data type from the '
                            'list of supported data types: ')
            console_text = '\n'.join(wrap(console_text,
                                          width=self.__banner_w__))
            val = input(console_text)
            if str(val) not in self.data_types:
                print('..invalid entry, please enter one of the listed data '
                      'types')
            else:
                self.file_extension = val
                print('')
                print('Selected data type:', self.file_extension)
                confirm = validate_entry()
                if confirm == 'y':
                    valid = True
            print('')

    def selectDataSets(self):
        select_options = ['directory', 'recursive directory', 'files']
        self.printSelectionBanner('Select Data Files or Directory',
                                      options=[select_options])

        valid = False
        while valid is False:
            console_text = (f'Enter how to select {self.data_type} datasets '
                            f'from the list of options above: ')
            console_text = '\n'.join(wrap(console_text,
                                          width=self.__banner_w__))
            val = input(console_text)
            if str(val) not in select_options:
                print('..invalid entry, please enter one of the options '
                      'listed above')
            else:
                self._dataset_selection = val
                print('')
                print('Select data sets by', self._dataset_selection)
                confirm = validate_entry()
                if confirm == 'y':
                    valid = True
            print('')

    def copyDataSets(self):
        self.printSelectionBanner('Copy Data Files to the Project Directory',
                                  options=[])
        print('')
        self.file_list = copy_datasets(data_type=self.data_type,
                                       path=self.path,
                                       select=self._dataset_selection,
                                       file_extension=self.file_extension,
                                       return_filenames=True,
                                       **self.dataset_kwargs)
        enter_continue()

    def loadDataFile(self, file, **kwargs):

        load_table = kwargs.get('load_table', False)
        if load_table:
            df = pd.read_table(file,
                               nrows=kwargs.get('nrows', 1),
                               header=None)

        elif self.file_extension == '.csv' or self.file_extension == '.txt':
            df = pd.read_csv(file, header=self.header_iloc,
                             names=self.header_names,
                             nrows=kwargs.get('nrows', 1),
                             skiprows=self.data_row_idx,
                             on_bad_lines='skip'
                             )
        elif self.file_extension == '.xlsx':
            df = pd.read_excel(file, header=self.header_iloc,
                               names=self.header_names,
                               nrows=kwargs.get('nrows', 1),
                               skiprows=self.data_row_idx
                               )
        else:
            raise TypeError('Invalid data type')

        return df

    def setDataRelPath(self):
        self.data_rel_path = f'/Data and Figures/{self.data_type}_data/'
        if self.data_type == 'sensor':
            self.data_rel_path += f'{self.name}/raw_data'
        if self.data_type == 'reference':
            self.data_rel_path += f'{self.dataset_kwargs["ref_data_source"]}/raw/{self.ref_data_subfolder}/'

    def parseDataSets(self, print_banner=True):
        if print_banner:
            self.printSelectionBanner('Parsing Datasets',
                                      options=[])
            print('')

        # Load data files and populate a dictionary of unique headers that occur.
        # Top level is ordered by the row index, so if some files have different headers,
        # there will be multiple entries within the particular row index key.

        print(f'Parsing datasets at "..{self.data_rel_path}"')

        for i, file in enumerate(self.file_list):
            df = self.loadDataFile(file)
            file_col_list = list(df.columns)

            for j, col in enumerate(file_col_list):
                if 'col_idx_' + str(j) not in self.col_headers:
                    self.col_headers['col_idx_' + str(j)] = {}

                if col not in self.col_headers['col_idx_' + str(j)]:
                    self.col_headers['col_idx_' + str(j)][col] = {"sdfs_param": None,
                                                             "in_file_list_idx": [i]}
                else:
                    self.col_headers['col_idx_' + str(j)][col]["in_file_list_idx"].append(i)

        # Create a nested list of unique column names
        col_list = [list(self.col_headers[key].keys()) for key in
                    list(self.col_headers.keys())]
        self.all_col_headers = flatten_list(col_list)

        for i, cols in enumerate(col_list):
            print('..Header(s) at column index {0:d}: {1}'.format(i, cols))

        enter_continue()

    def setHeaderIndex(self, print_banner=True):
        if print_banner:
            self.printSelectionBanner('Column Header Index',
                                      options=['..type "None" if no header '
                                               'columns in recorded sensor '
                                               'dataset'])

        # Load the first dataset (display 10 rows to user)
        #self.findDataFiles()
        if self.file_list == []:
            data_path = os.path.normpath(os.path.join(self.path,
                                                      self.data_ref_path))
            sys.exit('No data files found with type'
                     ' {0} at {1}'.format(self.file_extension, data_path))

        df = self.loadDataFile(self.file_list[0],
                               nrows=10,
                               load_table=True)

        filename = self.file_list[0].split('/')[-1]
        print('')
        print('The first ten unformatted rows of {0} are displayed'
              ' below:'.format(filename))
        print(df.head(n=10))

        valid = False
        while valid is False:
            self.header_iloc = input('Enter the row index number for column '
                                     'headers: ')
            try:
                self.header_iloc = int(self.header_iloc)
            except ValueError:
                self.header_iloc = self.header_iloc

            if (self.header_iloc != 'None' and
               type(self.header_iloc) is not int):
                print('..invalid entry, enter either an integer or "None"')
            elif self.header_iloc == 'None':
                self.header_iloc = None
                valid = True
            elif type(self.header_iloc) is int:
                if self.header_iloc < 0:
                    print('..invalid entry, enter either an integer or "None"')
                else:
                    valid = True

        print('')
        print('Header row index:', str(self.header_iloc))
        confirm = validate_entry()
        if confirm == 'n':
            self.setHeaderIndex(print_banner=False)
        print('')

    def setColumnHeaders(self, print_banner=True):
        if print_banner:
            self.printSelectionBanner('Manually Set Column Headers',
                                      options=[self.end_str])
        self.header_names = []
        edit = True
        col_n = 1
        while edit:
            confirm = 'n'
            while confirm == 'n':
                col_name = input("Enter Column Header #{0}: ".format(str(col_n)))
                if col_name == 'X':
                    edit = False
                    break

                confirm = validate_entry()

            if edit is False:
                break
            else:
                self.header_names.append(col_name)
                col_n += 1

        print('')
        print('Column Headers:', self.header_names)
        enter_continue()

        confirm = 'n'
        while confirm == 'n':
            self.data_row_idx = input("Enter the row index that data begin "
                                      "on: ")
            try:
                self.data_row_idx = int(self.data_row_idx)
                if self.data_row_idx < 0:
                    raise ValueError
                confirm = validate_entry()
            except ValueError:
                print('..invalid entry, enter an integer >= 0')

        print('')

    def setTimeHeaders(self, print_banner=True):
        if print_banner:
            self.printSelectionBanner('Specify Timestamp columns',
                                      options=[self.end_str, self.del_str])
        # Create a list of time-like columns, update the col_headers list with the
        # DateTime type corresponding to the specified header name
        # Enter in the time like columns [LOOP]
        end = False
        i = 1
        while end is False:
            val = input("Enter Timestamp column name #{0}: ".format(str(i)))

            if val == 'X':
                end = True
            elif val == 'D':
                try:
                    self.timestamp_col_headers.pop(i-2)
                    print('..removing timestamp column #{0} from '
                          'list'.format(str(i-1)))
                    i -= 2
                    print('..updated timestamp column headers list: ')
                    print(' ', self.timestamp_col_headers)
                except IndexError:
                    print('Empty list, no entries to delete')
                    continue

            elif val in self.all_col_headers:
                # TODO: depreciate?
                self.timestamp_col_headers.append(val)

                self.add_param_attrib(val,
                                    attrib_key='header_class',
                                    attrib_val='datetime')

                self.add_param_attrib(val,
                                    attrib_key='sdfs_param',
                                    attrib_val='DateTime')

                # # Get a list of the row index locations where the column header name is
                # header_loc = [row for row in self.col_headers if val in
                #               self.col_headers[row].keys()]
                # for key in header_loc:
                #     self.col_headers[key][val]['SDFS_param'] = 'DateTime'
            else:
                print('..Invalid entry. Choose from the following list:')
                print(' ', self.all_col_headers)
                continue
            i += 1

        print('\nTimestamp column list:', self.timestamp_col_headers)
        enter_continue()

    def setParamHeaders(self, print_banner=True):
        if print_banner:
            txt = 'Choose from the following list of SDFS parameter names'
            self.printSelectionBanner('Specify Parameter columns',
                                      options=[self.skip_str],
                                      notes=[txt, self.params])
        # drop time-like columns and ask user for SDFS parameter associated with
        # remaining cols
        self.param_col_list = [param for param in self.all_col_headers
                               if param not in self.timestamp_col_headers]

        n_params = len(self.param_col_list)
        renaming_dict = {}
        for i, param in enumerate(self.param_col_list, 1):
            valid = False
            while valid is False:
                sdfs_param = input('[{0}/{1}] Enter SDFS parameter associated '
                                   'with {2}: '.format(i, n_params, param))
                if sdfs_param in self.params:
                    valid = True
                    self.sdfs_header_names.append(sdfs_param)
                    if self.data_type == 'reference':
                        self.setParamRDFSInfo(param, sdfs_param)
                    unit_transform = self.checkParamUnits(param, sdfs_param)

                    self.add_param_attrib(param,
                                        attrib_key='unit_transform',
                                        attrib_val=unit_transform)
                    drop = False

                elif sdfs_param == '':
                    valid = True
                    print('..{0} will be dropped'.format(param))
                    drop = True

                else:
                    print('..Invalid entry. Choose from the list above.')

            renaming_dict[param] = sdfs_param

            self.add_param_attrib(param,
                                attrib_key='header_class',
                                attrib_val='parameter')

            self.add_param_attrib(param,
                                attrib_key='sdfs_param',
                                attrib_val=sdfs_param)

            self.add_param_attrib(param,
                                attrib_key='drop',
                                attrib_val=drop)


            # # Get a list of the col index locations where the column header name is
            # header_loc = [col for col in self.col_headers if param in
            #               self.col_headers[col].keys()]
            # for key in header_loc:
            #     self.col_headers[key][param]['SDFS_param'] = sdfs_param

        #TODO: Print dictionary with renaming scheme, ask to confirm
        # add something like following code block,
        print('')
        print('Configured renaming scheme:')
        self.pp.pprint(renaming_dict)
        enter_continue()

    def checkParamUnits(self, param, sdfs_param):
        sdfs_param_units = Parameter(sdfs_param).units
        print('')
        print(f'  Are the units of measure for {param} {sdfs_param_units}?')
        confirm = validate_entry(indent_statement=2)
        if confirm == 'n':
            val = input('  Enter the scalar quanitity for converting the '
                        'recorded measurements to the following unit basis: '
                        f'{sdfs_param_units}')
        else:
            val = None

        return val

    def setDateTimeFormat(self):
        cite = ('..format code list: https://docs.python.org/3/library/'
                'datetime.html#strftime-and-strptime-format-codes')
        epoch = ('..If a timestamp column is formatted as the number of '
                 'seconds since the Unix epoch (1 Jan. 1970), enter "epoch"')
        self.printSelectionBanner('Configure Timestamp Column Formatting',
                                  options=[epoch, self.skip_str],
                                  notes=[cite])

        self.time_format_dict = {}
        for col in self.timestamp_col_headers:
            invalid = True
            while invalid is True:
                val = input('Enter date/time formatting for "' + col + '": ')
                if val == '':
                    self.add_param_attrib(col,
                                attrib_key='drop',
                                attrib_val=True)
                    invalid = False
                    continue
                else:
                    confirm = validate_entry()
                    if confirm == 'y':
                        invalid = False
                        self.time_format_dict[col] = val

                        self.add_param_attrib(col,
                                            attrib_key='dt_format',
                                            attrib_val=val)

        print('')
        print('Configured formatting scheme:')
        self.pp.pprint(self.time_format_dict)
        enter_continue()


    def setTimeZone(self):
        self.printSelectionBanner('Specify DateTime Index Time Zone',
                                  options=[self.skip_str],
                                  notes=['For a list of all time zones, type'
                                         ' "pytz.all_timezones"'])

        for col in self.timestamp_col_headers:
            invalid = True
            while invalid is True:
                val = input('Enter time zone for "' + col + '": ')
                if val == '':
                    # timezone is unspecified
                    print('..time zone not specified, continuing with tz-naive'
                          ' DateTime index')
                    tzone = None
                    self.time_format_dict[col + '_tz'] = tzone
                    invalid = False
                    continue
                else:
                    try:
                        tzone = pytz.timezone(val)
                    except UnknownTimeZoneError:
                        print('..invalid time zone')
                        continue

                    confirm = validate_entry()
                    if confirm == 'y':
                        invalid = False
                        self.time_format_dict[col + '_tz'] = tzone.zone

                        self.add_param_attrib(col,
                                            attrib_key='dt_timezone',
                                            attrib_val=tzone.zone)

        print('')
        print('Configured time zone formatting:')
        self.pp.pprint(self.time_format_dict)
        enter_continue()

    def exportSetup(self):
        self.printSelectionBanner('Setup Configuration')
        self.config_dict = self.__dict__.copy()
        del self.config_dict['end_str']
        del self.config_dict['del_str']
        del self.config_dict['skip_str']
        del self.config_dict['header_names']
        del self.config_dict['timestamp_col_headers']
        del self.config_dict['all_col_headers']
        del self.config_dict['sdfs_header_names']

        if self.data_type == 'sensor':
            filename = self.name + '_setup.json'
            sensor_path = os.path.normpath(
                            os.path.join(self.data_rel_path, '..'))
            outpath = os.path.normpath(self.path + sensor_path)
        if self.data_type == 'reference':
            filename = 'reference_setup.json'
            outpath = os.path.normpath(self.path + self.data_rel_path)

        if not os.path.isdir(outpath):
            os.makedirs(outpath)

        self.outpath = os.path.join(outpath, filename)
        print('')
        print('..writing setup configuration to the following path:')
        print(self.outpath)
        print('')

        with open(self.outpath, 'w') as outfile:
            self.config_dict = json.dumps(self.config_dict, indent=4)
            outfile.write(self.config_dict)


class SensorSetup(_Setup):
    """Interactive class for handling the sensor data ingestion process.

    Users specify various attributes about sensor datasets, including column
    names for parameter data and timestamp entries. A renaming scheme is then
    constructed for converting the original naming scheme for columns into
    a standardized format for parameter names. The formatting for columns with
    date or time-like entries is then specified. The file type for sensor
    data is selected from a dictionary of valid data types than can be
    ingested.
    """
    def __init__(self, name, path=None):

        super().__init__(path)

        self.name = name
        self.data_type = 'sensor'
        self.dataset_kwargs = {'name':self.name}

        self.config()
        self.setSerials()
        self.exportSetup()

    def setSerials(self):
        self.printSelectionBanner('Configure Sensor Serial Identifiers',
                                  options=[self.end_str])
        print('')

        self.serials = {}
        edit = True
        col_n = 1

        abbrev_files = []
        for file in self.file_list:
            file = file.replace(self.path + '/Data and Figures/sensor_data/' +
                                self.name + '/raw_data/', '')
            abbrev_files.append(file)
            print('..{0}'.format(file))

        confirm = 'n'
        while confirm == 'n':
            val = input("Enter the number of unique sensors corresponding "
                        "to the datasets above: ")
            try:
                val = int(val)
            except ValueError:
                print('..Invalid entry, enter an integer value')
                continue

            confirm = validate_entry()

        self.number_of_sensors = val

        print('Enter unique serial identifiers for each sensor associated '
              'with the datasets listed above:')

        while col_n <= self.number_of_sensors:
            confirm = 'n'
            while confirm == 'n':
                serial = input("Enter serial identifier #{0}: ".format(str(col_n)))

                if serial == 'X':
                    edit = False
                    break

                elif not any(serial in file for file in abbrev_files):
                    print('..invalid entry, identifier must be contained in '
                          'the filenames listed above')

                else:
                    confirm = validate_entry()

            if edit is False:
                break
            else:
                self.serials[str(col_n)] = serial
                col_n += 1

        print('')
        print('Configured serial identifiers:')
        self.pp.pprint(self.serials)
        print('')
        enter_continue()


class ReferenceSetup(_Setup):
    """Interactive class for handling the reference data ingestion process.

    """
    # Method code lookup tables
    criteria_methods_path = os.path.abspath(os.path.join(__file__,
                                  '../../reference/method_codes/methods_criteria.csv'))
    criteria_lookup = pd.read_csv(criteria_methods_path)

    critera_params = {'CO': 'Carbon monoxide',
                     'Pb_TSP': 'Lead (TSP) LC',
                     'Pb_PM10': 'Lead PM10 LC FRM/FEM',
                     'NO2': 'Nitrogen dioxide (NO2)',
                     'O3': 'Ozone',
                     'PM10': 'PM10 Total 0-10um STP',
                     'PM25': 'PM2.5 - Local Conditions',
                     'SO2': 'Sulfur dioxide'}

    api_services = ['aqs', 'airnow']

    met_methods_path = os.path.abspath(os.path.join(__file__,
                                  '../../reference/method_codes/methods_met.csv'))
    met_lookup = pd.read_csv(met_methods_path)


    def __init__(self, path):

        super().__init__(path)

        self.data_type = 'reference'
        self.dataset_kwargs = {'ref_data_source': None}
        self.agency = None
        self.site_name = None
        self.site_aqs = None
        self.site_lat = None
        self.site_lon = None

        self.selectDataSource()
        self.setSiteInfo()

        if self.dataset_kwargs['ref_data_source'] in self.api_services:
            self.setDataRelPath()
        elif self.dataset_kwargs['ref_data_source'] == 'airnowtech':
            self.setDataRelPath()
            self.processAirNowTech()
        else:
            self.config()

        self.exportSetup()

        if self.dataset_kwargs['ref_data_source'] == 'local':
            self.localRefDataIngest()

    def selectDataSource(self):
        # Indicate the service used to acquire the dataset.
        select_options = ['airnow', 'aqs', 'airnowtech', 'local']
        self.printSelectionBanner('Select Name of Service for Data Source',
                                    options=[select_options])

        valid = False
        while valid is False:
            console_text= (f'Enter the name of the service from the list of'
                           f' options above: ')
            console_text = '\n'.join(wrap(console_text,
                                          width=self.__banner_w__))
            val = input(console_text)
            if str(val) not in select_options:
                print('..invalid entry, please enter one of the options '
                      'listed above')
            else:
                selection = val
                print('')
                print('Data acquired from:', selection)
                confirm = validate_entry()
                if confirm == 'y':
                    valid = True
                    self.dataset_kwargs['ref_data_source'] = selection
            print('')


    def setSiteInfo(self):
        self.printSelectionBanner('Enter Ambient Air Monitoring Site Information',
                                  options=['..press enter to skip entries'],
                                  notes=['Site AQS ID required for AQS queries',
                                         'Site Latitude and Longitude required for AirNow queries'])
        self.agency = None
        self.site_name = None
        self.site_aqs = None
        self.site_lat = None
        self.site_lon = None

        site_dict = {
            'Enter the name of the monitoring site: ': 'site_name',
            'Enter the name of the Agency overseeing the monitoring site: ': 'agency',
            'Enter the AQS site ID (if applicable) [format XX-XXX-XXXX]: ': 'site_aqs',
            'Enter the site latitude (in decimal coordinates): ': 'site_lat',
            'Enter the site longitude (in decimal coordinates): ': 'site_lon'
            }

        for console_statement, attrib in zip(site_dict.keys(), site_dict.values()):
            valid = False
            while valid is False:

                console_statement = '\n'.join(wrap(console_statement,
                                              width=self.__banner_w__))
                val = input(console_statement)

                if attrib == 'site_aqs':
                    if val == '' and self.dataset_kwargs['ref_data_source'] == 'aqs':
                        print('..Invalid entry, AQS Site ID must be specified for AQS queries')
                        continue
                    elif val != '':
                        list_val = val.split('-')
                        if len(list_val) != 3:
                            print('..Invalid format, enter site ID in the format XX-XXX-XXXX')
                            continue

                        # length of components in aqs site ID
                        aqs_fmt = {'State Code': 2,
                                   'County Code':3,
                                   'Site Code':4}
                        invalid_fmt = False
                        for entry, expect_key, expect_len in zip(list_val, aqs_fmt.keys(), aqs_fmt.values()):
                            if len(entry) != expect_len:
                                print(f'..Invalid format for AQS Site ID {expect_key}: {entry}')
                                print(f'....expected code length {expect_len}')
                                invalid_fmt = True
                        if invalid_fmt:
                            continue

                if attrib == 'site_lat' or attrib == 'site_lon':
                    if val == '' and self.dataset_kwargs['ref_data_source'] == 'airnow':
                        print('..Invalid entry, Latitude and Longitude must be specified for AirNow queries')
                        continue
                    elif val != '':
                        try:
                            cast_val = float(val)
                        except ValueError:
                            print('..Invalid entry, value must be numeric')
                            continue
                        if attrib == 'site_lat' and (cast_val <-90 or cast_val > 90):
                            print('..Invalid entry, Latitude must be between -90 and +90 degrees')
                            continue
                        if attrib == 'site_lon' and (cast_val <-180 or cast_val > 180):
                            print('..Invalid entry, Longitude must be between -180 and +180 degrees')
                            continue

                if val == '':
                    print('..skipping')
                    valid = True
                    continue

                confirm = validate_entry()
                if confirm == 'y':
                    valid = True
                    self.__dict__.update({attrib: val})
                print('')

        if self.site_name == None:
            self.site_name = 'Unspecified Site Name'
        self.site_name = self.site_name.title()
        self.fmt_site_name = self.site_name.replace(' ', '_')

        if self.site_aqs == None:
            self.site_aqs = 'Unspecified Site ID'
        self.fmt_site_aqs = self.site_aqs.replace('-', '').replace(' ', '_')

        self.dataset_kwargs['site_name'] = self.fmt_site_name
        self.dataset_kwargs['site_aqs'] = self.fmt_site_aqs

        self.ref_data_subfolder = '_'.join([self.fmt_site_name,
                                            self.fmt_site_aqs])

    def setParamRDFSInfo(self, param, sdfs_param):
        entry_dict = {
            f'Enter the units of measure for {param}: ': f'{sdfs_param}' + '_Unit',
            f'Enter the parameter code for {param}: ': f'{sdfs_param}' + '_Param_Code',
            f'Enter the method code corresponding to the reference method for {param}: ': f'{sdfs_param}' + '_Method_Code',
            f'Enter the parameter occurance code for the above reference method: ': f'{sdfs_param}' + '_Method_POC'
            }

        indent = '  '
        param_obj = Parameter(sdfs_param)
        param_code = param_obj.aqs_parameter_code
        custom_method = False

        for console_statement, attrib in zip(entry_dict.keys(), entry_dict.values()):
            valid = False
            while valid is False:

                if attrib == f'{sdfs_param}' + '_Method_Code':
                    if param_obj.criteria_pollutant:
                        method_table = self.displayMethods(param_code,
                                                           self.criteria_lookup
                                                           )
                    elif param_obj.classifier == 'Met':
                        method_table = self.displayMethods(param_code,
                                                           self.met_lookup
                                                           )

                if attrib == f'{sdfs_param}' + '_Param_Code':
                    print('')
                    print(f'{indent}Is the parameter code for reference measurements {param_code}?')
                    confirm = validate_entry(indent_statement=2)
                    if confirm == 'n':
                        val = input(f'{indent}{console_statement}')
                        param_obj.aqs_parameter_code = val
                        param_obj.criteria_pollutant = False
                        custom_method = True
                    self.__dict__.update({attrib: val})
                    valid = True
                    continue

                console_statement = '\n'.join(wrap(console_statement,
                                              width=self.__banner_w__))

                val = input(f'{indent}{console_statement}')

                if val == '':
                    print(f'{indent}..skipping')
                    valid = True
                    # set valid true, step to next attribute
                    continue

                if attrib == f'{sdfs_param}' + '_Method_Code':
                    try:
                        val = int(val)
                    except ValueError:
                        print(f'{indent}..invalid entry, enter either an integer or "None"')
                        # valid is still false, will continue with current attribute
                        continue
                    if val not in method_table['Method Code'].values:
                        print(f'{indent}..method code not in table of methods, continue with entry?')
                        custom_method = True

                confirm = validate_entry(indent_statement=2)

                if confirm == 'y':
                    valid = True
                    self.__dict__.update({attrib: val})

                    if attrib == f'{sdfs_param}' + '_Method_Code':
                        if custom_method:
                            name = input(f'{indent}Enter the reference method name: ')
                            if name == '':
                                print(f'{indent}..skipping')
                                valid = True
                                continue
                            confirm = validate_entry(indent_statement=2)
                            valid = True
                            self.__dict__.update({f'{sdfs_param}' + '_Method': name})

                        else:
                            name = method_table[
                                method_table['Method Code']==int(val)
                                    ]['Collection Description'].values[0]
                            self.__dict__.update({f'{sdfs_param}' + '_Method': name})


    def displayMethods(self, param_code, lookup_data):
        with pd.option_context('display.expand_frame_repr', False,
                                           'display.max_rows', None):
            table = lookup_data[
                lookup_data['Parameter Code']==param_code].reset_index(drop=True)
            print(table[['Method Code',
                         'Collection Description',
                         'Method Type']].reset_index(drop=True))
        return table

    def processAirNowTech(self):

        self._dataset_selection = 'files'
        self.setDataExtension()
        self.copyDataSets()

        self.printSelectionBanner('Pre-process AirNowTech Datasets',
                                    options=[])
        for file in self.file_list:
            preprocess_airnowtech(file, self.path)

    def localRefDataIngest(self):
        self.printSelectionBanner('Ingest Local Datasets',
                                    options=[])

        process_path = os.path.normpath(os.path.join(self.outpath,
                            f'../../../processed/{self.ref_data_subfolder}'))

        if not os.path.isdir(process_path):
            os.makedirs(process_path)

        parameter_classes = {}
        for param in self.sdfs_header_names:
            parameter_classes[param] = Parameter(param).classifier

        for file in self.file_list:
            df = standard_ingest(file, name=None,
                                 setup_file_path=self.outpath)

            # Separate dataframe by parameter classifier
            for classifier in ['PM', 'Gases', 'Met']:
                class_params = [param for param in parameter_classes
                                if parameter_classes[param] == classifier]

                class_param_cols = []
                site_cols = ['Site_Name', 'Agency', 'Site_AQS',
                             'Site_Lat', 'Site_Lon']
                for param in class_params:
                    class_param_cols.extend([col for col in df.columns
                                             if col.startswith(param)])
                if class_param_cols != []:
                    class_param_cols.extend(site_cols)
                else:
                    continue

                class_df = df[class_param_cols]

                # Save class dataframe in monthly segements
                for date in pd.date_range(start=class_df.index.min(),
                              end=class_df.index.max()).to_period('M').unique():
                    month = str(date.month).zfill(2)
                    year = str(date.year)
                    month_df = class_df.loc[year + '-' + month, :]

                    # Write to processed folder as csv
                    filename = 'H_' + year + month + '_' + classifier + '.csv'
                    print(f'..{filename}')
                    month_df.to_csv(os.path.join(process_path, filename))


# Testing out using new method dataset for criteria pollutants
def displayMethods(param, lookup_data, verbose=False):

        if verbose:
            expand_frame_repr =  False
            col_width = 1000
        else:
            expand_frame_repr =  True
            col_width = 65
        with pd.option_context('display.expand_frame_repr', expand_frame_repr,
                               'display.max_colwidth', col_width,
                               'display.max_rows', None,
                               'display.colheader_justify', 'right'):
            table = lookup_data[
                lookup_data['Method Type'].str.startswith(param)
                            ].reset_index(drop=True)

            if not verbose:
                table['Make/Model'] = table.Abbrev_Make + ' ' + table.Model
                print(table[['Make/Model', 'Method Code']
                            ].reset_index(drop=True))
            else:
                print(table[['Make', 'Model', 'Method Code']
                            ].reset_index(drop=True))

        return table

if __name__ == '__main__':
    sensor_name = 'Example_Make_Model'
    work_path = (r'C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\sensortoolkit_testing')

    test = SensorSetup(name=sensor_name,
                path=work_path)


    #test = ReferenceSetup(path=work_path)
