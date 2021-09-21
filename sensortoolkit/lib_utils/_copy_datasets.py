# -*- coding: utf-8 -*-
"""
@Author:
    | Samuel Frederick, NSSC Contractor (ORAU)
    | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Tue Aug 31 14:00:34 2021
Last Updated:
  Tue Aug 31 14:00:34 2021
"""
import tkinter as tk
from tkinter import filedialog
from distutils.dir_util import copy_tree
from shutil import copy2
import os
import sys

valid_extensions = ['.csv', '.txt', '.xlsx']

def _prompt_directory():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory(parent=root)

    return path

def _prompt_files():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilenames(parent=root)

    return path

def check_extension(file_name):
    filename_l = file_name.lower()
    # check the file has one of the listed valid extensions
    valid_file = any(filename_l.endswith(extension) for
                     extension in valid_extensions)
    return valid_file


def copy_datasets(name=None, path=None, select='directory'):
    """Prompts the user to select a source directory for datasets and copies
    files to "/Data and Figures.." raw data subdirectory for a sensor.

    Args:
        name (TYPE, optional): The name of the sensor. Defaults to None.
        path (TYPE, optional): The full path of the work directory in
        which data will be stored. Defaults to None.

    Returns:
        None.

    """
    print(f'[File Browser: Select the {select} for recorded sensor datasets]')
    print('')

    dest_dir = os.path.join(path, 'Data and Figures',
                        'sensor_data', name,  'raw_data')

    if select == 'directory':
        src_dir = _prompt_directory()

        print('Source Directory:')
        print('..{0}'.format(src_dir))

        if os.path.normpath(src_dir) == os.path.normpath(dest_dir):
            sys.exit('Source directory for datasets can not be the same as the '
                     'destination directory')

        file_list = []
        for path, folders, files in os.walk(src_dir):
            for filename in files:
                valid_file = check_extension(filename)
                print(filename, valid_file)
                if valid_file:
                    file_list.append(filename)

    if select == 'files':
        files_tup = _prompt_files()

        print('Source Files:')
        print(files_tup)

        file_list = []
        for filename in files_tup:
            valid_file = check_extension(filename)
            if valid_file:
                file_list.append(filename)

    print('')
    print('Destination Directory:')
    print('..{0}'.format(dest_dir))

    if file_list == []:
        sys.exit('Source directory does not contain any files corresponding to'
                 ' the following file types: {0}'.format(valid_extensions))

    end = False
    while end is False:
        return_val = input('Press enter to continue.')
        if return_val == '':
            end = True
    print('')

    for filename in file_list:
        copy2(filename, dest_dir)

    abbrev_file_list = [file.replace(path, '') for file in file_list]

    print('Copying the following files:')
    for file in abbrev_file_list:
        print('..' + file)

