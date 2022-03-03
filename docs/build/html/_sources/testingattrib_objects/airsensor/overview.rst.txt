AirSensor Instantiation
=======================
The first object the user encounters is the AirSensor object. This structure is
used to keep track of sensor attributes and can be used to import and access
sensor datasets. First, users create an instance of the AirSensor object type,
specifying the make and model of the sensor. Below is an example of instantiating the
AirSensor object for the 'Toco Toucan' example mentioned in the `Quickstart Guide <../../quickstart.html#example-scenario-toco-toucan>`_:

.. code-block:: python

  sensor = sensortoolkit.AirSensor(make='Toco',
                                   model='Toucan')

.. list-table:: ``sensortoolkit.AirSensor() attributes``
 :widths: 50 75
 :header-rows: 1

 * - Attribute name
   - Description
 * - ``make``
   - The name of the manufacturer for the sensor. Users are recommended to |br|
     replace spaces with underscores.
 * - ``model``
   - The name of the sensor model. Users are recommended to replace spaces with |br|
     underscores.

Constructing the sensortoolkit Directory Structure
--------------------------------------------------
sensortoolkit utilizes a folder structure for storing datasets and organizing
related files. This folder structure is located at the path to a directory the
user wishes to store evaluation-related content in. This path is referred to as
the `project path` and is set by using the ``sensortoolkit.presets.set_project_path()`` method. Sensor and
reference datasets as well as supplementary statistics are stored in a ``/data``
folder. Figures created by the library are stored in a ``/figures`` folder.
Testing reports are saved within a ``/reports`` folder. Users should run the
following line of code to construct this folder structure at the user’s
``project_path``:

.. code-block:: python

  sensor.create_directories()

.. note::
  The above code snippet assumes that the user named their instance of the ``sensortoolkit.AirSensor``
  object ``sensor``. If a different name was chosen, replace instances of ``sensor`` with ``[custom_name]``
  to access the instance attributes such as the ``create_directories()`` method.

Users should see the following printed to the console indicating the constructed directory structure (note that
the parent folder location where the folders are placed will depend on where you define the project path - the code
block below follows the 'Toco Toucan' Quickstart example, where the project directory has been set to
`C:\Users\...\Documents\toucan_evaluation`):

.. code-block:: console

  Creating "data" subdirectory within C:\Users\...\Documents\toucan_evaluation
  ..\data\eval_stats
  ..\data\reference_data
  ....\data\reference_data\airnow
  ......\data\reference_data\airnow\raw
  ......\data\reference_data\airnow\processed
  ....\data\reference_data\airnowtech
  ......\data\reference_data\airnowtech\raw
  ......\data\reference_data\airnowtech\processed
  ....\data\reference_data\aqs
  ......\data\reference_data\aqs\raw
  ......\data\reference_data\aqs\processed
  ..\data\sensor_data
  ..\data\eval_stats\Toco_Toucan
  ..\data\sensor_data\Toco_Toucan
  ....\data\sensor_data\Toco_Toucan\processed_data
  ....\data\sensor_data\Toco_Toucan\raw_data

  Creating "figures" subdirectory within C:\Users\...\Documents\toucan_evaluation
  ..\figures\Toco_Toucan

  Creating "reports" subdirectory within C:\Users\...\Documents\toucan_evaluation


Directory Structure
-------------------

Below is the directory structure created by running the ``sensor.create_directories()``
function for the ``Toco_Toucan`` sensor type.

.. code-block:: console

  toucan_evaluation                       <-- Top level directory. Set as ``work_path``.
  ├───data                                <-- Sensor and reference data, statistics, setup configuration files, etc.
  │   ├───eval_stats
  │   │   └───Toco_Toucan
  │   ├───reference_data                  <-- Subdirectories organized by reference data source.
  │   │   ├───airnow
  │   │   │   ├───processed
  │   │   │   └───raw
  │   │   ├───airnowtech
  │   │   │   ├───processed
  │   │   │   └───raw
  │   │   └───aqs
  │   │       ├───processed
  │   │       └───raw
  │   └───sensor_data                     <-- Subdirectories organized by sensor type.
  │       └───Toco_Toucan
  │           ├───processed_data
  │           └───raw_data
  ├───figures                             <-- Figures. Subdirectories organized by sensor type.
  │   └───Toco_Toucan
  └───reports

.. |br| raw:: html

   <br />
