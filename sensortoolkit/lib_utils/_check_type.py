# -*- coding: utf-8 -*-
"""
This module contains a method for evaluting the type of an object to determine
whether the type matches a list of accepted or anticipated types.

This module is used by various methods including
``sensortoolkit.calculate.regression_stats()`` to ensure that arguments passed
to functions are of an accepted/expected type.

===============================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Mon Nov  1 10:10:08 2021
Last Updated:
  Mon Nov  1 10:10:08 2021
"""

def check_type(obj, accept_types):
    """Verify the type of an object is an anticipated type or is contained
    within a list of accepted types.

    Args:
        obj (type ambiguous):
            The object whose type will be assessed.
        accept_types (list):
            A list of types to check the passed object against.

    Raises:
        TypeError: If the object type is not in the list of accepted
            (anticipated) types.

    Returns:
        obj_type (type): The type of the object.

    """

    obj_type = type(obj)

    if obj_type not in accept_types:
        raise TypeError('Invalid object type. Received '
                        'type {0} but expected one of the following '
                        'types: {1}'.format(obj_type, accept_types))
    return obj_type
