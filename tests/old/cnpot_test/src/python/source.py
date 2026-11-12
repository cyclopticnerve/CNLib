"""
A Python source file to test the cnpot.py module.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# local imports
# from tests.cnpot_test.helpers.i18n import _

import gettext
import locale
from pathlib import Path

STR_DOMAIN = "cnpot_test"
PATH_PRJ = Path(__file__).parents[2].resolve()
PATH_LOCALE = PATH_PRJ / "i18n/locale"

# set locale
locale.setlocale(locale.LC_ALL, "")
locale.bindtextdomain(STR_DOMAIN, PATH_LOCALE)

# get a translation object
translation = gettext.translation(STR_DOMAIN, PATH_LOCALE, fallback=True)

# return translation object's gettext method
_ = translation.gettext

# ------------------------------------------------------------------------------

# i18n: appears if tag is i18n
# I18N: appears if tag is i18n or I18N
# str_2 = _("")

# use underscore function (this comment SHOULD NOT appear in the .pot file)
# I18N: context for string (this comment SHOULD appear in the .pot file)
# NB: other comment
string = _("Hello")
print(string)

# i18n: does this comment appear? NO!
# NB: commented strings are ignored by xgettext (it's SMRT!)
# string2 = _("Not in .pot file")

# works inside nested parentheses
print(_("Goodbye"))

# tag = i18n
# This comment appears if tag = i18n, but after the tag
# this line appears if it contains I18N or i18n
# I18N: this tag appears because it comes after
srt2 = _("test2")

# tag = I18N or the word None
# This comment appears if tag = I18N, but after the tag
# this line appears if it contains I18N or i18n
# None = new comment
# This comment ignores i18n and
# I18N: foobar
srt3 = _("test3")
