"""
A Python source file to test the cnpot.py module.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import gettext
from pathlib import Path

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

STR_DOMAIN = "chapter4"
# NB: does not exist yet, so fallback=True
PATH_LOCALE = Path("i18n/locale")

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# get a translation object
translation = gettext.translation(STR_DOMAIN, PATH_LOCALE, fallback=True)

# return translation object's gettext method
_ = translation.gettext
