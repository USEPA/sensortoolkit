# -*- coding: utf-8 -*-
"""
This module contains the ParameterTargets class, which is used to access and
configure performance metrics and target values for parameters that may be
measured by an air sensor.

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
    """Assign and retreive parameter performance metrics and target values for
    the evaluation of air sensor performance for devices measuring the
    indicated parameter.

    Preset performance metrics and target values are included for sensors
    measuring either fine particulate matter (PM2.5) or ozone (O3), where
    U.S. EPA's recommended performance metrics and target values for devices
    measuring these pollutants are utilized.

    Args:
        param (sensortoolkit.Parameter object):
            The parameter for which air sensor performance is evaluated against
            using the metrics and target values included in this module.

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

    def set_metric(self, metric_category, metric_name, **kwargs):
        """Assign a new performance metric to an existing metric category.

        Args:
            metric_category (str):
                The name of an existing performance metric category within
                the dictionary of metric values, accessed via
                ``get_all_metrics()`` (e.g., 'Bias' or 'Error').
            metric_name (str):
                The name of a new performance metric that will be added to
                the indicated metric category.

        **Keyword Arguments:**

        :param str description:
            A textual description of the metric.
        :param bounds:
            The target range (lower bound, upper bound) for the metric.
        :type bounds: Two-element tuple
        :param goal:
            The goal/ideal achievable performance metric value.
        :type goal: int or float
        :param str metric_units:
            The units associated with the metric (if applicable)

        Raises:
            KeyError: Raise if the passed metric category is not in the list
                metric categories (keys) indicated by the dictionary of metric
                values accessed via ``get_all_metrics()``.

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

    def get_metric(self, metric_name):
        """Return details about a single performance metric (description,
        target range, goal value, metric units).

        Args:
            metric_name (str):
                The name of the metric to return information about. Must be
                contained within the list of metrics indicated by
                ``get_all_metrics()``.

        Raises:
            KeyError: Raise if passed metric name is not in the dictionary of
                configured metrics.

        Returns:
            metric (dict):
                Return a dictionary containing a textual description
                of the metric (key- 'description'), the target range for the
                metric (key- 'bounds'), the goal/ideal achievable performance
                metric value (key- 'goal'), and the units associated with the
                metric if applicable (key- 'metric_units').

        """
        # Ensure title case
        # metric_category = metric_category.title()
        # #metric_name = metric_name.title()

        for cat, cat_metrics in self._metrics.items():
            for name, info in cat_metrics.items():
                if name == metric_name:
                    return info

        # If metric name not found, raise keyerror indicating the metric is not
        # in the list of performance metrics
        raise KeyError(f'Unspecified metric name: {metric_name}. Metric name '
                       f'must be one of the following: {self._metrics}')

    def get_all_metrics(self):
        """Returns all performance metrics and target values associated with
        the Parameter object.

        Returns:
            dict: A dictionary containing the performance metric categories,
            metric names, and target values.

        """
        return self._metrics

    def set_metric_category(self, metric_category, metric_names=None):
        """Assign a new metric category. Optionally, users can also add new
        metrics and associated target values to this new category.

        Example:

            Say we are working with a parameter (pollutant) that is neither
            ``PM25`` nor ``O3``, so the existing set of performance targets for
            these pollutants (metrics and target values recommended by U.S. EPA)
            are not utilized. Let's also assume that the name of our parameter
            object is ``param_obj``. After instantiating the parameter object,
            we may call the ``get_all_metrics()`` method to display all of the
            performance metrics and target values for our parameter. Since no
            preset metrics were specified, we will see the following printed to
            the console:

            >>> param_obj.PerformanceTargets.get_all_metrics()
            {'Bias': {}, 'Linearity': {}, 'Error': {}, 'Precision': {}}

            We can add a new performance evaluation metric category as well as
            any metrics and associated target values we may wish to include in
            the new category using the ``set_metric_category()`` method. For
            instance, say we wish to add a category 'Data Quality' and a metric
            within this category called 'Uptime' with a target value of 70%
            uptime or greater. This new category and metric can be added via
            the following:

            >>> param_obj.PerformanceTargets.set_metric_category(
                    metric_category='Data Quality',
                    metric_names={'Uptime': {'description': 'Measurement uptime',
                                             'bounds': (70, 100),
                                             'goal': 100,
                                             'metric_units': '%'}
                                  }
                    )

            If we again call the ``get_all_metrics()`` method, we will see that
            the dictionary has been updated to include the new category and
            metric name.

            >>> param_obj.PerformanceTargets.get_all_metrics()
            {'Bias': {},
             'Linearity': {},
             'Error': {},
             'Precision': {},
             'Data_Quality': {'Uptime': {'description': 'Measurement uptime',
                                         'bounds': (70, 100),
                                         'goal': 100,
                                         'metric_units': '%'}
                              }
             }

        Args:
            metric_category (str):
                The name of the new performance metric category to add.
            metric_names (dict, optional):
                A dictionary of metrics (dictionary keys) and a description
                of each metric (sub-dictionary for each metric containing
                'description' - a textual description of the metric,
                'bounds' - the lower and upper bounds of the target range for
                the specified metric, 'goal' - the goal/ideal achievable
                performance metric value, and 'metric_units' - the units
                associated with the metric if applicable). Defaults to None.

        Raises:
            TypeError: Raise if the type of metric_names is not a dictionary.

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
                self.set_metric(metric_category,
                                metric_name,
                                **kwargs)
