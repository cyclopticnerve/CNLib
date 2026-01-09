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

btns = ["y", "N"]

RES = F.dialog("question", btns, default="", loop=True)
print(RES)

# while True:
#     RES = F.dialog("question", btns, default="")
#     print(RES)
#     if RES == "q":
#         break

# -)
