Reference Data Structures
-------------------------
Reference data are accessed via the ``ReferenceMonitor`` object instance. Following
the `Toco Toucan Quickstart Guide example <../quickstart.html#example-scenario-toco-toucan>`_,
mention of ``reference`` variable below refers to the ``ReferenceMonitor``
object instantiated under the `Testing Attribute Objects - The ReferenceMonitor Object` section.

Accessing Reference Data
^^^^^^^^^^^^^^^^^^^^^^^^
Both 1-hour and 24-hour averaged data sets are computed for FRM/FEM reference data,
and data sets are organized by parameter classification (either ``PM`` for particulate matter,
``Gases`` for gaseous pollutants, or ``Met`` for meteorological parameters).

.. tip::
  Parameter classifications for each SDFS parameter can be found in the
  `Table of SDFS Parameters <../sdfs/index.html#id1>`_.

Reference datasets are access via the ``reference.data`` attribute, which stores pandas
DataFrames for each parameter classification in a dictionary structure at both
1-hour and 24-hour averaged intervals:

.. code-block:: python

  {'PM': {'1-hour': pandas DataFrame object,
          '24-hour': pandas DataFrame object},
   'Gases': {'1-hour': pandas DataFrame object,
             '24-hour': pandas DataFrame object},
   'Met': {'1-hour': pandas DataFrame object,
           '24-hour': pandas DataFrame object}
  }

Dataset Example
^^^^^^^^^^^^^^^

The first five rows of data for particulate matter measurements collected at the Burdens Creek
monitoring site in RTP, NC, averaged to 1-hour intervals, and formatted as an SDFS dataset
(accessed as ``reference['PM']['1-hour']``) are shown at the following link:
`Example Reference Dataset <../sdfs/index.html#example-sdfs-datasets>`_

..
  * ``pm_``: Instruments measuring particulate matter (:math:`PM_{1}`, :math:`PM_{2.5}`, :math:`PM_{10}`)

    * ``pm_hourly_ref_df``
    * ``pm_daily_ref_df``

  * ``gas_``: Instruments measuring gaseous pollutants (:math:`O_3`, :math:`CO`, :math:`CO_2`, :math:`NO`, :math:`NO_2`, :math:`NO_x`, :math:`SO_2`, :math:`SO_x`)

    * ``gas_hourly_ref_df``
    * ``gas_daily_ref_df``

  * ``met_``: Instruments measuring meteorlogical parameters (temperature, relative humidity, pressure, dewpoint, wind speed, wind direction)

    * ``met_hourly_ref_df``
    * ``met_daily_ref_df``

  .. tip::

    Since working with six reference dataframes can be challenging to track and retreive
    reference data for the selected ``Eval.param``, the dataframes ``Eval.hourly_ref_df`` and
    ``Eval.daily_ref_df`` are aliases of the reference dataframes corresponding to the parameter
    classification of the ``Eval.param``.

    For instance, if ``Eval.param.name = 'PM25'``, ``Eval.hourly_ref_df`` corresponds to
    ``Eval.pm_hourly_ref_df`` and ``Eval.daily_ref_df`` corresponds
    to  ``Eval.pm_daily_ref_df``. Note that corresponding dataframes point to the same object
    in memory, and as a result, modifications to one dataframe will be reflected in the corresponding
    dataframe.
