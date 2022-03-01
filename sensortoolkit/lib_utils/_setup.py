# -*- coding: utf-8 -*-
"""
Interactive module for specifying the setup configuration for both sensor
and reference data.

Users are asked to supply various details about their
dataset(s) for the purpose of data ingestion into the Sensor Data
Formatting Scheme (SDFS).

===============================================================================

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
from pandas.errors import EmptyDataError
import pprint
import charset_normalizer
import pytz
from pytz.exceptions import UnknownTimeZoneError
from sensortoolkit.lib_utils import (flatten_list, validate_entry,
                                     enter_continue, copy_datasets)
from sensortoolkit.param import Parameter
from sensortoolkit.reference import preprocess_airnowtech
from sensortoolkit.ingest import standard_ingest
from sensortoolkit.datetime_utils import (interval_averaging,
                                          get_timestamp_interval)
from sensortoolkit import _param_dict
from sensortoolkit.lib_utils._copy_datasets import _prompt_files, _check_extension


class _Setup:
    """Setup methods for Sensor and Reference data ingestion configuration.

    Args:
        path (str, optional):
            The path to the directory where the user intends to store data,
            figures, and reports relating to the sensor being testing.
            Defaults to None.

    """

    #params = sorted(list(Parameter.__param_dict__.keys()))

    sdfs_params = [key for key in _param_dict if not _param_dict[key]['custom']]
    custom_params = [key for key in _param_dict if _param_dict[key]['custom']]

    data_types = ['.csv', '.txt', '.xlsx']
    __banner_w__ = 79
    pp = pprint.PrettyPrinter()

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
        self.custom_ingest = False
        self.use_previous_setup = False
        self.sdfs_header_names = []
        self.all_col_headers = []
        self.timestamp_col_headers = []
        self.col_headers = {}

    def config(self):
        """Wrapper method for standard configuration setup.

        Utilized by both sensor and reference setup schemes.

        Returns:
            None.

        """
        # Indicate the dataset file type (.csv, .txt, .xlsx)
        self.setDataExtension()

        # Ask user for either directory or files to load in, parse datasets
        # and copy datasets to transfer to 'data' subdirectory
        self.setDataRelPath()
        self.selectDataSets()
        self.copyDataSets()

        # Ask if using custom ingest module, if true, exit config
        self.specifyCustomIngest()
        if self.custom_ingest:
            return

        # Ask user if they have a previously configured setup.json for the device
        self.loadPreviousSetup()
        if self.use_previous_setup:
            return

        # set the row position where the data header is located
        self.setHeaderIndex()

        if self.header_iloc is None:
            # Manually specify column names if none provided
            self.setColumnHeaders()
        # otherwise, specify column headers in parsedatasets, infer header at
        # iloc position
        self.parseDataSets()
        # Specify which headers are assocaited with timestamp info
        self.setTimeHeaders()
        # Specify how to convert recorded parameter headers to SDFS
        self.setParamHeaders()
        # Specify datetime formatting for time-like columns and tzone
        self.setDateTimeFormat()
        self.setTimeZone()

    def printSelectionBanner(self, select_type, options=[], notes=[]):
        """Display a banner indicating the current configuration step.

        Args:
            select_type (str): The title of the configuration section.
            options (list, optional):
                List of interactive options indicating keyword characters
                used to modify the state of thge console and
                a description of what entering that keyword does. Defaults
                to [].

                Example:

                    >>> options = ['..press X to end adding entries',
                                   '..press D to delete the previous entry']

            notes (list, optional):
                A list of strings containing notes or
                resources that may provide helpful context for the selection
                input or operation. Defaults to [].

        Returns:
            None.

        """
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
            if options != []:
                print('')
            print('Notes\n-----')
            notes = ['\n'.join(wrap(str(l),
                               width=self.__banner_w__)) for l in notes]
            for line in notes:
                print(line)

        print(len(flier)*'=')

    def add_param_attrib(self, param, attrib_key, attrib_val):
        """Assign parameter header attribute.

        Search through the column index entries, if the parameter name within
        the column index subdictionary, add the passed attribute key and value.

        Args:
            param (str):
                The name of the parameter.
            attrib_key (str):
                The key to assign to the subdictionary entry.
            attrib_val (int, float, or str):
                The value to assign to the subdictionary entry.

        Returns:
            None.

        """
        for col_idx in self.col_headers.keys():
            if param in self.col_headers[col_idx]:
                self.col_headers[col_idx][param][attrib_key] = attrib_val


    def setDataExtension(self):
        """Select the file data extension for to the datasets that will be
        loaded.

        Choose the corresponding data file type for recorded
        datasets from ``'.csv'``, ``'.txt'``, ``'.xlsx'``.

        Returns:
            None.

        """
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
        """Choose the selection scheme for pointing to recorded data files.

        Selection options include the following:

        - ``'directory'``, which will locate and copy all of the data files
          in the specified directory for the indicated data type
        - ``'recursive directory'``, which will locate and copy all data
          files within the specified directory and any subdirectories
          contained within the indicated folder path
        - ``'files'`` which copies over files that the user manually selects
          within a directory.


        Returns:
            None.

        """
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
        """Copy recorded datasets from the selected file or folder
        location to the ``../data/sensor_data/[sensor_name]/raw_data``
        directory path.

        Returns:
            None.

        """
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

    def specifyCustomIngest(self):
        """Ask the user whether a custom, prewritten ingestion module will be
        used to import sensor data instead of the standard_ingest() method.


        Returns:
            None.

        """
        self.printSelectionBanner('Indicate whether to use a custom ingestion method',
                                  options=[])

        confirm = validate_entry(
            statement='Will a custom, prewritten ingestion module be used to import data?')

        if confirm == 'y':
            self.custom_ingest = True
            # TODO: could make note of how to use AirSensor.load_data with custom ingest module here
        enter_continue()

    def loadPreviousSetup(self):
        """Ask the user if a previous setup config exists for the type of sensor
        or reference dataset that they are loading. If they choose to use a
        previously configured setup.json file, use the file attributes to fill
        in various setup components, such as the parameter renaming, datetime
        formatting, etc.

        Returns:
            None.

        """
        self.printSelectionBanner('Indicate whether to use a previous setup configuration',
                                  options=[])
        console_text = ('Have you previously created a setup.json config '
                        'file that [1] matches the device type associated with '
                        'the selected data sets and [2] intend to use the previous '
                        'setup.json file to configure the current setup session?')
        console_text = '\n'.join(wrap(console_text,
                                      width=self.__banner_w__))

        confirm = validate_entry(statement=console_text)

        if confirm == 'y':
            self.use_previous_setup = True

            # Ask user to locate where the setup.json file is
            valid_file = False
            while valid_file is False:
                # TODO: print something to console prompting user to select file
                print('')
                print('Select the setup.json file you wish to use')
                file_path = _prompt_files(single_file=True)
                valid_file = _check_extension(file_path, '.json')

            enter_continue()

            # import that json
            with open(file_path) as p:
                previous_setup_data = json.loads(p.read())
                p.close()

            # extract attributes
            self.header_iloc = previous_setup_data['header_iloc']
            self.data_row_idx = previous_setup_data['data_row_idx']
            self.sdfs_header_names = previous_setup_data['sdfs_header_names']

            self.parseDataSets()

            previous_col_headers = previous_setup_data['col_headers']

            col_descrip = {}
            for col_idx in previous_col_headers:
                for label in previous_col_headers[col_idx]:
                    if label not in col_descrip:
                        col_descrip[label] = {}

                    col_descrip[label]['sdfs_param'] = previous_col_headers[col_idx][label]['sdfs_param']
                    col_descrip[label]['header_class'] = previous_col_headers[col_idx][label]['header_class']

                    if col_descrip[label]['header_class'] == 'datetime':
                        col_descrip[label]['dt_format'] = previous_col_headers[col_idx][label]['dt_format']
                        col_descrip[label]['dt_timezone'] = previous_col_headers[col_idx][label]['dt_timezone']
                    col_descrip[label]['drop'] = previous_col_headers[col_idx][label]['drop']
                    if (col_descrip[label]['header_class'] == 'parameter') and (col_descrip[label]['drop'] is False):
                        col_descrip[label]['unit_transform'] = previous_col_headers[col_idx][label]['unit_transform']

            # TODO: Implement some sort of error catching mechanism that kicks in
            # if the formatting for the current datasets and previous setup config
            # do not match, fall back with standard setup process (i.e.,
            # set use_previous_setup to false and continue)
            self._not_in_previous_setup = {}
            for col_idx in self.col_headers.copy():
                for label in self.col_headers[col_idx].copy():

                    # Check if the recorded dataset doesnt have a header,
                    # if so, use previously manually configured names
                    if previous_setup_data['header_iloc'] == None:
                        # label is an integer value, reassign to previously
                        # manually configured name
                        former_label = label
                        label = list(col_descrip.keys())[former_label]
                        self.col_headers[col_idx][label] = self.col_headers[col_idx].pop(former_label)

                    try:
                        self.col_headers[col_idx][label]['sdfs_param'] = col_descrip[label]['sdfs_param']
                        self.col_headers[col_idx][label]['header_class'] = col_descrip[label]['header_class']

                        if col_descrip[label]['header_class'] == 'datetime':
                            self.col_headers[col_idx][label]['dt_format'] = col_descrip[label]['dt_format']
                            self.col_headers[col_idx][label]['dt_timezone'] = col_descrip[label]['dt_timezone']
                        self.col_headers[col_idx][label]['drop'] = col_descrip[label]['drop']
                        if (col_descrip[label]['header_class'] == 'parameter') and (col_descrip[label]['drop'] is False):
                            self.col_headers[col_idx][label]['unit_transform'] = col_descrip[label]['unit_transform']
                    except KeyError as e:
                        # header in the current datasets but not in previous setup
                        # For now, just assume the columns are not going to be used
                        if label in self.all_col_headers:
                            self.col_headers[col_idx][label]['sdfs_param'] = ''
                            self.col_headers[col_idx][label]['header_class'] = 'parameter'
                            self.col_headers[col_idx][label]['drop'] = True
                        if col_idx not in self._not_in_previous_setup:
                            self._not_in_previous_setup[col_idx] = {}
                        self._not_in_previous_setup[col_idx][label] = {'sdfs_param': '',
                                                                       'header_class': '',
                                                                       'drop': False}
                        continue

            # Ask the user to specify attributes for columns that
            # didnt appear in the previously configured setup.
            if self._not_in_previous_setup != {}:
                new_cols = []

                for col_idx in self._not_in_previous_setup:
                    new_cols.extend(self._not_in_previous_setup[col_idx].keys())

                new_cols = list(set(new_cols))

                self.all_col_headers.extend(new_cols)
                self.all_col_headers = list(set(self.all_col_headers))

                self.setTimeHeaders(
                    print_statement=f'\nFrom the following list of column names, enter the names of columns which contain timestamps\n{new_cols}')
                self.setDateTimeFormat()
                self.setTimeZone()
                self.setParamHeaders(col_list=new_cols)


    def loadDataFile(self, file, **kwargs):
        """Helper function for loading the first few rows of recorded datasets.

        Args:
            file (str):
                Full path to dataset file.

        **Keyword Arguments:**

        :param int nrows:
            The number of rows to load for the passed dataset. Defaults to 1.

        Raises:
            TypeError: If data type is not in the list of valid extensions.

        Returns:
            df (pandas DataFrame):
                A DataFrame containing the first few rows of recorded datasets.

        """

        load_table = kwargs.get('load_table', False)
        encoding = kwargs.get('encoding', None)

        if load_table:
            df = pd.read_table(file,
                               nrows=kwargs.get('nrows', 1),
                               header=None,
                               encoding=encoding)

        elif self.file_extension == '.csv' or self.file_extension == '.txt':
            df = pd.read_csv(file, header=self.header_iloc,
                             names=self.header_names,
                             nrows=kwargs.get('nrows', 1),
                             skiprows=self.data_row_idx,
                             on_bad_lines='skip',
                             encoding=encoding
                             )
        elif self.file_extension == '.xlsx':
            df = pd.read_excel(file, header=self.header_iloc,
                               names=self.header_names,
                               nrows=kwargs.get('nrows', 1),
                               skiprows=self.data_row_idx,
                               encoding=encoding
                               )
        else:
            raise TypeError('Invalid data type')

        return df

    def setDataRelPath(self):
        """Assign the relative path for the recorded dataset subdirectory.

        The relative path stems from the project path.

        For sensor data, the relative path to raw (recorded datasets)
        should appear something like:
        ``/data/sensor_data/[sensor_name]/raw_data`` where 'sensor_name' is the
        name given to the air sensor.

        For reference datasets, the relative path to raw (recorded datasets)
        should appear something like:
        ``/data/reference_data/[reference_data_source]/raw/[sitename_siteid]``
        where 'reference_data_source' is the source or api service from which
        data were acquired, 'sitename' is the name given to the site, and
        'siteid' is the AQS id for the site (if applicable).

        Returns:
            None.

        """
        self.data_rel_path = os.path.join('data', f'{self.data_type}_data')
        if self.data_type == 'sensor':
            self.data_rel_path = os.path.join(self.data_rel_path, self.name, 'raw_data', '')
        if self.data_type == 'reference':
            self.data_rel_path = os.path.join(self.data_rel_path,
                                              self.dataset_kwargs["ref_data_source"],
                                              'raw', self.ref_data_subfolder, '')


    def parseDataSets(self, print_banner=True):
        """Load the  first few rows of recorded sensor datasets located in the
        ``../data/sensor_data/[sensor_name]/raw_data`` directory path.

        The names of column headers are located based on the
        indicated head index. A list of unique column headers is stored for
        subsequent reassignment of column header names.

        Args:
            print_banner (bool, optional):
                If ``'True'``, a banner indicating the title of the section,
                user input options, and notes will be printed to the console.
                Defaults to True.

        Returns:
            None.

        """
        if print_banner:
            self.printSelectionBanner('Parsing Datasets',
                                      options=[])
            print('')

        # Load data files and populate a dictionary of unique headers that
        # occur. Top level is ordered by the row index, so if some files have
        # different headers, there will be multiple entries within the
        # particular row index key.

        print(f'Parsing datasets at "..{self.data_rel_path}"')
        print('')
        self.encoding_predictions = {}
        for i, file in enumerate(self.file_list):
            # Try loading with utf-8 encoding, if error raised, predict encoding
            try:
                df = self.loadDataFile(file)
            except UnicodeDecodeError:
                print('[WARNING]: Reading the following dataset with uft-8 encoding '
                      'unsuccessful')
                print(file.replace(self.data_rel_path, ''))
                print('..Attempting to guess encoding')

                with open(file, 'rb') as f:
                    data = f.read(10000)
                prediction = charset_normalizer.detect(data)
                print('..encoding prediction:')
                print(f'....{prediction}')
                print('')

                try:
                    df = self.loadDataFile(file, encoding=prediction['encoding'])
                    self.encoding_predictions[str(i)] = prediction['encoding']
                except UnicodeError as e:
                    print('Error encountered in file:', file)
                    print(e)
                    print(f'Encoding prediction {prediction["encoding"]} unsuccessful for {file}')
                    #self.encoding_predictions[str(i)] = prediction['encoding']
                except UnicodeDecodeError as e:
                    print('Error encountered in file:', file)
                    print(e)
                    print(f'Encoding prediction {prediction["encoding"]} unsuccessful for {file}')
            except EmptyDataError as e:
                print(f'[Warning] {e}:')
                print(f'  {file}')
                print('')

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
        """Select the integer index position for the row containing headers.

        Args:
            print_banner (bool, optional):
                If ``'True'``, a banner indicating the title of the section,
                user input options, and notes will be printed to the console.
                Defaults to True.

        Returns:
            None.

        """
        if print_banner:
            self.printSelectionBanner('Column Header Index',
                                      options=['..type "None" if no header '
                                               'columns in recorded sensor '
                                               'dataset'])

        # Load the first dataset (display 10 rows to user)
        if self.file_list == []:
            data_path = os.path.normpath(os.path.join(self.path,
                                                      self.data_ref_path))
            sys.exit('No data files found with type'
                     ' {0} at {1}'.format(self.file_extension, data_path))

        # First try loading with utf-8 encoding, if error raised, try utf-16
        file = self.file_list[0]
        try:
            df = self.loadDataFile(file,
                                   nrows=10,
                                   load_table=True)
        except UnicodeDecodeError:
            print('[WARNING]: Reading the following dataset with uft-8 encoding '
                  'unsuccessful')
            print(file.replace(self.data_rel_path, ''))
            print('..Attempting to guess encoding')

            with open(file, 'rb') as f:
                data = f.read(10000)
            prediction = charset_normalizer.detect(data)
            print('..encoding prediction:')
            print(f'....{prediction}')

            try:
                df = self.loadDataFile(file,
                                       nrows=10,
                                       load_table=True,
                                       encoding=prediction['encoding'])
            except UnicodeError as e:
                print('')
                print('Error encountered in file:', file)
                print(e)
                print(f'Encoding prediction {prediction["encoding"]} unsuccessful for {file}')
                #self.encoding_predictions[str(i)] = prediction['encoding']
            except UnicodeDecodeError as e:
                print('')
                print('Error encountered in file:', file)
                print(e)
                print(f'Encoding prediction {prediction["encoding"]} unsuccessful for {file}')
        except EmptyDataError as e:
            print(f'[Warning] {e}:')
            print(f'  {file}')
            print('')

        filename = file.split('/')[-1]
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
        """Manually set column headers if the user indicates ``'None'`` for the
        row index for the column headers in ``setHeaderIndex()``.

        Args:
            print_banner (bool, optional):
                If ``'True'``, a banner indicating the title of the section,
                user input options, and notes will be printed to the console.
                Defaults to True.

        Raises:
            ValueError: Raise if the value of the entered index is invalid
                (less than zero).

        Returns:
            None.

        """
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

                # Shortcut method for copying and pasting list of columns into
                # first entry
                replace_strs = ['\n', ' ', '"']
                for char in replace_strs:
                    col_name = col_name.replace(char, '')
                col_list = col_name.split(',')
                if len(col_list) > 1:
                    # Assign only if list of strings passed
                    if '[' in col_list[0] and ']' in col_list[-1]:
                        col_list[0] = col_list[0].replace('[', '')
                        col_list[-1] = col_list[-1].replace(']', '')
                        print('..assigning column names based on passed list')
                        self.header_names = col_list
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

    def setTimeHeaders(self, print_banner=True, print_statement=None):
        """Specify the column(s) containing date/timestamp information.

        Args:
            print_banner (bool, optional):
                If ``'True'``, a banner indicating the title of the section,
                user input options, and notes will be printed to the console.
                Defaults to True.

        Returns:
            None.

        """
        if print_banner:
            self.printSelectionBanner('Specify Timestamp columns',
                                      options=[self.end_str, self.del_str])
        # Create a list of time-like columns, update the col_headers list with
        # the DateTime type corresponding to the specified header name
        # Enter in the time like columns [LOOP]

        if print_statement is not None:
            print(print_statement)

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
                self.timestamp_col_headers.append(val)

                self.add_param_attrib(val,
                                      attrib_key='header_class',
                                      attrib_val='datetime')

                self.add_param_attrib(val,
                                      attrib_key='sdfs_param',
                                      attrib_val='DateTime')

                self.add_param_attrib(val,
                                      attrib_key='drop',
                                      attrib_val=False)

            else:
                print('..Invalid entry. Choose from the following list:')
                print(' ', self.all_col_headers)
                continue
            i += 1

        print('\nTimestamp column list:', self.timestamp_col_headers)
        enter_continue()

    def setParamHeaders(self, print_banner=True, col_list=None):
        """Select the SDFS parameters corresponding to column names discovered
        by ``ParseDataSets()``.

        A parameter renaming dictionary is created for reassigning the names
        of header labels.

        Args:
            print_banner (bool, optional):
                If ``'True'``, a banner indicating the title of the section,
                user input options, and notes will be printed to the console.
                Defaults to True.

        Returns:
            None.

        """
        param_types = {'S': 'The header corresponds to an SDFS Parameter',
             'C': 'The header corresponds to an existing custom Parameter',
             'N': 'Create a new custom Parameter for the header',
             '': '(enter key) Skip the current header and drop from SDFS datasets'}
        pretty_params = pprint.pformat(param_types)


        if print_banner:
            #txt = 'Choose from the following list of SDFS parameter names'
            self.printSelectionBanner('Specify Parameter columns',
                                      options=[self.skip_str],
                                      #notes=[txt, self.params]
                                      )
        # drop time-like columns and ask user for SDFS parameter associated
        # with remaining cols
        # param_col_list = [param for param in self.all_col_headers
        #                   if param not in self.timestamp_col_headers)]
        if col_list is None:
            param_col_list = list(set(param for param in self.all_col_headers
                              if param not in self.timestamp_col_headers))
        else:
            param_col_list = list(set(param for param in col_list if param
                                      not in self.timestamp_col_headers))

        n_params = len(param_col_list)
        renaming_dict = {}
        for i, rec_header in enumerate(param_col_list, 1):
            valid = False
            while valid is False:
                print(f'\n[{i}/{n_params}]')
                print('-----')

                header_type = input('Enter the character indicating the type of'
                   f' parameter \n{pretty_params}\n\nParameter type for header'
                   f' name "{rec_header}": ')

                if header_type == 'S':
                    print('SDFS Parameters:')
                    print(self.sdfs_params)
                    set_header = input(f'From the list above, select the SDFS '
                                       f'parameter associated with {rec_header}: ')

                    if set_header in self.sdfs_params:
                        valid = True

                        self.sdfs_header_names.append(set_header)
                        self.sdfs_header_names = list(set(self.sdfs_header_names))

                        if self.data_type == 'reference':
                            self.setParamMetaCols(rec_header, set_header)
                        unit_transform = self.checkParamUnits(rec_header, set_header)

                        self.add_param_attrib(rec_header,
                                              attrib_key='unit_transform',
                                              attrib_val=unit_transform)
                        drop = False

                    else:
                        print('..Invalid entry')

                if header_type == 'C':
                    if self.custom_params != []:

                        set_header = input('Enter custom parameter associated with '
                                           f'{rec_header}: ')
                        print(self.custom_params)
                        if set_header in self.sdfs_params:
                            valid = True
                            drop = False
                        else:
                            print('..Invalid entry')
                    else:
                        print('No custom Parameters previously configured')

                if header_type == 'N':
                    set_header = input('Enter new custom parameter associated with '
                                       f'{rec_header}: ')
                    response = validate_entry(statement=f'Do you wish to save {set_header} to the catalog of sensortoolkit.Parameter attributes?')

                    if response == 'y':
                        save_param = True
                    else:
                        save_param = False
                    print('')
                    Parameter(set_header, save_custom_param=save_param)
                    valid = True
                    drop = False

                if header_type == '':
                    valid = True
                    print('..{0} will be dropped'.format(rec_header))
                    drop = True
                    set_header = ''

                if header_type not in param_types.keys():
                    print('..Invalid parameter header type')

            renaming_dict[rec_header] = set_header

            self.add_param_attrib(rec_header,
                                  attrib_key='header_class',
                                  attrib_val='parameter')

            self.add_param_attrib(rec_header,
                                  attrib_key='sdfs_param',
                                  attrib_val=set_header)

            self.add_param_attrib(rec_header,
                                  attrib_key='drop',
                                  attrib_val=drop)

        #TODO: Print dictionary with renaming scheme, ask to confirm
        # add something like following code block,
        print('')
        print('Configured renaming scheme:')
        self.pp.pprint(renaming_dict)
        enter_continue()

    def checkParamUnits(self, param, sdfs_param):
        """Prompt user to indicate whether units for passed parameter are the
        same as the preset units specified for the corresponding SDFS parameter.

        Args:
            param (str):
                The name of the parameter as logged in recorded datasets.
            sdfs_param (str):
                The name of the SDFS parameter corresponding to the recorded
                parameter.

        Returns:
            val (int, float, or Nonetype): A scalar quantity for converting the
            concentrations from the unit basis in which data were recorded to
            the unit basis for the SDFS parameter.

        """
        val = None
        sdfs_param_units = Parameter(sdfs_param).units
        print('')
        print(f'  Are the units of measure [{sdfs_param_units}] for column header "{param}"?')
        confirm = validate_entry(indent_statement=2)
        print('')
        if confirm == 'n':
            if param == 'Temp' or 'DP':
                print(f'  Are the units of measure for {param} Fahrenheit?')
                temp_confirm = validate_entry(indent_statement=2)
                if temp_confirm == 'y':
                    print('')
                    print(f'  {param} will be converted from Fahrenheit to Celsius')
                    val = 'f_c'
                else:
                    print('  Temperature must be in either degree Fahrenheit or Celsius')

            else:
                val = input('  Enter the scalar quanitity for converting the '
                            'recorded measurements to the following unit basis: '
                            f'{sdfs_param_units}')

        return val

    def setDateTimeFormat(self):
        """Configure the date/time formatting for date/time column(s) specified
        in ``setTimeHeaders()``.


        Returns:
            None.

        """
        cite = ('..format code list: https://docs.python.org/3/library/'
                'datetime.html#strftime-and-strptime-format-codes')
        epoch = ('..If a timestamp column is formatted as the number of '
                 'seconds since the Unix epoch (1 Jan. 1970), enter "epoch"')
        self.printSelectionBanner('Configure Timestamp Column Formatting',
                                  options=[epoch, self.skip_str],
                                  notes=[cite])

        self.time_format_dict = {}
        for col in self.timestamp_col_headers:

            # Pass over previously configured timestamp columns (when using
            # loadPreviousSetup())
            for col_idx in self.col_headers.keys():
                if col in self.col_headers[col_idx]:
                    col_attribs = self.col_headers[col_idx][col]
            if 'dt_format' in col_attribs:
                continue

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
        """Select the time zone associated with the date/time column(s).

        Timezones should be valid timezone names recognized by the ``pytz``
        library.


        Returns:
            None.

        """
        self.printSelectionBanner('Specify DateTime Index Time Zone',
                                  options=[self.skip_str],
                                  notes=['For a list of all time zones, type'
                                         ' "pytz.all_timezones"'])

        for col in self.timestamp_col_headers:

            # Pass over previously configured timestamp columns (when using
            # loadPreviousSetup())
            for col_idx in self.col_headers.keys():
                if col in self.col_headers[col_idx]:
                    col_attribs = self.col_headers[col_idx][col]
            if ('dt_timezone' in col_attribs):
                continue

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
        """Save the setup configuration to a ``setup.json`` file.

        Returns:
            None.

        """
        self.printSelectionBanner('Setup Configuration')
        self.config_dict = self.__dict__.copy()

        drop_attribs = ['end_str', 'del_str', 'skip_str', 'header_names',
                        'timestamp_col_headers', 'time_format_dict',
                        'all_col_headers']
        for attrib in drop_attribs:
            try:
                del self.config_dict[attrib]
            except KeyError:
                pass

        if self.data_type == 'sensor':
            filename = self.name + '_setup.json'
            sensor_path = os.path.normpath(
                            os.path.join(self.data_rel_path, '..'))
            outpath = os.path.normpath(os.path.join(self.path, sensor_path))
        if self.data_type == 'reference':
            filename = 'reference_setup.json'
            outpath = os.path.normpath(os.path.join(self.path, self.data_rel_path))

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

    Args:
        name (str):
            The name assigned to the air sensor. Typically incudes the sensor
            make (manufacturer) and model.
        path (str, optional):
            The path to the directory where the user intends to store data,
            figures, and reports relating to the sensor being testing.
            Defaults to None.

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
        """Indicate unique serial identifiers for each sensor unit tested.

        The identifying keyword for each sensor unit should be indicated within
        the recorded sensor dataset file names.

        Returns:
            None.

        """
        self.printSelectionBanner('Configure Sensor Serial Identifiers',
                                  options=[self.end_str])
        print('')

        self.serials = {}
        edit = True
        col_n = 1

        abbrev_files = []
        for file in self.file_list:
            file = file.replace(os.path.join(self.path, 'data', 'sensor_data',
                                             self.name, 'raw_data', ''), '')
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

    Args:
        path (str, optional):
            The path to the directory where the user intends to store data,
            figures, and reports relating to the sensor being testing.
            Defaults to None.

    """
    # Method code lookup tables
    criteria_methods_path = os.path.abspath(os.path.join(__file__, '..', '..',
                                            'reference', 'method_codes',
                                            'methods_criteria.csv'))
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

    met_methods_path = os.path.abspath(os.path.join(__file__, '..', '..',
                                            'reference', 'method_codes',
                                            'methods_met.csv'))
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
        """Select the service/source from which reference data were acquired.

        Choose from the following options:

        - ``'local'``: Data files aqcuired locally (e.g., local transfer
          from agency overseeing reference instrumentation at air monitoring
          site).
        - ``'airnowtech'``: User has downloaded files from the AirNowTech
          system and has saved files locally to the user’s system.
        - ``'aqs'``: User will query EPA's Air Quality System (AQS) API for
          reference data.
        - ``'airnow'``: User will query the AirNow API for reference data.

        Returns:
            None.

        """
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
        """Prompt user to enter various site attributes.

        The user is prompted to provide the following site attributes:
        - Site name
        - Agency overseeing site
        - Site AQS ID
        - Site latitude
        - Site longitude

        .. important

            **The following attrbiutes are required for querying API services:**

            - If the reference data source is ``'aqs'``, an AQS ID must be
              specified.
            - If the reference data source is ``'airnow'``, the site latitude
              and longitude must be specified.

        Returns:
            None.

        """
        airdata_link = 'https://epa.maps.arcgis.com/apps/webappviewer/index.html?id=5f239fd3e72f424f98ef3d5def547eb5'
        self.printSelectionBanner('Enter Ambient Air Monitoring Site Information',
                                  options=['..press enter to skip entries'],
                                  notes=['Site AQS ID required for AQS queries',
                                         'Use the EPA AirData Air Quality Monitors Map to locate AQS Sites'
                                         f'  {airdata_link}'
                                         'Site Latitude and Longitude required for AirNow queries',
                                         '  Latitude must be between -90 and +90 degrees ',
                                         '  Longitude must be between -180 and +180 degrees'])
        self.agency = None
        self.site_name = None
        self.site_aqs = None
        self.site_lat = None
        self.site_lon = None

        site_dict = {
            'Enter the name of the monitoring site: ': 'site_name',
            'Enter the name of the Agency overseeing the monitoring site: ': 'agency',
            'Enter the AQS site ID (if applicable, format XX-XXX-XXXX): ': 'site_aqs',
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

    def setParamMetaCols(self, param, sdfs_param):
        """Prompt user to enter various parameter metadata attributes.

        The user is prompted to enter the following attributes:
        - Units
        - Parameter AQS Code
        - Reference Method Code
        - Parameter Occurence Code

        Args:
            param (str):
                The name of the parameter as it appears in recorded datasets.
            sdfs_param (str):
                The corresponding SDFS parameter name.

        Returns:
            None.

        """
        entry_dict = {
            f'Enter the units of measure for {param}: ': f'{sdfs_param}' + '_Unit',
            f'Enter the parameter code for {param}: ': f'{sdfs_param}' + '_Param_Code',
            f'Enter the method code corresponding to the reference method for {param}: ': f'{sdfs_param}' + '_Method_Code',
            f'Enter the parameter occurence code for the above reference method: ': f'{sdfs_param}' + '_Method_POC'
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
                    if confirm == 'y':
                        val = param_code
                    self.__dict__.update({attrib: val})
                    valid = True
                    continue

                console_statement = '\n'.join(wrap(console_statement,
                                              width=self.__banner_w__))

                val = input(f'{indent}{console_statement}')

                if val == '':
                    # set valid true, step to next attribute
                    print(f'{indent}..skipping')
                    valid = True

                    if attrib == f'{sdfs_param}' + '_Method_Code':
                        name = 'Unknown Reference'
                        self.__dict__.update({f'{sdfs_param}' + '_Method': name})
                    else:
                        self.__dict__.update({attrib: None})

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
        """Helper function for printing an abbreviated dataset of reference
        methods correponding to the indicated parameter.

        Args:
            param_code (int):
                AQS parameter code.
            lookup_data (pandas DataFrame):
                AQS method code lookup table containing a list of FRM/FEM
                reference methods.

        Returns:
            table (pandas DataFrame):
                A table containing a listing of reference methods designated
                FRM/FEMs for the indicated parameter.

        """
        with pd.option_context('display.expand_frame_repr', False,
                                           'display.max_rows', None):
            table = lookup_data[lookup_data['Parameter Code']==param_code]
            print('')
            print(table[['Method Code',
                         'Collection Description',
                         'Method Type']].to_markdown(index=False))
        return table

    def processAirNowTech(self):
        """Wrapper method for calling the ``sensortoolkit.reference.preprocess_airnowtech()``
        method for converting downloaded AirNowTech datasets to SDFS format.

        Returns:
            None.

        """

        self._dataset_selection = 'files'
        self.setDataExtension()
        self.copyDataSets()

        self.printSelectionBanner('Pre-process AirNow-Tech Datasets',
                                    options=[])
        print('')
        for file in self.file_list:
            preprocess_airnowtech(file, self.path)
        print('')

    def localRefDataIngest(self):
        """Wrapper method for ingesting reference datasets acquired locally.

        Datasets are ingested into SDFS format via the
        ``sensortoolkit.ingest.standard_ingest()`` method and processed datasets
        are grouped into one of three parameter classifications (``'PM'``,
        ``'Gases'``, or ``'Met'``). These datasets are then saved in monthly
        intervals to the ``../data/reference_data/local/[sitename_siteid]/processed``
        directory path.

        Returns:
            None.

        """
        self.printSelectionBanner('Ingest Local Datasets',
                                    options=[])

        process_path = os.path.normpath(os.path.join(self.outpath, '..', '..',
                                        '..', 'processed', self.ref_data_subfolder))

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
                             'Site_Lat', 'Site_Lon', 'Data_Source']
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

                    samp_freq = get_timestamp_interval(month_df,
                                                       as_timedelta=True)

                    ONE_HOUR = pd.to_timedelta('60 m')
                    if samp_freq < ONE_HOUR:
                        N = ONE_HOUR / samp_freq
                        month_df = interval_averaging(month_df, freq='H',
                                                      interval_count=N,
                                                      thres=0.75)

                    # Write to processed folder as csv
                    filename = 'H_' + year + month + '_' + classifier + '.csv'
                    print(f'..{filename}')
                    month_df.to_csv(os.path.join(process_path, filename))
