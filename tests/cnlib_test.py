#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: cnlib_test.py                                         |     ()     |
# Date    : 01/01/2026                                            |            |
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

D_DEF = {
    "one": 1,
    "two": 2,
    "three": 3,
    "five": 5
}

D_FIN = F.load_paths_into_dict("tests/cfg.json", D_DEF)

F.pp(D_FIN)

# -)
