#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: cnlib_test.py                                         |     ()     |
# Date    : 06/12/2025                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A simple script to test a package from within the project itself
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# local imports
from cnlib import cnfunctions as F

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    S_MSG_DEBUG = (
        "WARNING! YOU ARE IN DEBUG MODE!\n\
IT IS POSSIBLE TO OVERWRITE EXISTING PROJECTS!"
    )

    # another test
    F.printc(S_MSG_DEBUG, bg=F.C_BG_RED, fg=F.C_FG_WHITE, bold=True)

# -)
