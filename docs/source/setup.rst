Setting Up for sensortoolkit
==============================

Setting up for sensortoolkit requires downloading Python and an IDE, creating a project directory, and
downloading your sensor and reference data. Given below is a detailed guide for setting up for sensortoolkit.

.. note::

  Users will need an installation of Python |min_python_version| or greater. It’s highly recommended that users
  download an `Anaconda distribution of Python <https://www.anaconda.com/products/individual>`_. Anaconda is
  a package distribution of Python that includes many widely used libraries as
  well as the `Spyder IDE <https://www.spyder-ide.org>`__ for editing and compiling code. Anaconda is free for
  individuals.

Setup
-----

1 - Download Python and IDE
"""""""""""""""""""""""""""

As sensortoolkit is a python package, we will need Python to use it.
In `Installing and Updating sensortoolkit <./install.html#Installing-with-Conda-Virtual-Environment>`_,
Conda is used as it’s a simple open source environment and package manager.
Hence, I suggest downloading `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ or
`Anaconda <https://www.anaconda.com/products/individual>`_ as both are free installers for Conda and Python.
They mainly differ in the number of packages automatically downloaded. The Conda documentation,
found `here <https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html#anaconda-or-miniconda>`_,
can help you decide which package manager to use.

sensortoolkit works best in development environments that allow you to simultaneously develop scripts, view 
and explore variables, and, execute code. These types of software utilities are called integrated development
environments (IDEs). To create scripts that utilize the sensortoolkit library, it’s recommended that users
develop their code in an IDE. One popular IDE for Python included alongside Anaconda distributions of
the coding language is the `Spyder IDE <https://www.spyder-ide.org>`__ which can be accessed via the
Anaconda Prompt with the following command:

.. code-block:: console

  spyder

.. caution::

  The PATH environment variable specifies the directories to be searched to find a command.
  When downloading softwares, **don't forget to adjust your path environment to add the
  respective software to your path**. This will come up in the installation steps for
  Miniconda, Anaconda, and Spyder IDE.

2 - Create a Project Directory
""""""""""""""""""""""""""""""

You will need to decide where to store scripts, data, figures, and reports that are related
to your current project. This could be any folder location on your computer. I suggest
creating a new folder in your documents directory. Let's call this directory ``toucan_evaluation``.

3 - Download Sensor and Reference Data Sets
"""""""""""""""""""""""""""""""""""""""""""

Example data sets for the *Toco Toucan* example are included in the 
`GitHub repository <https://github.com/USEPA/sensortoolkit>`_ under
the ``/example_datasets`` folder. Download these files to your project directory.
The files include one collocated reference monitor data set called ``airnowtech_example_reference_data.csv``
and three *Toco Toucan* sensor data sets called ``toco_toucan_RT01_raw.csv``, ``toco_toucan_RT02_raw.csv``,
and ``toco_toucan_RT03_raw.csv``.

.. tip::

  To download the .csv files from Github, select the .csv file and click ``View raw`` 
  or the ``Download`` button. The raw file will open in your browser. 
  Then, right-click anywhere on the page and select ``Save as...`` and save the file to the 
  project directory, ``toucan_evaluation``. **Make sure it is saved with a .csv extension.**
