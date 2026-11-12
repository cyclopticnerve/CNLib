"""docstring"""

# DEBUG: these imports are for debug only
from pathlib import Path
from shutil import rmtree

# imports
from subprocess import run, SubprocessError

# DEBUG: make file struct thus far
dir_i18n = Path("tests/steps/i18n")
dir_lo = dir_i18n / "locales"
# NB: trust me...
if dir_lo.exists():
    rmtree(dir_lo)  # nuke old
dir_mo = dir_lo / "es/LC_MESSAGES"
dir_mo.mkdir(parents=True)  # make new

cmd = [
    "msgfmt",
    "--desktop",
    "--template=tests/steps/template.desktop",
    "-l",
    "es",
    "-o",
    "tests/steps/i18n/desktop/MyProject.desktop",
    "tests/steps/i18n/po/es.po",
]

try:
    cp = run(cmd, check=True)
except SubprocessError as e:
    print(e)
