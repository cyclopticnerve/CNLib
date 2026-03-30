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

F.printc("Hello", "world")
F.B_DEBUG = True
F.printd("Hello", "world")
F.printe("Hello", "world")
F.printl("Hello", "world... ")
print("farts")

# -)
