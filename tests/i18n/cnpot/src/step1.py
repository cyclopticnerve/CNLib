#!/usr/bin/env python3

import gettext
from pathlib import Path

S_DOMAIN = "cnpot"
P_DIR_PRJ = Path(__file__).parents[1]
P_DIR_LOCALE = P_DIR_PRJ / "i18n/locale"

t = gettext.translation(S_DOMAIN, P_DIR_LOCALE, fallback=True)
_ = t.gettext

# ------------------------------------------------------------------------------

my_str = _("Hello world!")
another_str = _("58008")

# ------------------------------------------------------------------------------

print(my_str)
print(another_str)
