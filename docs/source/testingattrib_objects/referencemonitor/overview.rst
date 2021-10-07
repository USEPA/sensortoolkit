ReferenceMonitor Instantiation
==============================
After creating an ``AirSensor`` object, users follow a similar procedure for
configuring the `ReferenceMonitor` object for importing and accessing FRM/FEM
data.

Continuing with the `evaluation.py` example, an instance of the ``ReferenceMonitor``
object is created via the following code:

.. code-block:: python

  # Loading reference object for the first time
  reference_object = sensortoolkit.ReferenceMonitor(project_path=work_path)

.. note::
  The above code snippet assumes that the user named their instance of the ``sensortoolkit.ReferenceMonitor``
  object ``reference_object``. If a different name was chosen, replace instances of ``reference_object.`` with ``[custom_name].``
  to access the instance attributes.

.. note::
  The above code snippet assumes that the user hasn't set up reference data for
  the testing site that were retrieved from a reference data service or source,
  such as the `AQS API`, `AirNow API`, `AirNowTech`, or a locally acquired data set.

  For users that have already gone through the setup process during past evaluations
  for reference data corresponding to a particular site and source and intend to use
  the same data source for subsequent evaluations at the monitoring site, a ``reference_setup.json``
  should have been created during the original setup process. In order to point to the
  particular ``reference_setup.json`` file, the user will need to specify additional parameters
  during the ``sensortoolkit.ReferenceMonitor()`` object instantiation. Please see [X]
  for more detail about instantiating ``ReferenceMonitor`` objects for
  previously-configured reference data sources.

..
  # Loading a pre-configured reference object (indicate source, site, site id
  # if applicable)
  reference_object = sensortoolkit.ReferenceMonitor(project_path=work_path,
                                              data_source='airnowtech',
                                              site_name='Burdens Creek',
                                              site_id='370630099')

When running the above code, the following message will be printed to the console
indicating that the user should continue the setup process by running the ``reference_setup()``
method:

.. code-block:: console

  ..reference data source and monitoring site information not specified, run
   ReferenceMonitor.reference_setup() to continue
