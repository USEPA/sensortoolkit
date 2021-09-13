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
  Thu Sep  2 09:43:36 2021
Last Updated:
  Thu Sep  2 09:43:36 2021
"""
import warnings

class ParameterTargets:
    """
    """

    def __init__(self, param):

        __target_dict__ = {'PM25':
                               {'Bias':
                                    {'Slope': {'description': 'Ordinary least squares regression slope',
                                               'bounds': (0.65, 1.35),
                                               'goal': 1.0,
                                               'metric_units': None},

                                     'Intercept': {'description': 'Ordinary least squares regression intercept',
                                                   'bounds': (-5.0, 5.0),
                                                   'goal': 1.0,
                                                   'metric_units': '$\\mu g/m^3$'},
                                     },

                                'Linearity':
                                    {'R^2': {'description': 'Coefficient of determination',
                                               'bounds': (0.70, 1.0),
                                               'goal': 1.0,
                                               'metric_units': None}
                                     },

                                'Error': {'RMSE': {'description': 'Root mean square error',
                                                   'bounds': (0.0, 7.0),
                                                   'goal': 0.0,
                                                   'metric_units': '$\\mu g/m^3$'},

                                          'NRMSE': {'description': 'Normalized root mean square error',
                                                    'bounds': (0.0, 30.0),
                                                    'goal': 0.0,
                                                    'metric_units': '%'}
                                          },

                                'Precision': {'SD': {'description': 'Standard deviation',
                                                     'bounds': (0.0, 5.0),
                                                     'goal': 0.0,
                                                     'metric_units': '$\\mu g/m^3$'},

                                              'CV': {'description': 'Coefficient of variation',
                                                     'bounds': (0.0, 30.0),
                                                     'goal': 0.0,
                                                     'metric_units': '%'}}
                                },

                           'O3':
                               {'Bias':
                                    {'Slope': {'description': 'Ordinary least squares regression slope',
                                               'bounds': (0.8, 1.2),
                                               'goal': 1.0,
                                               'metric_units': None},

                                     'Intercept': {'description': 'Ordinary least squares regression intercept',
                                                   'bounds': (-5.0, 5.0),
                                                   'goal': 0.0,
                                                   'metric_units': 'ppbv'},
                                     },

                                'Linearity':
                                    {'R^2': {'description': 'Coefficient of determination',
                                               'bounds': (0.80, 1.0),
                                               'goal': 1.0,
                                               'metric_units': None}
                                     },

                                'Error': {'RMSE': {'description': 'Root mean square error',
                                                   'bounds': (0.0, 5.0),
                                                   'goal': 0.0,
                                                   'metric_units': 'ppbv'}
                                          },

                                'Precision': {'SD': {'description': 'Standard deviation',
                                                     'bounds': (0.0, 5.0),
                                                     'goal': 0.0,
                                                     'metric_units': 'ppbv'},

                                              'CV': {'description': 'Coefficient of variation',
                                                     'bounds': (0.0, 30.0),
                                                     'goal': 0.0,
                                                     'metric_units': '%'}}
                                }
                           }

        self.__metrics__ = {'Bias': {},
                            'Linearity': {},
                            'Error': {},
                            'Precision': {}
                            }

        if param in __target_dict__:
            self.__metrics__ = __target_dict__[param]

        self.metric_categories = list(self.__metrics__.keys())

    def set_PerformanceMetric(self, metric_category, metric_name, **kwargs):
        """


        Args:
            metric_category (TYPE): DESCRIPTION.
            metric_name (TYPE): DESCRIPTION.
            **kwargs (TYPE): DESCRIPTION.

        Raises:
            KeyError: DESCRIPTION.

        Returns:
            None.

        """

        # Ensure title case
        metric_category = metric_category.title()
        #metric_name = metric_name.title()

        if metric_category not in self.__metrics__:
            raise KeyError('Unspecified metric category: '
                           '{0}. Category must be one of the '
                           'following: {1}'.format(metric_category,
                                                   list(self.__metrics__.keys())))

        self.__metrics__[metric_category][metric_name] = {}

        metric_entry = self.__metrics__[metric_category][metric_name]
        metric_entry['description'] = kwargs.get('description', None)
        metric_entry['bounds'] = kwargs.get('bounds', None)
        metric_entry['goal'] = kwargs.get('goal', None)
        metric_entry['metric_units'] = kwargs.get('metric_units', None)

    def get_PerformanceMetric(self, metric_category, metric_name):
        """


        Args:
            metric_category (TYPE): DESCRIPTION.
            metric_name (TYPE): DESCRIPTION.

        Raises:
            KeyError: DESCRIPTION.

        Returns:
            metric (TYPE): DESCRIPTION.

        """

        # Ensure title case
        metric_category = metric_category.title()
        #metric_name = metric_name.title()

        if metric_category not in self.__metrics__:
            raise KeyError('Unspecified metric category: '
                           '{0}. Category must be one of the '
                           'following: {1}'.format(metric_category,
                                                   list(self.__metrics__.keys())))

        if metric_name not in self.__metrics__[metric_category]:
            raise KeyError('Unspecified metric name: '
                           '{0}. Metric name must be one of the '
                           'following: {1}'.format(metric_name,
                                list(self.__metrics__[metric_category].keys())))

        metric = self.__metrics__[metric_category][metric_name]

        return metric

    def get_AllMetrics(self):
        """


        Returns:
            TYPE: DESCRIPTION.

        """
        return self.__metrics__

    def set_MetricCategory(self, metric_category, metric_names=None):
        """


        Args:
            metric_category (TYPE): DESCRIPTION.
            metric_names (TYPE, optional): DESCRIPTION. Defaults to None.

        Raises:
            TypeError: DESCRIPTION.

        Returns:
            None.

        """

        # Ensure title case
        metric_category = metric_category.title()

        if metric_category in self.__metrics__:
            warnings.warn("Warning: Overwriting existing metric category.")

        self.__metrics__[metric_category] = {}

        if metric_names is not None:
            if type(metric_names) is not dict:
                raise TypeError('Expected "metric_names" to be type dict,'
                                ' received type {0}'.format(type(metric_names))
                                )
            for metric_name in metric_names:
                metric_info = metric_names[metric_name]
                kwargs = metric_info
                self.set_PerformanceMetric(metric_category,
                                           metric_name,
                                           **kwargs)
