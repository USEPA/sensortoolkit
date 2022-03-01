# -*- coding: utf-8 -*-
"""This module contains the parameter object, which is used to keep track of
attributes pertaining to the parameter or pollutant for which sensor data are
being evaluated.

Resources
---------

1. A list of AQS parameter codes is located at
   `<https://aqs.epa.gov/aqsweb/documents/codetables/parameters.html>`_

2. A list of AQS unit codes is located at
   `<https://aqs.epa.gov/aqsweb/documents/codetables/units.html>`_


===============================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Sep  1 15:47:14 2021
Last Updated:
  Wed Sep  1 15:47:14 2021
"""
import os
import json
import pandas as pd
import pathlib
from sensortoolkit.lib_utils import validate_entry
from ._targets import ParameterTargets
from sensortoolkit import _param_dict
from sensortoolkit import _app_data_dir

class Parameter:
    """Object for accessing parameter attributes.

    Here, parameters are defined as measurable environmental quantities such
    as pollutants or meteorological conditions for which air sensors and
    reference instrumentation may collect measurements at regular sampling
    intervals.

    Args:
        param (str):
            The name of a parameter. Passing an SDFS parameter will initialize
            a parameter instance with preset parameter attributes. Non-SDFS
            parameters will require user-input for specifying these attributes.
        set_units (bool, optional):
            If true, will attempt to assign units to the parameter. If the
            parameter name is not recognized as an SDFS parameter and set_units
            is True, the user will be prompted to enter the units for the
            parameter instance. Defaults to True.

    Attributes:
        name (str):
            The name of the parameter (e.g., ``'PM25'``).
        format_name (str):
            A formatted expression for the parameter used for displaying the
            name of the parameter on plots (e.g., ``'PM$_{2.5}$'``).
        format_baseline (str):
            For ``format_name``, contains the baseline component of the
            parameter name (e.g., ``'PM'`` for fine particulate matter)
        format_subscript (str):
            For ``format_name``, contains the subscripted component of the
            parameter name (e.g., ``'2.5'`` for fine particulate matter)
        classifier (str):
            A term for sorting the parameter into one of three environmental
            parameter classifications, either 'PM' for particulate matter
            pollutants, 'Gases' for gaseous pollutants, or 'Met' for
            meteorological environmental parameters (e.g., ``'PM25'`` is
            assigned to the 'PM' classifier).
        criteria_pollutant (bool):
            Describes whether the parameter is a criteria pollutant (True) or
            non-criteria (False).
        aqs_parameter_code (int):
            The AQS Parameter code. See resource #1 in the module docstring
            for a detailed list of AQS parameter codes.
        averaging (list):
            The reference measurement averaging intervals commonly utilized for
            analyzing parameter data. Common averaging intervals are included
            in a list (e.g., fine particulate matter as measured by FRM or
            FEM instrumentation may report data at either 1-hour or 24-hour
            sampling or averaging intervals, such that averaging would be
            ``['1-hour', '24-hour']``).
        units (str):
            The units of measure, expressed symbolically in unicode characters
            (e.g., for fine particulate matter, ``'µg/m³'``).
        units_description (str):
            A textual description of the units of measure (e.g., for fine
            particulate matter, 'Micrograms per Cubic Meter').
        units_aqs_code (int):
            The AQS unit code. See resource #2 in the module docstring for a
            detailed list of AQS parameter codes.
        PerformanceTargets (sensortoolkit.ParameterTargets object):
            Performance metrics, target values and ranges associated with the
            parameter. Preset values are configured for :math:`PM_{2.5}` and
            :math:`O_3` using U.S. EPA's recommended performance metrics and
            targets for air sensors measuring these pollutants.

    """
    __param_dict__ = _param_dict

    def __init__(self, param, set_units=True, **kwargs):

        self.name = param
        self.format_name = kwargs.get('format_name', None)
        self.format_baseline = kwargs.get('format_baseline', None)
        self.format_subscript = kwargs.get('format_subscript', None)
        self.classifier = kwargs.get('classifier', None)
        self.criteria_pollutant =kwargs.get('criteria_pollutant', False)
        self.aqs_parameter_code = kwargs.get('aqs_parameter_code', None)
        self.units_aqs_code = kwargs.get('units_aqs_code', None)
        self.averaging = kwargs.get('averaging', ['1-hour', '24-hour'])

        save_custom_param = kwargs.get('save_custom_param', False)

        if self.name in self.__param_dict__:
            self._autoset_param()

        if set_units:
            unit_info = self._get_units()
            self.units = unit_info['Label']
            self.units_description = unit_info['Description']
            if isinstance(unit_info['Context'], str):
                self.units_description += f" ({unit_info['Context']})"
            self.units_aqs_code = unit_info['Unit Code']
        else:
            unit_info = {}

        self._set_parametertargets()

        if param not in self.__param_dict__:
            self.__param_dict__[param] = {'baseline': self.name,
                                          'classifier': self.classifier,
                                          'subscript': self.format_subscript,
                                          'aqs_unit_code': self.units_aqs_code,
                                          'averaging': self.averaging,
                                          'usepa_targets': False,
                                          'criteria': self.criteria_pollutant,
                                          'aqs_param_code': self.aqs_parameter_code,
                                          'custom': True,
                                          'unit_info': unit_info
                                          }
        if save_custom_param:
            file_path = pathlib.Path(__file__)
            parent_path = file_path.parent.absolute()
            with open(os.path.join(_app_data_dir, 'param_info.json'), 'w') as file:
                print(f'..updating param_info.json with custom parameter {self.name}')
                json.dump(self.__param_dict__, file, indent=4, ensure_ascii=True)


    def _autoset_param(self):
        """Assign attributes for SDFS parameters.


        Returns:
            None.

        """
        self.classifier = self.__param_dict__[self.name]['classifier']
        self.criteria_pollutant = self.__param_dict__[self.name]['criteria']
        self.aqs_parameter_code = self.__param_dict__[self.name]['aqs_param_code']
        averaging = self.__param_dict__[self.name]['averaging']
        if averaging is not None:
            self.averaging = averaging
        baseline = self.__param_dict__[self.name]['baseline']
        subscript = self.__param_dict__[self.name]['subscript']
        self._set_parameterformatting(baseline, subscript)
        self.format_baseline = baseline
        self.format_subscript = subscript


    def _set_parameterformatting(self, baseline=None, subscript=None):
        """


        Args:
            baseline (str, optional): DESCRIPTION. Defaults to None.
            subscript (str, optional): DESCRIPTION. Defaults to None.

        Returns:
            None.

        """
        self.format_name = baseline
        if subscript is not None:
            self.format_name += '$_{' + subscript + '}$'

    def _set_parametertargets(self):
        """


        Returns:
            None.

        """
        self.PerformanceTargets = ParameterTargets(self.name)

    def is_sdfs(self):
        """Indicate whether the passed parameter name is in the catalog of
        parameter names for the sensortoolkit Data Formatting Scheme (SDFS).

        Returns:
            bool:
                Return ``True`` if in the catalog, otherwise return ``False``.

        """
        if self.name in self.__param_dict__.keys():
            sdfs = not bool(self.__param_dict__[self.name]['custom'])
        else:
            sdfs = False
        return sdfs

    def _get_units(self):
        unit_table_path = os.path.abspath(os.path.join(__file__, '..', 'units.csv'))

        # Preset options
        if self.name in self.__param_dict__:
            unit_info = self.__param_dict__[self.name]['unit_info']
        else:
            # Use table of AQS units for setting custom parameter units
            unit_data = pd.read_csv(unit_table_path)
            unit_info = self._set_units(unit_data)

        return unit_info


    def _set_units(self, unit_data):

        validate = False
        while validate is False:
            self.classifier = input(f'Enter the parameter classification ("PM", '
                        f'"Gases", "Met", or "Ancillary") for {self.name}: ')

            if self.classifier not in ['PM', 'Gases', 'Met', 'Ancillary']:
                print('..invalid entry, enter "PM", "Gases", or "Met"')
                continue

            response = validate_entry()
            if response == 'y':
                validate = True
            print('')

        # Set units using table options for params with classif. PM, Gases, or Met
        if self.classifier != 'Ancillary':
            options =  unit_data[unit_data.Classification == self.classifier]

            print('Choose from the following unit codes:')
            with pd.option_context('display.expand_frame_repr', False,
                                   'display.max_rows', None):
                print('')
                print(options[['Unit Code', 'Description', 'Label', 'Conditions',
                               'Context']].to_markdown(index=False))
                # Could also include "SDFS" and "Classification" if space allows

            validate = False
            while validate is False:
                unit_code = input('Enter the integer unit code value '
                            f'for the {self.name} unit of measure: ')

                try:
                    unit_code = int(unit_code)
                except ValueError:
                    print('..invalid entry, expected integer value')
                    continue

                if unit_code not in options['Unit Code'].values:
                    print('..invalid entry, unit code not in listed values')
                    continue

                response = validate_entry()
                if response == 'y':
                    validate = True

                unit_info = options[options['Unit Code'] == unit_code]
                unit_info = unit_info.to_dict('records')[0]
        else:
            unit_info = {'Label': None,
                         'Description': None,
                         'Context': None,
                         'Unit Code': None}

        return unit_info
