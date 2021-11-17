Importing sensortoolkit
=======================

To create scripts that utilize the `sensortoolkit` library, it’s recommended
that users develop their code in the integrated development environment (IDE).
Anaconda comes with the Spyder IDE, which can be accessed via the Anaconda
Prompt with the following command:

::

  spyder

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
