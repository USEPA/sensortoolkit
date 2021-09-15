import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent
readme = (here / 'README.md').read_text()

setup(name='sensortoolkit',
      version='0.4.0b1',
      description='Library for evaluating air sensor data',
      long_description=readme,
      long_description_content_type='text/markdown',
      author='Samuel Frederick, ORAU Contractor for U.S. EPA ORD',
      author_email='frederick.samuel@epa.gov',
      license='The MIT License (MIT)',
      license_files=('LICENSE.txt'),
      classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        ],
      packages=find_packages(include=['sensortoolkit',
                'sensortoolkit.calculate',
                'sensortoolkit.datetime_utils',
                'sensortoolkit.deploy',
                'sensortoolkit.evaluation',
                'sensortoolkit.lib_utils',
                'sensortoolkit.model',
                'sensortoolkit.param',
                'sensortoolkit.performancereport',
                'sensortoolkit.plotting',
                'sensortoolkit.qc',
                'sensortoolkit.reference',
                'sensortoolkit.sensor_ingest'
                ]),
      package_data={'': ["performancereport/templates/O3/Reporting_Template_Base_O3.pptx",
                         "performancereport/templates/PM25/Reporting_Template_Base_PM25.pptx",
                         "performancereport/templates/placeholder_image.png",
                         "reference/method_codes/methods_criteria.csv",
                         "reference/method_codes/methods_met.csv"
                         ]
                    },
      install_requires=['matplotlib',
                        'numpy',
                        'pandas',
                        'pathlib2',
                        'python-pptx',
                        'requests',
                        'scipy',
                        'seaborn',
                        'statsmodels',
                        'urllib3',
                        'pip'
                        ]
      )
