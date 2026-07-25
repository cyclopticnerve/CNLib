from pathlib import Path
from cnlib import cnpot

S_DOMAIN = "cnpot"
P_DIR_LOC = Path(__file__).parent / "i18n/locale"

_ = cnpot.underscore(S_DOMAIN, P_DIR_LOC)

print(_("Hello world!"))
