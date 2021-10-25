# -*- coding: utf-8 -*-
"""
Description.

================================================================================

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
from ._targets import ParameterTargets
from sensortoolkit.lib_utils import validate_entry

class Parameter:
    """
    """
    __param_dict__ = {'CO': {'baseline': 'CO',
                             'classifier': 'Gases',
                             'fmt_param': 'CO',
                             'subscript': None,
                             'aqs_unit_code': 8,
                             'averaging': None,
                             'usepa_targets': False,
                             'criteria': True,
                             'aqs_param_code': 42101
                             },

                      'DP': {'baseline': 'Dew point',
                             'classifier': 'Met',
                             'fmt_param': 'Dew point',
                             'subscript': None,
                             'aqs_unit_code': 17,
                             'averaging': None,
                             'usepa_targets': False,
                             'criteria': False,
                             'aqs_param_code': 62103
                             },

                      'NO': {'baseline': 'NO',
                             'classifier': 'Gases',
                             'fmt_param': 'NO',
                             'subscript': None,
                             'averaging': None,
                             'usepa_targets': False,
                             'criteria': False,
                             'aqs_param_code': 42601
                             },

                      'NO2': {'baseline': 'NO',
                              'classifier': 'Gases',
                              'fmt_param': '$NO_2$',
                              'subscript': '2',
                              'aqs_unit_code': 8,
                              'averaging': None,
                              'usepa_targets': False,
                              'criteria': True,
                              'aqs_param_code': 42602
                              },

                      'NOx': {'baseline': 'NO',
                              'classifier': 'Gases',
                              'fmt_param': '$NO_x$',
                              'subscript': 'x',
                              'aqs_unit_code': 8,
                              'averaging': None,
                              'usepa_targets': False,
                              'criteria': False,
                              'aqs_param_code': 42603
                              },


                      'O3': {'baseline': 'O',
                             'classifier': 'Gases',
                             'fmt_param': '$O_3$',
                             'subscript': '3',
                             'aqs_unit_code': 8,
                             'averaging': ['1-hour'],
                             'usepa_targets': True,
                             'criteria': True,
                             'aqs_param_code': 44201
                             },


                      'PM1': {'baseline': 'PM',
                              'classifier': 'PM',
                              'fmt_param': 'PM$_{1}$',
                              'subscript': '1',
                              'aqs_unit_code': 105,
                              'averaging': None,
                              'usepa_targets': False,
                              'criteria': False,
                              'aqs_param_code': ''
                              },

                      'PM10': {'baseline': 'PM',
                               'classifier': 'PM',
                               'fmt_param': 'PM$_{10}$',
                               'subscript': '10',
                               'aqs_unit_code': 105,
                               'averaging': None,
                               'usepa_targets': False,
                               'criteria': True,
                               'aqs_param_code': 81102
                               },

                      'PM25': {'baseline': 'PM',
                               'classifier': 'PM',
                               'fmt_param': 'PM$_{2.5}$',
                               'subscript': '2.5',
                               'aqs_unit_code': 105,
                               'averaging': ['1-hour', '24-hour'],
                               'usepa_targets': True,
                               'criteria': True,
                               'aqs_param_code': 88101
                               },

                      'SO2': {'baseline': 'SO',
                              'classifier': 'Gases',
                              'fmt_param': '$SO_2$',
                              'subscript': '2',
                              'aqs_unit_code': 8,
                              'averaging': None,
                              'usepa_targets': False,
                              'criteria': True,
                              'aqs_param_code': 42401
                              },

                      'SOx': {'baseline': 'SO',
                              'classifier': 'Gases',
                              'fmt_param': '$SO_x$',
                              'subscript': 'x',
                              'aqs_unit_code': 8,
                              'averaging': None,
                              'usepa_targets': False,
                              'criteria': False,
                              'aqs_param_code': ''
                              },

                      'Temp': {'baseline': 'Temperature',
                               'classifier': 'Met',
                               'fmt_param': 'Temperature',
                               'subscript': None,
                               'aqs_unit_code': 17,
                               'averaging': None,
                               'usepa_targets': False,
                               'criteria': False,
                               'aqs_param_code': 62101  # Also 68105
                               },

                      'RH': {'baseline': 'Relative Humidity',
                             'classifier': 'Met',
                             'fmt_param': 'Relative Humidity',
                             'subscript': None,
                             'aqs_unit_code': 19,
                             'averaging': None,
                             'usepa_targets': False,
                             'criteria': False,
                             'aqs_param_code': 62201
                             },

                      'Press': {'baseline': 'Pressure',
                                'classifier': 'Met',
                                'fmt_param': 'Pressure',
                                'subscript': None,
                                'aqs_unit_code': 128,
                                'averaging': None,
                                'usepa_targets': False,
                                'criteria': False,
                                'aqs_param_code': 68108  # or 64101
                                },

                      'WD': {'baseline': 'Wind Direction',
                             'classifier': 'Met',
                             'fmt_param': 'Wind Direction',
                             'subscript': None,
                             'aqs_unit_code': 14,
                             'averaging': None,
                             'usepa_targets': False,
                             'criteria': False,
                             'aqs_param_code': 61102  # also 61104
                             },

                      'WS': {'baseline': 'Wind Speed',
                             'classifier': 'Met',
                             'fmt_param': 'Wind Speed',
                             'subscript': None,
                             'aqs_unit_code': 11,
                             'averaging': None,
                             'usepa_targets': False,
                             'criteria': False,
                             'aqs_param_code': 61101  # also 61103
                             }
                      }

    def __init__(self, param, set_units=True, **kwargs):

        self.name = param
        self.format_name = None
        self.format_baseline = None
        self.format_subscript = None
        self.classifier = None
        self.criteria_pollutant = False
        self.aqs_parameter_code = None
        self.averaging = ['1-hour', '24-hour']  # default averaging
        self.__verbose__ = kwargs.get('verbose', False)

        if set_units:
            unit_info = self._get_units()
            self.units = unit_info['Label']
            self.units_description = unit_info['Description']
            self.units_aqs_code = unit_info['Unit Code']

        if self.name in self.__param_dict__:
            self.__Autoset_Param__()

        self.__set_ParameterTargets__()

    def __Autoset_Param__(self):
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
        self.set_ParameterFormatting(baseline, subscript)
        self.format_baseline = baseline
        self.format_subscript = subscript


    def set_ParameterFormatting(self, baseline=None, subscript=None):
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

    def __set_ParameterTargets__(self):
        """


        Returns:
            None.

        """
        if self.__verbose__:
            print('..Initializing performance targets '
                  'for {0}'.format(self.name))
        self.PerformanceTargets = ParameterTargets(self.name)

    def is_sdfs(self):
        """
        Indicate whether the passed parameter name is in the catalog of
        parameter names for the Sensor Data Formatting Scheme.

        Returns:
            TYPE: DESCRIPTION.

        """
        return self.name in self.__param_dict__.keys()

    # def format_units(self, to=None):
    #     if to == 'latex':
    #         return self._format_units_latex()


    # def _format_units_latex(self):
    #     replacements = {'Micrograms': '\\mu g',
    #                             'per': r'/',
    #                             'cubic meter': 'm^3'}

    #     self.latex_units = self.units
    #     for text, latex in replacements.items():
    #         self.latex_units = self.latex_units.replace(text, latex)

    #     return self.latex_units


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
                validate == True

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
                validate == True

        return unit_code


if __name__ == '__main__':
    # Testing
    # ----------------------
    PM25 = Parameter('PM25')
    # O3 = Parameter('O3')
    # SO2 = Parameter('SO2')

    #Temp = Parameter('Temp')
    #RH = Parameter('RH')
