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

def validate_entry(indent_statement=0):
    val = ''
    indent = ' '*indent_statement
    options = ['y', 'n']
    while val not in options:
        val = input(f'{indent}Confirm entry [y/n]: ')
        if val in options:
            return val
        else:
            print(f'{indent}..invalid entry, select [y/n]')

def enter_continue(indent_statement=0):
    indent = ' '*indent_statement
    end = False
    while end is False:
        return_val = input(f'{indent}Press enter to continue.')
        if return_val == '':
            end=True
    print('')
