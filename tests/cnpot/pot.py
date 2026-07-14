#! /usr/bin/env python3
# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: pot.py                                                |     ()     |
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
from pathlib import Path

# local imports
from cnlib import cnpot

# ------------------------------------------------------------------------------

P_DIR_PRJ = Path(__file__).parent.resolve()
P_FILE_TMP = P_DIR_PRJ / "template.desktop"
P_FILE_OUT = P_DIR_PRJ / "i18n/cnlib.desktop"

POTPY = cnpot.CNPotPy(
    # header
    "cnlib",
    "3.2.1",
    "cyclopticnerve",
    "cyclopticnerve@gmail.com",
    # base prj dir
    P_DIR_PRJ,
    # in
    [P_DIR_PRJ],
    {"Python": [".py"],
     "Desktop": [".desktop"]},
    # out
    "i18n",
    "i18n/po",
    "i18n/locale",
    # optional in
    "I18N",
    "UTF-8"
)

POTPY.main()
# POTPY.make_desktop(P_FILE_TMP, P_FILE_OUT)

DIR_LOCALE = P_DIR_PRJ / "i18n/locale"
_ = cnpot.underscore("cnlib", DIR_LOCALE)

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------

# test with:
# $ LANGUAGE=xx ./pot.py

# I18N: empty string
print(_(""))
print(_("Hello"))
print(_("boobs"))


# -)
