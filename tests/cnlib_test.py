#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: cnlib_test.py                                         |     ()     |
# Date    : 11/24/2025                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A simple script to test a package from within the project itself
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

from pathlib import Path

# local imports
# from cnlib import cnfunctions as F
from cnlib import cntree

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # run main function
    # print(F.pascal_case("my_project"))

    a_start_dir = Path(__file__).parents[1]

    a_tree = cntree.CNTree(a_start_dir)
    a_tree.make_tree()

    print(a_tree.text)


# -)
