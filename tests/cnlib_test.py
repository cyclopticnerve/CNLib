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
from cnlib.cndecorators import cnspin

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------


MSG = "Downloading new apod dict{} xxx"
CHARS = CHARS = ["    ", ".   ", "..  ", "... "]
LAST_MSG = "Downloading new apod dict... Done"
INTERVAL = 1

# ------------------------------------------------------------------------------

@cnspin.spin(MSG, CHARS, LAST_MSG, INTERVAL)
def do_long(interval):

    # NB: printing in this method is sketchy, probably don't do it
    # print("do_long start", end="\r")
    sleep(interval)
    # print("do_long end", end="\r")

do_long(5)

# -)
