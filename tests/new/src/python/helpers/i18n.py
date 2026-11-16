"""docstring"""

# system imports
from gettext import translation
from pathlib import Path

# constants
DOMAIN = "domain"
PATH_I18N = Path(__file__).parents[2].resolve() / "i18n"
PATH_LOCALE = PATH_I18N / "locale"

# get gettext stuff
t = translation(DOMAIN, PATH_LOCALE, fallback=True)
_ = t.gettext
_p = t.ngettext
