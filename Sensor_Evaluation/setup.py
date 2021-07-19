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
  Mon Jul 19 08:25:55 2021
Last Updated:
  Mon Jul 19 08:25:55 2021
"""
from textwrap import wrap
import json


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
    data_types = {'1': '.csv', '2': '.txt', '3': '.xlsx'}
    __banner_w__ = 79

    def __init__(self):
        self.name = None
        self.dtype = None
        self.param_col_headers = []
        self.timestamp_col_headers = []
        self.configSensor()

    def configSensor(self):
        self.setSensorName()
        self.setColumnHeaders(col_type='Parameter')
        self.setParamColumnRenaming()
        self.setColumnHeaders(col_type='Timestamp', column_headers=[])
        self.setDateTimeFormat()
        self.setDataType()
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

    def printSelectionBanner(self, select_type, options=[]):

        self.end_str = '..press X to end adding entries'
        self.del_str = '..press D to delete the previous entry'
        self.skip_str = '..press enter to skip columns that will be dropped'

        banner_c = int(self.__banner_w__ / 2)
        select_len = len(select_type)
        select_start = banner_c - int(select_len / 2) - 1
        n_left, n_right = select_start, select_start

        if select_len % 2 != 0:
            n_right -= 1

        print(n_left*'=' + ' ' + select_type + ' ' + n_right*'=')
        print('Options\n-------')
        options = ['\n'.join(wrap(str(l),
                             width=self.__banner_w__)) for l in options]
        for line in options:
            print(line)
        print(self.__banner_w__*'=')

    def setSensorName(self):
        self.printSelectionBanner('Set Sensor Name', options=[''])
        confirm = 'n'
        while confirm == 'n':
            self.name = input('Enter the name of the sensor: ')
            print('')
            print('Sensor name: ' + self.name)
            confirm = self.validateEntry()
        print('')

    def setColumnHeaders(self, col_type=None, print_banner=True, i=1,
                         column_headers=[], reset=False):
        if print_banner:

            self.printSelectionBanner('Set ' + col_type + ' Column Headers',
                                      options=[self.end_str, self.del_str])

        col_type = col_type.lower()
        i = int(i)
        esc = False
        while esc is False:
            val = input('Enter ' + col_type + ' column ' + str(i) +
                        ' header name: ')

            if val == 'X':
                print(column_headers)
                confirm = self.validateEntry()
                esc = True
            elif val == 'D':
                try:
                    column_headers.pop(i-2)
                    i -= 1
                    print('..deleting ' + col_type + ' column ' + str(i) +
                          ' header name')
                    print('..updated column headers list: ',
                          column_headers)
                except IndexError:
                    print('Empty list, no entries to delete')
                    pass
            elif val == '':
                print('..invalid entry')
            else:
                if reset is True:
                    column_headers[i-1] = val
                    reset = False
                else:
                    column_headers.append(val)
                i += 1

            if esc is True and len(column_headers) == 0:
                print('..warning, ' + col_type + ' column headers list',
                      ' is empty')

        if col_type == 'parameter':
            self.param_col_headers = column_headers
        else:
            self.timestamp_col_headers = column_headers

        if confirm == 'n':
            valid = False
            while valid is False:
                iloc = input('Enter column number to edit: ')
                if (int(iloc) < 1) or (int(iloc) > len(column_headers)):
                    print('..invalid entry')
                else:
                    valid = True
            self.setColumnHeaders(col_type, print_banner=False,
                                  i=iloc, column_headers=column_headers,
                                  reset=True)
        print('')

    def setParamColumnRenaming(self, print_banner=True):
        if print_banner:
            self.printSelectionBanner('Configure Parameter Column Renaming',
                                      options=[self.skip_str,
                                               'Choose from the followng list',
                                               self.params])
        self.param_rename_dict = {}
        self.drop_cols = []
        for col in self.param_col_headers:
            invalid = True
            while invalid is True:
                val = input('Enter parameter associated with "' + col + '": ')
                if val == '':
                    self.drop_cols.append(col)
                    print('.."' + col + '" will be dropped')
                    if self.drop_cols == self.param_col_headers:
                        print('..warning, all columns will be dropped')
                    invalid = False
                    continue
                elif val not in self.params:
                    invalid = True
                    print('..invalid entry, parameter name must be in the '
                          'above list')
                else:
                    invalid = False
                    self.param_rename_dict[col] = val

        print('Configured renaming scheme:', self.param_rename_dict)
        confirm = self.validateEntry()
        if confirm == 'n':
            self.setParamColumnRenaming(print_banner=False)
        print('')

    def setDateTimeFormat(self):
        self.printSelectionBanner('Configure Timestamp Column Formatting',
                                  options=[self.skip_str])

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

        print('Configured formatting scheme:', self.time_format_dict)
        print('')

    def setDataType(self):
        self.printSelectionBanner('Select Data Type',
                                  options=[self.data_types])

        while self.dtype is None:
            val = input('Enter the number associated with the data type: ')
            if str(val) not in self.data_types:
                print('..invalid entry, please enter an integer')
            else:
                self.dtype = self.data_types[val]

        print('Selected data type:', self.dtype)
        print('')

    def exportSetup(self):
        self.printSelectionBanner('Setup Configuration')
        self.config_dict = self.__dict__.copy()
        del self.config_dict['end_str']
        del self.config_dict['del_str']
        del self.config_dict['skip_str']

        #today = se.Get_Date()

        # check if sensor-specific subfolder exists
        #if not os.path.exists(self.stats_path):
        #    os.makedirs(self.stats_path)

        with open('test_setup.json', 'w') as outfile:
            self.config_dict = json.dumps(self.config_dict, indent=4)
            outfile.write(self.config_dict)

if __name__ == '__main__':
    test = Setup()
