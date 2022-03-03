Installing and Updating sensortoolkit
=====================================

.. note::

  Users will need an installation of Python (v3.6 or greater). It’s highly
  recommended that users download an `Anaconda distribution of Python <https://www.anaconda.com/products/individual>`_. Anaconda is
  a package distribution of Python that includes many widely used libraries as
  well as the `Spyder IDE <https://www.spyder-ide.org>`_ for editing and compiling code. Anaconda is free for
  individuals.

Installation
------------

Installing with pip
~~~~~~~~~~~~~~~~~~~

The easiest way to install sensortoolkit is via ``pip``. Open up a command line interface (for Anaconda users,
the Anaconda Prompt is recommended) and type the following command:

.. code-block:: console

  pip install sensortoolkit

Installing from source
~~~~~~~~~~~~~~~~~~~~~~

sensortoolkit is developed and maintained in a USEPA GitHub repository. The latest
development build can be obtained by cloning the repository:

::

  git clone https://github.com/USEPA/sensortoolkit.git

Next, navigate to the folder location for the cloned repository:

.. code-block:: console

  cd path/to/sensortoolkit

Next, sensortoolkit needs to be installed to a target directory where python
looks for packages whenever the user tells python to import a package name.
By default, this is the `/site-packages`` directory, and should be located at a
path that looks something like ``C:\Users\...\Anaconda3\Lib\site-packages``
(if you have Anaconda installed). The location of this package may be a little
different depending on how your python installation was configured, although this
shouldn't matter too much.

Type the following CLI prompt to install sensortoolkit (don't forget the period!):

.. code-block:: console

  pip install .

The installation process checks for several packages sensortoolkit needs to run (dependencies).
If you have Anaconda installed, you'll notice that the installation process may indicate
that a lot of the required libraries are already installed as those packages come with
the base installation of Anaconda.

Updating sensortoolkit
----------------------

Updating from a PyPI package distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you've installed sensortoolkit using the `installing with pip <./install.html#installing-with-pip>`_ instructions listed
above, updating your installation is equally as easy!

Open a command line interface and type the following:

.. code-block:: console

  pip install --upgrade sensortoolkit

.. tip::

	If you wish to upgrade to a specific version of sensortoolkit, this can be done
  via the following command:

  .. code-block:: console

    pip install --upgrade sensortoolkit==X.X.X

  where X.X.X is replaced by the version you would like to install.

Updating from source
~~~~~~~~~~~~~~~~~~~~

If you cloned the GitHub repository, first, open a command line interface and
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
