``sensortoolkit.reference``
---------------------------

The ``sensortoolkit.reference`` subpackage contains various modules for the
ingestion and import of reference datasets. Methods are also included for
querying reference data API services such as EPA's Air Quality System (AQS) and
the AirNow API.

Clicking on each module below will open a page with a detailed description and
list of functions included within the module.

.. autosummary::
  :toctree: _autosummary
  :template: custom-module-template.rst
  :recursive:

  sensortoolkit.reference._airnowtech_to_long
  sensortoolkit.reference._import_airnowtech
  sensortoolkit.reference._load_ref_data
  sensortoolkit.reference._ref_api_query
