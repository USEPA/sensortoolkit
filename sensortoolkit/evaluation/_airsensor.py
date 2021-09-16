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


class AirSensor:
    def __init__(self, make, model, param_headers, **kwargs):
        """


        Args:
            make (str): The name of the device manufacturer.
            model (str): The name of the sensor model.
            param_headers (TYPE): DESCRIPTION.
            **kwargs (TYPE): DESCRIPTION.

        Returns:
            None.

        """
        self.__dict__.update(**kwargs)
        self._kwargs = kwargs

        self.make = make
        self.model = model
        self.param_headers = param_headers
        self.setup_path = None

        if self.make is not None and self.model is not None:
            self.name = '_'.join([self.make.replace(' ', '_'),
                                  self.model.replace(' ', '_')])

        if self._kwargs.get('project_path'):
            self.project_path = self._kwargs.get('project_path')
            self.setup_path = rf"{self.project_path}\Data and Figures\sensor_data\{self.name}\{self.name}_setup.json"

        self._get_ingest_config()

    @property
    def param_headers(self):
        return self._param_headers

    @param_headers.setter
    def param_headers(self, labels):
        if isinstance(labels, str):
            self._param_headers = [labels]
        elif isinstance(labels, list):
            self._param_headers = labels
        else:
            raise TypeError('Invalid type for "param_headers". Must be either'
                            ' type str or list of strings.')

        for label in self._param_headers:
            valid_label = self._check_param_headers(label)
            if not valid_label:
                sdfs_params= list(Parameter.__param_dict__.keys())
                raise NameError('Invalid parameter label {0}. Name must be one'
                                ' of the following: {1}'.format(label,
                                                                sdfs_params))

    def _check_param_headers(self, label):
        test_param = Parameter(label)

        valid = bool(test_param.classifier)
        return valid

    def _get_ingest_config(self):

        if os.path.isfile(self.setup_path):
            with open(self.setup_path) as p:
                self.setup_data = json.loads(p.read())
                self.serials = self.setup_data['serials']
                p.close()
        elif self._kwargs.get('setup_data'):
            self.setup_data = self._kwargs.get('setup_data')
            self.serials = self.setup_data['serials']

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


    def create_directories(self):
        try:
            self.project_path
        except AttributeError as error_message:
            print(error_message)
            return

        lib_utils.create_sensor_directories(name=self.name,
                                            param=self.param_headers,
                                            path=self.project_path)

    def copy_datasets(self):
        try:
            self.project_path
        except AttributeError as error_message:
            print(error_message)
            return

        lib_utils.copy_datasets(name=self.name,
                                path=self.project_path)

    def sensor_setup(self):
        setup_config = lib_utils.Setup(name=self.name,
                                       path=self.project_path)

        self._get_ingest_config()


class ReferenceMethod:
    def __init__(self):
        pass


if __name__ == '__main__':
    work_path = r'C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\test_dir'
    setup_path = rf"{work_path}\Data and Figures\sensor_data\Example_Make_Model\Example_Make_Model_setup.json"

    # EMM = AirSensor('Example_Make', 'Model', param_headers=['PM25', 'O3'],
    #                  setup_path=setup_path, project_path=work_path)

    test_sensor = AirSensor('test', 'sensor', param_headers=['PM25', 'O3'],
                            project_path=work_path)
    # test_sensor.create_directories()
    # test_sensor.copy_datasets()
    # test_sensor.sensor_setup()