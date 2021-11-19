# -*- coding: utf-8 -*-
"""
This module contains the AirSensor testing attribute object class.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Sep 15 07:18:41 2021
Last Updated:
  Wed Sep 15 07:18:41 2021
"""
import os
import json
from sensortoolkit import lib_utils
from sensortoolkit import ingest
from sensortoolkit import datetime_utils


class AirSensor:
    """Object for storing and accessing air sensor data and device attributes.

    Args:
        make (str):
            The name of the air sensor manufacturer.
        model (str):
            The name of the air sensor model.
        project_path (str):
            The path to the directory where the user intends to store data,
            figures, and reports relating to the sensor being testing.
            Defaults to None.

    """

    def __init__(self, make, model, project_path=None):

        self.make = make
        self.model = model
        self._setup_path = None

        if self.make is not None and self.model is not None:
            self.name = '_'.join([self.make.replace(' ', '_'),
                                  self.model.replace(' ', '_')])

        if project_path is not None:
            self.project_path = project_path
            self._setup_path = rf"{self.project_path}\data\sensor_data\{self.name}\{self.name}_setup.json"

            self._get_ingest_config()

    def _get_ingest_config(self):

        if os.path.isfile(self._setup_path):
            with open(self._setup_path) as p:
                self.setup_data = json.loads(p.read())
                p.close()
            self.serials = self.setup_data['serials']
            self.param_headers = self.setup_data['sdfs_header_names']
            self.create_directories(param_headers=self.param_headers)

    @property
    def setup_data(self):
        return self._setup_data

    @setup_data.setter
    def setup_data(self, config_data):
        if config_data['name'] != self.name:
            raise RuntimeError('Setup file at passed path indicates different '
                               'sensor name: \n..AirSensor name: {0}\n..setup.'
                               'json name: {1}'.format(self.name,
                                                       config_data['name']))
        self._setup_data = config_data

    @property
    def project_path(self):
        return self._project_path

    @project_path.setter
    def project_path(self, path):
        if os.path.isdir(path):
            if os.path.isabs(path):
                self._project_path = path
            else:
                raise ValueError('Invalid project path, path not absolute: '
                                 f'{path}')
        else:
            raise ValueError('Invalid project path, directory not found: '
                             f'{path}')


    def create_directories(self, param_headers=None):
        """Construct parameter-specific subdirectories in the project path.

        Subdirectories are constructed within the ``/figures/[sensor_name]``
        path for SDFS parameters measured by the air sensor. Calls the
        ``sensortoolkit.lib_utils.create_sensor_subdirectories()`` method.

        Args:
            param_headers (list, optional):
                A list of SDFS parameters measured by the air sensor. Defaults
                to None.

        Returns:
            None.

        """
        try:
            self.project_path
        except AttributeError as error_message:
            print(error_message)
            return

        lib_utils.create_sensor_directories(name=self.name,
                                            param=param_headers,
                                            path=self.project_path
                                            )

    def copy_datasets(self, select='directory'):
        """Prompts the user to select files or folders where recorded sensor
        datasets  are located and copies files to the
        ``../data/sensor_data/[sensor_name]/raw_data`` data subdirectory.

        Args:
            select (str, optional):
                The selection scheme for indicating items
                in the location for sensor datasets within the  file explorer
                menu. Options include ``directory`` (the user selects a
                directory and data files within the directory are copied),
                ``recursive directory`` (the user specifies a parent directory
                and all files within folders nested in the parent directory are
                copied over), or ``files`` (the user selects the files that
                they intend to copy over. Defaults to ``directory``.

        Returns:
            None.

        """
        try:
            self.project_path
        except AttributeError as error_message:
            print(error_message)
            return

        lib_utils.copy_datasets(data_type='sensor',
                                name=self.name,
                                path=self.project_path,
                                select=select)

    def sensor_setup(self):
        """Interactive method for configuring sensor data ingestion.

        1. **Selecting File Data Type**:

           Choose the corresponding data file type for recorded sensor
           datasets from ``'.csv'``, ``'.txt'``, ``'.xlsx'``.

        2. **Selecting Data Files**:

           Choose the selection scheme for pointing to recorded data files from
           the following options:

           - ``'directory'``, which will locate and copy all of the data files
             in the specified directory for the indicated data type
           - ``'recursive directory'``, which will locate and copy all data
             files within the specified directory and any subdirectories
             contained within the indicated folder path
           - ``'files'`` which copies over files that the user manually selects
             within a directory.

        3. **Copying Data Files**:

           Recorded sensor datasets are copied from the selected file or folder
           location to the ``../data/sensor_data/[sensor_name]/raw_data``
           directory path.

        4. **Selecting the Column Header Index**:

           Users indicate the integer index position for the row of header
           data in sensor datasets.

        5. **Parsing Sensor Datasets**:

           The first few rows of recorded sensor datasets located in the
           ``../data/sensor_data/[sensor_name]/raw_data`` directory path are
           imported and the names of column headers are located based on the
           indicated head index. A list of unique column headers is stored for
           subsequent reassignment of column header names.

        6. **Specifying Timestamp Columns**:

           Users indicate the column(s) containing date/timestamp information.

        7. **Specifying the Parameter Renaming Scheme**:

           Users indicate the SDFS parameters corresponding to column names
           discovered in step 5. This creates a parameter renaming dictionary
           for reassigning the names of header labels.

        8. **Configuring Timestamp Column Formatting**:

           Users indicate the date/time formatting for date/time column(s)
           indicated in step 6. Formatting should correspond to the
           ``strftime`` formatting keywords located at https://strftime.org/

        9. **Specifying the DateTime Index Time Zone**:

           Users indicate the time zone associated with the date/time
           column(s). Timezones should be valid timezone names recognized by
           the ``pytz`` library.

        10. **Configuring Sensor Serial Identifiers**:

            Users should select unique serial identifiers corresponding to
            each sensor unit in the testing group. Identifying keywords for
            each sensor unit should be indicated within the recorded sensor
            dataset file names.

        11. **Saving the Setup Configuration to** ``setup.json``:

            The setup configuration specified by the user is saved to a
            ``setup.json`` file for subsequent use by the ingestion module for
            importing recorded sensor datasets and conversion to SDFS datasets.

        Returns:
            None.

        """
        if hasattr(self, 'setup_data'):
            print(f'A setup configuration has previously been created for {self.name}')
            print('Do you wish to continue and overwrite the previously created configuration?')
            val = lib_utils.validate_entry()
            if val == 'n':
                return

        setup_config = lib_utils.SensorSetup(name=self.name,
                                             path=self.project_path)

        self._get_ingest_config()

    def load_data(self, load_raw_data, write_to_file, **kwargs):
        """Import sensor datasets and load to the ``AirSensor.data`` attribute.

        Args:
            load_raw_data (bool):
                If true, processed (SDFS formatted) sensor datasets will be
                saved as csv files to the ``/data/sensor_data/[sensor_name]/processed_data``
                directory. If false, formatted datasets will not be saved to
                the user’s hard drive.
            write_to_file (bool):
                If true, raw data (datasets as originally recorded) in the
                appropriate subdirectory will be loaded and 1-hour and 24-hour
                averages will be computed. If false, processed data will be
                loaded.
            **kwargs (dict):

        Returns:
            None.

        """
        custom_ingest = kwargs.get('custom_ingest_module', False)

        if not custom_ingest:
            try:
                self.setup_data
            except AttributeError:
                print(f'No setup configuration specified for {self.name}.')
                print("Run the 'AirSensor.sensor_setup()' module before loading"
                      " sensor data.")
                return

        # path to raw sensor data
        self._data_path = os.path.join(self.project_path, 'data',
                                    'sensor_data', self.name,
                                    'raw_data', '')
        # path to processed sensor data
        self._processed_path = os.path.join(self.project_path, 'data',
                                         'sensor_data', self.name,
                                         'processed_data', '')

        df_tuple = ingest.sensor_import(
                                        sensor_name=self.name,
                                        sensor_serials=self.serials,
                                        load_raw_data=load_raw_data,
                                        data_path=self._data_path,
                                        processed_path=self._processed_path,
                                        write_to_file=write_to_file,
                                        **kwargs)
        self._set_data(df_tuple)

    def _set_data(self, data_obj):
        self.data = {}
        for dataset_group in data_obj:
            # Check that the intervals in the datasets are similar
            t_intervals = [datetime_utils.get_timestamp_interval(df)
                           for df in dataset_group]

            same_t_interval = all(interval==t_intervals[0] for
                                  interval in t_intervals)

            if not same_t_interval:
                print('Warning, timestamp intervals not consistent.')
                print(t_intervals)
            else:
                t_interval = t_intervals[0]
                self.data[t_interval] = {}
                for serial_id, df in zip(self.serials.values(), dataset_group):
                    self.data[t_interval][serial_id] = df

        self.recording_interval = list(self.data.keys())[0]

if __name__ == '__main__':
    work_path = r'C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\sensortoolkit_testing'
