# sensortoolkit - Air Sensor Data Analysis Library

[![PyPI version](https://badge.fury.io/py/sensortoolkit.svg)](https://badge.fury.io/py/sensortoolkit)
[![Documentation Status](https://readthedocs.org/projects/sensortoolkit/badge/?version=latest)](https://sensortoolkit.readthedocs.io/en/latest/?badge=latest)
[![Downloads](https://pepy.tech/badge/sensortoolkit)](https://pepy.tech/project/sensortoolkit)

![Sensors at an Ambient Air Monitoring Site](https://github.com/USEPA/sensortoolkit/blob/master/docs/_readmefigs_/CSAM_3_crop.jpg?raw=true)

*Sensors at an ambient air monitoring site. Photo Credit - South Coast AQMD AQ-SPEC Program*

*Samuel Frederick, NSSC Contractor (ORAU)*

****
## Readme Guide
* [Overview](#overview)
  * [Key Features](#key-features)
  * [Dependencies](#dependencies)
  * [Contact and Resources](#contact)
* [Installation](#install)

## Overview <a name="overview"></a>

sensortoolkit is a Python library for evaluating air sensor data. The
library is intended for use with sensors collocated at ambient air
monitoring sites alongside FRM/FEM monitors for comparison and analysis
of sensor data against reference-grade data.

<span class="title-ref">sensortoolkit</span> can be used to evaluate
sensor data for a single or multiple sensors measuring one of the
following pollutants: PM<sub>1</sub>, PM<sub>2.5</sub> [criteria], PM<sub>10</sub> [criteria], CO [criteria],
NO, NO<sub>2</sub> [criteria], NO<sub>x</sub>, O<sub>3</sub> [criteria], SO<sub>2</sub> [criteria], SO<sub>x</sub>.

sensortoolkit is most suitable for individuals who have some prior
coding experience in python. The library is equipped with an API
(application programming interface) that allows for ease of navigation
and customization, making sensortoolkit accessible to individuals with a
wide range of skillsets (e.g., individuals interested in monitoring
their own sensor data, students and academic researchers, and industry
professionals).

In February 2021, EPA released [two reports](https://www.epa.gov/air-sensor-toolbox/air-sensor-performance-targets-and-testing-protocols#reports) detailing recommended performance testing protocols, metrics, and target values for the evaluation of sensors measuring either fine particulate matter (PM<sub>2.5</sub>) or ozone (O<sub>3</sub>). The sensortoolkit library includes numerous modules for computing performance metrics recommended by U.S. EPA for evaluating PM<sub>2.5</sub> and O<sub>3</sub> sensors. Additionally, plotting functions are included for visualizing performance evaluation results, including visualization of sensor performance metric values against U.S. EPA’s performance targets, sensor time series, scatter plots comparing collocated sensor and reference measurements, distribution plots for displaying the range of meteorological conditions during the deployment, etc. Tabular statistics and figures can be automatically compiled into testing reports recommended by U.S. EPA’s performance targets documents for testing conducting at ambient air monitoring sites.

## Key features: <a name="key-features"></a>

**The primary goal of `sensortoolkit` is to provide a platform for
analyzing air sensor data regardless of formatting differences across
sensor data formatting schemes.** This goal extends to reference data as
well, and interactive setup modules are included for interpreting the
recorded format for datasets for subsequent Ingestion into standardized
formatting schemes for sensor and reference data.

-   Import sensor data via a standardized ingestion process and
    interactive setup module
-   Average to 1-hour and/or 24-hour averaging intervals.
-   Import FRM/FEM reference data from a variety of sources, including
    ingestion modules for importing data from AirNowTech, and modules
    for querying either the AQS or AirNow API services.
-   Submit queries for single or multiple parameters, parse datasets
    into a consistent reference data format and save unmodified and
    processed datasets to a data directory.
- Conduct analysis with the `SensorEvaluation` module  
-   Compute U.S. EPA’s recommended performance metrics for evaluating
    PM<sub>2.5</sub> and O<sub>3</sub> sensors.

-   Visualize sensor performance with various figures and save to file location.  
    -   Sensor vs. FRM/FEM scatter plots
    -   Timeseries indicating both sensor and FRM/FEM concentrations
    -   Performance metric results and comparison against target
        values/ranges.
    -   Save performance evaluation results, statistics, and
        supplemental information detailing the deployment conditions to
        a deployment JSON file.

-   Create testing reports using U.S. EPA’s base-testing report template
    (PowerPoint file) with the `PerformanceReport` module.
-   Additional modules are included for calculating quantities (AQI,
    PM<sub>2.5</sub> NowCast, application of sensor correction
    equations, the U.S. Wide correction equation for PurpleAir sensors
    via [Barkjohn et al. 2021](https://amt.copernicus.org/articles/14/4617/2021/), etc.) and conducting additional analysis
    (quality control modules for identifying outliers, invalidation of
    datapoints, A&B channel cleaning for PurpleAir data via [Barkjohn et al. 2021](https://amt.copernicus.org/articles/14/4617/2021/), etc.)
-   Access to modules utilized by the `SensorEvaluation` and `PerformanceReport` for greater customization
    in conducting analysis.


## Dependencies: <a name="dependencies"></a>
* [Python](https://www.python.org/) >= 3.6
* [pandas](https://pypi.org/project/pandas/) >= 1.3.0
* [numpy](https://pypi.org/project/numpy/) >= 1.16.5
* [matplotlib](https://pypi.org/project/matplotlib/) >= 3.1.1
* [seaborn](https://pypi.org/project/seaborn/) >= 0.9.0
* [statsmodels](https://pypi.org/project/statsmodels/) >= 0.10.1
* [pathlib2](https://pypi.org/project/pathlib2/) >= 2.3.5
* [requests](https://pypi.org/project/requests/) >= 2.25.1
* [python-pptx](https://pypi.org/project/python-pptx/) >= 0.6.18
* [tabulate](https://pypi.org/project/tabulate/) >= 0.8.9
* [SciPy](https://pypi.org/project/scipy/)
* [urllib3](https://pypi.org/project/urllib3/)
* [pip](https://pypi.org/project/pip/)

## Contact and Resources <a name="contact"></a>
*Please direct all inquiries to*\
&nbsp;&nbsp;&nbsp;&nbsp;Andrea Clements Ph.D., Research Physical Scientist\
&nbsp;&nbsp;&nbsp;&nbsp;U.S. EPA, Office of Research and Development\
&nbsp;&nbsp;&nbsp;&nbsp;Center for Environmental Measurement and Modeling\
&nbsp;&nbsp;&nbsp;&nbsp;Air Methods & Characterization Division, Source and Fine Scale Branch\
&nbsp;&nbsp;&nbsp;&nbsp;109 T.W. Alexander Drive, Research Triangle Park, NC  27711\
&nbsp;&nbsp;&nbsp;&nbsp;Email: clements.andrea@epa.gov

Additional information about EPA's research involving air sensors including the reports for fine particulate matter sensors and ozone sensors, past evaluation results, and additional documentation are located at EPA's [Air Sensor Toolbox](https://www.epa.gov/air-sensor-toolbox).

## Disclaimer

This software/application was developed by the U.S. Environmental Protection
Agency (USEPA). No warranty expressed or implied is made regarding the accuracy
or utility of the system, nor shall the act of distribution constitute any such
warranty. The USEPA has relinquished control of the information and no longer
has responsibility to protect the integrity, confidentiality or availability of
the information. Any reference to specific commercial products, processes, or
services by service mark, trademark, manufacturer, or otherwise, does not
constitute or imply their endorsement, recommendation or favoring by the USEPA.
The USEPA seal and logo shall not be used in any manner to imply endorsement of
any commercial product or activity by the USEPA or the United States Government.

****
## Installation <a name="install"></a>

***The following installation guide is pulled from the HTML formatted documentation packaged alongside `sensortoolkit`. Once the repository has been downloaded, users
are strongly recommended to follow the remainder of the documentation via the HTML
documentation. The HTML documentation contains greater detail regarding the implementation of the
`sensortoolkit` library, including a quick start guide, detailed API documentation, formatted tips, notes, and general recommendations for using the library.***

To open the included HTML documentation, open a command line interface and ensure that the current working directory is the folder location
where the repository was downloaded. Next, type the following command and hit enter:
```
python opendocs.py
```
The documentation should open in your default browser, and you should see a landing page that looks something like this:

![sensortoolkit Landing Page](https://github.com/USEPA/sensortoolkit/blob/master/docs/_readmefigs_/toolkit_landing_page.png?raw=true)

Note: Users will need an installation of Python (v3.6 or greater). It’s
highly recommended that users download an Anaconda distribution of
Python. Anaconda is a package distribution of Python that includes many
widely used libraries as well as the Spyder IDE for editing and
compiling code. Anaconda is free for individuals.

### 1. Clone the repository on BitBucket:

From a command line interface, the repository can be cloned via the following command

    git clone https://github.com/USEPA/sensortoolkit.git

### 2. Install `sensortoolkit`

First, navigate to the folder location for the cloned repository:

```
cd path/to/sensortoolkit
```

Next, install the library with pip:

```
pip install .
```

Users will see something similar to the following be printed to the
console:
```
Processing c:\users\...\documents\sensortoolkit
Requirement already satisfied: matplotlib in c:\users\...\anaconda3\lib\site-packages (from sensortoolkit) (3.3.4)
Requirement already satisfied: numpy in c:\users\...\anaconda3\lib\site-packages (from sensortoolkit) (1.20.1)
Requirement already satisfied: pandas in c:\users\...\anaconda3\lib\site-packages (from sensortoolkit) (1.2.4)
Requirement already satisfied: pathlib2 in c:\users\...\anaconda3\lib\site-packages (from sensortoolkit) (2.3.5)
Requirement already satisfied: python-pptx in c:\users\...\anaconda3\lib\site-packages (from sensortoolkit) (0.6.18)
Requirement already satisfied: requests in c:\users\...\anaconda3\lib\site-packages (from sensortoolkit) (2.25.1)
Requirement already satisfied: scipy in c:\users\...\anaconda3\lib\site-packages (from sensortoolkit) (1.6.2)
Requirement already satisfied: seaborn in c:\users\...\anaconda3\lib\site-packages (from sensortoolkit) (0.11.1)
Requirement already satisfied: statsmodels in c:\users\...\anaconda3\lib\site-packages (from sensortoolkit) (0.12.2)
Requirement already satisfied: urllib3 in c:\users\...\anaconda3\lib\site-packages (from sensortoolkit) (1.26.4)
Requirement already satisfied: pip in c:\users\...\anaconda3\lib\site-packages (from sensortoolkit) (21.0.1)
Requirement already satisfied: pyparsing!=2.0.4,!=2.1.2,!=2.1.6,>=2.0.3 in c:\users\...\anaconda3\lib\site-packages (from matplotlib->sensortoolkit) (2.4.7)
Requirement already satisfied: pillow>=6.2.0 in c:\users\...\anaconda3\lib\site-packages (from matplotlib->sensortoolkit) (8.2.0)
Requirement already satisfied: python-dateutil>=2.1 in c:\users\...\anaconda3\lib\site-packages (from matplotlib->sensortoolkit) (2.8.1)
Requirement already satisfied: kiwisolver>=1.0.1 in c:\users\...\anaconda3\lib\site-packages (from matplotlib->sensortoolkit) (1.3.1)
Requirement already satisfied: cycler>=0.10 in c:\users\...\anaconda3\lib\site-packages (from matplotlib->sensortoolkit) (0.10.0)
Requirement already satisfied: six in c:\users\...\anaconda3\lib\site-packages (from cycler>=0.10->matplotlib->sensortoolkit) (1.15.0)
Requirement already satisfied: pytz>=2017.3 in c:\users\...\anaconda3\lib\site-packages (from pandas->sensortoolkit) (2021.1)
Requirement already satisfied: lxml>=3.1.0 in c:\users\...\anaconda3\lib\site-packages (from python-pptx->sensortoolkit) (4.6.3)
Requirement already satisfied: XlsxWriter>=0.5.7 in c:\users\...\anaconda3\lib\site-packages (from python-pptx->sensortoolkit) (1.3.8)
Requirement already satisfied: chardet<5,>=3.0.2 in c:\users\...\anaconda3\lib\site-packages (from requests->sensortoolkit) (4.0.0)
Requirement already satisfied: idna<3,>=2.5 in c:\users\...\anaconda3\lib\site-packages (from requests->sensortoolkit) (2.10)
Requirement already satisfied: certifi>=2017.4.17 in c:\users\...\anaconda3\lib\site-packages (from requests->sensortoolkit) (2020.12.5)
Requirement already satisfied: patsy>=0.5 in c:\users\...\anaconda3\lib\site-packages (from statsmodels->sensortoolkit) (0.5.1)
Building wheels for collected packages: sensortoolkit
  Building wheel for sensortoolkit (setup.py) ... done
  Created wheel for sensortoolkit: filename=sensortoolkit-py3-none-any.whl size=264195 sha256=255f3b7f2818bc10ed695d7bbdf9facfcde8fbe88866621d77cba99376ef8fbb
  Stored in directory: C:\Users\...\AppData\Local\Temp\pip-ephem-wheel-cache-k4dnnl3u\wheels\d0\5d\9f\8f5c8d55a67e2c9d9ff85111d0e96da3ef3782e3356c46e010
Successfully built sensortoolkit
Installing collected packages: sensortoolkit
Successfully installed sensortoolkit
```

### *Note*
The above console output indicates that the dependencies for ``sensortoolkit``
were previously installed and found on the user's system. Any packages not found
during installation will be installed by pip.
