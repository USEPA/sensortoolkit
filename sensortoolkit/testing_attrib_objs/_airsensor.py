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
import pandas as pd
from sensortoolkit import calculate
from sensortoolkit import lib_utils
from sensortoolkit import ingest
from sensortoolkit import datetime_utils
from sensortoolkit import presets as _presets
from pathlib import Path


class AirSensor:
    """Object for storing and accessing air sensor data and device attributes.

    Args:
        make (str):
            The name of the air sensor manufacturer.
        model (str):
            The name of the air sensor model.

    """
    # Default project path set to library path, should be something like
    # 'C:/Users/.../Anaconda3/Lib/site-packages/sensortoolkit'
    default_proj_path = Path(__file__).parent.parent

    def __init__(self, make, model):

        self.make = make
        self.model = model
        self._setup_path = None
        self.bdate = None
        self.edate = None
        self.data = {}
        self.recording_interval = None
        self.project_path = _presets._project_path

        if self.make is not None and self.model is not None:
            self.name = '_'.join([self.make.replace(' ', '_'),
                                  self.model.replace(' ', '_')])

        if Path(self.project_path) == self.default_proj_path:
            print('..Warning, project path has not been specified. Use the '
                  'sensortoolkit.presets.set_project_path() method to assign '
                  'a directory path.')
            return

        self._setup_path = os.path.join(self.project_path, 'data', 'sensor_data',
                                        self.name, f'{self.name}_setup.json')

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
        if _presets._project_path != self._project_path:
            print('[Note] Project path changed by user, setting AirSensor '
                  'instance project path to new location')
            self._project_path = _presets._project_path

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
            path = self.project_path
        except AttributeError as error_message:
            print(error_message)
            return

        lib_utils.create_sensor_directories(name=self.name,
                                            param=param_headers,
                                            path=path
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
            path = self.project_path
        except AttributeError as error_message:
            print(error_message)
            return

        lib_utils.copy_datasets(data_type='sensor',
                                name=self.name,
                                path=path,
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

        self.data = ingest.sensor_import(sensor_name=self.name,
                                        sensor_serials=self.serials,
                                        load_raw_data=load_raw_data,
                                        data_path=self._data_path,
                                        processed_path=self._processed_path,
                                        write_to_file=write_to_file,
                                        **kwargs)

        # Compute dewpoint
        if 'Temp' in self.param_headers and 'RH' in self.param_headers:
            for interval in self.data:

                for serial in self.data[interval]:
                    if not self.data[interval][serial].empty:
                        self.data[interval][serial] = calculate.dewpoint(
                                                        self.data[interval][serial])

        self._set_data()

    def _set_data(self):

        for interval in self.data.copy():
            t_intervals = [datetime_utils.get_timestamp_interval(df)
                           for df in self.data[interval].values() if df is not None]
            t_interval_series = pd.Series(t_intervals)
            t_interval_mode = t_interval_series.mode()
            if t_interval_mode.shape != (1,):
                print('Warning, timestamp intervals not consistent.')
                print(t_intervals)
            else:
                t_mode = t_interval_mode.values[0]
                t_interval = t_mode
                self.data[t_interval] = self.data.pop(interval)

        self.recording_interval = list(self.data.keys())[0]

        self._check_empty_datasets()

        eval_bdate, eval_edate = datetime_utils.timeframe_search(
                                            self.data['1-hour'].values())
        self.bdate = pd.to_datetime(eval_bdate)
        self.edate = pd.to_datetime(eval_edate)

    def _check_empty_datasets(self):

        empty_datasets = {}
        for key, serial in self.serials.items():
            empty_datasets[serial] = {}
            for interval in self.data.keys():
                dataset = self.data[interval][serial]
                empty_datasets[serial][interval] = dataset.empty

        for sensor_to_drop in empty_datasets.keys():
            if all(empty_datasets[sensor_to_drop].values()) is True:
                print(f'..empty datasets detected for {sensor_to_drop}, may be '
                      'due to user-specified evaluation period concatenation')
                print(f'..dropping {sensor_to_drop} from evaluation group')
                serial_loc = [key for (key, val) in self.serials.items()
                              if val == sensor_to_drop][0]

                # Remove serial corresponding to sensor with empty datasets
                # from serial dict
                self.serials.pop(serial_loc)
                # Reorder serial IDs
                self.serials = {str(i): serial_id for i, (key, serial_id)
                                in enumerate(self.serials.items(), 1)}

                # Remove empty datasets from data object
                for interval in self.data.copy():
                    for serial_id in self.data[interval].copy():
                        if serial_id == sensor_to_drop:
                            self.data[interval].pop(serial_id)
