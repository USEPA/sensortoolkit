============
Installation
============

Note: Users will need an installation of Python (v3.7 or greater). It’s highly
recommended that users download an Anaconda distribution of Python. Anaconda is
a package distribution of Python that includes many widely used libraries as
well as the Spyder IDE for editing and compiling code. Anaconda is free for
individuals.

Clone the repository on BitBucket:
----------------------------------

There are a couple ways this can be done, either via a program with a UI like
SourceTree or via a command-line interface. For users just getting starting with how to
use Git, Bitbucket has a `tutorial <https://www.atlassian.com/git/tutorials/setting-up-a-repository/git-clone?utm_campaign=learn-git-clone&utm_medium=in-app-help&utm_source=stash>`_
on how to clone repositories that may be helpful. From the terminal, the
repository can be cloned via the following command

::

  $ git clone https://bitbucket.epa.gov/scm/~sfrede01/sensor-evaluation.git

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
