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

# system imports
from time import sleep

# local imports
from cnlib.decorators.cnspinner import spin

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------

@spin("Downloading file")
def do_long():
    """docstring"""

    sleep(5)
    return (True, None)

do_long()
print("goodbye")

# -)
