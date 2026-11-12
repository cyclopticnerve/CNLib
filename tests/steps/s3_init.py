"""docstring"""

# DEBUG: these imports are for debug only
from pathlib import Path
from shutil import rmtree

# imports
from subprocess import run, SubprocessError

# DEBUG: make file struct thus far
dir_i18n = Path("tests/steps/i18n")
dir_po = dir_i18n / "po"
# NB: trust me...
if dir_po.exists():
    rmtree(dir_po)  # nuke old
dir_po.mkdir()  # make new

# format command
cmd = [
    "msginit",
    # ------------------------------
    # input options
    "-i",
    "tests/steps/i18n/domain.pot",
    # ------------------------------
    # output options
    "-o",
    "tests/steps/i18n/po/es.po",
    # ------------------------------
    # output details
    "-l",
    "es",
    "--no-translator",
]

# run cmd
try:
    cp = run(cmd, check=True)
except SubprocessError as e:
    print(e)

# TODO: still need to fix:
#
# how to avoid asking about email?
# DONE: use --no-translator

# comments:
# replace 'Translation template for MyProject package.' with
#   'Spanish translations for MyProject package.'
# DONE: if using --no-translator and -l
# "Automatically generated, 2026."
#
# commands
# remove #, fuzzy
# DONE: if using --no-translator
#
# header:
# Last-translator
# Language
# DONE: if using --no-translator
# plurals
# DONE: if using --no-translator

# OH THE JANK!
# create a tmp file (using --no-translator)
# pull out first comment line, lang, and plural form
