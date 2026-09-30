# ------------------------------------------------------------------------------
# Package :__PP_NAME_BIG__                                        /          \
# Filename:                                                       |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
Demonstrate using helpers/i18n as an import.

Run this in your debugger or REPL and it should create/update your i18n folder.

If you want to know why the imports look the way they do (AND WORK!!!), see:
    https://stackoverflow.com/a/50193944

    TLDR: use a "pyproject.toml" file in your project. You can find a
    bare-bones implementation of "pyproject.toml" file in "CNLib/misc".
"""

# NB: imports are relative to the dir with the "pyproject.toml" file
from tests.cnpot_test.helpers.i18n import potpy

print("running run.py with import")

# "That's all, folks!" -- Mel Blanc
potpy.main()

# -)
