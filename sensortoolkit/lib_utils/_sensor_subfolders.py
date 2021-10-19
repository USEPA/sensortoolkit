# -*- coding: utf-8 -*-
"""
Description.

================================================================================

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
from sensortoolkit.param import Parameter

def create_sensor_directories(name=None, param=None, path=None):
    """Construct the sensor directory file structure required for conducting
    analysis with the SensorEvaluation library.

    Args:
        name (str, optional): The name assigned to the sensor. Recommend using
            the sensor's make and model, separated by underscores ('_').
            Defaults to None.
        param (str or list of strings, optional): The parameter(s) measured by
            the sensor that the user wishes to evaluate. Defaults to None.
        path (str, optional): The full path to the work directory where the
            user intends to store datasets, figures, and reports. Defaults to
            None.

    Raises:
        TypeError: Raise if type for param is neither list or string.

    Returns:
        None.

    """
    if isinstance(param, str):
        param = [param]

    data_path = os.path.join(path, 'data')
    figure_path = os.path.join(path, 'figures')
    report_path = os.path.join(path, 'reports')

    new_folders = []

    # Check if 'data' folder in work directory
    if not os.path.exists(data_path):

        print('Creating "data" subdirectory within', path)
        os.makedirs(data_path)

        # create eval_stats, figures, reference_data, sensor_data subdirs
        folders = {'eval_stats': None,
                   'reference_data': {'airnow': ['raw',
                                                 'processed'],
                                      'airnowtech': ['raw',
                                                     'processed'],
                                      'aqs': ['raw',
                                              'processed']},
                   'sensor_data': None}

        for folder in folders:
            folder_path = os.path.join(data_path, folder)
            os.makedirs(folder_path)
            new_dir = folder_path.replace(path, '')
            print('..' + new_dir)
            new_folders.append(new_dir)

            subfolders = folders[folder]
            if subfolders is not None:
                for subfolder in subfolders:
                    subfolder_path = os.path.join(folder_path, subfolder)
                    os.makedirs(subfolder_path)
                    new_dir = subfolder_path.replace(path, '')
                    print('....' + new_dir)
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
                            print('......' + new_dir)
                            new_folders.append(new_dir)

    # Create subfolders for sensor data, figures
    subfolders = {'eval_stats': data_path,
                  'sensor_data': data_path,
                  '': figure_path}
    for subfolder, folder_path in subfolders.items():
        subfolder_path = os.path.join(folder_path, subfolder)
        sensor_subfolder = os.path.join(subfolder_path, name)

        # Check if 'figures' folder in work directory
        if subfolder == '' and not os.path.exists(figure_path):
            print('\nCreating "figures" subdirectory within', path)
            os.makedirs(figure_path)

        # Create sensor subfolder
        if not os.path.exists(sensor_subfolder):
            os.makedirs(sensor_subfolder)
            new_dir = sensor_subfolder.replace(path, '')
            print('..' + new_dir)
            new_folders.append(new_dir)

        # Create sub-subfolders for figures
        if subfolder == '' and param is not None:
                # Only create separate folders for pollutants. Met params
                # grouped into single folder.
                param = [name for name in param if
                         Parameter(name).classifier != 'Met']

                figure_params = param + ['Met', 'deployment']
                # Create figure subfolders for specified eval params
                for fig_folder in figure_params:
                    param_fig_subfolder = os.path.join(sensor_subfolder,
                                                       fig_folder)

                    if not os.path.exists(param_fig_subfolder):
                        os.makedirs(param_fig_subfolder)
                        new_dir = param_fig_subfolder.replace(path, '')
                        print('....' + new_dir)
                        new_folders.append(new_dir)

        # Create sub-subfolders for sensor data folders
        if subfolder == 'sensor_data':
            dataset_types = ['processed_data', 'raw_data']
            # Create data subfolders for processed, raw data
            for dataset_type in dataset_types:
                data_subfolder = os.path.join(sensor_subfolder, dataset_type)
                if not os.path.exists(data_subfolder):
                    os.makedirs(data_subfolder)
                    new_dir = data_subfolder.replace(path, '')
                    print('....' + new_dir)
                    new_folders.append(new_dir)

    # Check if 'reports' folder in work directory
    if not os.path.exists(report_path):
        print('\nCreating "reports" subdirectory within', path)
        os.makedirs(report_path)


if __name__ == '__main__':
    create_sensor_directories(name='Example_Make_Model',
                              param=['PM25', 'O3'],
                              path=r'C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\sensortoolkit_testing')
