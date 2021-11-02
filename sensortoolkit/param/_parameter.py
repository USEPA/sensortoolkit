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
import pandas as pd
from sensortoolkit.lib_utils import validate_entry
from ._targets import ParameterTargets

class Parameter:
    """Object for accessing parameter attributes.

    Here, parameters are defined as measurable environmental quantities such
    as pollutants or meteorological conditions for which air sensors and
    reference instrumentation may collect measurements at regular sampling
    intervals.

    Args:
        param (str): DESCRIPTION.
        set_units (bool, optional): DESCRIPTION. Defaults to True.

    Attributes:
        name (str):
            The name of the parameter (e.g., 'PM25').
        format_name (str):
            A formatted expression for the parameter used for displaying the
            name of the parameter on plots (e.g., 'PM$_{2.5}$').
        format_baseline (str):
            For ``format_name``, contains the baseline component of the
            parameter name (e.g., 'PM' for fine particulate matter)
        format_subscript (str):
            For ``format_name``, contains the subscripted component of the
            parameter name (e.g., '2.5' for fine particulate matter)
        classifier (str):
            A term for sorting the parameter into one of three environmental
            parameter classifications, either 'PM' for particulate matter
            pollutants, 'Gases' for gaseous pollutants, or 'Met' for
            meteorological environmental parameters (e.g., 'PM25' is assigned
            to the 'PM' classifier).
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
            ['1-hour', '24-hour']).
        units (str):
            The units of measure, expressed symbolically in unicode characters
            (e.g., for fine particulate matter, 'µg/m³').
        units_description (str):
            A textual description of the units of measure (e.g., for fine
            particulate matter,'Micrograms per Cubic Meter').
        units_aqs_code (int):
            The AQS unit code. See resource #2 in the module docstring for a
            detailed list of AQS parameter codes.
        PerformanceTargets (sensortoolkit.ParameterTargets object):
            Performance metrics, target values and ranges associated with the
            parameter. Preset values are configured for PM25 and O3 using
            U.S. EPA's recommended performance metrics and targets for air
            sensors measuring these pollutants.

    """
    __param_dict__ = {'CO': {'baseline': 'CO',
                             'classifier': 'Gases',
                             'subscript': None,
                             'aqs_unit_code': 8,
                             'averaging': None,
                             'usepa_targets': False,
                             'criteria': True,
                             'aqs_param_code': 42101
                             },

                      'DP': {'baseline': 'Dew point',
                             'classifier': 'Met',
                             'subscript': None,
                             'aqs_unit_code': 17,
                             'averaging': None,
                             'usepa_targets': False,
                             'criteria': False,
                             'aqs_param_code': 62103
                             },

                      'NO': {'baseline': 'NO',
                             'classifier': 'Gases',
                             'subscript': None,
                             'averaging': None,
                             'usepa_targets': False,
                             'criteria': False,
                             'aqs_param_code': 42601
                             },

                      'NO2': {'baseline': 'NO',
                              'classifier': 'Gases',
                              'subscript': '2',
                              'aqs_unit_code': 8,
                              'averaging': None,
                              'usepa_targets': False,
                              'criteria': True,
                              'aqs_param_code': 42602
                              },

                      'NOx': {'baseline': 'NO',
                              'classifier': 'Gases',
                              'subscript': 'x',
                              'aqs_unit_code': 8,
                              'averaging': None,
                              'usepa_targets': False,
                              'criteria': False,
                              'aqs_param_code': 42603
                              },


                      'O3': {'baseline': 'O',
                             'classifier': 'Gases',
                             'subscript': '3',
                             'aqs_unit_code': 8,
                             'averaging': ['1-hour'],
                             'usepa_targets': True,
                             'criteria': True,
                             'aqs_param_code': 44201
                             },


                      'PM1': {'baseline': 'PM',
                              'classifier': 'PM',
                              'subscript': '1',
                              'aqs_unit_code': 105,
                              'averaging': None,
                              'usepa_targets': False,
                              'criteria': False,
                              'aqs_param_code': ''
                              },

                      'PM10': {'baseline': 'PM',
                               'classifier': 'PM',
                               'subscript': '10',
                               'aqs_unit_code': 105,
                               'averaging': None,
                               'usepa_targets': False,
                               'criteria': True,
                               'aqs_param_code': 81102
                               },

                      'PM25': {'baseline': 'PM',
                               'classifier': 'PM',
                               'subscript': '2.5',
                               'aqs_unit_code': 105,
                               'averaging': ['1-hour', '24-hour'],
                               'usepa_targets': True,
                               'criteria': True,
                               'aqs_param_code': 88101
                               },

                      'SO2': {'baseline': 'SO',
                              'classifier': 'Gases',
                              'subscript': '2',
                              'aqs_unit_code': 8,
                              'averaging': None,
                              'usepa_targets': False,
                              'criteria': True,
                              'aqs_param_code': 42401
                              },

                      'SOx': {'baseline': 'SO',
                              'classifier': 'Gases',
                              'subscript': 'x',
                              'aqs_unit_code': 8,
                              'averaging': None,
                              'usepa_targets': False,
                              'criteria': False,
                              'aqs_param_code': ''
                              },

                      'Temp': {'baseline': 'Temperature',
                               'classifier': 'Met',
                               'subscript': None,
                               'aqs_unit_code': 17,
                               'averaging': None,
                               'usepa_targets': False,
                               'criteria': False,
                               'aqs_param_code': 62101  # Also 68105
                               },

                      'RH': {'baseline': 'Relative Humidity',
                             'classifier': 'Met',
                             'subscript': None,
                             'aqs_unit_code': 19,
                             'averaging': None,
                             'usepa_targets': False,
                             'criteria': False,
                             'aqs_param_code': 62201
                             },

                      'Press': {'baseline': 'Pressure',
                                'classifier': 'Met',
                                'subscript': None,
                                'aqs_unit_code': 128,
                                'averaging': None,
                                'usepa_targets': False,
                                'criteria': False,
                                'aqs_param_code': 68108  # or 64101
                                },

                      'WD': {'baseline': 'Wind Direction',
                             'classifier': 'Met',
                             'subscript': None,
                             'aqs_unit_code': 14,
                             'averaging': None,
                             'usepa_targets': False,
                             'criteria': False,
                             'aqs_param_code': 61102  # also 61104
                             },

                      'WS': {'baseline': 'Wind Speed',
                             'classifier': 'Met',
                             'subscript': None,
                             'aqs_unit_code': 11,
                             'averaging': None,
                             'usepa_targets': False,
                             'criteria': False,
                             'aqs_param_code': 61101  # also 61103
                             }
                      }

    def __init__(self, param, set_units=True):

        self.name = param
        self.format_name = None
        self.format_baseline = None
        self.format_subscript = None
        self.classifier = None
        self.criteria_pollutant = False
        self.aqs_parameter_code = None
        self.averaging = ['1-hour', '24-hour']  # default averaging

        if set_units:
            unit_info = self._get_units()
            self.units = unit_info['Label']
            self.units_description = unit_info['Description']
            self.units_aqs_code = unit_info['Unit Code']

        if self.name in self.__param_dict__:
            self._autoset_param()

        self._set_parametertargets()

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
            baseline (TYPE, optional): DESCRIPTION. Defaults to None.
            subscript (TYPE, optional): DESCRIPTION. Defaults to None.

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
        return self.name in self.__param_dict__.keys()

    def _get_units(self):
        unit_table_path = os.path.abspath(os.path.join(__file__,
                                                       "../units.csv"))

        unit_data = pd.read_csv(unit_table_path)

        # Dataset values where the SDFS column contains the specified parameter
        options = unit_data[unit_data.SDFS.str.contains(self.name) == True]

        if self.is_sdfs():
            unit_code = self.__param_dict__[self.name]['aqs_unit_code']
        else:
            unit_code = self._set_units(unit_data)

        unit_info = options[options['Unit Code'] == unit_code]

        return unit_info.to_dict('records')[0]

    def _set_units(self, unit_data):

        validate = False
        while validate is False:
            self.classifier = input(f'Enter the parameter classification ("PM", '
                        f'"Gases", or "Met" for {self.name}')

            if self.classifier not in ['PM', 'Gases', 'Met']:
                print('..invalid entry, enter "PM", "Gases", or "Met"')
                continue

            response = validate_entry()
            if response == 'y':
                validate = True

        options =  unit_data[unit_data.Classification == self.classifier]
        print('Choose from the following unit codes:')
        with pd.option_context('display.expand_frame_repr', False,
                               'display.max_colwidth', 65,
                               'display.max_rows', None,
                               'display.colheader_justify', 'right'):
            print(options)
        validate = False
        while validate is False:
            unit_code = input('Enter the integer unit code value '
                        'for the {self.name} unit of measure')

            if unit_code not in options['Unit Code'].values:
                print('..invalid entry.')
                continue

            response = validate_entry()
            if response == 'y':
                validate = True

        return unit_code


if __name__ == '__main__':
    # Testing
    # ----------------------
    PM25 = Parameter('PM25')
    # O3 = Parameter('O3')
    # SO2 = Parameter('SO2')

    #Temp = Parameter('Temp')
    #RH = Parameter('RH')
