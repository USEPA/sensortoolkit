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
  Wed Sep  1 15:47:14 2021
Last Updated:
  Wed Sep  1 15:47:14 2021
"""
from .targets_class import ParameterTargets

class Parameter:
    """
    """
    __param_dict__ = {'CO': {'baseline': 'CO',
                            'classifier': 'Gases',
                            'fmt_param': 'CO',
                            'subscript': None,
                            'units': '(ppbv)',
                            'averaging': None,
                            'usepa_targets': False
                            },

                    'DP': {'baseline': 'Dew point',
                           'classifier': 'Met',
                           'fmt_param': 'Dew point',
                           'subscript': None,
                           'units': '($\\degree$C)',
                           'averaging': None,
                           'usepa_targets': False
                           },

                    'NO': {'baseline': 'NO',
                           'classifier': 'Gases',
                           'fmt_param': 'NO',
                           'subscript': None,
                           'units': 'units undef',
                           'averaging': None,
                           'usepa_targets': False
                           },

                    'NO2': {'baseline': 'NO',
                            'classifier': 'Gases',
                            'fmt_param': '$NO_2$',
                            'subscript': '2',
                            'units': '(ppbv)',
                            'averaging': None,
                            'usepa_targets': False
                            },

                    'NOx': {'baseline': 'NO',
                            'classifier': 'Gases',
                            'fmt_param': '$NO_x$',
                            'subscript': 'x',
                            'units': 'units undef',
                            'averaging': None,
                            'usepa_targets': False
                            },


                    'O3': {'baseline': 'O',
                           'classifier': 'Gases',
                           'fmt_param': '$O_3$',
                           'subscript': '3',
                           'units': '(ppbv)',
                           'averaging': ['1-hour'],
                           'usepa_targets': True
                           },


                    'PM1': {'baseline': 'PM',
                            'classifier': 'PM',
                            'fmt_param': 'PM$_{1}$',
                            'subscript': '1',
                            'units': '($\\mu g/m^3$)',
                            'averaging': None,
                            'usepa_targets': False
                            },

                    'PM10': {'baseline': 'PM',
                             'classifier': 'PM',
                             'fmt_param': 'PM$_{10}$',
                             'subscript': '10',
                             'units': '($\\mu g/m^3$)',
                             'averaging': None,
                             'usepa_targets': False
                              },

                    'PM25': {'baseline': 'PM',
                             'classifier': 'PM',
                             'fmt_param': 'PM$_{2.5}$',
                             'subscript': '2.5',
                             'units': '($\\mu g/m^3$)',
                             'averaging': ['1-hour', '24-hour'],
                             'usepa_targets': True
                             },

                    'RH': {'baseline': 'Relative Humidity',
                           'classifier': 'Gases',
                           'fmt_param': 'Relative Humidity',
                           'subscript': None,
                           'units': '(%)',
                           'averaging': None,
                           'usepa_targets': False
                           },

                    'SO2': {'baseline': 'SO',
                            'classifier': 'Gases',
                            'fmt_param': '$SO_2$',
                            'subscript': '2',
                            'units': 'units undef',
                            'averaging': None,
                            'usepa_targets': False
                            },

                    'SOx': {'baseline': 'SO',
                            'classifier': 'Gases',
                            'fmt_param': '$SO_x$',
                            'subscript': 'x',
                            'units': 'units undef',
                            'averaging': None,
                            'usepa_targets': False
                            },

                    'Temp': {'baseline': 'Temperature',
                             'classifier': 'Gases',
                             'fmt_param': 'Temperature',
                             'subscript': None,
                             'units': '($\\degree$C)',
                             'averaging': None,
                             'usepa_targets': False
                             },

                    'WD': {'baseline': 'Wind Direction',
                           'classifier': 'Met',
                           'fmt_param': 'Wind Direction',
                           'subscript': None,
                           'units': 'Angular Degrees',
                           'averaging': None,
                           'usepa_targets': False
                           },

                    'WS': {'baseline': 'Wind Speed',
                           'classifier': 'Met',
                           'fmt_param': 'Wind Speed',
                           'subscript': None,
                           'units': 'm/s',
                           'averaging': None,
                           'usepa_targets': False
                           }
                    }

    def __init__(self, param, **kwargs):

        self.param_name = param
        self.param_format_name = None
        self.param_format_baseline = None
        self.param_format_subscript = None
        self.param_units = None
        self.param_classifier = None
        self.param_averaging = ['1-hour', '24-hour']  # default averaging
        self.__verbose__ = kwargs.get('verbose', False)


        if self.param_name in self.__param_dict__:
            self.__Autoset_Param__()

        self.__set_ParameterTargets__()

    def __Autoset_Param__(self):
        """


        Returns:
            None.

        """
        self.param_units = self.__param_dict__[self.param_name]['units']
        self.param_classifier = self.__param_dict__[self.param_name]['classifier']
        averaging = self.__param_dict__[self.param_name]['averaging']
        if averaging is not None:
            self.param_averaging = averaging
        baseline = self.__param_dict__[self.param_name]['baseline']
        subscript = self.__param_dict__[self.param_name]['subscript']
        self.set_ParameterFormatting(baseline, subscript)
        self.param_format_baseline = baseline
        self.param_format_subscript = subscript


    def set_ParameterFormatting(self, baseline=None, subscript=None):
        """


        Args:
            baseline (TYPE, optional): DESCRIPTION. Defaults to None.
            subscript (TYPE, optional): DESCRIPTION. Defaults to None.

        Returns:
            None.

        """
        self.param_format_name = baseline
        if subscript is not None:
            self.param_format_name += '_{' + subscript + '}'

    def __set_ParameterTargets__(self):
        """


        Returns:
            None.

        """
        if self.__verbose__:
            print('..Initializing performance targets '
                  'for {0}'.format(self.param_name))
        self.PerformanceTargets = ParameterTargets(self.param_name)



if __name__ == '__main__':
    # Testing
    # ----------------------
    PM25 = Parameter('PM25')
    O3 = Parameter('O3')
    SO2 = Parameter('SO2')
