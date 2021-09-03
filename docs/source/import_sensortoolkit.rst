===================================
Importing the sensortoolkit Library
===================================

To create scripts that utilize the `sensortoolkit` library, it’s recommended
that users develop their code in the integrated development environment (IDE).
Anaconda comes with the Spyder IDE, which can be accessed via the Anaconda
Prompt with the following command:

::

  spyder
..
  .. note::

      A reminder that `conda` users should be actively working in the ``sensor-eval``
      environment.

Once the IDE opens, the `sensortoolkit` library can be imported in the same
manner as other python packages via the following code:

.. code-block:: python

  import sensortoolkit

.. tip::
  Users can verify that the sensortoolkit library is loaded properly by checking
  the library version:

  .. code-block:: Python

    import sensortoolkit
    print(sensortoolkit.__version__)

  Console output:

  |formatted_version|



.. Users are recommended to save custom scripts that use the `sensortoolkit` library
  in the ``User_Scripts`` folder within the main library directory:

  .. parsed-literal::

      +---Data and Figures
      +---docs
      +---Documentation
      +---Example_Scripts
      +---Reports
      +---sensortoolkit
      +---User_Scripts


  In order to load modules in the `sensortoolkit` library, the python interpreter
  needs to know the directory path where the library is located. To use the library
  in a new file, user's should add the following lines of code (copy and paste).

  .. note::

    The following code block defines ``lib_path`` relative to the current directory (highlighted line),
    and assumes the file is located in either the User_Scripts folder or a parallel
    directory. If users wish to place their files elsewhere, the path for the
    library should be set by the absolute path to the main library directory.

  .. code-block:: python
      :emphasize-lines: 3

      import os
      import sys
      lib_path = os.path.abspath(__file__ + '../../..')
      if lib_path not in sys.path:
          sys.path.append(lib_path)
      import sensortoolkit
      from sensortoolkit.sensor_eval import SensorEvaluation

  .. important::

      The code above adds the library path to ``sys.path``, which is a listing of
      directories the python interpreter looks through at run time for loading
      required packages. **The code above MUST be included in files in which users
      intend to use sensortoolkit.**
