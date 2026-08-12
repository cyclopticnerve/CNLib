#!/usr/bin/env python3

# ------------------------------------------------------------------------------
# 10 lines

# import gettext
# import locale
# from pathlib import Path

# S_DOMAIN = "potpy"
# P_DIR_PRJ = Path(__file__).parent.resolve()
# P_DIR_LOCALE = P_DIR_PRJ / "i18n/locale"

# locale.setlocale(locale.LC_ALL, '')
# locale.bindtextdomain(S_DOMAIN, P_DIR_LOCALE)
# translation = gettext.translation(S_DOMAIN, P_DIR_LOCALE, fallback=True)
# _ = translation.gettext

# ------------------------------------------------------------------------------
# 12 lines

# import gettext
# import locale
# from pathlib import Path

# S_DOMAIN = "potpy"
# P_DIR_PRJ = Path(__file__).parent.resolve()
# P_DIR_LOCALE = P_DIR_PRJ / "i18n/locale"

# def underscore(domain, path):

#     locale.setlocale(locale.LC_ALL, '')
#     locale.bindtextdomain(domain, path)
#     translation = gettext.translation(domain, path, fallback=True)
#     return translation.gettext

# _ = underscore(S_DOMAIN, P_DIR_LOCALE)

# ------------------------------------------------------------------------------
# 6 lines

from pathlib import Path
from cnlib import cnpot

S_DOMAIN = "potpy"
P_DIR_PRJ = Path(__file__).parent.resolve()
P_DIR_LOCALE = P_DIR_PRJ / "i18n/locale"

_ = cnpot.underscore(S_DOMAIN, P_DIR_LOCALE)

# ------------------------------------------------------------------------------

print(_("Hello world!"))
