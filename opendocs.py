# -*- coding: utf-8 -*-
"""
@Author:
  Samuel Frederick, NSSC Contractor (ORAU)
  U.S. EPA, Office of Research and Development
  Center for Environmental Measurement and Modeling
  Air Methods and Characterization Division, Source and Fine Scale Branch
  109 T.W Alexander Drive, Research Triangle Park, NC 27711
  Office: 919-541-4086 | Email: frederick.samuel@epa.gov

Created:
  Wed Oct  6 11:27:22 2021
Last Updated:
  Wed Oct  6 11:27:22 2021
"""
import os
import webbrowser


file_path = os.path.abspath(__file__)

index_path = os.path.join(file_path, '..', 'docs', 'build',
                          'html', 'index.html')

webbrowser.open_new_tab(index_path)