#! /usr/bin/env python3
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

# system imports
from time import sleep

# local imports
from cnlib import cnfunctions as F
from cnlib.decorators import cnspinner as S

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------

F.B_DEBUG = True
# ------------------------------------------------------------------------------

# S.skip("Downloading file")
@S.spin("Downloading file")
def do_long():
    """docstring"""

    sleep(2)
    # return IOError("boobs")
# ------------------------------------------------------------------------------

do_long()
# print("goodbye")

# -)
