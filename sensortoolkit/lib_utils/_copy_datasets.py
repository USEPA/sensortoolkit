# -*- coding: utf-8 -*-
"""
This module contains methods for interactively prompting user input to select
data files that will be copied from a specified location on the user's system
to the ``/data`` directory located within the project path.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Tue Aug 31 14:00:34 2021
Last Updated:
  Tue Aug 31 14:00:34 2021
"""
import os
import sys
from textwrap import wrap
import tkinter as tk
from tkinter import filedialog
from shutil import copy2
from sensortoolkit.lib_utils import enter_continue

valid_extensions = ['.csv', '.txt', '.xlsx']


def _prompt_directory():
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    path = filedialog.askdirectory(parent=root)
    if path == '':
        raise ValueError('Directory selection terminated by user')
    return path


def _prompt_files(**kwargs):
    single_file = kwargs.get('single_file', False)
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    if not single_file:
        path = filedialog.askopenfilenames(parent=root)
    else:
        path = filedialog.askopenfilename(parent=root)
    if path == '':
        raise ValueError('File selection terminated by user')
    return path


def _check_extension(file_name, expect_extension):
    filename_l = file_name.lower()

    if expect_extension is None:
        # check the file has one of the listed valid extensions
        valid_file = any(filename_l.endswith(extension) for
                         extension in valid_extensions)
    else:
        valid_file = bool(filename_l.endswith(expect_extension))

    return valid_file


def copy_datasets(data_type=None, path=None, select='directory', **kwargs):
    """Prompts the user to select a source directory for datasets and copies
    files to ``/data..`` raw data subdirectory for a sensor.

    Args:
        data_type (str, optional):
            Indicates the type of device that recorded the datasets the user
            wishes to copy to the ``[project_path]/data`` directory. Select
            either ``'sensor'`` to indicate copying of air sensor datasets or
            ``'reference'`` to indicate copying of reference monitor datasets.
        path (str, optional):
            The full path of the work directory in which data will be stored.
            Defaults to None.
        select (str, optional):
            Selection method for indicating how datasets should be identified
            within the file explorer menu. Defaults to 'directory'.

            Selection options include the following:

            - ``'directory'``, which will locate and copy all of the data files
              in the specified directory for the indicated data type
            - ``'recursive directory'``, which will locate and copy all data
              files within the specified directory and any subdirectories
              contained within the indicated folder path
            - ``'files'`` which copies over files that the user manually
              selects within a directory.

    **Keyword Arguments:**

    :param str file_extension:
        The type of data file to select. Choose from ``'.csv'``, ``'.txt'``,
        ``'.xlsx'``.
    :param str name:
        (``data_type = 'sensor'`` only). The name given to the air sensor. Used
        to locate the air sensor data subdirectory at
        ``[project_data]/data/sensor_data/[sensor_name]``.
    :param str ref_data_source:
        (``data_type = 'reference'`` only). The name of the service or source
        from which reference data were acquired.

        Choose from the following options:

        - ``'local'``: Data files aqcuired locally (e.g., local transfer
          from agency overseeing reference instrumentation at air monitoring
          site).
        - ``'airnowtech'``: User has downloaded files from the AirNowTech
          system and has saved files locally to the user’s system.

    :param str site_name:
        (``data_type = 'reference'`` only). The name of the air monitoring
        site. Used to locate the reference data subdirectory at
        ``[project_data]/data/reference_data/[ref_data_source]/[sitename_siteid]``.
    :param str site_aqs:
        (``data_type = 'reference'`` only). The AQS  ID for the air monitoring
        site. Used to locate the reference data subdirectory at
        ``[project_data]/data/reference_data/[ref_data_source]/[sitename_siteid]``.
    :param bool return_filenames:
        If true, a list of full paths for datasets that have been copied into
        the ``/data`` directory will be returned.

    Returns:
        copy_file_list (list):
            If 'return_filenames' is True, return a list of full paths to data
            files that have been copied into the ``[project_data]/data``
            directory.

    """
    banner_w = 79
    source_file_list = []
    extension = kwargs.get('file_extension', None)

    statement = (f'[File Browser: Select the {select} for recorded'
                 f' {data_type} datasets')
    if extension is not None:
        statement += f' with file type "{extension}"'
    statement += ']'

    print(statement)
    print('')

    if data_type == 'sensor':
        name = kwargs.get('name')
        dest_dir = os.path.join(path, 'data',
                                'sensor_data', name,  'raw_data')
    if data_type == 'reference':
        data_source = kwargs.get('ref_data_source')
        site_name = kwargs.get('site_name')
        site_aqs = kwargs.get('site_aqs')
        site_subfolder = '_'.join([site_name, site_aqs])

        dest_dir = os.path.join(path, 'data',
                                'reference_data', data_source, 'raw',
                                site_subfolder)

    if 'directory' in select:
        src_dir = _prompt_directory()

        print('Source Directory:')
        print('..{0}'.format('\n'.join(wrap(src_dir, width=banner_w))))

        if os.path.normpath(src_dir) == os.path.normpath(dest_dir):
            sys.exit('Source directory for datasets can not be the same as the'
                     ' destination directory')

        if select.startswith('recursive'):

            for path, folders, files in os.walk(src_dir):
                for filename in files:
                    valid_file = _check_extension(filename, extension)
                    if valid_file:
                        source_file_list.append(os.path.join(path, filename))
        else:
            for item in next(os.walk(src_dir))[2]:
                if os.path.isfile(os.path.join(src_dir, item)):
                    valid_file = _check_extension(item, extension)
                    if valid_file:
                        source_file_list.append(os.path.join(src_dir, item))
        print('')
        print('Source Files:')
        print(['\n'.join(wrap(file, width=banner_w))
                         for file in source_file_list])

    if select == 'files':
        files_tup = _prompt_files()

        # Assuming all files in the same directory
        src_dir = os.path.abspath(os.path.join(files_tup[0], '..'))

        print('Source Files:')
        print(['\n'.join(wrap(file, width=banner_w))
                         for file in files_tup])

        for filename in files_tup:
            valid_file = _check_extension(filename, extension)
            if valid_file:
                source_file_list.append(filename)

    print('')
    print('Destination Directory:')
    print('..{0}'.format('\n'.join(wrap(dest_dir, width=banner_w))))

    if source_file_list == []:
        sys.exit('Source directory does not contain any files corresponding to'
                 ' the following file types: {0}'.format(valid_extensions))

    enter_continue()

    os.makedirs(dest_dir, exist_ok=True)
    for filename in source_file_list:
        copy2(filename, dest_dir)

    abbrev_file_list = [file.replace(src_dir, '') for file in source_file_list]

    copy_file_list = [os.path.join(dest_dir,
                      os.path.basename(file)) for file in source_file_list]

    print('Copying the following files:')
    for file in abbrev_file_list:
        print('..' + '\n'.join(wrap(file, width=banner_w)))


    if 'return_filenames' in kwargs:
        val = kwargs.get('return_filenames')
        if val:
            return copy_file_list
