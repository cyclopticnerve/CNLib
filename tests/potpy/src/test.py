#!/usr/bin/env python3

from pathlib import Path
from cnlib import cnpot

P_DIR_PRJ = Path(__file__).parent.resolve()
_ = cnpot.underscore("potpy", P_DIR_PRJ / "i18n/locale")

print(_("Hello world!"))
# print(_("Farts"))