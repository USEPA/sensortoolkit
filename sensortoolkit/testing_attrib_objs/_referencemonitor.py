# -*- coding: utf-8 -*-
"""
Description.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Thu Sep 23 08:34:17 2021
Last Updated:
  Thu Sep 23 08:34:17 2021
"""
import os
import json
import pandas as pd
from sensortoolkit import lib_utils
from sensortoolkit.reference import ref_api_query, load_ref_dataframes
from sensortoolkit.param import Parameter
from sensortoolkit.datetime_utils import interval_averaging


class ReferenceMonitor:
    """
    Object for storing and accessing reference monitor (FRM/FEM) data as well as
    instrument and monitoring site attributes.

    Args:
        project_path (str, optional):
            The path to the directory where the user intends to store data,
            figures, and reports relating to the sensor being testing.
            Defaults to None.
        data_source (str, optional):
            The name of the data service that
            reference measurements were acquired from. Defaults to None.

            Options:

                - ``airnow``: Reference data from the AirNow API

                - ``aqs``: Reference data from U.S. EPA's Air Quality System

                - ``airnowtech``: Reference data from AirNowTech, files
                  downloaded locally.

                - ``local``: A catch-all category for datasets stored locally on
                  the user's system.

        site_name (str, optional):
            The name of the air monitoring site. Defaults to None.
        site_id (str, optional):
            The unique identification number for the air monitoring site.
            Typically the AQS Site ID if applicable. Defaults to None.
        **kwargs (TYPE): Additional keyword arguments.

    Raises:
        ValueError: If both the site name and site ID are not None but the
            data source is None, raise ValueError as the source must be
            specified to indicate where reference data are located. Also,
            a ValueError will be raised if the passed data source, site name,
            and site id do not point to a valid reference data subdirectory.

    """
    _data_sources = ['airnow', 'aqs', 'airnowtech', 'local']

    def __init__(self, project_path=None, data_source=None, site_name=None,
                 site_id=None, **kwargs):

        self.__dict__.update(**kwargs)
        self._kwargs = kwargs

        self._setup_path = None
        self.data_source = data_source
        self.site_name = site_name

        if site_id is not None:
            lib_utils.check_type(site_id, accept_types=[int, str])
            site_id = str(site_id)
        self.site_id = site_id

        self.data = {'PM': {'1-hour': pd.DataFrame(),
                            '24-hour':  pd.DataFrame()},
                    'Gases': {'1-hour': pd.DataFrame(),
                              '24-hour':  pd.DataFrame()},
                    'Met': {'1-hour': pd.DataFrame(),
                            '24-hour':  pd.DataFrame()}
                    }

        if project_path is not None:
            self.project_path = project_path

            if all([self.site_name == None, self.site_id == None,
                    self.data_source == None]):
                print('..reference data source and monitoring site information'
                      ' not specified, run ReferenceMonitor.reference_setup() to continue')
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

            self._ref_parent_path = rf"{self.project_path}\data\reference_data\{self.data_source}"
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
        self.setup_data = json.loads(setup_config.config_dict)

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

    def get_method_name(self, param):
        classifier = Parameter(param).classifier
        if self.data[classifier]['1-hour'].empty:
            print('No reference data found, load data via ReferenceMontior.load_data()')
            return
        try:
            method_name = self.data[classifier]['1-hour'][param + '_Method'].dropna().unique()[0]

            ref_replace = {'Thermo Scientific ': '',
                   'Dichotomous': 'Dichot'}

            for key, value in zip(ref_replace.keys(), ref_replace.values()):
                method_name = method_name.replace(key, value)

        except IndexError:
            method_name = 'Unknown Reference'
        except KeyError:
            method_name = None
            print(f'No reference monitor found for {param}')

        return method_name


    def query_aqs(self, username, key, param_list, bdate, edate,
                  site_id=None, query_met_data=True):
        """Send a data query to the AQS API.

        Args:
            username (str):
                The email account registered with the API service.
            key (str):
                The API authentication key code.
            param_list (list):
                A list of SDFS parameters measured by reference monitors at
                the monitoring site for which data will be loaded.
            bdate (str):
                The beginning date (“YYYY-MM-DD” format) for the sensor
                testing period.
            edate (str):
                The ending date (“YYYY-MM-DD” format) for the sensor testing
                period.
            site_id (dict, optional):
                The AQS site ID for the air monitoring site from which
                reference measurements will be returned by the API. The site
                ID is passed as a dictionary with three key-value pairs:

                    - ``'state'``: The two digit FIPS code for the state
                      (leading zero included).
                    - ``'county'``: The three digit FIPS code for the county
                      (leading zeros included) located within the state.
                    - ``'site'``: The four digit AQS site number within the
                      county (leading zeros included).

                .. note::

                    If site_id is not null, the site ID passed will be used
                    instead of any previously configured reference monitor
                    configuration via the
                    ``sensortoolkit.ReferenceMonitor.reference_setup()``
                    method.

            query_met_data (bool, optional):
                If true, meteorological data for temperature and
                relative humidity measurements will be queried in addition to
                parameters passed to param_list. Defaults to true (U.S. EPA’s
                documents for recommended performance testing protocols,
                metrics, and target values encourage users to report
                meteorological conditions for sensor performance evaluations
                and reports).

        Returns:
            None.

        """
        if site_id is None:
            try:
                site_list = self.setup_data['site_aqs'].split('-')
                site_id = {'state': site_list[0],
                                'county': site_list[1],
                                'site': site_list[2]
                            }
            except AttributeError:
                print('Setup configuration does not specify a site AQS ID, run'
                      'ReferenceMonitor.reference_setup() and enter a site ID')
                return

        aqs_param_df = ref_api_query(query_type='AQS',
                                     param=param_list,
                                     bdate=bdate,
                                     edate=edate,
                                     aqs_id=site_id,
                                     username=username,
                                     key=key,
                                     path=self._project_path)

        if not aqs_param_df.empty:
            aqs_d_param_df = interval_averaging(aqs_param_df,
                                                freq='D',
                                                interval_count=24,
                                                thres=0.75)

        if query_met_data:
            aqs_met_df = ref_api_query(query_type='AQS',
                                       param=['Temp', 'RH'],
                                       bdate=bdate,
                                       edate=edate,
                                       aqs_id=site_id,
                                       username=username,
                                       key=key,
                                       path=self._project_path)
            if not aqs_met_df.empty:
                aqs_d_met_df = interval_averaging(aqs_met_df,
                                                  freq='D',
                                                  interval_count=24,
                                                  thres=0.75)

        classifier = Parameter(param_list[0]).classifier

        if not aqs_param_df.empty:
            self.data[classifier]['1-hour'] = aqs_param_df
            self.data[classifier]['24-hour'] = aqs_d_param_df
        if (query_met_data) and (not aqs_met_df.empty):
            self.data['Met']['1-hour'] = aqs_met_df
            self.data['Met']['24-hour'] = aqs_d_met_df

    def query_airnow(self, key, param_list, bdate, edate, bbox=None,
                     bbox_size=0.01):
        """Send a data query to the AirNow API.

        Args:
            key (str):
                The API authentication key code.
            param_list (list):
                A list of SDFS parameters measured by reference monitors at
                the monitoring site for which data will be loaded.
            bdate (str):
                The beginning date (“YYYY-MM-DD” format) for the sensor
                testing period.
            edate (str):
                The ending date (“YYYY-MM-DD” format) for the sensor testing
                period.
            bbox (dict, optional):
                A bounding box of coordinates within which data will be
                queried. Defaults to None. ``bbox`` accepts four key-value
                pair entries, where the following keys should be specified:

                - ``'minLat'``: The northern-most latitude for the bounding
                  box.
                - ``'maxLat'``: The southern-most latitude for the bounding
                  box.
                - ``'minLong'``: The western-most longitude for the bounding
                  box.
                - ``'maxLong'``: The eastern-most longitude for the bounding
                  box.

                Values for each key should be type float.

            bbox_size (float, optional):
                DESCRIPTION. Defaults to 0.01.

        Returns:
            None.

        """

        if bbox is None:
            try:
                site_lat = float(self.setup_data['site_lat'])
                site_lon = float(self.setup_data['site_lon'])

                bbox = {"minLat": round(float(site_lat - bbox_size), 3),
                        "maxLat": round(float(site_lat + bbox_size), 3),
                        "minLong": round(float(site_lon - bbox_size), 3),
                        "maxLong": round(float(site_lon + bbox_size), 3)}
            except AttributeError:
                print('Setup configuration does not specify site latitude '
                      'and/or longitude, run ReferenceMonitor.reference_setup'
                      '() and enter a site ID')
                return


        airnow_df = ref_api_query(query_type='AirNow',
                                  param=param_list,
                                  bdate=bdate,
                                  edate=edate,
                                  airnow_bbox=bbox,
                                  key=key,
                                  path=self._project_path)

        if not airnow_df.empty:
            airnow_d_df = interval_averaging(airnow_df,
                                              freq='D',
                                              interval_count=24,
                                              thres=0.75)

        classifier = Parameter(param_list[0]).classifier

        if not airnow_df.empty:
            self.data[classifier]['1-hour'] = airnow_df
            self.data[classifier]['24-hour'] = airnow_d_df


    def load_data(self, bdate, edate, param_list, path=None, met_data=True):
        """Load reference data from locally acquired files.

        Args:
            bdate (str):
                The beginning date (“YYYY-MM-DD” format) for the sensor
                testing period.
            edate (str):
                The ending date (“YYYY-MM-DD” format) for the sensor testing
                period.
            param_list (list):
                A list of SDFS parameters measured by reference monitors at
                the monitoring site for which data will be loaded.
            path (str, optional):
                Full path to the data directory where processed reference
                datasets are located. If None (default), will attempt to
                construct path from an existing setup configuration if the
                ``sensortoolkit.ReferenceMonitor.reference_setup()`` method
                was run prior to calling ``load_data()``.

                .. note::

                    If path is not null (i.e., a valid directory path is
                    passed) and a reference monitor configuration was created
                    with
                    ``sensortoolkit.ReferenceMonitor.reference_setup()``
                    prior to running ``load_data()``, the path will point to
                    datasets located at the indicated path instead of
                    datasets pointed to by the path configured by the
                    ``reference_setup()`` method.

            met_data (bool, optional):
                If true, meteorological data will be loaded in addition to
                datasets corresponding to parameters passed to param_list.
                Defaults to true (U.S. EPA’s documents for recommended
                performance testing protocols, metrics, and target values
                encourage users to report meteorological conditions for sensor
                performance evaluations and reports).

        Returns:
            None.

        """
        if path is None:
            try:
                path = os.path.normpath(
                    os.path.join(
                        self.setup_data['path'] +
                        self.setup_data['data_rel_path'].replace('/raw/',
                                                                 '/processed/')
                        )
                    )
            except AttributeError:
                print('Setup configuration does not specify reference data '
                      'source, run ReferenceMonitor.reference_setup()')
                return

        if met_data is True:
            for param in ['Temp', 'RH']:
                if param not in param_list:
                    param_list.append(param)

        classes = []
        for param in param_list:
            if param in Parameter.__param_dict__.keys():
                classes.append(Parameter(param).classifier)
        classes = set(classes)

        bdate = pd.to_datetime(bdate)
        edate = pd.to_datetime(edate)

        data_dict = load_ref_dataframes(bdate, edate, path, classes)

        for classifier in data_dict:
            for interval in data_dict[classifier]:
                df = data_dict[classifier][interval]
                if not df.empty:
                    self.data[classifier][interval] = df


if __name__ == '__main__':

    work_path = r'C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\test_dir'

    ref = ReferenceMonitor(project_path=work_path)

    ref = ReferenceMonitor(site_name='Test Site',
                    site_id=None,
                    data_source='local',
                    project_path=work_path)
