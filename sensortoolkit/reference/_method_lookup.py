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
  Tue Apr 19 08:48:04 2022
Last Updated:
  Tue Apr 19 08:48:04 2022
"""
import numpy as np
import pandas as pd
from textwrap import wrap

def get_reference_method(lookup_table, aqs_param_code, aqs_method_code):
    """


    Args:
        lookup_table (pandas DataFrame): A table containing a list of parameter
            codes, method codes, and corresponding instrument names. Lookup
            tables for instruments measuring criteria pollutants or those
            measuring meteorological parameters are located at
            `sensortoolkit/reference/method_codes`.
        aqs_param_code (str): Parameter code used by the AQS API that is
             associated with an environmental parameter, such as a criteria
             pollutant or meteorological parameter (e.g., "88101" is the AQS
             parameter code for PM2.5).
        aqs_method_code (str): Method code used by the AQS API that is assigned
            to instruments measuring an environmental parameter. Many methods
            for criteria pollutants receive a Federal Reference Method (FRM) or
            Federal Equivalent Method designation (e.g., "238" is the AQS
            method code for the Teledyne API T640X FEM for PM2.5).

    Returns:
        instrument_name (str): The make and model of the instrument measuring
            the specified parameter.
        instrument_dict (dict): A dictionary containing various attributes
            associated with the reference instrument, such as its detection
            limit, units, designation (FRM/FEM), etc.

    """

    mask= ((lookup_table['Parameter Code'] == int(aqs_param_code)) &
            (lookup_table['Method Code'] == int(aqs_method_code)))

    selections = lookup_table.where(mask).dropna(how='all', axis=0)

    instrument_dict = {}
    for entry in selections.to_dict('record'):

        if (entry['Make']=='-'and entry['Model']=='-'):
            entry_collect_descrip = entry['Collection Description']
            entry_analysis_descrip = entry['Analysis Description']
            instrument_name = f'{entry_collect_descrip}-{entry_analysis_descrip}'
        else:
            entry_make = entry['Make']
            entry_model = entry['Model']
            instrument_name = f'{entry_make} {entry_model}'

        instrument_dict[instrument_name]  = entry

    if len(instrument_dict) > 1:

        param_name = selections['Parameter'].unique()[0].replace('(', '[').replace(')', ']')

        selection_info = (f'AQS Parameter Code: {int(aqs_param_code)} ({param_name}), '
                          f'AQS Method Code: {int(aqs_method_code)}')

        print('-'*80)
        print(selection_info)
        print('-'*80)
        text = ('Multiple instruments correspond to indicated parameter '
                'and method code')
        text = '\n..'.join(wrap(text, width=80))
        print(text)

        text = ('..From the table of instruments below, enter the index for '
                'the appropriate make and model')

        text = '\n..'.join(wrap(text, width=80))
        print(text)
        print('')

        with pd.option_context('display.expand_frame_repr', False,
                                'display.max_rows', None):
            selection_view = selections[['Make', 'Model']].reset_index(drop=True)
            selection_view.index.name = 'Index'
            print(selection_view.to_markdown())

            valid = False
            while valid is False:
                value = input('Reference Instrument Index: ')
                if int(value) in selection_view.index:
                    # enter continue
                    instrument_make = selection_view.loc[int(value), "Make"]
                    instrument_model = selection_view.loc[int(value), "Model"]
                    instrument_name = f'{instrument_make} {instrument_model}'

                    valid=True
                    print('')

                else:
                    print('..invalid index, select from those listed in the table above')
                    continue

    instrument_dict = instrument_dict[instrument_name]

    return (instrument_name, instrument_dict)
