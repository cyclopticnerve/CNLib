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

# T_DIR_PRJ = Path(__file__).parents[1].resolve()
# potpy = cnpot.CNPotPy(
#     "cnlib",
#     "0.0.0",
#     "cyclopticnerve",
#     "cyclopticnerve@gmail.com",
#     T_DIR_PRJ,
#     [T_DIR_PRJ],
#     "i18n/pot",
#     "i18n/po",
#     "i18n/locale",
#     "I18N",
#     {"Python": [".py"]},
#     ["en", "es"],
#     "UTF-8"
# )
# potpy.main()

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------

# test with:
# $ LANGUAGE=xx ./pot.py

P_DIR_PRJ = Path(__file__).parents[1].resolve()
_ = cnpot.underscore("cnlib", P_DIR_PRJ / "i18n/locale")

# ------------------------------------------------------------------------------

print(_("Hello"))

# -)
