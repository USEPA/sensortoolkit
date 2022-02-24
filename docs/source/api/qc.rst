``sensortoolkit.qc``
--------------------

The ``sensortoolkit.qc`` subpackage contains various modules for quality control
(QC) methods, including the identification and removal of duplicated timestamp
entries, downsampling of irregularly spaced data, invalidation of data points,
detection and removal of persistent or constant values, and the method of cleaning
A and B channel data for PurpleAir PA-II measurements developed by Barkjohn et al. 2021 [#f1]_.

.. note::

  U.S. EPA's Performance Targets Reports for air sensors measuring fine particulate
  matter or ozone outline protocols for testing and evaluating air sensors
  that aim to reflect "out-of-the-box" performance. As such, these documents do
  not make recommendations about quality control measures that testers may wish
  to apply to sensor data.

  **Modules in the** ``sensortoolkit.qc`` **sub-package should be considered an
  exploratory supplement to the data analysis methods recommended by EPA for
  evaluating air sensor performance.**


Clicking on each module below will open a page with a detailed description and
list of functions included within the module.

.. autosummary::
  :toctree: _autosummary
  :template: custom-module-template.rst
  :recursive:

  sensortoolkit.qc._duplicate_removal
  sensortoolkit.qc._interval_downsampling
  sensortoolkit.qc._invalidate
  sensortoolkit.qc._outlier_detection
  sensortoolkit.qc._persistent_values
  sensortoolkit.qc._purpleair_abcleaning

.. rubric:: Footnotes

.. [#f1] Barkjohn, K. K., Gantt, B., and Clements, A. L.: Development and application of a United States-wide correction for PM2.5 data collected with the PurpleAir sensor, Atmos. Meas. Tech., 14, 4617–4637, https://doi.org/10.5194/amt-14-4617-2021, 2021.
