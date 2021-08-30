import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent
readme = (here / 'README.md').read_text()

setup(name='sensortoolkit',
      version='0.1.0b2',
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
                'sensortoolkit._analysis',
                'sensortoolkit._format',
                'sensortoolkit._ingest',
                'sensortoolkit._models',
                'sensortoolkit._plotting',
                'sensortoolkit._qc',
                'sensortoolkit._reference',
                'sensortoolkit._performancereport',
                'sensortoolkit._evaluation',
                'sensortoolkit._pkg'
                ]),
      package_data={'': ["_performancereport/templates/O3/Reporting_Template_Base_O3.pptx",
                         "_performancereport/templates/PM25/Reporting_Template_Base_PM25.pptx"
                         # data and figures/example_make_model placeholder image
                         # method code lookup table
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
