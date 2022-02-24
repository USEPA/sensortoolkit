# -*- coding: utf-8 -*-
"""
@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

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

webbrowser.open_new_tab('file://' + os.path.normpath(index_path))
