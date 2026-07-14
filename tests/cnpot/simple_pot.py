#! /usr/bin/env python3

# import gettext
# from pathlib import Path

# DOMAIN = "cnlib"
# PATH = Path(__file__).parent.resolve() / "i18n/locale"
# TRANSLATION = gettext.translation(DOMAIN, PATH, fallback=True)
# _ = TRANSLATION.gettext

def _(string: str) -> str:
    return string

# ------------------------------------------------------------------------------

print(_("Hello"))
