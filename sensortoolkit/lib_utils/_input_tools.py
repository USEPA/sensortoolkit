# -*- coding: utf-8 -*-
"""
This module contains various methods for sensortoolkit functions that make use
of interactive, user-input components.

================================================================================

@Author:
  | Samuel Frederick, NSSC Contractor (ORAU)
  | U.S. EPA / ORD / CEMM / AMCD / SFSB

Created:
  Mon Sep 20 15:13:36 2021
Last Updated:
  Mon Sep 20 15:13:36 2021
"""


def validate_entry(statement='Confirm entry', indent_statement=0):
    """Ask the user to confirm an entry by typing 'y' (yes) or 'n' (no).

    Args:
        indent_statement (int, optional):
            Optional argument for indenting the printed statement (useful for
            setup module where indenting indicates subsection). Defaults to 0
            (no indent).

    Returns:
        val (str): The user's input choice, either 'y' or 'n'.

    """
    val = ''
    indent = ' '*indent_statement
    options = ['y', 'n']
    while val not in options:
        val = input(f'{indent}{statement} [y/n]: ')
        if val in options:
            return val
        else:
            print(f'{indent}..invalid entry, select [y/n]')


def enter_continue(indent_statement=0):
    """Prompt the user to press the enter key to continue.

    Useful for inserting a break in an interactive module where users may
    wish to review a console output or decision before continuing.

    Args:
        indent_statement (int, optional):
            Optional argument for indenting the printed statement (useful for
            setup module where indenting indicates subsection). Defaults to 0
            (no indent).

    Returns:
        None.

    """
    indent = ' '*indent_statement
    end = False
    while end is False:
        return_val = input(f'{indent}Press enter to continue.')
        if return_val == '':
            end = True
    print('')
