Installing and Updating sensortoolkit
=====================================

sensortoolkit can be installed using a provided YAML file to create a Conda virtual environment,
using ``pip``, or by cloning the GitHub repository. This section will explain the three
installation methods in detail and how to update sensortoolkit.

.. note::

  Users will need an installation of Python |min_python_version| or greater. It’s highly recommended that users
  download an `Anaconda distribution of Python <https://www.anaconda.com/products/individual>`_. Anaconda is
  a package distribution of Python that includes many widely used libraries as well as
  the `Spyder IDE <https://www.spyder-ide.org>`__ for editing and compiling code. Anaconda is free for individuals.

.. tip::

  Have familiarity with your operating system's command line interface (CLI) commands. Mainly
  in navigating through directories. For Anaconda users, the Anaconda Prompt is recommended.

Install sensortoolkit
---------------------

Installing with Conda Virtual Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A virtual environment is a tool for dependency management to isolate your project by creating an
environment on top of an existing Python installation. **It is highly recommended to use a virtual environment
for each new python project to ensure that the base installation of python isn't tampered with.**
It's much easier to start over by deleting the virtual environment than deleting your installation of Python!

In this documentation, Conda is used as it’s a simple open source environment and package manager.
To quickly create a suitable Conda virtual environment for sensortoolkit,
with the required package versions, we can use the ``sensortoolkit_env.yml`` file included
in the GitHub repository under the ``/environments`` folder to create the ``stk-env`` Conda virtual environment.

