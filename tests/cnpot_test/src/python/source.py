"""
A Python source file to test the cnpot.py module.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# local imports
from tests.cnpot_test.helpers.i18n import _

# ------------------------------------------------------------------------------

# use underscore function (this comment SHOULD NOT appear in the .pot file when
# tag=I18N)
# I18N: context for string (this comment SHOULD appear in the .pot file when
# tag=I18N)
string = _("Hello")
print(string)

# NB: commented strings are ignored by xgettext (it's SMRT!)
# string2 = _("Not in .pot file")

# works inside nested parentheses
print(_("Goodbye"))
