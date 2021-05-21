# Air Sensor Evaluation Library - Testing reports

*Samuel Frederick, NSSC Contractor (ORAU)*\
*Office: 919-541-4086 | Email: frederick.samuel@epa.gov*

**Warning: This code is currently under development and is intended for internal EPA use only. Please do not distribute or share components of this repository with individuals external to EPA.**
****

Creating testing reports is very similar to using the `SensorEvaluation` class,
as the `PerformanceReport` class that generates reports is an inherited class of
`SensorEvaluation`. This means that users pass the same attributes to the `PerformanceReport` class as they do to conduct analysis with `SensorEvaluation`. There are a few additional attributes users can pass to the `PerformanceReport` class, including the dictionaries `testing_org` and `testing_loc`. These dictionaries house information about the testing organization, contact information, and site details including the address, coordinates, and site AQS ID if applicable. Below is an example of running the `PerformanceReport` class to create a testing report for the `Example_Make_Model` sensor evaluating its PM<sub>2.5</sub> performance.   
```python
# Testing organization information
testing_org = {'Deployment number': 'Deployment #1',
               'Org name': ['U.S. Environmental Protection Agency',
                            'Office of Research and Development'],
               'Link': 'https://www.epa.gov/air-sensor-toolbox/'
                       'evaluation-emerging-air-sensor-performance',
               'Contact email': 'PI: Clements.Andrea@epa.gov',
               'Contact phone': '919-541-1364'}

# Testing location information
testing_loc = {'Site name': '(AIRS) Ambient Monitoring Innovative '
                            'Research Station ',
               'Site address': '111 TW Alexander Dr. RTP, NC 27713',
               'Site lat': '35.889510N',
               'Site long': '-78.874572W',
               'Site AQS ID': '37 – 063 – 0099'}

# Instantiate the PerformanceReport class for the example sensor dataset
test_report = PerformanceReport(
                sensor_name='Example_Make_Model',
                eval_param='O3',
                reference_data=ref_path.as_posix() + '/airnowtech/processed',
                serials={'1': 'SN01',
                         '2': 'SN02',
                         '3': 'SN03'},
                tzone_shift=5,
                load_raw_data=False,
                write_to_file=True,
                testing_org=testing_org,
                testing_loc=testing_loc)

# Compile the report and save the file to the reports subfolder
test_report.CreateReport()
```
