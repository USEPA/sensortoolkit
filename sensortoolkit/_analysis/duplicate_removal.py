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
  Thu Feb 18 13:19:54 2021
Last Updated:
  Tue Jul 13 09:39:18 2021
"""


def Remove_Duplicates(full_df):
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
    # Average duplicate entries, remove duplicated timestamps
    dup_data = full_df[full_df.index.duplicated() == True]

    if dup_data.empty:
        print('No duplicate timestamps found')
    else:
        original_df_len = full_df.shape[0]
        full_df = full_df.groupby(full_df.index).mean()
        modified_df_len = full_df.shape[0]

        n_duplicates = original_df_len - modified_df_len
        print(str(n_duplicates), 'duplicate timestamps found')
        print('...Removing duplicate entries')

    return full_df