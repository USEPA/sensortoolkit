# -*- coding: utf-8 -*-
"""
@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Tue Jan 11 14:55:45 2022
Last Updated:
  Tue Jan 11 14:55:45 2022
"""
import os
import json
import pandas as pd
from sensortoolkit.param import Parameter
from sensortoolkit.datetime_utils import get_todays_date

def reference_flags(sensor, reference, return_type='JSON', write_to_file=False):
    """


    Args:
        sensor (TYPE): DESCRIPTION.
        reference (TYPE): DESCRIPTION.
        return_type (TYPE, optional): DESCRIPTION. Defaults to 'JSON'.
        write_to_file (TYPE, optional): DESCRIPTION. Defaults to False.

    Raises:
        ValueError: DESCRIPTION.
        AttributeError: DESCRIPTION.

    Returns:
        TYPE: DESCRIPTION.

    """

    if return_type not in ['JSON', 'dict', 'dataframe', None]:
        raise ValueError(f'Invalid return type "{return_type}"')

    monthly_labels = pd.date_range(sensor.bdate.strftime('%Y-%m'),
                                   sensor.edate.strftime('%Y-%m'),
                                   freq='MS').strftime('%Y%m')

    data_subfolder = f'{reference.site_name.replace(" ", "_")}_{reference.site_id}'
    ref_path = (f'{sensor.project_path}//data//reference_data//{reference.data_source}//'
                f'processed//{data_subfolder}')

    file_list = [obj for obj in os.listdir(ref_path) if obj.lower().endswith('.csv')]
    # limit to monthly datasets corresponding to sensor data sampling period
    file_list = [obj for obj in file_list if obj.split('_')[1] in monthly_labels]

    incidents = {}
    for classifier in reference.data.keys():
        print(classifier)
        incidents[classifier] = {}

        if all(df.empty for df in reference.data[classifier].values()):
            print('..No datasets found')
            continue

        classifier_file_list = [obj for obj in file_list if
                                obj.endswith(f'{classifier}.csv')]

        intervals = set([obj.split('_')[0] for obj in classifier_file_list])

        if 'min' in intervals:
            interval = 'min'
            tdelta = '1 minute'
        elif 'H' in intervals:
            interval = 'H'
            tdelta = '1 hour'
        elif 'D' in intervals:
            interval = 'D'
            tdelta = '1 day'
        else:
            raise AttributeError('Sampling/averaging interval not found in file names')

        # Limit list of files to datasets with right classifier and sampling interval
        classifier_file_list = [obj for obj in classifier_file_list if
                                obj.split('_')[0] == interval]

        for file in classifier_file_list:
            print(f'..{file}')
            file_path = f'{ref_path}//{file}'
            df = pd.read_csv(file_path, index_col='DateTime', parse_dates=['DateTime'])
            # Concatenate to evaluation timeframe
            df = df[sensor.bdate:sensor.edate]
            df_params = [col.replace('_Value', '') for col in df.columns
                          if col.endswith('_Value')]

            for param in df_params:
                #param_obj = Parameter(param)
                if param not in incidents[classifier]:
                    incidents[classifier][param] = {}

                flag_data = df[f'{param}_QAQC_Code']
                month_incidents = flag_incidents(flag_data, param,
                                                  interval=tdelta)
                incidents[classifier][param].update(month_incidents)



    # Return either JSON, dictionary, or Nonetype
    if return_type == 'JSON':
        if write_to_file:
            today = get_todays_date()
            file_path = (f'{sensor.project_path}\\data\\eval_stats\\{sensor.name}\\'
                         f'{sensor.name}_reference_flags_{today}.json')
            with open(file_path, 'w') as file:
                json.dump(incidents, file, indent=4)

        return json.dumps(incidents)
    if return_type == 'dict':
        if write_to_file:
            today = get_todays_date()
            file_path = (f'{sensor.project_path}\\data\\eval_stats\\{sensor.name}\\'
                         f'{sensor.name}_reference_flags_{today}.json')
            with open(file_path, 'w') as file:
                json.dump(incidents, file, indent=4)

        return incidents
    if return_type == 'dataframe':
        flag_df = pd.DataFrame(columns=['Classifier', 'Parameter',
                                        'Flag_Timestamp', 'Description'])
        i = 0
        for classifier in incidents:
            for param in incidents[classifier]:
                for date in incidents[classifier][param]:
                    descrip = incidents[classifier][param][date]
                    flag_df.loc[i, :] = classifier, param, date, descrip
                    i+=1
        if write_to_file:
            flag_df.to_csv(f'{sensor.project_path}/data/eval_stats/'
                           f'{sensor.name}/{sensor.name}_ref_flags_'
                           f'{sensor.bdate.strftime("%Y-%m-%d")}-'
                           f'{sensor.edate.strftime("%Y-%m-%d")}.csv')
        return flag_df
    else:
        return


