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
  Thu Sep 23 08:34:17 2021
Last Updated:
  Thu Sep 23 08:34:17 2021
"""
import os
import json
from sensortoolkit import lib_utils


class ReferenceMonitor:
    """

    Args:
        project_path (TYPE, optional):
            DESCRIPTION. Defaults to None.
        data_source (TYPE, optional):
            The name of the data service that
            reference measurements were acquired from. Defaults to None.
            Options:
                - "airnow": Reference data from the AirNow API

                - "aqs": Reference data from U.S. EPA's Air Quality System

                - "airnowtech": Reference data from AirNowTech, files
                  downloaded locally.

                - "local": A catch-all category for datasets stored locally on
                  the user's system.
        site_name (TYPE, optional):
            The name of the air monitoring site. Defaults to None.
        site_id (TYPE, optional):
            The unique identification number for the air monitoring site.
            Typically the AQS Site ID if applicable. Defaults to None.
        **kwargs (TYPE): Additional keyword arguments.

    Raises:
        ValueError: If both the site name and site ID are not None but the
        data source is None, raise ValueError as the source must be
        specified to indicate where reference data are located. Also,
        a ValueError will be raised if the passed data source, site name,
        and site id do not point to a valid reference data subdirectory.

    Returns:
        None.

    """
    _data_sources = ['airnow', 'aqs', 'airnowtech', 'local']

    def __init__(self, project_path=None, data_source=None, site_name=None,
                 site_id=None, **kwargs):

        self.__dict__.update(**kwargs)
        self._kwargs = kwargs

        self._setup_path = None
        self.data_source = data_source
        self.site_name = site_name
        self.site_id = site_id

        if project_path is not None:
            self.project_path = project_path

            if all([self.site_name == None, self.site_id == None,
                    self.data_source == None]):
                print('..reference data source and monitoring site information'
                      ' not specified, run Reference.reference_setup() to continue')
                return

            if self.data_source == None:
                raise ValueError('No reference data source specified, choose'
                                 f' from the following sources: {self._data_sources}')

            if self.site_name == None:
                self.site_name = 'Unspecified Site Name'
            self.site_name = self.site_name.title()
            self._fmt_site_name = self.site_name.replace(' ', '_')

            if self.site_id == None:
                self.site_id = 'Unspecified Site ID'
            self._fmt_site_id = self.site_id.replace('-', '').replace(' ', '_')

            self._ref_data_subfolder = '_'.join([self._fmt_site_name,
                                                self._fmt_site_id])

            self._ref_parent_path = rf"{self.project_path}\Data and Figures\reference_data\{self.data_source}"
            self._ref_raw_path = rf"{self._ref_parent_path}\raw\{self._ref_data_subfolder}"
            self._setup_path = rf"{self._ref_raw_path}\reference_setup.json"

            if not os.path.isdir(os.path.normpath(self._ref_raw_path)):
                raise ValueError(f'No reference data folder with the path {self._ref_raw_path}')

            self._get_ingest_config()

    def _get_ingest_config(self):

        if os.path.isfile(self._setup_path):
            with open(self._setup_path) as p:
                self.setup_data = json.loads(p.read())
                p.close()

    def reference_setup(self):
        if hasattr(self, 'setup_data'):
            print(f'A setup configuration has previously been created for {self.setup_data["site_name"]}')
            print('Do you wish to continue and overwrite the previously created configuration?')
            val = lib_utils.validate_entry()
            if val == 'n':
                return

        setup_config = lib_utils.ReferenceSetup(path=self.project_path)

        self._get_ingest_config()

    @property
    def data_source(self):
        return self._data_source

    @data_source.setter
    def data_source(self, val):


        if val == None:
            self._data_source = val
        elif val.lower() in self._data_sources:
            self._data_source = val.lower()
        else:
            raise ValueError(f'Invalid entry for data source, must be of the'
                             f' following: {self._data_sources}')

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


if __name__ == '__main__':

    work_path = r'C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\test_dir'

    ref = ReferenceMonitor(project_path=work_path)

    # ref = ReferenceMonitor(site_name='Test Site',
    #                 site_id=None,
    #                 data_source='local',
    #                 project_path=work_path)