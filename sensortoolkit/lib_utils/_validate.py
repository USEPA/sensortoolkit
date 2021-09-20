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
  Mon Sep 20 15:13:36 2021
Last Updated:
  Mon Sep 20 15:13:36 2021
"""

def validate_entry():
    val = ''
    options = ['y', 'n']
    while val not in options:
        val = input('Confirm entry [y/n]: ')
        if val in options:
            return val
        else:
            print('..invalid entry, select [y/n]')