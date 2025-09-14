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

# system imports
from pathlib import Path
import sys

# NB: i know this looks ugly, but it *WILL* work
# NB: its basically me being lazy so i dont have to create a venv in the
# package just to install the library in itself

# local imports
PATH_PRJ = Path(__file__).parents[1].resolve()
PATH_SRC = PATH_PRJ
sys.path.append(str(PATH_SRC))

# pylint: disable=import-error
# pylint: disable=wrong-import-position

from cnlib.cnmkdocs import CNMkDocs  # type: ignore

# pylint: enable=import-error
# pylint: enable=wrong-import-position

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    C = CNMkDocs()
    C.make_docs(
        "/home/dana/Projects/Python/CNLib/tests/Test_Project",
        dir_img="img",
        use_rm=False,
        file_rm="readme.md",
        use_api=True,
        dir_api="API"
    )

# -)
