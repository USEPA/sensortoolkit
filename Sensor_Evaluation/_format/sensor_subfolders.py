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
  Thu May 20 08:23:00 2021
"""
import os


def Create_Sensor_Directories(name=None, eval_params=[]):

    library_path = os.path.abspath(__file__ + '../../../..')
    data_fig_path = os.path.join(library_path, 'Data and Figures')

    subfolders = ['eval_stats', 'figures', 'sensor_data']

    print('Creating directories for ' + name + ' and evaluation parameters: '
          + ', '.join(eval_params))

    for subfolder in subfolders:
        subfolder_path = os.path.join(data_fig_path, subfolder)
        sensor_subfolder = os.path.join(subfolder_path, name)

        # Create sensor subfolder
        if not os.path.exists(sensor_subfolder):
            os.makedirs(sensor_subfolder)
            new_dir = sensor_subfolder.replace(library_path, '')
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
                    new_dir = param_fig_subfolder.replace(library_path, '')
                    print('....Creating sub-directory:')
                    print('......' + new_dir)

        if subfolder == 'sensor_data':
            dataset_types = ['processed_data', 'raw_data']
            # Create data subfolders for processed, raw data
            for dataset_type in dataset_types:
                data_subfolder = os.path.join(sensor_subfolder, dataset_type)

                if not os.path.exists(data_subfolder):
                    os.makedirs(data_subfolder)
                    new_dir = data_subfolder.replace(library_path, '')
                    print('....Creating sub-directory:')
                    print('......' + new_dir)
