# all system imports
from pathlib import Path

import gettext
# from cnlib import cnpot

DOMAIN = "py-pot2"
PATH = Path(__file__).parent.resolve() / "locale"

TRANSLATION = gettext.translation(DOMAIN, PATH, fallback=True)
_ = TRANSLATION.gettext
# _ = cnpot.underscore(DOMAIN, PATH)

print(_("Hello"))
