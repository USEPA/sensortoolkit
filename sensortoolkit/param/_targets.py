# -*- coding: utf-8 -*-
"""
Description.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

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

        _usepa_targets = {'PM25':
                               {'Bias':
                                    {'Slope': {'description': 'Ordinary least '
                                               'squares regression slope',
                                               'bounds': (0.65, 1.35),
                                               'goal': 1.0,
                                               'metric_units': None},

                                     'Intercept': {'description': 'Ordinary '
                                                   'least squares regression '
                                                   'intercept',
                                                   'bounds': (-5.0, 5.0),
                                                   'goal': 0.0,
                                                   'metric_units': '$\\mu g/m^3$'},
                                     },

                                'Linearity':
                                    {'R^2': {'description': 'Coefficient of '
                                             'determination',
                                               'bounds': (0.70, 1.0),
                                               'goal': 1.0,
                                               'metric_units': None}
                                     },

                                'Error': {'RMSE': {'description': 'Root mean '
                                                   'square error',
                                                   'bounds': (0.0, 7.0),
                                                   'goal': 0.0,
                                                   'metric_units': '$\\mu g/m^3$'},

                                          'NRMSE': {'description': 'Normalized'
                                                    ' root mean square error',
                                                    'bounds': (0.0, 30.0),
                                                    'goal': 0.0,
                                                    'metric_units': '%'}
                                          },

                                'Precision': {'SD': {'description': 'Standard'
                                                     ' deviation',
                                                     'bounds': (0.0, 5.0),
                                                     'goal': 0.0,
                                                     'metric_units': '$\\mu g/m^3$'},

                                              'CV': {'description': 'Coeffici'
                                                     'ent of variation',
                                                     'bounds': (0.0, 30.0),
                                                     'goal': 0.0,
                                                     'metric_units': '%'}}
                                },

                           'O3':
                               {'Bias':
                                    {'Slope': {'description': 'Ordinary least'
                                               ' squares regression slope',
                                               'bounds': (0.8, 1.2),
                                               'goal': 1.0,
                                               'metric_units': None},

                                     'Intercept': {'description': 'Ordinary '
                                                   'least squares regression'
                                                   ' intercept',
                                                   'bounds': (-5.0, 5.0),
                                                   'goal': 0.0,
                                                   'metric_units': 'ppbv'},
                                     },

                                'Linearity':
                                    {'R^2': {'description': 'Coefficient of de'
                                             'termination',
                                               'bounds': (0.80, 1.0),
                                               'goal': 1.0,
                                               'metric_units': None}
                                     },

                                'Error': {'RMSE': {'description': 'Root mean '
                                                   'square error',
                                                   'bounds': (0.0, 5.0),
                                                   'goal': 0.0,
                                                   'metric_units': 'ppbv'},

                                          'NRMSE': {'description': None,
                                                    'bounds': (0, 0),
                                                    'goal': None,
                                                    'metric_units': None}
                                          },

                                'Precision': {'SD': {'description': 'Standard '
                                                     'deviation',
                                                     'bounds': (0.0, 5.0),
                                                     'goal': 0.0,
                                                     'metric_units': 'ppbv'},

                                              'CV': {'description': 'Coeffici'
                                                     'ent of variation',
                                                     'bounds': (0.0, 30.0),
                                                     'goal': 0.0,
                                                     'metric_units': '%'}}
                                }
                           }

        self._metrics = {'Bias': {},
                         'Linearity': {},
                         'Error': {},
                         'Precision': {}
                         }

        if param in _usepa_targets:
            self._metrics = _usepa_targets[param]

        self.metric_categories = list(self._metrics.keys())

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

        if metric_category not in self._metrics:
            raise KeyError('Unspecified metric category: '
                           '{0}. Category must be one of the '
                           'following: {1}'.format(metric_category,
                                                   list(self._metrics.keys())))

        self._metrics[metric_category][metric_name] = {}

        metric_entry = self._metrics[metric_category][metric_name]
        metric_entry['description'] = kwargs.get('description', None)
        metric_entry['bounds'] = kwargs.get('bounds', None)
        metric_entry['goal'] = kwargs.get('goal', None)
        metric_entry['metric_units'] = kwargs.get('metric_units', None)

    def get_PerformanceMetric(self, metric_name):
        """


        Args:
            metric_name (TYPE): DESCRIPTION.

        Raises:
            KeyError: DESCRIPTION.

        Returns:
            metric (TYPE): DESCRIPTION.

        """

        # Ensure title case
        # metric_category = metric_category.title()
        # #metric_name = metric_name.title()

        # if metric_category not in self._metrics:
        #     raise KeyError('Unspecified metric category: '
        #                    '{0}. Category must be one of the '
        #                    'following: {1}'.format(metric_category,
        #                                            list(self._metrics.keys())))

        # if metric_name not in self._metrics[metric_category]:
        #     raise KeyError('Unspecified metric name: '
        #                    '{0}. Metric name must be one of the '
        #                    'following: {1}'.format(metric_name,
        #                         list(self._metrics[metric_category].keys())))

        # metric = self._metrics[metric_category][metric_name]

        for cat, cat_metrics in self._metrics.items():
            for name, info in cat_metrics.items():
                if name == metric_name:
                    return info

        # If metric name not found, raise keyerror indicating the metric is not
        # in the list of performance metrics
        raise KeyError(f'Unspecified metric name: {metric_name}. Metric name '
                       f'must be one of the following: {self._metrics}')

    def get_AllMetrics(self):
        """


        Returns:
            TYPE: DESCRIPTION.

        """
        return self._metrics

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

        if metric_category in self._metrics:
            warnings.warn("Warning: Overwriting existing metric category.")

        self._metrics[metric_category] = {}

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
