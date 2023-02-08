Installing and Updating sensortoolkit
=====================================

sensortoolkit can be installed using a provided YAML file to create a Conda virtual environment,
using ``pip``, and by cloning the GitHub repository. This section will explain the three
installation methods in detail and how to update sensortoolkit.

.. note::

  Users will need an installation of Python (v3.6 or greater). It’s highly recommended that users
  download an `Anaconda distribution of Python <https://www.anaconda.com/products/individual>`_. Anaconda is
  a package distribution of Python that includes many widely used libraries as well as
  the `Spyder IDE <https://www.spyder-ide.org>`__ for editing and compiling code. Anaconda is free for individuals.

Install sensortoolkit
---------------------

Installing with Conda Virtual Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A virtual environment is a tool for dependency management to isolate your project by creating an
environment on top of an existing Python installation. It is highly recommended to use a virtual environment
for each new python project to ensure that the base installation of python isn't tampered with.
It's much easier to start over by deleting the virtual environment than deleting your installation of Python!

In this documentation, Conda is used as it’s a simple open source environment and package manager.
To quickly create a suitable Conda virtual environment for sensortoolkit,
with the required package versions, we can use the ``stk-environment.yml`` file included
in the GitHub repository under the ``/environments`` folder to create the ``stk-env`` Conda virtual environment.

1 - Download YAML file
""""""""""""""""""""""

Download the ``stk-environment.yml`` file included in the GitHub repository under the ``/environments``
folder to the root of your project directory.

2 - Create Conda Virtual Environment
""""""""""""""""""""""""""""""""""""

In your command line interface (CLI), (for Anaconda users, the Anaconda Prompt is recommended)
navigate to your project directory where ``stk-environment.yml`` was downloaded.
In your CLI, type in the following command:

.. code-block:: console

  conda env create -f stk-environment.yml

To activate the ``stk-env`` virtual environment, type in the following command:

.. code-block:: console

  conda activate stk-env

When activated, the virtual environment name enclosed in parenthesis will appear in your CLI as shown below. When
the virtual environment is active, any additions, deletions, and changes to installed python packages will only
exist within the virtual environment.

.. code-block:: console

  (stk-env) C:\Users\...\Documents\toucan_evaluation>

.. note::

  The above commands when creating a virtual environment assume the user has downloaded Miniconda or Anaconda.

Now, we have created a virtual environment called ``stk-env`` where python v3.8.15, sensortoolkit,
and other required package dependencies for sensortoolkit and Spyder IDE are downloaded.

.. note::

  Before running an analysis with sensortoolkit, make sure you modify your IDE's python interpreter to point to the ``/python.exe`` file within the ``stk-env`` virtual environment we created from the ``stk-environment.yml`` file. After, restart the IDE.

.. tip::

  To find the path of ``/python.exe`` within the virtual environment, open up your CLI and make sure the Conda virtual environment is activated. For Windows, type in the following command:

  .. code-block:: console

    where python

  Similar commands can be done for other operating systems.
  Copy the path of the ``/python.exe`` in the ``stk-env`` virtual environment. It should be located
  at a path that looks something like ``C:\Users\...\Miniconda3\envs\stk-env\python.exe``
  (if you have Miniconda installed). If using Spyder IDE, paste this path into the Spyder python interpreter
  (Tools>Preferences>Python Interpreter>Use the following Python interpreter: [Insert ``/python.exe`` path]).
  Then, restart the IDE.

.. tip::

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

Type the following into your CLI to install sensortoolkit (don't forget the period!):

.. code-block:: console

  pip install .

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

Open a your CLI and type the following:

.. code-block:: console

  pip install --upgrade sensortoolkit

.. tip::

	If using a virtual environment, make sure your virtual environment is activated before modifying packages!

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
