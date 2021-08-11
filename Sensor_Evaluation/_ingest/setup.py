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
        self.all_col_headers = []
        self.timestamp_col_headers = []
        self.configSensor()

    def configSensor(self):
        self.setSensorName()
        #self.setDeploymentPeriod()
        self.setHeaderIndex()
        self.setColumnHeaders(col_type='')  # Specify all header column names
        self.setColumnRenaming()
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

        flier = (n_left*'=' + ' ' + select_type + ' ' + n_right*'=')
        print(flier)
        print('Options\n-------')
        options = ['\n'.join(wrap(str(l),
                             width=self.__banner_w__)) for l in options]
        for line in options:
            print(line)
        print(len(flier)*'=')

    def setSensorName(self):
        self.printSelectionBanner('Set Sensor Name', options=[''])
        confirm = 'n'
        while confirm == 'n':
            self.name = input('Enter the name of the sensor: ')
            print('')
            print('Sensor name: ' + self.name)
            confirm = self.validateEntry()
        print('')

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

        print('Header row index:', str(self.header_iloc))
        confirm = self.validateEntry()
        if confirm == 'n':
            self.setHeaderIndex(print_banner=False)
        print('')

    def setColumnHeaders(self, col_type=None, print_banner=True, i=1,
                         column_headers=[], reset=False):
        """If col_type is '', specify all column headers. If col_type is
        'Timestamp', the specified column header names must be in the
        previously entered list of all column header names.
        """
        if print_banner:
            if col_type != '':
                fmt_col_type = " {:s} ".format(col_type)
            else:
                fmt_col_type = ' '
            self.printSelectionBanner('Set' + fmt_col_type + 'Column Headers',
                                      options=[self.end_str, self.del_str])

        col_type = col_type.lower()

        i = int(i)
        esc = False
        while esc is False:
            val = input('Enter ' + col_type + ' column ' + str(i) +
                        ' header name: ')

            # Shortcut method: specify first entry as list of parameter names
            # rather than entering in one by one
            if val.startswith('[') and val.endswith(']'):
                # Since input sets val to string, have to work backwards a bit
                # to recover the list as type list
                column_headers = val[1:-1].replace("'", '').replace(" ",
                                    '').replace('\n', '').split(',')
                val = 'X'

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
                if col_type == 'timestamp' and val not in self.all_col_headers:
                    print('..invalid entry, name not in passed list of '
                          'column headers')
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

        if col_type == '':
            self.all_col_headers = column_headers
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

    def setColumnRenaming(self, print_banner=True):
        if print_banner:
            note = ('Note, timestamp columns should be skipped by pressing '
                    'enter. These columns are assigned as the index during '
                    'ingestion, and as a result, timestamp columns are '
                    'redundant and should be dropped.')
            self.printSelectionBanner('Configure Column Renaming Scheme',
                                      options=[self.skip_str, note,
                                               'Choose from the followng list',
                                               self.params])
        self.col_rename_dict = {}
        self.drop_cols = []
        for col in self.all_col_headers:
            invalid = True
            while invalid is True:
                val = input('Enter parameter associated with "' + col + '": ')
                if val == '':
                    self.drop_cols.append(col)
                    print('.."' + col + '" will be dropped')
                    if self.drop_cols == self.all_col_headers:
                        print('..warning, all columns will be dropped')
                    invalid = False
                    continue
                elif val not in self.params:
                    invalid = True
                    print('..invalid entry, parameter name must be in the '
                          'above list')
                else:
                    invalid = False
                    self.col_rename_dict[col] = val

        print('Configured renaming scheme:', self.col_rename_dict)
        confirm = self.validateEntry()
        if confirm == 'n':
            self.setColumnRenaming(print_banner=False)
        print('')

    def setDateTimeFormat(self):
        cite = ('..format code list: https://docs.python.org/3/library/'
                'datetime.html#strftime-and-strptime-format-codes')
        epoch = ('..If a timestamp column is formatted as the number of '
                 'seconds since the Unix epoch (1 Jan. 1970), enter "epoch"')
        self.printSelectionBanner('Configure Timestamp Column Formatting',
                                  options=[cite, epoch, self.skip_str])

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
        self.name
        print('..writing setup configuration to ' + self.name + '_setup.json')
        with open(self.name + '_setup.json', 'w') as outfile:
            self.config_dict = json.dumps(self.config_dict, indent=4)
            outfile.write(self.config_dict)

if __name__ == '__main__':
    test = Setup()
