============
Installation
============

.. note::

  Users will need an installation of Python (v3.6 or greater). It’s highly
  recommended that users download an `Anaconda distribution of Python <https://www.anaconda.com/products/individual>`_. Anaconda is
  a package distribution of Python that includes many widely used libraries as
  well as the `Spyder IDE <https://www.spyder-ide.org>`_ for editing and compiling code. Anaconda is free for
  individuals.

Clone the repository on BitBucket:
----------------------------------

There are a couple ways this can be done, either via a program with a UI like
SourceTree or via a command-line interface. For users just getting starting with how to
use Git, Bitbucket has a `tutorial <https://www.atlassian.com/git/tutorials/setting-up-a-repository/git-clone?utm_campaign=learn-git-clone&utm_medium=in-app-help&utm_source=stash>`_
on how to clone repositories that may be helpful. From the terminal, the
repository can be cloned via the following command

::

  git clone https://bitbucket.epa.gov/scm/~sfrede01/sensortoolkit.git


Installing ``sensortoolkit``
----------------------------

First, navigate to the folder location for the cloned repository:

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

The installation process checks for a number of packages sensortoolkit needs to run (dependencies).
If you have Anaconda installed, you'll notice that the installation process may indicate
that a lot of the required libraries are already installed as those packages come with
the base installation of Anaconda. Pip may need to install `python-pptx`, which is
used by sensortoolkit to create testing reports as .pptx files.

Users will see something similar to the following be printed to the console:

.. code-block:: console

  Processing c:\users\..\documents\sensortoolkit
  Requirement already satisfied: matplotlib in c:\users\sfrede01\anaconda3\lib\site-packages (from sensortoolkit==0.1.0b2) (3.3.4)
  Requirement already satisfied: numpy in c:\users\sfrede01\anaconda3\lib\site-packages (from sensortoolkit==0.1.0b2) (1.20.1)
  Requirement already satisfied: pandas in c:\users\sfrede01\anaconda3\lib\site-packages (from sensortoolkit==0.1.0b2) (1.2.4)
  Requirement already satisfied: pathlib2 in c:\users\sfrede01\anaconda3\lib\site-packages (from sensortoolkit==0.1.0b2) (2.3.5)
  Requirement already satisfied: python-pptx in c:\users\sfrede01\anaconda3\lib\site-packages (from sensortoolkit==0.1.0b2) (0.6.18)
  Requirement already satisfied: requests in c:\users\sfrede01\anaconda3\lib\site-packages (from sensortoolkit==0.1.0b2) (2.25.1)
  Requirement already satisfied: scipy in c:\users\sfrede01\anaconda3\lib\site-packages (from sensortoolkit==0.1.0b2) (1.6.2)
  Requirement already satisfied: seaborn in c:\users\sfrede01\anaconda3\lib\site-packages (from sensortoolkit==0.1.0b2) (0.11.1)
  Requirement already satisfied: statsmodels in c:\users\sfrede01\anaconda3\lib\site-packages (from sensortoolkit==0.1.0b2) (0.12.2)
  Requirement already satisfied: urllib3 in c:\users\sfrede01\anaconda3\lib\site-packages (from sensortoolkit==0.1.0b2) (1.26.4)
  Requirement already satisfied: pip in c:\users\sfrede01\anaconda3\lib\site-packages (from sensortoolkit==0.1.0b2) (21.0.1)
  Requirement already satisfied: pyparsing!=2.0.4,!=2.1.2,!=2.1.6,>=2.0.3 in c:\users\sfrede01\anaconda3\lib\site-packages (from matplotlib->sensortoolkit==0.1.0b2) (2.4.7)
  Requirement already satisfied: pillow>=6.2.0 in c:\users\sfrede01\anaconda3\lib\site-packages (from matplotlib->sensortoolkit==0.1.0b2) (8.2.0)
  Requirement already satisfied: python-dateutil>=2.1 in c:\users\sfrede01\anaconda3\lib\site-packages (from matplotlib->sensortoolkit==0.1.0b2) (2.8.1)
  Requirement already satisfied: kiwisolver>=1.0.1 in c:\users\sfrede01\anaconda3\lib\site-packages (from matplotlib->sensortoolkit==0.1.0b2) (1.3.1)
  Requirement already satisfied: cycler>=0.10 in c:\users\sfrede01\anaconda3\lib\site-packages (from matplotlib->sensortoolkit==0.1.0b2) (0.10.0)
  Requirement already satisfied: six in c:\users\sfrede01\anaconda3\lib\site-packages (from cycler>=0.10->matplotlib->sensortoolkit==0.1.0b2) (1.15.0)
  Requirement already satisfied: pytz>=2017.3 in c:\users\sfrede01\anaconda3\lib\site-packages (from pandas->sensortoolkit==0.1.0b2) (2021.1)
  Requirement already satisfied: lxml>=3.1.0 in c:\users\sfrede01\anaconda3\lib\site-packages (from python-pptx->sensortoolkit==0.1.0b2) (4.6.3)
  Requirement already satisfied: XlsxWriter>=0.5.7 in c:\users\sfrede01\anaconda3\lib\site-packages (from python-pptx->sensortoolkit==0.1.0b2) (1.3.8)
  Requirement already satisfied: chardet<5,>=3.0.2 in c:\users\sfrede01\anaconda3\lib\site-packages (from requests->sensortoolkit==0.1.0b2) (4.0.0)
  Requirement already satisfied: idna<3,>=2.5 in c:\users\sfrede01\anaconda3\lib\site-packages (from requests->sensortoolkit==0.1.0b2) (2.10)
  Requirement already satisfied: certifi>=2017.4.17 in c:\users\sfrede01\anaconda3\lib\site-packages (from requests->sensortoolkit==0.1.0b2) (2020.12.5)
  Requirement already satisfied: patsy>=0.5 in c:\users\sfrede01\anaconda3\lib\site-packages (from statsmodels->sensortoolkit==0.1.0b2) (0.5.1)
  Building wheels for collected packages: sensortoolkit
    Building wheel for sensortoolkit (setup.py) ... done
    Created wheel for sensortoolkit: filename=sensortoolkit-0.1.0b2-py3-none-any.whl size=264195 sha256=255f3b7f2818bc10ed695d7bbdf9facfcde8fbe88866621d77cba99376ef8fbb
    Stored in directory: C:\Users\SFREDE01\AppData\Local\Temp\pip-ephem-wheel-cache-k4dnnl3u\wheels\d0\5d\9f\8f5c8d55a67e2c9d9ff85111d0e96da3ef3782e3356c46e010
  Successfully built sensortoolkit
  Installing collected packages: sensortoolkit
  Successfully installed sensortoolkit-0.1.0b2

