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
  Wed Sep 15 07:18:41 2021
Last Updated:
  Wed Sep 15 07:18:41 2021
"""
import os
import json
from sensortoolkit.param import Parameter
from sensortoolkit import lib_utils
from sensortoolkit import sensor_ingest
from sensortoolkit import datetime_utils


class AirSensor:
    def __init__(self, make, model, project_path=None, **kwargs):
        """


        Args:
            make (str): The name of the device manufacturer.
            model (str): The name of the sensor model.
            **kwargs (TYPE): DESCRIPTION.

        Returns:
            None.

        """
        self.__dict__.update(**kwargs)
        self._kwargs = kwargs

        self.make = make
        self.model = model
        self._setup_path = None

        if self.make is not None and self.model is not None:
            self.name = '_'.join([self.make.replace(' ', '_'),
                                  self.model.replace(' ', '_')])

        if project_path is not None:
            self.project_path = project_path
            self._setup_path = rf"{self.project_path}\Data and Figures\sensor_data\{self.name}\{self.name}_setup.json"

            self._get_ingest_config()

    def _get_ingest_config(self):

        if os.path.isfile(self._setup_path):
            with open(self._setup_path) as p:
                self.setup_data = json.loads(p.read())
                p.close()
            self.serials = self.setup_data['serials']
            self.param_headers = self.setup_data['sdfs_header_names']
            self.create_directories(param_headers=self.param_headers)

        # elif self._kwargs.get('setup_data'):
        #     self.setup_data = self._kwargs.get('setup_data')
        #     self.serials = self.setup_data['serials']
        #     self.param_headers = self.setup_data['sdfs_header_names']
        #     self.create_directories(param_headers=self.param_headers)

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
        try:
            self.project_path
        except AttributeError as error_message:
            print(error_message)
            return

        lib_utils.copy_datasets(name=self.name,
                                path=self.project_path,
                                select=select)

    def sensor_setup(self):
        if hasattr(self, 'setup_data'):
            print(f'A setup configuration has previously been created for {self.name}')
            print('Do you wish to continue and overwrite the previously created configuration?')
            val = lib_utils.validate_entry()
            if val == 'n':
                return

        setup_config = lib_utils.Setup(name=self.name,
                                       path=self.project_path)

        self._get_ingest_config()

    # Experimental
    def load_data(self, load_raw_data, write_to_file, **kwargs):
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
        self._data_path = os.path.join(self.project_path, 'Data and Figures',
                                    'sensor_data', self.name,
                                    'raw_data', '')
        # path to processed sensor data
        self._processed_path = os.path.join(self.project_path, 'Data and Figures',
                                         'sensor_data', self.name,
                                         'processed_data', '')

        df_tuple = sensor_ingest.sensor_import(
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


class ReferenceMethod:
    def __init__(self):
        pass



if __name__ == '__main__':
    work_path = r'C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\test_dir'

    EMM = AirSensor('Example_Make', 'Model',
                     project_path=work_path)

    # test_sensor = AirSensor('test', 'sensor',
    #                         project_path=work_path)
    # test_sensor.create_directories()
    # test_sensor.copy_datasets()
    # test_sensor.sensor_setup()

    EMM.load_data(load_raw_data=False, tzone_shift=5, write_to_file=False)