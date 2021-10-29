# -*- coding: utf-8 -*-
"""
This module contains a method for converting nested lists into a list with a
single depth.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Wed Sep  8 10:27:42 2021
Last Updated:
  Wed Sep  8 10:27:42 2021
"""


def flatten_list(list_of_lists):
    """Flatten a nested list of values.

    Args:
        list_of_lists (list):
            A nested list, example: ['a', ['b', 'c']]
    Returns:
        flat_list (list):
            A flattened list, example: ['a', 'b', 'c']

    """
    flat_list = []
    for i in list_of_lists:
        if isinstance(i, list):
            flat_list.extend(flatten_list(i))
        else:
            flat_list.append(i)
    return flat_list