def flag_incidents(flag_data, param, interval=None):
    """


    Args:
        flag_data (TYPE): DESCRIPTION.
        param (TYPE): DESCRIPTION.
        interval (TYPE, optional): DESCRIPTION. Defaults to None.

    Raises:
        KeyError: DESCRIPTION.

    Returns:
        incidents (TYPE): DESCRIPTION.

    Example:

        flag_data:

        | DateTime            | PM25_QAQC_Code   |
        |:--------------------|:-----------------|
        | 2019-08-08 09:02:00 | <Samp            |
        | 2019-08-13 09:58:00 | <Samp            |
        | 2019-08-21 07:56:00 | Down             |
        | 2019-08-21 07:57:00 | Down             |
        | 2019-08-21 07:58:00 | Down             |

        incidents:

        {'2019-08-08 09:02:00': '<Samp',
         '2019-08-13 09:58:00': '<Samp',
         '2019-08-21 07:56:00 to 2019-08-21 07:58:00': 'Down'}

    """
    flag_data = flag_data.dropna()
    if flag_data.empty:
        return {}

    if isinstance(flag_data.index, pd.core.indexes.datetimes.DatetimeIndex):
        idx_name = flag_data.index.name
        flag_data = flag_data.reset_index()
        if idx_name != 'DateTime':
            flag_data = flag_data.rename(columns={idx_name: 'DateTime'})

    if 'DateTime' not in flag_data:
        raise KeyError('"DateTime" timestamp column not found in index')
    if param + '_QAQC_Code' not in flag_data:
        raise KeyError(f'"{param}_QAQC_Code" not in passed dataset')

    # Hyphens (like the hyphen in "1-minute") can cause pandas' to_timedelta()
    # function to interpret input as negative timedelta value. Remove hyphens
    # before passing to method.
    interval = interval.replace('-', ' ')
    interval = pd.to_timedelta(interval)

    flag_data['value_grp'] = (flag_data.DateTime.diff(1)!= interval
                              ).astype('int').cumsum()
    incidents = {}
    tstamp_fmt = '%Y-%m-%d %H:%M:%S%z'
    for value in flag_data.value_grp.unique():
        consec_flags = flag_data[flag_data.value_grp==value]
        for flag in consec_flags[f'{param}_QAQC_Code'].unique():
            consec_flag_data = consec_flags[consec_flags[f'{param}_QAQC_Code']==flag]

            # Flag occurs for single timestamp
            if consec_flag_data.shape[0] == 1:
                time = consec_flag_data.DateTime.dt.strftime(tstamp_fmt).values[0]
                incidents[time] = consec_flag_data[f'{param}_QAQC_Code'].unique()[0]
            # Flag occurs for consecutive timestamp interval
            else:
                btime = consec_flag_data.DateTime.dt.strftime(tstamp_fmt).values[0]
                etime = consec_flag_data.DateTime.dt.strftime(tstamp_fmt).values[-1]
                time = f'{btime} to {etime}'
                incidents[time] = consec_flag_data[f'{param}_QAQC_Code'].unique()[0]

    return incidents


if __name__ == '__main__':

    # Generate a dictionary of flags for PM, Gases, and Met reference
    # instruments during the evaluation timeframe. Save the log to a JSON file.
    flag_dict= reference_flags(sensor=sensor,
                               reference=ref,
                               return_type='dict',
                               write_to_file=True)


    # Code for generating logs spanning the entire duration of EPA sensor evals
    path = r'C:\Users\SFREDE01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\sensortoolkit_testing\data\reference_data\local\processed\Burdens_Creek_370630099'
    """
    # Flags for PM25 (May 2018 to July 2021, T640x)
    pm25_incidents = {}
    for file in os.listdir(path):
        if file.startswith('min') and file.endswith('PM.csv'):
            print(file)
            file_path = f'{path}//{file}'
            df = pd.read_csv(file_path, index_col='DateTime', parse_dates=['DateTime'])
            flag_data = df['PM25_QAQC_Code']
            month_incidents = flag_incidents(flag_data,
                                             param='PM25',
                                             interval='1-minute')
            pm25_incidents.update(month_incidents)

    # Flags for O3 (June 2018 to July 2021, T265)
    O3_incidents = {}
    for file in os.listdir(path):
        if file.startswith('min') and file.endswith('Gases.csv'):
            print(file)
            file_path = f'{path}//{file}'
            df = pd.read_csv(file_path, index_col='DateTime', parse_dates=['DateTime'])
            flag_data = df['O3_QAQC_Code']
            month_incidents = flag_incidents(flag_data,
                                             param='O3',
                                             interval='1-minute')
            O3_incidents.update(month_incidents)
   """