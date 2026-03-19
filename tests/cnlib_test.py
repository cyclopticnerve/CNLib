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

# print(F.clamp(-25, -100, -50))
# print(F.clamp(-50, -100, 0))

# print(F.interpolate(50.0, 0.0, 100.0, 0.0, 255.0))
# print(F.interpolate(50, 0, 100, 0, 255))

print(F.interpolate(-25, -100, -50, -255, 0))
print(F.interpolate(-107, -100, -50, -255, 0))

# -)
