=========================
Testing Attribute Objects
=========================
sensortoolkit contains several class objects to aid users in various data
analysis tasks. **These objects can be roughly divided into two categories:
testing attribute objects and evaluation objects.**

Since users may wish to evaluate multiple sensor types and numerous pollutants,
the intent in organizing the evaluation workflow into a set of recognizable and
consistent class objects is to provide an easy-to-navigate platform for conducting
evaluations and data analysis, while also allowing a high degree of customization.

-------

Testing attribute objects include the
``sensortoolkit.AirSensor`` object, ``sensortoolkit.ReferenceMonitor`` object,
and the ``sensortoolkit.Parameter`` object. These objects are used to house
information about the air sensor being tested (``sensortoolkit.AirSensor``), the
FRM/FEM monitor against which sensor measurements are being evaluated
(``sensortoolkit.ReferenceMonitor``), and the parameter or pollutant corresponding
to the measurement data of interest for the evaluation (``sensortoolkit.Parameter``).
In addition, both the ``sensortoolkit.AirSensor`` and ``sensortoolkit.ReferenceMonitor``
objects house sensor and reference data, respectively.

.. note::

  sensortoolkit organizes datasets and various outputs, such as figures,
  evaluation datasets, and reports into several sub-directories within a project folder
  that user specifies.

  The following guide assumes that the user intends to place all user-created scripts,
  datasets, figures, and reports at a project folder location ``C:/Users/.../Documents/my_evaluation``. While we name this
  folder ``my_evaluation``, users are free to assign their project directory whatever name suits best.

In the note above, we've created a folder called ``my_evaluation`` which will contain data,
figures, and reports, as well as any scripts that we create related to this project. The
path to the directory will be referred to as the **project path**.

From within the project directory, create a new python file and import the sensortoolkit library.
Next, users should indicate the project path to sensortoolkit. This is done by using the
``sensortoolkit.presets.set_project_path()`` method as indicated in the code snippet below. Users can either
pass the full path to the project directory as a string to the ``set_project_path()`` method, or if a path is
not passed, a file explorer window will open up and prompt the user to select the folder corresponding to the
project directory. 

.. code-block:: python

  # This python script is located at "../my_evaluation/evaluation.py"
  import sensortoolkit

  # Point to the full directory path for this scripts' parent directory
  # This is the project folder path

  sensortoolkit.presets.set_project_path('C:/Users/.../Documents/my_evaluation')



.. toctree::
    :caption: Overview of sensortoolkit Testing Attribute Objects
    :titlesonly:

    airsensor/index
    referencemonitor/index
    parameter
    setup_overview
