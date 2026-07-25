from pathlib import Path
import gettext

S_DOMAIN = "test"
P_DIR_LOC = Path(__file__).parent / "locale"

t = gettext.translation(S_DOMAIN, P_DIR_LOC)
_ = t.gettext

print(_("Hello world!"))
