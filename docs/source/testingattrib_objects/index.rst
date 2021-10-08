=========================
Testing Attribute Objects
=========================
sensortoolkit contains a number of class objects to aid users in various data
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
FRM/FEM monitor against which sensor measurments are being evaluated
(``sensortoolkit.ReferenceMonitor``), and the parameter or pollutant corresponding
to the measurement data of interest for the evaluation (``sensortoolkit.Parameter``).
In addition, both the ``sensortoolkit.AirSensor`` and ``sensortoolkit.ReferenceMonitor``
objects house sensor and reference data, respectively.

The library organizes datasets and various outputs, such as figures,
evaluation datasets, and reports into several sub-directories within a project folder
that user specifies.

.. important::
  Users have the option of working from within the folder location where the `sensortoolkit`
  repository was downloaded, storing sensor and reference data in the provided ``/Data and Figures`` directory,
  or users may wish to organize their work in a separate directory. In either case, various
  subdirectories and folders must be created to store data, figures, and evaluation
  statistics.

.. note::

  The following guide assumes that the user intends to place all user-created scripts,
  datasets, figures, and reports at a folder location ``C:/Users/.../Documents/my_evaluation``. While we name this
  folder ``my_evaluation``, users are free to assign their directory whatever name suits best.

From within the work directory, create a new python file and import the sensortoolkit library.
Create a variable for indicating the project folder path (below, named ``work_path``). This should also be the full directory
path for the parent directory of the script. Data, figures, and reports will be stored in this
directory location, so users may wish to create a new or empty folder for evaluations.

.. code-block:: python

  # This python script is located at "../my_evaluation/evaluation.py"
  import sensortoolkit

  # Point to the full directory path for this scripts' parent directory
  # This is the project folder path
  work_path = ('C:/Users/.../Documents/my_evaluation')


.. toctree::
    :caption: Overview of sensortoolkit Testing Attribute Objects
    :titlesonly:

    airsensor/index
    referencemonitor/index
    parameter
    setup_overview