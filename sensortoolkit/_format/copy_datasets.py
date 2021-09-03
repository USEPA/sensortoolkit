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
  Tue Aug 31 14:00:34 2021
Last Updated:
  Tue Aug 31 14:00:34 2021
"""
import tkinter as tk
from tkinter import filedialog
from distutils.dir_util import copy_tree
import os
import sys


def PromptDirectory():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory(parent=root)

    return path


def CopySensorData(name=None, path=None):
    """Prompts the user to select a source directory for datasets and copies
    files to "/Data and Figures.." raw data subdirectory for a sensor.

    Args:
        name (TYPE, optional): The name of the sensor. Defaults to None.
        path (TYPE, optional): The full path of the work directory in
        which data will be stored. Defaults to None.

    Returns:
        None.

    """
    print('[File Browser: Select the directory for recorded sensor datasets]')
    src_dir = PromptDirectory()

    dest_dir = os.path.join(path, 'Data and Figures',
                            'sensor_data', name,  'raw_data')

    print('')
    print('Source Directory:')
    print('..{0}'.format(src_dir))
    print('')
    print('Destination Directory:')
    print('..{0}'.format(dest_dir))

    if os.path.normpath(src_dir) == os.path.normpath(dest_dir):
        sys.exit('Source directory for datasets can not be the same as the '
                 'destination directory')

    valid_extensions = ['.csv', '.txt', '.xlsx']
    file_list = []
    for path, folders, files in os.walk(src_dir):
        for filename in files:
            filename_l = filename.lower()
            # check the file has one of the listed valid extensions
            valid_file = any(filename_l.endswith(extension) for
                             extension in valid_extensions)
            if valid_file:
                file_list.extend(filename)

    if file_list == []:
        sys.exit('Source directory does not contain any files corresponding to'
                 ' the following file types: {0}'.format(valid_extensions))

    end = False
    while end is False:
        return_val = input('Press enter to continue.')
        if return_val == '':
            end = True
    print('')

    copied_files = copy_tree(src_dir, dest_dir, verbose=1)
    abbrev_file_list = [file.replace(path, '') for file in copied_files]

    print('Copying the following files:')
    for file in abbrev_file_list:
        print('..' + file)
