# -*- coding: utf-8 -*-
"""
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
from sensortoolkit.lib_utils import flatten_list


class Setup:
    """Interactive class for handling the sensor data ingestion process.

    Users specify various attributes about sensor datasets, including column
    names for parameter data and timestamp entries. A renaming scheme is then
    constructed for converting the original naming scheme for columns into
    a standardized format for parameter names. The formatting for columns with
    date or time-like entries is then specified. The file type for sensor
    data is selected from a dictionary of valid data types than can be
    ingested.
    """
    params = ['PM1', 'PM25', 'PM10', 'O3', 'NO2', 'NO', 'NOx',
              'SO2', 'SOx', 'CO', 'CO2', 'Temp', 'RH', 'Press',
              'DP', 'WS', 'WD']
    data_types = ['.csv', '.txt', '.xlsx']
    __banner_w__ = 79
    pp = pprint.PrettyPrinter()

    def __init__(self, name, path=None):
        self.name = name
        if path is None:
            raise AttributeError('Path for working directory not specified')
        self.path = path
        self.dtype = None
        self.header_names = None
        self.header_iloc = None
        self.all_col_headers = []
        self.timestamp_col_headers = []
        self.drop_cols = []
        self.configSensor()

    def configSensor(self):
        #self.setDeploymentPeriod()
        self.setDataType()
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

        self.exportSetup()
        return

    def validateEntry(self):
        val = ''
        options = ['y', 'n']
        while val not in options:
            val = input('Confirm entry [y/n]: ')
            if val in options:
                return val
            else:
                print('..invalid entry, select [y/n]')

    def enterContinue(self):
        end = False
        while end is False:
            return_val = input('Press enter to continue.')
            if return_val == '':
                end=True
        print('')

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

    # def setSensorName(self):
    #     self.printSelectionBanner('Set Sensor Name', options=[''])
    #     confirm = 'n'
    #     while confirm == 'n':
    #         self.name = input('Enter the name of the sensor: ')
    #         print('')
    #         print('Sensor name: ' + self.name)
    #         confirm = self.validateEntry()
    #     print('')

    # def setDeploymentPeriod(self):
    #     self.printSelectionBanner('Set Deployment Start and End',
    #             options=['..start and End date must be entered as MM/DD/YYYY'])
    #     confirm = 'n'
    #     while confirm == 'n':
    #         self.startdate = input('Enter the start date for the deployment: ')
    #         self.enddate = input('Enter the end date for the deployment: ')
    #         print('')
    #         print('Deployment start: ' + self.startdate)
    #         print('Deployment end: ' + self.enddate)
    #         confirm = self.validateEntry()
    #     print('')

    def setHeaderIndex(self, print_banner=True):
        if print_banner:
            self.printSelectionBanner('Column Header Index',
                                      options=['..type "None" if no header '
                                               'columns in recorded sensor '
                                               'dataset'])

        # Load the first dataset (display 10 rows to user)
        self.findDataFiles()
        if self.file_list == []:
            data_path = os.path.normpath(self.path +
                                         '/Data and Figures/sensor_data/' +
                                         self.name +'/raw_data')
            sys.exit('No data files found with type'
                     ' {0} at {1}'.format(self.dtype, data_path))

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
        confirm = self.validateEntry()
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

                confirm = self.validateEntry()

            if edit is False:
                break
            else:
                self.header_names.append(col_name)
                col_n += 1

        print('')
        print('Column Headers:', self.header_names)
        print('')
        self.enterContinue()

    def findDataFiles(self):
        # Create a list of data files to load
        self.file_list = []
        self.data_path = (self.path + '/Data and Figures/sensor_data/'
                          + self.name+ '/raw_data')

        for cwd, folders, files in os.walk(self.data_path):
            self.file_list.extend([cwd+ '/' + file for file in files if
                                   file.lower().endswith(self.dtype)])

    def loadDataFile(self, file, **kwargs):

        load_table = kwargs.get('load_table', False)
        if load_table:
            df = pd.read_table(file,
                               nrows=kwargs.get('nrows', 1),
                               header=None)

        elif self.dtype == '.csv' or self.dtype == '.txt':
            df = pd.read_csv(file, header=self.header_iloc,
                             names=self.header_names,
                             nrows=kwargs.get('nrows', 1),
                             on_bad_lines='skip'
                             )
        elif self.dtype == '.xlsx':
            df = pd.read_excel(file, header=self.header_iloc,
                               names=self.header_names,
                               nrows=kwargs.get('nrows', 1))
        else:
            raise TypeError('Invalid data type')

        return df

    def parseDataSets(self, print_banner=True):
        if print_banner:
            self.printSelectionBanner('Parsing Datasets',
                                      options=[])
            print('')

        print('The following data files were found at "../Data and Figures/'
              'sensor_data/"' + self.name + '/raw_data":')
        for file in self.file_list:
            print('..{0}'.format(file.replace(self.path, '')))

        # Load data files and populate a dictionary of unique headers that occur.
        # Top level is ordered by the row index, so if some files have different headers,
        # there will be multiple entries within the particular row index key.
        self.col_headers = {}
        print('\nParsing datasets at "../Data and Figures/sensor_data/"' +
              self.name + '/raw_data"')

        for file in self.file_list:
            df = self.loadDataFile(file)
            file_col_list = list(df.columns)

            for i, col in enumerate(file_col_list):
                if 'col_idx_' + str(i) not in self.col_headers:
                    self.col_headers['col_idx_' + str(i)] = {}

                if col not in self.col_headers['col_idx_' + str(i)]:
                    self.col_headers['col_idx_' + str(i)][col] = {"SDFS_param": None,
                                                             "files": [file]}
                else:
                    self.col_headers['col_idx_' + str(i)][col]["files"].append(file)

        # Create a nested list of unique column names
        col_list = [list(self.col_headers[key].keys()) for key in
                    list(self.col_headers.keys())]
        self.all_col_headers = flatten_list(col_list)

        for i, cols in enumerate(col_list):
            print('..Header(s) at column index {0:d}: {1}'.format(i, cols))

        self.enterContinue()


    def setTimeHeaders(self, print_banner=True):
        if print_banner:
            self.printSelectionBanner('Specify Timestamp columns',
                                      options=[self.end_str, self.del_str])
        # Create a list of time-like columns, update the col_headers list with the
        # datetime_utc type corresponding to the specified header name
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
                self.timestamp_col_headers.append(val)

                # Get a list of the row index locations where the column header name is
                header_loc = [row for row in self.col_headers if val in
                              self.col_headers[row].keys()]
                for key in header_loc:
                    self.col_headers[key][val]['SDFS_param'] = 'DateTime_UTC'
            else:
                print('..Invalid entry. Choose from the following list:')
                print(' ', self.all_col_headers)
                continue
            i += 1

        print('\nTimestamp column list:', self.timestamp_col_headers)
        self.enterContinue()


        #TODO: Once press X, print list of timestamp columns and ask to confirm before moving on

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
                elif sdfs_param == '':
                    valid = True
                    print('..{0} will be dropped'.format(param))
                    self.drop_cols.append(param)
                else:
                    print('..Invalid entry. Choose from the list above.')

            renaming_dict[param] = sdfs_param

            # Get a list of the col index locations where the column header name is
            header_loc = [col for col in self.col_headers if param in
                          self.col_headers[col].keys()]
            for key in header_loc:
                self.col_headers[key][param]['SDFS_param'] = sdfs_param

        #TODO: Print dictionary with renaming scheme, ask to confirm
        # add something like following code block,
        print('')
        print('Configured renaming scheme:')
        self.pp.pprint(renaming_dict)
        self.enterContinue()

        # confirm = self.validateEntry()
        # if confirm == 'n':
        #     valid = False
        #     while valid is False:
        #         iloc = input('Enter column number to edit: ')
        #         if (int(iloc) < 1) or (int(iloc) > n_params):
        #             print('..invalid entry')
        #         else:
        #             valid = True

    # def setColumnHeaders(self, col_type=None, print_banner=True, i=1,
    #                      column_headers=[], reset=False):
    #     """If col_type is '', specify all column headers. If col_type is
    #     'Timestamp', the specified column header names must be in the
    #     previously entered list of all column header names.
    #     """
    #     if print_banner:
    #         if col_type != '':
    #             fmt_col_type = " {:s} ".format(col_type)
    #         else:
    #             fmt_col_type = ' '
    #         self.printSelectionBanner('Set' + fmt_col_type + 'Column Headers',
    #                                   options=[self.end_str, self.del_str])

    #     col_type = col_type.lower()

    #     i = int(i)
    #     esc = False
    #     while esc is False:
    #         val = input('Enter ' + col_type + ' column ' + str(i) +
    #                     ' header name: ')

    #         # Shortcut method: specify first entry as list of parameter names
    #         # rather than entering in one by one
    #         if val.startswith('[') and val.endswith(']'):
    #             # Since input sets val to string, have to work backwards a bit
    #             # to recover the list as type list
    #             column_headers = val[1:-1].replace("'", '').replace(" ",
    #                                 '').replace('\n', '').split(',')
    #             val = 'X'

    #         if val == 'X':
    #             print(column_headers)
    #             confirm = self.validateEntry()
    #             esc = True
    #         elif val == 'D':
    #             try:
    #                 column_headers.pop(i-2)
    #                 i -= 1
    #                 print('..deleting ' + col_type + ' column ' + str(i) +
    #                       ' header name')
    #                 print('..updated column headers list: ',
    #                       column_headers)
    #             except IndexError:
    #                 print('Empty list, no entries to delete')
    #                 pass
    #         elif val == '':
    #             print('..invalid entry')
    #         else:
    #             if col_type == 'timestamp' and val not in self.all_col_headers:
    #                 print('..invalid entry, name not in passed list of '
    #                       'column headers')
    #             else:
    #                 if reset is True:
    #                     column_headers[i-1] = val
    #                     reset = False
    #                 else:
    #                     column_headers.append(val)
    #                 i += 1

    #         if esc is True and len(column_headers) == 0:
    #             print('..warning, ' + col_type + ' column headers list',
    #                   ' is empty')

    #     if col_type == '':
    #         self.all_col_headers = column_headers
    #     else:
    #         self.timestamp_col_headers = column_headers

    #     if confirm == 'n':
    #         valid = False
    #         while valid is False:
    #             iloc = input('Enter column number to edit: ')
    #             if (int(iloc) < 1) or (int(iloc) > len(column_headers)):
    #                 print('..invalid entry')
    #             else:
    #                 valid = True
    #         self.setColumnHeaders(col_type, print_banner=False,
    #                               i=iloc, column_headers=column_headers,
    #                               reset=True)
    #     print('')

    # def setColumnRenaming(self, print_banner=True):
    #     if print_banner:
    #         note = ('Note, timestamp columns should be skipped by pressing '
    #                 'enter. These columns are assigned as the index during '
    #                 'ingestion, and as a result, timestamp columns are '
    #                 'redundant and should be dropped.')
    #         self.printSelectionBanner('Configure Column Renaming Scheme',
    #                                   options=[self.skip_str, note,
    #                                            'Choose from the followng list',
    #                                            self.params])
    #     self.col_rename_dict = {}
    #     self.drop_cols = []
    #     for col in self.all_col_headers:
    #         invalid = True
    #         while invalid is True:
    #             val = input('Enter parameter associated with "' + col + '": ')
    #             if val == '':
    #                 self.drop_cols.append(col)
    #                 print('.."' + col + '" will be dropped')
    #                 if self.drop_cols == self.all_col_headers:
    #                     print('..warning, all columns will be dropped')
    #                 invalid = False
    #                 continue
    #             elif val not in self.params:
    #                 invalid = True
    #                 print('..invalid entry, parameter name must be in the '
    #                       'above list')
    #             else:
    #                 invalid = False
    #                 self.col_rename_dict[col] = val

    #     print('Configured renaming scheme:', self.col_rename_dict)
    #     confirm = self.validateEntry()
    #     if confirm == 'n':
    #         self.setColumnRenaming(print_banner=False)
    #     print('')

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
                    self.drop_cols.append(col)
                    if self.drop_cols == self.timestamp_col_headers:
                        print('..warning, all columns will be dropped')
                    invalid = False
                    continue
                else:
                    confirm = self.validateEntry()
                    if confirm == 'y':
                        invalid = False
                        self.time_format_dict[col] = val

        print('')
        print('Configured formatting scheme:')
        self.pp.pprint(self.time_format_dict)
        self.enterContinue()


    def setDataType(self):
        self.printSelectionBanner('Select Data Type',
                                  options=[self.data_types])

        valid = False
        while valid is False:
            val = input('Enter the sensor data type from the list of supported data types: ')
            if str(val) not in self.data_types:
                print('..invalid entry, please enter one of the listed data '
                      'types')
            else:
                self.dtype = val
                print('')
                print('Selected data type:', self.dtype)
                confirm = self.validateEntry()
                if confirm == 'y':
                    valid = True
            print('')

    def exportSetup(self):
        self.printSelectionBanner('Setup Configuration')
        self.config_dict = self.__dict__.copy()
        del self.config_dict['end_str']
        del self.config_dict['del_str']
        del self.config_dict['skip_str']
        del self.config_dict['header_names']

        outpath = (self.path + '\\Data and Figures\\sensor_data\\'
                   + self.name)
        filename = self.name + '_setup.json'
        outpath = os.path.join(outpath, filename)
        print('')
        print('..writing setup configuration to the following path:')
        print(outpath)
        with open(outpath, 'w') as outfile:
            self.config_dict = json.dumps(self.config_dict, indent=4)
            outfile.write(self.config_dict)

if __name__ == '__main__':
    # sensor_name = 'Example_Make_Model'
    # work_path = r'C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\test_dir'

    # test = Setup(name=sensor_name,
    #              path=work_path)

    work_path = r"C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Public_Sensor_Evaluation"

    sensor_name = 'Vaisala_AQT420'

    test = Setup(name=sensor_name,
                 path=work_path)
