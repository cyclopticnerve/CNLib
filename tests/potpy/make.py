#!/usr/bin/env python3
"""docstring"""

from pathlib import Path
from cnlib import cnpot

P_DIR_PRJ = Path(__file__).parent.resolve()
pp = cnpot.CNPotPy(P_DIR_PRJ, Path("i18n"))

pp.main()

P_DESK_IN = P_DIR_PRJ / "src/template.desktop"
P_DESK_OUT = P_DIR_PRJ / "i18n/potpy.desktop"
pp.make_desktop(P_DESK_IN, P_DESK_OUT)
