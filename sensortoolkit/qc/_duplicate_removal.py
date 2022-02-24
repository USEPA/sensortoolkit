# -*- coding: utf-8 -*-
"""
This module contains a method for identifiying and removing duplicated timestamp
entries in datasets. Since SDFS datasets utilize a pandas DatetimeIndex,
duplicated timestamp entries may cause indexing issues when accessing and
assigning values for duplicate timestamps (e.g., computing averages).

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB
  
Created:
  Thu Feb 18 13:19:54 2021
Last Updated:
  Tue Jul 13 09:39:18 2021
"""


def remove_duplicates(full_df, agg_numeric_by='mean', agg_object_by='first',
                      **kwargs):
    """Locate and remove duplicate timestamp entries if present in passed
    dataframe.

    Note that this module does not remove duplicate concentration values, only
    searches for duplicated index (assume time-like) values.

    Args:
        full_df (pandas dataframe):
            Sensor dataframe at recorded sampling frequency.
    Returns:
        full_df (pandas dataframe):
            Modified sensor dataframe at recorded sampling frequency with
            duplicated timestamps removed.

    """
    indent = kwargs.get('print_indent', 0)
    # Average duplicate entries, remove duplicated timestamps
    dup_data = full_df[full_df.index.duplicated() == True]

    if dup_data.empty:
        print(f'{indent*"."}no duplicate timestamps found')
    else:
        col_order = list(full_df.columns)
        original_df_len = full_df.shape[0]

        obj_df = full_df.select_dtypes(include=['object', 'datetime'])
        num_df = full_df.select_dtypes(exclude=['object', 'datetime'])

        num_df = num_df.groupby(num_df.index).agg(agg_numeric_by)
        obj_df = obj_df.groupby(obj_df.index).agg(agg_object_by)

        full_df = num_df.join(obj_df)
        full_df = full_df[col_order]
        modified_df_len = full_df.shape[0]

        n_duplicates = original_df_len - modified_df_len
        print(f'{indent*"."}{str(n_duplicates)} duplicate timestamps found')
        print(f'{(indent+2)*"."}removing duplicate entries')

    return full_df