..
  Install package dependencies:
  -----------------------------

  `conda` and `pip` are two popular package managers for installing python packages
  and manage the dependency structure for the packages the user wishes to install.
  Below are guides for installing dependencies for `senortoolkit` in either `conda`
  or `pip`.

  **Please note, users should either follow the conda installation process
  using a virtual environment or install dependencies with pip.**


  Installing dependencies in a conda virtual environment
  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  If users have an Anaconda distribution of Python, users may wish to create a virtual
  environment via `conda` for installing the dependencies required by the `sensortoolkit`
  library. The benefit of a virtual environment is that software package versions
  required by the library won't modify package versions in the
  default base environment (a virtual environment creates a walled garden where
  users can install the packages and the package versions they require without
  changing the state or version of packages installed in the base environment).

  `sensortoolkit` comes with the file ``env.yml`` that allows easy installation of
  dependencies into a `conda` virtual environment named ``sensor-eval``. First,
  navigate to the folder location for the cloned repository:
  ::
    $ cd path/to/library

  Next, create the virtual environment from the provided ``env.yml`` file. This
  will install various packages that are required by the `sensortoolkit` library.
  ::

    $ conda env create -f env.yml

  Finally, activate the environment to use packages installed in the environment:
  ::

    $ conda activate sensor-eval

  If the environment has been activate successfully, the command prompt should
  display the environment name in parentheses before the system prompt ``$``:
  ::

    (sensor-eval) $

  .. tip::

      To exit the ``sensor-eval`` environment, type: ``conda deactivate``


  Installing dependencies with pip
  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  .. warning::

      `conda` users are discouraged from using pip to install dependencies, as
      packages installed via `pip` may supersede previously installed packages
      via `conda`. In addition, `conda` and `pip` manage dependencies differently,
      and this may lead to potential issues if users wish to update package versions
      at a future point.

  First, navigate to the folder location for the cloned repository:
  ::

    $ cd path/to/library

  A list of dependencies and package versions is provided in the ``requirements.txt``
  file within the main directory of the library. Dependencies are installed with
  `pip` via the following command:
  ::

    $ pip install –r requirements.txt --user

  Run ``setup.py``
  ----------------------------------

  The last step in the installation process is ensuring that the ``sensortoolkit``
  package modules can be imported from any directory location on a users system. For Anaconda
  users, packages are placed in a directory location with a path that should look
  something like ``user/Anaconda3/Lib/site-packages``.

  To run the setup.py module, open a command line utility and ensure that the current
  directory is the location of the cloned repository. Then type the following command:
  ::

    $ python setup.py install
