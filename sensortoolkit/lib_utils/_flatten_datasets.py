# -*- coding: utf-8 -*-
"""
This module contains a method for converting datasets for AirSensor and
ReferenceMonitor objects corresponding to instruments that have been collocated
at an ambient monitoring site into a single pandas DataFrame object and
(optionally) saved as comma-separated value files for each sampling or
averaging interval present in sensor and reference datasets.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB


Created:
  Mon Jan 31 11:06:57 2022
Last Updated:
  Mon Jan 31 11:06:57 2022
"""
import os
import pandas as pd
import numpy as np
from sensortoolkit.datetime_utils import get_todays_date
from sensortoolkit.lib_utils import flatten_list

def flatten_datasets(AirSensor, ReferenceMonitor, verbose=True, include_units=True,
                     write_to_file=False):
    """


    Args:
        AirSensor (sensortoolkit.AirSensor): DESCRIPTION.
        ReferenceMonitor (sensortoolkit.ReferenceMonitor): DESCRIPTION.
        write_to_file (bool, optional): DESCRIPTION. Defaults to False.

    Returns:
        flat_dict (dict): DESCRIPTION.

    """
    state_fips_codes = pd.read_csv(os.path.join(__file__, '..', 'us_fips_codes.csv'))

    site_info_cols = ['Agency', 'Site_Name', 'Site_AQS','Site_Lat', 'Site_Lon',
                      'Data_Source', 'Data_Acquisition_Date_Time']


    ref_intervals = list(set(flatten_list([list(ReferenceMonitor.data[key].keys())
                                           for key in ReferenceMonitor.data])))

    flat_dict = {}
    meta_dfs = {}
    min_ref_df = pd.DataFrame()

    intervals = list(set().union(list(AirSensor.data.keys()), ref_intervals))

    for interval in intervals:
        flat_df = pd.DataFrame()
        print(f'Flattening {interval} datasets')
        if interval in AirSensor.data:
            for sensor_key in AirSensor.data[interval]:
                sensor_df = AirSensor.data[interval][sensor_key]
                suffix = f'_{sensor_key}'
                sensor_df = sensor_df.add_suffix(suffix)
                flat_df = flat_df.join(sensor_df, how='outer')
        else:
            flat_df = pd.DataFrame()

        for classifier in ReferenceMonitor.data.keys():
            for ref_interval in ReferenceMonitor.data[classifier]:

                if ref_interval == interval:
                    ref_df = ReferenceMonitor.data[classifier][interval]
                    site_info = ref_df[site_info_cols]

                    ref_df = ref_df.drop(columns=site_info_cols)
                    suffix = f'_Ref'
                    ref_df = ref_df.add_suffix(suffix)

                    param_ref_cols = [param.replace('_Value', '') for param
                                      in ref_df.columns if '_Value' in param]

                    source = site_info.Data_Source.dropna().unique()[0]
                    for param in param_ref_cols:
                        ref_df[f'{param}_Data_Source'] = source


                    if (interval != '1-minute'):
                        if not flat_df.empty:
                            flat_df = flat_df.join(ref_df, how='outer')
                    else:
                        min_ref_df = min_ref_df.join(ref_df, how='outer')

        verbose_cols = []
        ref_verbose_cols = []

        if not min_ref_df.empty:
            ref_verbose_cols, min_ref_df = verbose_columns(min_ref_df, ref_verbose_cols,
                                               include_units, verbose, interval)

        if not flat_df.empty:
            if (interval in ref_intervals) and interval != '1-minute':
                flat_df = flat_df.join(site_info)
                #ref_sources = list(set(ref_sources))
                #flat_df.Data_Source = ', '.join(ref_sources)
                verbose_cols.extend(site_info)

            verbose_cols, flat_df = verbose_columns(flat_df, verbose_cols,
                                               include_units, verbose, interval)
        if (not verbose) and (not flat_df.empty):
            #print(flat_df.columns, verbose_cols)
            flat_df, meta_df = remove_verbose(flat_df, verbose_cols, include_units)
        if not min_ref_df.empty:
            min_ref_df, _ = remove_verbose(min_ref_df, ref_verbose_cols, include_units)

        if write_to_file:


            print('..writing flattened dataset to .csv')
            today = get_todays_date()
            interv = interval.replace('-', '_')
            #interv_str = interval.replace('hour', 'hr')

            bdate = AirSensor.bdate.strftime('%y%m%d')
            edate = AirSensor.edate.strftime('%y%m%d')

            state_abbrev = ''
            if ReferenceMonitor.site_id != 'Unspecified Site ID':
                state_fips = int(ReferenceMonitor.site_id[0:2])
                state_abbrev = state_fips_codes[state_fips_codes.FIPS_Code==state_fips]['Abbreviation'].unique()[0]
                #site_address = test_loc['site_address'].split(', ')
                state_abbrev = f'_{state_abbrev}_'

            if (not verbose) and (not flat_df.empty):
                meta_dfs[interval] = meta_df

            if not min_ref_df.empty:
                file_name=  f'Ref{state_abbrev}{interv}_bdate{bdate}_edate{edate}_{today}.csv'
                file_path = os.path.join(AirSensor.project_path, 'data',
                                         'eval_stats', AirSensor.name, file_name)

                drop_cols = [col for col in verbose_cols if col in min_ref_df]
                min_ref_df = min_ref_df.drop(columns=drop_cols)

                min_ref_df.to_csv(file_path, float_format='%.2f')
                min_ref_df = pd.DataFrame()

            if pd.to_timedelta(interv.replace('_', ' ')) < pd.to_timedelta('1 h'):
                interv = 'RecRes'

            sensor_name = f'{AirSensor.make.replace(" ", "-")}_{AirSensor.model.replace(" ", "-")}'
            file_name=  f'{sensor_name}{state_abbrev}{interv}_bdate{bdate}_edate{edate}_{today}.csv'
            file_path = os.path.join(AirSensor.project_path, 'data',
                                     'eval_stats', AirSensor.name, file_name)

            if not flat_df.empty:
                for sensor_key in AirSensor.data[interval]:
                    for param in ['PM25', 'O3']:
                        if ((f'{param}_Value_{sensor_key}' in flat_df.columns)
                        and (f'{param}_Value_Ref' in flat_df.columns)):
                            flat_df[f'{param}_Ratio_{sensor_key}'] = flat_df[f'{param}_Value_{sensor_key}'] / flat_df[f'{param}_Value_Ref']
                            flat_df[f'{param}_Diff_{sensor_key}'] = flat_df[f'{param}_Value_{sensor_key}'] - flat_df[f'{param}_Value_Ref']
                            flat_df[f'{param}_AbsDiff_{sensor_key}'] = abs(flat_df[f'{param}_Diff_{sensor_key}'])

                flat_df.to_csv(file_path, float_format='%.2f')


        flat_dict[interval] = flat_df

        if (not verbose) and (interval == '1-hour'):
            meta_df = pd.DataFrame()
            for meta_data in meta_dfs.values():
                meta_df = meta_df.combine_first(meta_data)
            meta_file_name =  f'{AirSensor.name}{state_abbrev}metadata_{today}.csv'
            file_path = os.path.join(AirSensor.project_path, 'data',
                                     'eval_stats', AirSensor.name, meta_file_name)
            meta_df.to_csv(file_path)

    return flat_dict


def verbose_columns(df, verbose_cols, include_units, verbose, interval):
    ref_info_cols = ['Param_Code_Ref', 'Method_Ref', 'Method_Code_Ref',
                     'Method_POC_Ref']

    for col in df.columns:
        if '_Unit_' in col:
            if (include_units) and (not verbose):
                verbose_cols.append(col)
            elif (include_units) and (verbose):
                pass
            else:
                df = df.drop(columns=[col])
        if '_Data_Source' in col:
            verbose_cols.append(col)

        for ref_col_fragment in ref_info_cols:
            if ref_col_fragment in col:
                verbose_cols.append(col)

    return verbose_cols, df

def remove_verbose(df, verbose_cols, include_units):


    meta_dict = {col: df[col].dropna().unique()[0] for col in
                 verbose_cols if not df[col].isna().all()}
    #print(meta_dict)
    meta_df = pd.DataFrame(meta_dict, index=[0])

    df = df.drop(columns=verbose_cols)

    return df, meta_df
