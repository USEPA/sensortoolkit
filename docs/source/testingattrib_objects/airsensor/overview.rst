AirSensor Instantiation
=======================
The first object the user encounters is the AirSensor object. This structure is
used to keep track of sensor attributes and can be used to import and access
sensor datasets. First, users create an instance of the AirSensor object type,
specifying the make and model of the sensor. Below is an example of instantiating the
AirSensor object within the `example.py` script for the example sensor dataset included
alongside the sensortoolkit library:

.. code-block:: python

  sensor_object = sensortoolkit.AirSensor(make='Example_Make',
                                           model='Model',
                                           project_path=work_path)

.. list-table:: ``sensortoolkit.AirSensor() attributes``
 :widths: 50 75
 :header-rows: 1

 * - Attribute name
   - Description
 * - ``make``
   - The name of the manufacturer for the sensor. Users are recommended to replace spaces with underscores.
 * - ``model``
   - The name of the sensor model. Users are recommended to replace spaces with underscores.
 * - ``project_path``
   - The path to the directory where the user intends to store data, figures,
     and reports relating to the sensor being testing.

sensortoolkit organizes sensor and reference datasets, figures, and supplementary
statistics into a ‘Data and Figures’ subfolder within the user’s project path.
Users should run the following line of code to construct the folder structure
for ‘Data and Figures’ in the user’s project path:

.. code-block:: python

  sensor_object.create_directories()

.. note::
  The above code snippet assumes that the user named their instance of the ``sensortoolkit.AirSensor``
  object ``sensor_object``. If a different name was chosen, replace instances of ``sensor_object.`` with ``[custom_name].``
  to access the instance attributes such as the ``create_directories()`` method.

Users should see the following printed to the console indicating the constructed directory structure:

.. code-block:: console

  Creating "Data and Figures" subdirectory within C:\Users\...\Documents\sensortoolkit_testing
  ....\Data and Figures\eval_stats
  ....\Data and Figures\figures
  ....\Data and Figures\reference_data
  ......\Data and Figures\reference_data\airnow
  ........\Data and Figures\reference_data\airnow\raw
  ........\Data and Figures\reference_data\airnow\processed
  ......\Data and Figures\reference_data\airnowtech
  ........\Data and Figures\reference_data\airnowtech\raw
  ........\Data and Figures\reference_data\airnowtech\processed
  ......\Data and Figures\reference_data\aqs
  ........\Data and Figures\reference_data\aqs\raw
  ........\Data and Figures\reference_data\aqs\processed
  ....\Data and Figures\sensor_data

  Creating "Reports" subdirectory within C:\Users\...\Documents\sensortoolkit_testing
  ....\Data and Figures\eval_stats\Example_Make_Model
  ....\Data and Figures\figures\Example_Make_Model
  ....\Data and Figures\sensor_data\Example_Make_Model
  ......\Data and Figures\sensor_data\Example_Make_Model\processed_data
  ......\Data and Figures\sensor_data\Example_Make_Model\raw_data


Directory Structure
^^^^^^^^^^^^^^^^^^^

Below is the directory structure created by running the ``sensor_object.create_directories()``
function for the ``Example_Make_Model`` sensor type.

.. code-block:: console

  my_evaluation                             <-- Top level directory. Set as ``work_path``.
  |
  ├───Data and Figures                      <-- Sensor and reference data, statistics, and figures.
  │   ├───eval_stats                        <-- Subdirectories organized by sensor type.
  │   │   └───Example_Make_Model
  │   ├───figures                           <-- Subdirectories organized by sensor type.
  │   │   └───Example_Make_Model
  │   │       ├───deployment
  │   │       ├───Met
  │   │       ├───O3
  │   │       └───PM25
  │   ├───reference_data                    <-- Subdirectories organized by reference data source.
  │   │   ├───airnow
  │   │   │   ├───processed
  │   │   │   └───raw
  │   │   ├───airnowtech
  │   │   │   ├───raw
  │   │   │   └───processed
  │   │   └───aqs
  │   │       ├───processed
  │   │       └───raw
  │   └───sensor_data                       <-- Subdirectories organized by sensor type.
  │       └───Example_Make_Model
  │           ├───processed_data
  │           └───raw_data
  └───Reports                               <-- Performance testing reports. Subdirectories organized by sensor type.
      └───Example_Make_Model
          └───PM25
