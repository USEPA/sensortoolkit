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
  Wed May 19 16:08:15 2021
Last Updated:
  Wed Jul 14 08:49:37 2021
"""
import os
import sys

def Create_Sensor_Directories(name=None, eval_params=[], work_path=None,
                              lib_path=None):
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
        work_path (str):
            The full path to the work directory where the user intends to store
            datasets, figures, and reports.
        lib_path (str):
            The full path to the library as downloaded from the online
            repository.

    Returns:
        None
    """

    data_fig_path = os.path.join(work_path, 'Data and Figures')
    report_path = os.path.join(work_path, 'Reports')

    # Check if Data and Figures folder in work directory
    if not os.path.exists(data_fig_path):

        if lib_path is not None:
            print('Creating "Data and Figures" subdirectory within', work_path)
            os.makedirs(data_fig_path)

            # create eval_stats, figures, reference_data, sensor_data subdirs
            folders = {'eval_stats': None,
                       'figures': None,
                       'reference_data': {'airnow': ['raw_api_datasets',
                                                     'processed'],
                                          'airnowtech': ['downloaded_datasets',
                                                         'processed'],
                                          'aqs': ['raw_api_datasets',
                                                  'processed'],
                                          'method_codes': None,
                                          'oaqps': ['raw_data',
                                                    'processed_data']},
                       'sensor_data': None}

            for folder in folders:
                folder_path = os.path.join(data_fig_path, folder)
                os.makedirs(folder_path)
                new_dir = folder_path.replace(work_path, '')
                print('..Creating directory:')
                print('....' + new_dir)

                subfolders = folders[folder]
                if subfolders is not None:
                    for subfolder in subfolders:
                        subfolder_path = os.path.join(folder_path, subfolder)
                        os.makedirs(subfolder_path)
                        new_dir = subfolder_path.replace(work_path, '')
                        print('....Creating sub-directory:')
                        print('......' + new_dir)

                        subsubfolders = subfolders[subfolder]
                        if subsubfolders is not None:
                            for subsubfolder in subsubfolders:
                                subsubfolder_path = os.path.join(
                                                            subfolder_path,
                                                            subsubfolder)
                                os.makedirs(subsubfolder_path)
                                new_dir = subsubfolder_path.replace(work_path,
                                                                    '')
                                print('......Creating sub-sub-directory:')
                                print('........' + new_dir)

            #if sensor name is Example_Make_Model, copy over path to deployment figure
            #copy over method codes

        else:
            console = ('No path given to library location, not able '
                       'to copy over required files')
            sys.exit(console)

    # Check if Reports folder in work directory
    if not os.path.exists(report_path):

        if lib_path is not None:
            print('Creating "Reports" subdirectory within', work_path)
            os.makedirs(report_path)

            folders = {'templates': None}

            for folder in folders:
                print(folder)
                folder_path = os.path.join(report_path, folder)
                os.makedirs(folder_path)
                new_dir = folder_path.replace(work_path, '')
                print('..Creating directory:')
                print('....' + new_dir)

            # Copy over the templates

        else:
            console = ('No path given to library location, not able '
                       'to copy over required files')
            sys.exit(console)


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
            new_dir = sensor_subfolder.replace(work_path, '')
            print('..Creating directory:')
            print('....' + new_dir)

        # Create sub-subfolders for figures and sensor data folders
        if subfolder == 'figures':

            figure_params = eval_params + ['Met', 'deployment']
            # Create figure subfolders for specified eval params
            for param in figure_params:
                param_fig_subfolder = os.path.join(sensor_subfolder, param)

                if not os.path.exists(param_fig_subfolder):
                    os.makedirs(param_fig_subfolder)
                    new_dir = param_fig_subfolder.replace(work_path, '')
                    print('....Creating sub-directory:')
                    print('......' + new_dir)

        if subfolder == 'sensor_data':
            dataset_types = ['processed_data', 'raw_data']
            # Create data subfolders for processed, raw data
            for dataset_type in dataset_types:
                data_subfolder = os.path.join(sensor_subfolder, dataset_type)

                if not os.path.exists(data_subfolder):
                    os.makedirs(data_subfolder)
                    new_dir = data_subfolder.replace(work_path, '')
                    print('....Creating sub-directory:')
                    print('......' + new_dir)
