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
  Mon Jul 19 14:03:36 2021
Last Updated:
  Mon Jul 19 14:03:36 2021
"""
import json
import pandas as pd
import sys


def Ingest(path, name=None, setup_file_path=None):
    """Ingestion module for sensor data using setup.json configuration file
    via the Setup class.

    Sensor data file data type must be .csv, .txt, or .xlsx.

    Args:
        path (str):
            The full path to the recorded sensor data file
        name (str):
            The make and model of the sensor
        setup_file_path (str):
            The full path to the setup.json file

    Returns:
        df (pandas dataframe):
            Dataframe containing sensor data in standardized formatting for
            datetime index and header naming scheme.
    """
    # Will need to decide on where the json should go, modify path accordingly
    with open(setup_file_path) as file:
        setup = json.load(file)
        file.close()

    idx_list = setup['timestamp_col_headers']
    idx_format_dict = setup['time_format_dict']

    if setup['dtype'] in ('.csv', '.txt'):
        try:
            names = None
            if setup['header_iloc'] is None:
                names = setup['all_col_headers']
            df = pd.read_csv(path, header=setup['header_iloc'], names=names)
        except FileNotFoundError as e:
            sys.exit(e)
    else:
        # Put other pandas read functions here
        sys.exit()

    # If the header row loads on a row of data (may be intentional if
    # formatting for first row is unusual and doesnt follow delimited format).
    if df.columns.all() != setup['all_col_headers']:
        df.columns = setup['all_col_headers']

        # Set Datetime Index
    df['DateTime_UTC'] = df[idx_list].astype(str).apply(''.join, axis=1)
    time_format = ''.join(idx_format_dict.values())

    # Check whether the timestamp data are in Unix epoch
    if time_format == 'epoch':
        unit = 's'
        time_format = None
    else:
        unit = None

    # Convert the DateTime_UTC column to time-like data format and set as index
    df['DateTime_UTC'] = pd.to_datetime(df['DateTime_UTC'],
                                        format=time_format,
                                        unit=unit,
                                        # sets NaT if timestamps cant be parsed
                                        errors='coerce')
    df = df.set_index(df['DateTime_UTC'])
    df = df.sort_index(ascending=True)
    df = df.drop(columns='DateTime_UTC')

    # Rename parameter header columns
    df = df.rename(columns=setup['col_rename_dict'])

    # Drop unused columns
    if len(setup['drop_cols']) > 0:
        # ignore errors if column not in df (may happen if DateTime_UTC in list
        # of all header columns, already dropped)
        df = df.drop(columns=setup['drop_cols'],
                     errors='ignore')

        # Force non numeric values to Nans
        #df = df.apply(lambda x: pd.to_numeric(x, errors='coerce'))

    return df

"""
data_path = ('C:/Users/SFREDE01/OneDrive - Environmental Protection Agency'
             ' (EPA)/Profile/Documents/Public_Sensor_Evaluation/'
             'Data and Figures/sensor_data/Example_Make_Model/raw_data/'
             'Example_Make_Model_SN01_raw.csv')

df = Ingest(path=data_path, name='Example_Make_Model')


from setup import Setup
ramp_setup = Setup()

data_path = "C:/Users/SFREDE01/OneDrive - Environmental Protection Agency (EPA)\Profile/Documents/Public_Sensor_Evaluation/Data and Figures/sensor_data/Sensit_RAMP/raw_data/20190610_Data Collection/SN0182/NC_RAM_08_190530.TXT"
df = Ingest(path=data_path, name='Sensit_RAMP')


path = ("C:/Users/SFREDE01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/AIRS Project/AIRS Evaluation/Sensor_Raw_Data/APT_Maxima/20190322_Data Collection/SN03/NC_MAX_02_190322_raw.CSV")
df = pd.read_csv(path, header=1)

df = Ingest(path=path, name='APT_Maxima')
maxima_setup = Setup()

path = "C:/Users/SFREDE01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/AIRS Project/AIRS Evaluation/Sensor_Raw_Data/IQAir_AirVisual_Pro/20200108 Data Collection/AirVis_99x_01082020_AIRS_raw.csv"
df = pd.read_csv(path, header=0)
avp_setup = Setup()
df = Ingest(path=path, name='IQAir_AirVisual_Pro')
"""

data_path = 'C:/Users/SFREDE01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/AIRS Project/AIRS Evaluation/Sensor_Raw_Data/Vaisala_AQT420/'
setup_path = "C:/Users/SFREDE01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Public_Sensor_Evaluation/User_Scripts/sensor setup files/Vaisala_AQT420_setup.json"
df_list = []
for filename in os.listdir(data_path):
    print(filename)
    df = Ingest(path=data_path + '/' + filename,
                name='Vaisala_AQT420', setup_file_path=setup_path)
    df_list.append(df)

