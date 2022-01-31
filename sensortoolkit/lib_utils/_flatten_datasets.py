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
  Mon Jan 31 11:06:57 2022
Last Updated:
  Mon Jan 31 11:06:57 2022
"""
import pandas as pd
from sensortoolkit.datetime_utils import get_todays_date
from sensortoolkit.lib_utils import flatten_list

def flatten_datasets(AirSensor, ReferenceMonitor, write_to_file=False):
    """


    Args:
        AirSensor (TYPE): DESCRIPTION.
        ReferenceMonitor (TYPE): DESCRIPTION.
        write_to_file (TYPE, optional): DESCRIPTION. Defaults to False.

    Returns:
        flat_dict (TYPE): DESCRIPTION.

    """
    site_info_cols = ['Agency', 'Site_Name', 'Site_AQS','Site_Lat', 'Site_Lon',
                      'Data_Source', 'Data_Acquisition_Date_Time']

    ref_intervals = list(set(flatten_list([list(ReferenceMonitor.data[key].keys())
                                           for key in ReferenceMonitor.data])))

    flat_dict = {}
    for interval in AirSensor.data.keys():
        flat_df = pd.DataFrame()
        print(f'Flattening {interval} datasets')
        for sensor_key in AirSensor.data[interval]:
            sensor_df = AirSensor.data[interval][sensor_key]
            suffix = f'_{sensor_key}'
            sensor_df = sensor_df.add_suffix(suffix)
            flat_df = flat_df.join(sensor_df, how='outer')

        for classifier in ReferenceMonitor.data.keys():
            for ref_interval in ReferenceMonitor.data[classifier]:
                if ref_interval == interval:
                    ref_df = ReferenceMonitor.data[classifier][interval]
                    site_info = ref_df[site_info_cols]
                    ref_df = ref_df.drop(columns=site_info_cols)
                    suffix = f'_Ref'
                    ref_df = ref_df.add_suffix(suffix)
                    flat_df = flat_df.join(ref_df, how='outer')

        if interval in ref_intervals:
            flat_df = flat_df.join(site_info)

        if write_to_file:
            print('..writing flattened dataset to .csv')
            today = get_todays_date()
            interv = interval.replace('-', '_')
            flat_df.to_csv(f'flatten_data_export_{interv}_{today}.csv')

        flat_dict[interval] = flat_df

    return flat_dict


if __name__ == '__main__':
    data_dict = flatten_datasets(sensor, ref, write_to_file=True)
    df = data_dict['24-hour']
