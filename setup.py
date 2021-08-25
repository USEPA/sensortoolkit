from distutils.core import setup

setup(name='sensortoolkit',
      version='1.0.0',
      description='Library for evaluting air sensor data',
      author='Samuel Frederick, ORAU Contractor for U.S. EPA ORD',
      author_email='frederick.samuel@epa.gov',
      packages=['sensortoolkit',
                'sensortoolkit/_analysis',
                'sensortoolkit/_format',
                'sensortoolkit/_ingest',
                'sensortoolkit/_models',
                'sensortoolkit/_plotting',
                'sensortoolkit/_qc',
                'sensortoolkit/_reference',
                'sensortoolkit/_performancereport',
                'sensortoolkit/_evaluation',
                'sensortoolkit/_pkg'
                ]
      )
