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
from ._targets import ParameterTargets

class Parameter:
    """
    """
    __param_dict__ = {'CO': {'baseline': 'CO',
                            'classifier': 'Gases',
                            'fmt_param': 'CO',
                            'subscript': None,
                            'units': '(ppbv)',
                            'averaging': None,
                            'usepa_targets': False,
                            'criteria': True,
                            'aqs_param_code': 42101
                            },

                    'DP': {'baseline': 'Dew point',
                           'classifier': 'Met',
                           'fmt_param': 'Dew point',
                           'subscript': None,
                           'units': '($\\degree$C)',
                           'averaging': None,
                           'usepa_targets': False,
                           'criteria': False,
                           'aqs_param_code': 62103
                           },

                    'NO': {'baseline': 'NO',
                           'classifier': 'Gases',
                           'fmt_param': 'NO',
                           'subscript': None,
                           'units': 'units undef',
                           'averaging': None,
                           'usepa_targets': False,
                           'criteria': False,
                           'aqs_param_code': ''
                           },

                    'NO2': {'baseline': 'NO',
                            'classifier': 'Gases',
                            'fmt_param': '$NO_2$',
                            'subscript': '2',
                            'units': '(ppbv)',
                            'averaging': None,
                            'usepa_targets': False,
                            'criteria': True,
                            'aqs_param_code': 42602
                            },

                    'NOx': {'baseline': 'NO',
                            'classifier': 'Gases',
                            'fmt_param': '$NO_x$',
                            'subscript': 'x',
                            'units': 'units undef',
                            'averaging': None,
                            'usepa_targets': False,
                            'criteria': False,
                            'aqs_param_code': ''
                            },


                    'O3': {'baseline': 'O',
                           'classifier': 'Gases',
                           'fmt_param': '$O_3$',
                           'subscript': '3',
                           'units': '(ppbv)',
                           'averaging': ['1-hour'],
                           'usepa_targets': True,
                           'criteria': True,
                           'aqs_param_code': 44201
                           },


                    'PM1': {'baseline': 'PM',
                            'classifier': 'PM',
                            'fmt_param': 'PM$_{1}$',
                            'subscript': '1',
                            'units': '($\\mu g/m^3$)',
                            'averaging': None,
                            'usepa_targets': False,
                            'criteria': False,
                            'aqs_param_code': ''
                            },

                    'PM10': {'baseline': 'PM',
                             'classifier': 'PM',
                             'fmt_param': 'PM$_{10}$',
                             'subscript': '10',
                             'units': '($\\mu g/m^3$)',
                             'averaging': None,
                             'usepa_targets': False,
                             'criteria': True,
                             'aqs_param_code': 81102
                              },

                    'PM25': {'baseline': 'PM',
                             'classifier': 'PM',
                             'fmt_param': 'PM$_{2.5}$',
                             'subscript': '2.5',
                             'units': '($\\mu g/m^3$)',
                             'averaging': ['1-hour', '24-hour'],
                             'usepa_targets': True,
                             'criteria': True,
                             'aqs_param_code': 88101
                             },

                    'SO2': {'baseline': 'SO',
                            'classifier': 'Gases',
                            'fmt_param': '$SO_2$',
                            'subscript': '2',
                            'units': 'units undef',
                            'averaging': None,
                            'usepa_targets': False,
                            'criteria': True,
                            'aqs_param_code': 42401
                            },

                    'SOx': {'baseline': 'SO',
                            'classifier': 'Gases',
                            'fmt_param': '$SO_x$',
                            'subscript': 'x',
                            'units': 'units undef',
                            'averaging': None,
                            'usepa_targets': False,
                            'criteria': False,
                            'aqs_param_code': ''
                            },

                    'Temp': {'baseline': 'Temperature',
                             'classifier': 'Met',
                             'fmt_param': 'Temperature',
                             'subscript': None,
                             'units': '($\\degree$C)',
                             'averaging': None,
                             'usepa_targets': False,
                             'criteria': False,
                             'aqs_param_code': 62101 # Also 68105
                             },

                    'RH': {'baseline': 'Relative Humidity',
                           'classifier': 'Met',
                           'fmt_param': 'Relative Humidity',
                           'subscript': None,
                           'units': '(%)',
                           'averaging': None,
                           'usepa_targets': False,
                           'criteria': False,
                           'aqs_param_code': 62201
                           },

                    'Press': {'baseline': 'Pressure',
                              'classifier': 'Met',
                              'fmt_param': 'Pressure',
                              'subscript': None,
                              'units': 'hPa',
                              'averaging': None,
                              'usepa_targets': False,
                              'criteria': False,
                              'aqs_param_code': 68108 # or 64101
                              },

                    'WD': {'baseline': 'Wind Direction',
                           'classifier': 'Met',
                           'fmt_param': 'Wind Direction',
                           'subscript': None,
                           'units': 'Angular Degrees',
                           'averaging': None,
                           'usepa_targets': False,
                           'criteria': False,
                           'aqs_param_code': 61102 # also 61104
                           },

                    'WS': {'baseline': 'Wind Speed',
                           'classifier': 'Met',
                           'fmt_param': 'Wind Speed',
                           'subscript': None,
                           'units': 'm/s',
                           'averaging': None,
                           'usepa_targets': False,
                           'criteria': False,
                           'aqs_param_code': 61101 # also 61103
                           }
                    }

    def __init__(self, param, **kwargs):

        self.name = param
        self.format_name = None
        self.format_baseline = None
        self.format_subscript = None
        self.units = None
        self.classifier = None
        self.criteria_pollutant = False
        self.aqs_parameter_code = None
        self.averaging = ['1-hour', '24-hour']  # default averaging
        self.__verbose__ = kwargs.get('verbose', False)


        if self.name in self.__param_dict__:
            self.__Autoset_Param__()

        self.__set_ParameterTargets__()

    def __Autoset_Param__(self):
        """


        Returns:
            None.

        """
        self.units = self.__param_dict__[self.name]['units']
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



if __name__ == '__main__':
    # Testing
    # ----------------------
    PM25 = Parameter('PM25')
    O3 = Parameter('O3')
    SO2 = Parameter('SO2')
