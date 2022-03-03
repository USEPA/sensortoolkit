import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent
readme = (here / 'README.md').read_text()

setup(name='sensortoolkit',
      version='0.8.4b1',
      description='Library for evaluating air sensor data',
      long_description=readme,
      long_description_content_type='text/markdown',
      author='Samuel Frederick, ORAU Contractor for U.S. EPA ORD',
      maintainer_email='clements.andrea@epa.gov',
      project_urls={'Source': 'https://github.com/USEPA/sensortoolkit',
                    'Documentation': 'https://sensortoolkit.readthedocs.io/en/latest/',
                    'Tracker': 'https://github.com/USEPA/sensortoolkit/issues',
                    'US EPA Air Sensor Toolbox': 'https://www.epa.gov/air-sensor-toolbox'},
      license='The MIT License (MIT)',
      license_files=('LICENSE.txt'),
      classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Atmospheric Science"
        ],
      packages=find_packages(include=['sensortoolkit',
                'sensortoolkit.calculate',
                'sensortoolkit.datetime_utils',
                'sensortoolkit.deploy',
                'sensortoolkit.evaluation_objs',
                'sensortoolkit.lib_utils',
                'sensortoolkit.model',
                'sensortoolkit.param',
                'sensortoolkit.plotting',
                'sensortoolkit.qc',
                'sensortoolkit.reference',
                'sensortoolkit.ingest',
                'sensortoolkit.testing_attrib_objs'
                ]),
      package_data={'': ["evaluation_objs/templates/O3/Reporting_Template_Base_O3.pptx",
                         "evaluation_objs/templates/PM25/Reporting_Template_Base_PM25.pptx",
                         "evaluation_objs/templates/placeholder_image.png",
                         "reference/method_codes/methods_criteria.csv",
                         "reference/method_codes/methods_met.csv",
                         "param/units.csv",
                         "param/param_info.json"
                         ]
                    },
      install_requires=['matplotlib',
                        'numpy',
                        'pandas>=1.3.0',
                        'pathlib2',
                        'python-pptx',
                        'requests',
                        'scipy',
                        'seaborn',
                        'tabulate',
                        'statsmodels',
                        'urllib3',
                        'pip',
                        'chardet'
                        ]
      )
