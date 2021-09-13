# -*- coding: utf-8 -*-
"""
@Author:
    | Samuel Frederick, NSSC Contractor (ORAU)
    | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed May 19 16:08:15 2021
Last Updated:
  Wed Jul 14 08:49:37 2021
"""
import os
import sys


def create_sensor_directories(name=None, eval_params=[], path=None):
    """Construct the sensor directory file structure required for conducting
    analysis with the SensorEvaluation library.

    Args:
        name (str):
            The name assigned to the sensor. Recommend using the sensor's make
            and model, separated by underscores ('_').
        eval_params (list of strings):
            The  parameters measured by the sensor that the user
            wishes to evaluate. For instance, if a sensor measures both fine
            particulate matter (PM25) and ozone (O3) and the user intends to
            evalute the performance device with respecet to both of these
            pollutants, the user may specify 'eval_params=['PM25', 'O3']' to
            create necessary subfolders for figures and data structures created
            by the SensorEvaluation library for each of these evaluation
            parameters.
        path (str):
            The full path to the work directory where the user intends to store
            datasets, figures, and reports.

    Returns:
        None
    """

    data_fig_path = os.path.join(path, 'Data and Figures')
    report_path = os.path.join(path, 'Reports')

    new_folders = []
    # Check if Data and Figures folder in work directory
    if not os.path.exists(data_fig_path):

        print('Creating "Data and Figures" subdirectory within', path)
        os.makedirs(data_fig_path)

        # create eval_stats, figures, reference_data, sensor_data subdirs
        folders = {'eval_stats': None,
                   'figures': None,
                   'reference_data': {'airnow': ['raw',
                                                 'processed'],
                                      'airnowtech': ['raw',
                                                     'processed'],
                                      'aqs': ['raw',
                                              'processed'],
                                      #'method_codes': None,
                                      'oaqps': ['raw_data',
                                                'processed_data']},
                   'sensor_data': None}

        for folder in folders:
            folder_path = os.path.join(data_fig_path, folder)
            os.makedirs(folder_path)
            new_dir = folder_path.replace(path, '')
            print('....' + new_dir)
            new_folders.append(new_dir)

            subfolders = folders[folder]
            if subfolders is not None:
                for subfolder in subfolders:
                    subfolder_path = os.path.join(folder_path, subfolder)
                    os.makedirs(subfolder_path)
                    new_dir = subfolder_path.replace(path, '')
                    print('......' + new_dir)
                    new_folders.append(new_dir)

                    subsubfolders = subfolders[subfolder]
                    if subsubfolders is not None:
                        for subsubfolder in subsubfolders:
                            subsubfolder_path = os.path.join(
                                                        subfolder_path,
                                                        subsubfolder)
                            os.makedirs(subsubfolder_path)
                            new_dir = subsubfolder_path.replace(path,
                                                                '')
                            print('........' + new_dir)
                            new_folders.append(new_dir)

    # Check if Reports folder in work directory
    if not os.path.exists(report_path):
        print('/nCreating "Reports" subdirectory within', path)
        os.makedirs(report_path)
        print('/n')


    # Create Subfolders for Sensor Data and Figures
    subfolders = ['eval_stats', 'figures', 'sensor_data']

    print('Creating directories for ' + name + ' and evaluation parameters: '
          + ', '.join(eval_params))

    for subfolder in subfolders:
        subfolder_path = os.path.join(data_fig_path, subfolder)
        sensor_subfolder = os.path.join(subfolder_path, name)

        # Create sensor subfolder
        if not os.path.exists(sensor_subfolder):
            os.makedirs(sensor_subfolder)
            new_dir = sensor_subfolder.replace(path, '')
            print('....' + new_dir)
            new_folders.append(new_dir)

        # Create sub-subfolders for figures and sensor data folders
        if subfolder == 'figures':

            figure_params = eval_params + ['Met', 'deployment']
            # Create figure subfolders for specified eval params
            for param in figure_params:
                param_fig_subfolder = os.path.join(sensor_subfolder, param)

                if not os.path.exists(param_fig_subfolder):
                    os.makedirs(param_fig_subfolder)
                    new_dir = param_fig_subfolder.replace(path, '')
                    print('....Creating sub-directory:')
                    print('......' + new_dir)
                    new_folders.append(new_dir)

        if subfolder == 'sensor_data':
            dataset_types = ['processed_data', 'raw_data']
            # Create data subfolders for processed, raw data
            for dataset_type in dataset_types:
                data_subfolder = os.path.join(sensor_subfolder, dataset_type)

                if not os.path.exists(data_subfolder):
                    os.makedirs(data_subfolder)
                    new_dir = data_subfolder.replace(path, '')
                    print('....Creating sub-directory:')
                    print('......' + new_dir)
                    new_folders.append(new_dir)
