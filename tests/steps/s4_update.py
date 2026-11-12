"""docstring"""

# imports
from subprocess import run, SubprocessError

cmd = [
    "msgmerge",
    "--update",
    "--previous",
    "--backup=none",
    "--sort-by-file",
    "tests/steps/i18n/po/es.po",
    "tests/steps/i18n/domain.pot",
]

try:
    cp = run(cmd, check=True)
except SubprocessError as e:
    print(e)