1 - Download YAML file
""""""""""""""""""""""

Download the ``sensortoolkit_env.yml`` file included in the 
`GitHub repository <https://github.com/USEPA/sensortoolkit>`_ under the ``/environments``
folder to the root of your project directory.

.. tip::

  To download the ``sensortoolkit_env.yml`` file from Github, select the .yml file and right-click 
  the ``raw`` button at the top. Then, select ``Save link as...``, and save to the 
  project directory, ``toucan_evaluation``. **Make sure the file extension stays as just .yml**.

2 - Create Conda Virtual Environment
""""""""""""""""""""""""""""""""""""

Now, we will use the ``sensortoolkit_env.yml`` file to create a virtual environment.
In your command line interface (CLI), (for Anaconda users, the Anaconda Prompt is recommended)
navigate to your project directory where ``sensortoolkit_env.yml`` was downloaded. Something similar to
below should be seen in your CLI.

.. code-block:: console

  C:\Users\...\Documents\toucan_evaluation>

**While in your project directory**, type in the following command in your CLI:

.. code-block:: console

  conda env create -f sensortoolkit_env.yml 

The user will see something similar to the following printed after creating the virtual environment.

.. code-block:: console

  Retrieving notices: ...working... done
  Collecting package metadata (repodata.json): done
  Solving environment: done

  Downloading and Extracting Packages
                                                                                                                                                 
  Preparing transaction: done                                                                                                                      
  Verifying transaction: done                                                                                                                      
  Executing transaction: done                                                                                                                      
  Installing pip dependencies: | Ran pip subprocess with arguments:
  ['C:\\Users\\...\\Miniconda3\\envs\\stk-env\\python.exe', '-m', 'pip', 'install', '-U', '-r', 'C:\\Users\\...\\Documents\\toucan_evaluation\\condaenv.0ut78_b8.requirements.txt', '--exists-action=b']     
  Pip subprocess output:
  Requirement already satisfied: charset_normalizer==2.0.4 in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from -r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 1)) (2.0.4)
  Collecting timezonefinder==6.1.9
    Using cached timezonefinder-6.1.9-cp38-cp38-win_amd64.whl
  Collecting python-pptx==0.6.21
    Using cached python_pptx-0.6.21-py3-none-any.whl
  Collecting sensortoolkit
    Using cached sensortoolkit-1.0.0-py3-none-any.whl (367 kB)
  Requirement already satisfied: cffi<2,>=1.15.1 in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from timezonefinder==6.1.9->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 2)) (1.15.1)
  Collecting h3<4,>=3.7.6
    Using cached h3-3.7.6-cp38-cp38-win_amd64.whl (855 kB)
  Requirement already satisfied: setuptools>=65.5 in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from timezonefinder==6.1.9->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 2)) (65.6.3)
  Requirement already satisfied: numpy<2,>=1.18 in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from timezonefinder==6.1.9->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 2)) (1.23.5)
  Requirement already satisfied: Pillow>=3.3.2 in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from python-pptx==0.6.21->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 3)) (9.3.0)
  Requirement already satisfied: lxml>=3.1.0 in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from python-pptx==0.6.21->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 3)) (4.9.1)
  Collecting XlsxWriter>=0.5.7
    Using cached XlsxWriter-3.0.8-py3-none-any.whl (152 kB)
  Requirement already satisfied: appdirs in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from sensortoolkit->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 4)) (1.4.4)
  Requirement already satisfied: matplotlib in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from sensortoolkit->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 4)) (3.6.2)
  Requirement already satisfied: statsmodels in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from sensortoolkit->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 4)) (0.13.5)
  Requirement already satisfied: seaborn in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from sensortoolkit->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 4)) (0.11.2)
  Requirement already satisfied: pip in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from sensortoolkit->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 4)) (22.3.1)
  Requirement already satisfied: requests in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from sensortoolkit->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 4)) (2.28.1)
  Requirement already satisfied: tabulate in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from sensortoolkit->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 4)) (0.8.10)
  Requirement already satisfied: chardet in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from sensortoolkit->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 4)) (4.0.0)
  Requirement already satisfied: urllib3 in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from sensortoolkit->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 4)) (1.26.14)
  Requirement already satisfied: pandas>=1.3.0 in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from sensortoolkit->-r C:\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 4)) (1.3.5)
  Requirement already satisfied: pathlib2 in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from sensortoolkit->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 4)) (2.3.6)
  Requirement already satisfied: scipy in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from sensortoolkit->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 4)) (1.10.0)
  Requirement already satisfied: pycparser in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from cffi<2,>=1.15.1->timezonefinder==6.1.9->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 2)) (2.21)
  Requirement already satisfied: pytz>=2017.3 in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from pandas>=1.3.0->sensortoolkit->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 4)) (2022.7)
  Requirement already satisfied: python-dateutil>=2.7.3 in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from pandas>=1.3.0->sensortoolkit->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 4)) (2.8.2)
  Requirement already satisfied: kiwisolver>=1.0.1 in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from matplotlib->sensortoolkit->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 4)) (1.4.4)
  Requirement already satisfied: contourpy>=1.0.1 in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from matplotlib->sensortoolkit->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 4)) (1.0.5)
  Requirement already satisfied: fonttools>=4.22.0 in c:\users\...\miniconda3\envs\stk-env\lib\site-packages (from matplotlib->sensortoolkit->-r C:\Users\...\Documents\toucan_evaluation\condaenv.0ut78_b8.requirements.txt (line 4)) (4.25.0)

**To use the virtual environment we must activate it.** To activate the ``stk-env``
virtual environment, type in the following command:

.. code-block:: console

  conda activate stk-env

When activated, the virtual environment name enclosed in parenthesis will appear in your CLI as shown below.

.. code-block:: console

  (stk-env) C:\Users\...\Documents\toucan_evaluation>

.. caution:: 

  When the virtual environment is active, any additions, deletions, and changes to installed python packages will only
  exist within the virtual environment. **Hence, if any changes to packages must be done for this project
  the virtual environment must be activated first.**

.. note::

  The above commands when creating a virtual environment assume the user has downloaded Miniconda or Anaconda.
  `Click here <./setup.html#download-python-and-ide>`__ for more info about installing Python with Miniconda or Anaconda.

Now, we have created a virtual environment called ``stk-env`` where Python 3.8, sensortoolkit,
and other required package dependencies for sensortoolkit and Spyder IDE are downloaded!

.. caution::

  Before running an analysis with sensortoolkit, make sure you modify your IDE's Python interpreter to point to the ``/python.exe`` file within the ``stk-env`` virtual environment. After, restart the IDE.

.. tip::

  To find the path of ``/python.exe`` within the virtual environment, open up your CLI and make sure the Conda virtual environment is activated. For Windows, type in the following command:

  .. code-block:: console

    where python

  Similar commands can be done for other operating systems.
  Copy the path of the ``/python.exe`` in the ``stk-env`` virtual environment. It should be located
  at a path that looks something like ``C:\Users\...\Miniconda3\envs\stk-env\python.exe``
  (if you have Miniconda installed). If using Spyder IDE, paste this path into the Spyder python interpreter
  (Tools>Preferences>Python Interpreter>Use the following Python interpreter: [Insert path]).
  Then, restart the IDE.

.. tip::

  If you would like to return to the base environment after finishing your project work,
  the user should deactivate the virtual environment.
  To deactivate the Conda virtual environment, type in the following in your CLI:

  .. code-block:: console

    conda deactivate

Installing with pip
^^^^^^^^^^^^^^^^^^^

The easiest way to install sensortoolkit is via ``pip``. Open up a CLI and type the following command:

.. code-block:: console

  pip install sensortoolkit

Installing from source
^^^^^^^^^^^^^^^^^^^^^^

sensortoolkit is developed and maintained in a USEPA GitHub repository. The latest
development build can be obtained by cloning the repository:

.. code-block:: console

  git clone https://github.com/USEPA/sensortoolkit.git

.. note::

  Git is a free and open source distributed version control system. In order to use Git commands you will need to download Git found `here <https://git-scm.com/downloads>`_.

Next, navigate to the folder location for the cloned repository:

.. code-block:: console

  cd path/to/sensortoolkit

Next, sensortoolkit needs to be installed to a target directory where python
looks for packages when asked by the user to import a package.
By default, this is the ``/site-packages`` directory, and should be located at a
path that looks something like ``C:\Users\...\Anaconda3\Lib\site-packages``
(if you have Anaconda installed). The location of this package may be a little
different depending on how your python installation was configured, although this
shouldn't matter too much.

Type the following into your CLI to install sensortoolkit. **Don't forget the period!**:

.. code-block:: console

  pip install .

----

The installation process checks for several packages sensortoolkit needs to run (dependencies).
If you have Anaconda installed, you'll notice that the installation process may indicate
that a lot of the required libraries are already installed as those packages come with
the base installation of Anaconda.

.. tip::

  Users can verify that the sensortoolkit library is loaded properly by checking the library version:

  .. code-block:: Python

    import sensortoolkit
    print(sensortoolkit.__version__)

  Console output:

  |formatted_version|

Update sensortoolkit
--------------------

Updating from a PyPI package distribution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you've installed sensortoolkit using a
`Conda virtual environment <./install.html#Installing-with-Conda-Virtual-Environment>`_ or with
`pip <./install.html#installing-with-pip>`_, updating your installation is equally as easy!

.. caution::

	If using a virtual environment, make sure your virtual environment is activated before using commands to modify packages!

Open your CLI and type the following:

.. code-block:: console

  pip install --upgrade sensortoolkit

.. tip::

  If you wish to upgrade to a specific version of sensortoolkit, this can be done via the following command:

  .. code-block:: console

    pip install --upgrade sensortoolkit==X.X.X

  where X.X.X is replaced by the version you would like to install.

Updating from source
^^^^^^^^^^^^^^^^^^^^

If you cloned the GitHub repository, first, open your CLI and
change directories to the folder containing your cloned version of the sensortoolkit repository:

.. code-block:: console

  cd path/to/sensortoolkit

Next, install available updates via a 'git pull' command:

.. code-block:: console

  git pull

  remote: Enumerating objects: 4141, done.
  remote: Counting objects: 100% (4141/4141), done.
  remote: Compressing objects: 100% (690/690), done.
  remote: Total 3747 (delta 3334), reused 3396 (delta 3044), pack-reused 0
  Receiving objects: 100% (3747/3747), 7.86 MiB | 487.00 KiB/s, done.
  Resolving deltas: 100% (3334/3334), completed with 362 local objects.
  From https://github.com/USEPA/sensortoolkit.git
   e5aed929..026ee1c2  master -> origin/master
  Updating files: 100% (559/559), done.
  Updating e5aed929..026ee1c2
  Fast-forward
  [A log of various files in the source code that have been modified in the current dev. package]
