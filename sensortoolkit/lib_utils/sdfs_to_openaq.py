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
  Fri Dec 17 08:50:37 2021
Last Updated:
  Fri Dec 17 08:50:37 2021
"""
import pandas as pd
from sensortoolkit.param import Parameter
from sensortoolkit.datetime_utils import get_timestamp_interval


def sdfs_to_openaq(sensor, averaging_interval='1-hour', **kwargs):
    """Convert datasets formatted with the sensortoolkit Data Formatting
    Scheme (SDFS) to OpenAQ's data format for uploading to the OpenAQ API.

    Args:
        sensor (sensortoolkit.AirSensor):
            AirSensor object containing sensor datasets in SDFS format that
            will be converted to OpenAQ's data format.
        averaging_interval (str, optional):
            DESCRIPTION. Defaults to '1-hour'.
        **kwargs (TYPE):
            DESCRIPTION.

    Returns:
        openaq_data (dict):
            Dictionary containing datasets for each sensor (keys are sensor
            serial IDs, values are Pandas DataFrames) that have been converted
            to OpenAQ's data format.

    """
    #TODO: Openaq uses time ending format, need to convert?

    sdfs_data = sensor.data[averaging_interval]
    openaq_data = dict((serial, None) for serial in
                       sensor.data[averaging_interval].keys())

    param_renaming = {'BC': 'bc',
                      'CO': 'co',
                      'NO': 'no',
                      'NO2': 'no2',
                      'O3': 'o3',
                      'PM1': 'pm1',
                      'PM10': 'pm10',
                      'PM25': 'pm25',
                      'Press': 'pressure',
                      'RH': 'relativehumidity',
                      'SO2': 'so2',
                      'Temp': 'temperature'
                      }

    valid_params = [param for param in sensor.param_headers
                    if param in param_renaming.keys()]
    invalid_params = [param for param in sensor.param_headers
                      if param not in valid_params]
    param_units = {param: Parameter(param).units for param in valid_params}

    print('Converting SDFS dataset to openaq format')
    print(f'..data the following parameters will be converted:\n  {valid_params}')
    print(f'..the following parameters will NOT be converted:\n  {invalid_params}')

    openaq_cols = ['parameter', 'location', 'city', 'country',
                   'value', 'unit', 'date_utc', 'date_local',
                   'sourceType', 'mobile', 'coordinates_latitude',
                   'coordinates_longitude', 'averagingPeriod_unit',
                   'averagingPeriod_value', 'attribution_name',
                   'attribution_url']

    for serial, data in sdfs_data.items():
        openaq_row_list = []
        tzone = data.attrs['local_tzone']
        averaging_value = averaging_interval.split('-')[0]
        averaging_unit = averaging_interval.split('-')[1] + 's'

        for row in data.itertuples():
            idx = row.Index
            for param in valid_params:
                row_data = dict((col, None) for col in openaq_cols)

                openaq_param = param_renaming[param]
                param_value = getattr(row, f'{param}_Value')
                param_unit = param_units[param]

                if param_unit == 'ppbv':
                    param_value = param_value / 1000.0
                    param_unit = 'ppm'

                timestamp_utc = idx
                timestamp_local = timestamp_utc.tz_convert(tzone)

                row_data['parameter'] = openaq_param
                row_data['value'] = param_value
                row_data['unit'] = param_unit
                row_data['date_utc'] = timestamp_utc.isoformat().replace('+00:00', 'Z')
                row_data['date_local'] = timestamp_local.isoformat()
                row_data['averagingPeriod_value'] = averaging_value
                row_data['averagingPeriod_unit'] = averaging_unit

                row_data['sourceType'] = kwargs.get('sourceType', 'research')
                row_data['mobile'] = str(kwargs.get('mobile', False)).lower()
                row_data['location'] = kwargs.get('location', None)
                row_data['city'] = kwargs.get('city', None)
                row_data['country'] = kwargs.get('country', None) # Must be ISO alpha-2 code
                row_data['coordinates_latitude'] = kwargs.get('coordinates_latitude', None)
                row_data['coordinates_longitude'] = kwargs.get('coordinates_longitude', None)
                row_data['attribution_name'] = kwargs.get('attribution_name', None)
                row_data['attribution_url'] = kwargs.get('attribution_url', None)

                openaq_row_list.append(row_data)

        openaq_df = pd.DataFrame(openaq_row_list, columns=openaq_cols)
        openaq_data[serial] = openaq_df

    return openaq_data


def openaq_to_sdfs(openaq_data):
    # Currently works for converting parameter data columns
    # TODO: extend to reference data, include info about site, agency, etc.

    param_renaming = {'bc': 'BC',
                      'co': 'CO',
                      'no': 'NO',
                      'no2': 'NO2',
                      'o3': 'O3',
                      'pm1': 'PM1',
                      'pm10': 'PM10',
                      'pm25': 'PM25',
                      'pressure': 'Press',
                      'relativehumidity': 'RH',
                      'so2': 'SO2',
                      'temperature': 'Temp'}

    sdfs_data = pd.DataFrame()

    for param in openaq_data.parameter.unique():

        param_data = openaq_data[openaq_data.parameter==param]

        param_data = param_data.set_index(
                        pd.to_datetime(param_data.date_local)).tz_convert('UTC')
        param_data.index.name = 'DateTime'

        if (param_data.unit == 'ppm').all():
            param_data.value = param_data.value * 1000.0

        sdfs_param = param_renaming[param]
        sdfs_unit = Parameter(sdfs_param).units_description
        sdfs_data[f'{sdfs_param}_Value'] = param_data.value
        sdfs_data[f'{sdfs_param}_Unit'] = sdfs_unit

    return sdfs_data




if __name__ == '__main__':

    # NOTE: local_tzone dataset attribute is not preserved for loading
    # processed datasets. Would need to save attributes somewhere - sensor setup?
    aqy = aeroqual_aqy.evaluate()

    sensor = aqy.sensor

    openaq_data = sdfs_to_openaq(
                sensor,
                averaging_interval='1-hour',
                location='Ambient Monitoring Innovative Research Station (AIRS)',
                city='Research Triangle Park, NC',
                country='US',
                coordinates_latitude=35.889510,
                coordinates_longitude=-78.874572,
                attribution_name='U.S. EPA Office of Research and Development',
                attribution_url='https://www.epa.gov/air-sensor-toolbox')

    openaq_df = openaq_data['AQY_01']
    openaq_df.to_csv('openaq_test.csv', index=False)


    sdfs_data = openaq_to_sdfs(openaq_df)


