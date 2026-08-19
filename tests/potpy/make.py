#!/usr/bin/env python3
"""docstring"""

# ------------------------------------------------------------------------------

from pathlib import Path
from cnlib import cnpot

P_DIR_PRJ = Path(__file__).parent.resolve()
P_DIR_OUT = Path("i18n")
P_DIR_IN = Path("src")

pp = cnpot.CNPotPy(P_DIR_PRJ, P_DIR_OUT, [P_DIR_IN])

pp.main()

P_DESK_IN = P_DIR_PRJ / "src/template.desktop"
P_DESK_OUT = P_DIR_PRJ / "i18n/potpy.desktop"
pp.make_desktop(P_DESK_IN, P_DESK_OUT)
