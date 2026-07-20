#!/usr/bin/env python3

# all system imports
import gettext
from pathlib import Path

# NB: do this here to ensure ours is last set
DOMAIN = "py-pot"
PATH = Path(__file__).parent.resolve() / "locale"
gettext.install(DOMAIN, PATH)

# all prj imports
import module

print(_("Hello"))
